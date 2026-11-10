"""Validate all compressed rooms independently of the MCU pointer renderer."""
import re,struct
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def rooms(name):
    s=(ROOT/f'src/game/{name}.h').read_text()
    body=re.search(name+r'_map\[\d+\]\s*=\s*\{(.*?)\};',s,re.S).group(1)
    data=bytes(int(v,0) for v in re.findall(r'0x[0-9a-fA-F]+|\b\d+\b',re.sub(r'//[^\n]*','',body)))
    length,width,height=struct.unpack_from('<HBB',data)
    assert len(data)==length
    offsets=list(struct.unpack_from('<'+'H'*(width*height),data,4))
    header=4+2*width*height;offsets=[v+header for v in offsets]+[length]
    output={}
    for n in range(width*height):
        raw=[v for byte in data[offsets[n]:offsets[n+1]] for v in (byte>>4,byte&15)]
        tiles=[];i=0
        while i<len(raw) and len(tiles)<28:
            if raw[i]==15:
                assert i+2<len(raw)
                tiles.extend([raw[i+2]]*(raw[i+1]+4));i+=3
            else:tiles.append(raw[i]);i+=1
        assert len(tiles)==28,(name,n,len(tiles))
        assert all(t<=12 for t in tiles)
        output[n%width,n//width]=tiles
    return output
if __name__=='__main__':
    maps={name:rooms(name) for name in ('overworld','dungeons')}
    print('PASS:',sum(map(len,maps.values())),'rooms decoded to 28 valid tiles each')
    for xy in ((1,2),(2,2),(3,2),(4,5)):
        t=maps['overworld'][xy];print(xy, [t[i:i+7] for i in range(0,28,7)])
