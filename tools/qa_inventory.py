"""Exercise the actual inventory without granting gear or clearing a save."""
import argparse
import qa_board as qa

def tap(d,key):
    d.run(.09,key);d.run(.12)

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--port',default='COM4');a=p.parse_args()
    qa.OUT=qa.ROOT/'output/inventory-qa'
    d=qa.Device(a.port)
    try:
        d.run(1);d.send('MODE 3');d.send('LOCK 0');d.send('MIRROR 1');d.run(.5)
        assert 'menu_row' in d.ard,'Install the inventory-fix firmware first'
        if d.ard['scene']==3:tap(d,256)
        assert d.ard['scene']==0,'Return to normal gameplay before running this check'
        before={k:d.ard[k] for k in ('sword','items','equipped','rx','ry')}
        d.send('ARD SAVE')
        tap(d,256);assert d.ard['scene']==3
        assert d.ard['menu_row']==(before['equipped']-1 if 1<=before['equipped']<=3 else 0)
        d.run(.8,16);d.run(.12);assert d.ard['menu_row']==0
        d.snapshot('first-slot')
        tap(d,32);assert d.ard['menu_row']==1
        tap(d,32);assert d.ard['menu_row']==2
        tap(d,32);assert d.ard['menu_row']==2
        d.snapshot('third-slot')
        if before['items']<3:
            tap(d,2);assert d.ard['scene']==3 and d.ard['equipped']==before['equipped']
            d.snapshot('locked-confirm')
        d.send('MIRROR 0');d.run(.25);frames=d.frames
        tap(d,64);assert d.ard['menu_row']==1 and d.frames==frames
        tap(d,128);assert d.ard['menu_row']==2 and d.frames==frames
        d.send('MIRROR 1');d.run(.3);assert d.frames>frames
        # Exit from the original equipped row; this preserves the user's equipment.
        d.run(.8,16);d.run(.12)
        for _ in range(before['equipped']-1 if 1<=before['equipped']<=3 else 0):tap(d,32)
        tap(d,256);assert d.ard['scene']==0 and d.ard['equipped']==before['equipped']
        tap(d,256);assert d.ard['scene']==3
        assert d.ard['menu_row']==(before['equipped']-1 if 1<=before['equipped']<=3 else 0)
        d.snapshot('reopened')
        for k in ('sword','items','rx','ry'):assert d.ard[k]==before[k],(k,before,d.ard)
        tap(d,256);d.send('ARD SAVE')
        print('PASS: cursor steps/hold/bounds, locked item rejection, reopen, mirror off, inventory preserved')
    finally:d.close()

if __name__=='__main__':main()
