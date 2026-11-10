"""Play the port using real USB input; retain state and exact display readback."""
from pathlib import Path
import argparse,json,time,collections
import serial
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'output/board-qa'
class Device:
    def __init__(self,port):
        OUT.mkdir(parents=True,exist_ok=True)
        self.ser=serial.Serial(port,115200,timeout=.01,write_timeout=1)
        self.ser.dtr=True;self.ser.rts=False
        self.buffer=bytearray();self.hello={};self.state={};self.ard={};self.frame=None;self.frames=0;self.events=[]
    def send(self,s):self.ser.write((s+'\n').encode())
    def run(self,duration,keys=0,keepalive=True):
        start=time.monotonic();last=laststats=0
        while time.monotonic()-start<duration:
            now=time.monotonic()
            if keepalive and now-last>.06:self.send('KEY '+str(keys) if self.hello else 'HELLO');last=now
            if keepalive and self.hello and now-laststats>.03:self.send('ARD STATE');laststats=now
            self.buffer.extend(self.ser.read(8192))
            while b'\n' in self.buffer:
                line,_,self.buffer=self.buffer.partition(b'\n')
                try:m=json.loads(line)
                except ValueError:
                    if b'Guru' in line or b'ERROR' in line or b'assert' in line:raise RuntimeError(line.decode(errors='replace'))
                    continue
                t=m.get('t')
                if t=='hello':self.hello=m
                elif t=='ard':self.ard=m
                elif t=='state':self.state=m;assert not m['fault'],m
                elif t=='frame':self.frame=bytes.fromhex(m['hex']);self.frames+=1;assert len(self.frame)==360
        return dict(self.ard)
    def snapshot(self,name):
        self.events.append({'name':name,'ard':dict(self.ard),'board':dict(self.state)})
        assert self.frame
        im=Image.new('1',(72,40));im.putdata([255 if self.frame[y//8*72+x]&(1<<(y%8)) else 0 for y in range(40) for x in range(72)])
        im.save(OUT/(name+'-native.png'));im.resize((720,400),Image.Resampling.NEAREST).save(OUT/(name+'.png'))
        (OUT/'results.json').write_text(json.dumps(self.events,indent=2))
    def close(self):self.send('KEY 0');self.ser.close()

def route(state,goal):
    """Two-pixel grid, using observed room tiles and fixed obstacles."""
    sx,sy=state['x'],state['y'];start=(sx,sy)
    q=collections.deque([start]);prev={start:None}
    def free(x,y):
        if not (0<=x<112 and 0<=y<64):return False
        if state['tiles'][y//16*7+x//16] in (4,6):return False
        for t,ex,ey,h in state['entities']:
            if t in (3,15,16,19,20,22) and x+8>ex and x<ex+(14 if t==3 else 16) and y+8>ey and y<ey+(8 if t in (3,20,22) else 16):return False
            if 6<=t<=13 and x+10>ex and x<ex+18 and y+10>ey and y<ey+18:return False
        return True
    end=None
    while q:
        x,y=q.popleft()
        if abs(x-goal[0])<=2 and abs(y-goal[1])<=2:end=(x,y);break
        for dx,dy in ((2,0),(-2,0),(0,2),(0,-2)):
            p=(x+dx,y+dy)
            if p not in prev and free(*p):prev[p]=(x,y);q.append(p)
    if end is None:raise RuntimeError('No route '+str((start,goal,state)))
    path=[]
    while prev[end] is not None:path.append(end);end=prev[end]
    return list(reversed(path))

def move_to(d,goal,timeout=20):
    until=time.monotonic()+timeout
    while time.monotonic()<until:
        s=d.ard
        if s['scene']==2:raise RuntimeError('Player died during route')
        if s['scene']!=0:d.run(.15);continue
        if abs(s['x']-goal[0])<=4 and abs(s['y']-goal[1])<=4:d.run(.12);return
        path=route(s,goal)
        if not path:return
        dx,dy=path[0][0]-s['x'],path[0][1]-s['y']
        run=1
        for i in range(1,len(path)):
            if (path[i][0]-path[i-1][0],path[i][1]-path[i-1][1])!=(dx,dy):break
            run+=1
        key=128 if dx>0 else 64 if dx<0 else 32 if dy>0 else 16
        d.run(min(.1,max(.025,run*2/100-0.02)),key);d.run(.04)
    raise RuntimeError('Navigation timed out '+str(d.ard))

def east(d):
    rx,ry=d.ard['rx'],d.ard['ry']
    rows=[y for y in range(4) if d.ard['tiles'][y*7+6] in (0,2,3,11)]
    assert rows,'No east exit'
    y=min(rows,key=lambda r:abs(r*16+8-d.ard['y']))*16+8
    move_to(d,(106,y));d.run(.35,128);d.run(1.5)
    assert (d.ard['rx'],d.ard['ry'])==(rx+1,ry),d.ard

def main():
    p=argparse.ArgumentParser();p.add_argument('--port',default='COM4');p.add_argument('--inspect',action='store_true');a=p.parse_args()
    d=Device(a.port)
    try:
        d.run(1.5);assert d.hello.get('arduboy'),d.hello
        d.send('LOCK 0');d.send('MODE 3');d.send('MIRROR 1')
        if a.inspect:d.run(1);d.snapshot('inspect');print(json.dumps(d.ard));return
        d.send('ARD NEW');d.run(1);assert (d.ard['rx'],d.ard['ry'])==(1,2);d.snapshot('start')
        d.run(.08,256);d.run(.2);assert d.ard['scene']==3;d.snapshot('inventory')
        d.run(.08,256);d.run(.2);assert d.ard['scene']==0
        d.send('MIRROR 0');d.run(.3);before=d.frames;position=d.ard['x'];d.run(.15,128);d.run(.3)
        assert d.frames==before and d.ard['x']!=position,'Readback/input separation failed'
        d.send('MIRROR 1');d.run(.4);assert d.frames>before
        east(d);d.snapshot('room-two');east(d);d.snapshot('sword-room')
        move_to(d,(34,32));d.run(.15,16);d.run(1.4)
        assert d.ard['sword']==1,'Sword chest was not collected';d.snapshot('sword-acquired')
        d.run(.08,2);assert d.ard['attack']==1,'Sword input did not start an attack';d.snapshot('sword-attack');d.run(.5)
        d.send('ARD SAVE');d.send('LOCK 1');d.run(.3);frames=d.ard['frames'];d.run(.5);assert d.ard['frames']==frames
        d.send('LOCK 0');d.run(.4);assert d.ard['frames']>frames
        d.snapshot('complete');print('PASS: movement, two room transitions, sword pickup/attack, menu, mirror and pause',flush=True)
    finally:d.close()
if __name__=='__main__':main()
