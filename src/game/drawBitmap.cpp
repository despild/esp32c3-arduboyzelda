// SPDX-License-Identifier: MIT
// Portable clipped page-format bitmap blitter. No AVR assembler or old artwork.
#include "drawBitmap.h"
#include "../hal/Arduboy2.h"
void drawBitmap(int16_t x,int8_t y,const uint8_t* bitmap,const uint8_t* mask,bool plusMask,uint8_t frame,MirrorMode mirror,DrawMode mode,uint8_t maskFrame){
    if(!bitmap)return;
    int w=pgm_read_byte(bitmap),h=pgm_read_byte(bitmap+1),size=w*((h+7)/8);
    const uint8_t *bits=bitmap+2+frame*size*(plusMask?2:1);
    if(plusMask)mask=bits+size;
    else if(mask)mask+=2+(maskFrame==255?frame:maskFrame)*size;
    for(int yy=max(0,-(int)y);yy<h&&y+yy<HEIGHT;yy++)for(int xx=max(0,-(int)x);xx<w&&x+xx<WIDTH;xx++){
        int sx=(mirror&MIRROR_HORIZONTAL)?w-1-xx:xx,sy=(mirror&MIRROR_VERTICAL)?h-1-yy:yy;
        int index=(sy/8)*w+sx,bit=1<<(sy%8);
        if(mask&&!(pgm_read_byte(mask+index)&bit))continue;
        bool value=(pgm_read_byte(bits+index)&bit)!=0;
        if(mode==Invert)value=!value;
        if(mode==Xor)value^=(Arduboy2Base::sBuffer[((y+yy)/8)*WIDTH+x+xx]&(1<<((y+yy)%8)))!=0;
        Arduboy2Base::pixel(x+xx,y+yy,value);
    }
}
