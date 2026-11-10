// SPDX-License-Identifier: MIT
#pragma once
#include <Arduino.h>
#include <string.h>
#define WIDTH 128
#define HEIGHT 64
#define WHITE 1
#define BLACK 0
enum { A_BUTTON=1, B_BUTTON=2, UP_BUTTON=4, DOWN_BUTTON=8, LEFT_BUTTON=16, RIGHT_BUTTON=32 };
struct Arduboy2Audio { static bool enabled(){return false;} static void toggle(){} static void saveOnOff(){} };
struct SpritesB {};
class Arduboy2Base {
    uint8_t buttons=0,previous=0;
public:
    static uint8_t sBuffer[1024];
    void pollButtons(uint8_t value){previous=buttons;buttons=value;}
    bool pressed(uint8_t b) const{return (buttons&b)==b;}
    bool justPressed(uint8_t b) const{return (buttons&b)&&!(previous&b);}
    void clear(){memset(sBuffer,0,sizeof(sBuffer));}
    static void pixel(int x,int y,bool on){if((unsigned)x>=WIDTH||(unsigned)y>=HEIGHT)return;uint8_t &p=sBuffer[(y/8)*WIDTH+x],mask=1<<(y%8);if(on)p|=mask;else p&=~mask;}
    void fillRect(int x,int y,int w,int h,uint8_t c=WHITE){for(int j=max(0,y);j<min(HEIGHT,y+h);j++)for(int i=max(0,x);i<min(WIDTH,x+w);i++)pixel(i,j,c);}
    void drawRect(int x,int y,int w,int h,uint8_t c=WHITE){for(int i=0;i<w;i++){pixel(x+i,y,c);pixel(x+i,y+h-1,c);}for(int j=0;j<h;j++){pixel(x,y+j,c);pixel(x+w-1,y+j,c);}}
};
