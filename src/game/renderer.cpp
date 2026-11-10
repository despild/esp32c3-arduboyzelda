// SPDX-License-Identifier: MIT
#include "renderer.h"
#include "../hal/Font.h"
void Renderer::fillRect(int16_t x,int16_t y,uint8_t w,uint8_t h,uint8_t c){arduboy.fillRect(x+translateX,y+translateY,w,h,c);}
void Renderer::drawRect(int16_t x,int16_t y,uint8_t w,uint8_t h,uint8_t c){arduboy.drawRect(x+translateX,y+translateY,w,h,c);}
void Renderer::drawOverwrite(int16_t x,int16_t y,const uint8_t* b,uint8_t f,MirrorMode m,DrawMode d){drawBitmap(x+translateX,y+translateY,b,nullptr,false,f,m,d);}
void Renderer::drawPlusMask(int16_t x,int16_t y,const uint8_t* b,uint8_t f,MirrorMode m,DrawMode d){drawBitmap(x+translateX,y+translateY,b,nullptr,true,f,m,d);}
void Renderer::drawString(int8_t x,int8_t y,const uint8_t* str){
    if(!str)return;
    for(int cursor=x;*str;str++,cursor+=8){int g=questGlyph(*str);if(g<0)continue;for(int j=0;j<5;j++)for(int i=0;i<3;i++)if(questGlyphs[g][j]&(4>>i))fillRect(cursor+i*2,y+j*2,2,2,WHITE);}
}
