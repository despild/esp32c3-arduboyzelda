// SPDX-License-Identifier: MIT
#include "ArdAdventure.h"
#include "hal/Arduboy2.h"
#include "hal/SaveStore.h"
#include "hal/Font.h"
#include "game/game.h"
#include "game/renderer.h"
#include "game/state.h"
#include <new>
uint8_t Arduboy2Base::sBuffer[1024];
Arduboy2Base arduboy;
AdventureSaveStore adventureSave;
Renderer renderer(arduboy);
Game game;
static bool started=false;
static uint32_t totalFrames=0;
static uint16_t previousKeys=0;
static uint8_t frame=1;
void ardBegin(){if(started)return;started=true;game.beginPlay();}
void ardNewGame(){ardBegin();State::clearEEPROM();game.~Game();new (&game) Game();game.beginPlay();previousKeys=0;arduboy.pollButtons(0);arduboy.pollButtons(0);}
void ardSave(){if(started)State::saveToEEPROM();}
void ardStep(uint16_t keys){
    ardBegin();
    uint8_t buttons=0;
    if(keys&2)buttons|=A_BUTTON; // Ctrl/Z: sword and confirm.
    if(keys&1)buttons|=B_BUTTON; // Space: equipped item.
    if(keys&(1<<4))buttons|=UP_BUTTON;if(keys&(1<<5))buttons|=DOWN_BUTTON;
    if(keys&(1<<6))buttons|=LEFT_BUTTON;if(keys&(1<<7))buttons|=RIGHT_BUTTON;
    arduboy.pollButtons(buttons);
    if((keys&0x300)&&!(previousKeys&0x300))game.toggleMenu();
    previousKeys=keys;
    frame=frame==60?1:frame+1;
    arduboy.clear();game.update(frame);game.render(frame);totalFrames++;
}
ArdStats ardStats(){
    ardBegin();Player &p=game.hero();
    return {p.x,p.y,TileRoom::x,TileRoom::y,State::gameState.currentDungeon,p.health,State::gameState.totalHealth,
        State::gameState.numKeys[State::gameState.currentDungeon],State::gameState.hasSword,State::gameState.numAcquiredItems,game.scene(),p.entities[0].type==SWORD,totalFrames};
}
static void put(uint8_t *o,int x,int y,bool v=true){if((unsigned)x>=72||(unsigned)y>=40)return;uint8_t &b=o[y/8*72+x],m=1<<(y%8);if(v)b|=m;else b&=~m;}
static void label(uint8_t* o,int x,int y,const char* s){if(!s)return;for(;*s&&x<72;s++,x+=4){int g=questGlyph(*s);if(g>=0)for(int j=0;j<5;j++)for(int i=0;i<3;i++)if(questGlyphs[g][j]&(4>>i))put(o,x+i,y+j);if(*s==':'){put(o,x+1,y+1);put(o,x+1,y+3);}if(*s=='-')for(int i=0;i<3;i++)put(o,x+i,y+2);}}
void ardRender(uint8_t o[360]){
    ardBegin();memset(o,0,360);ArdStats s=ardStats();char text[32];
    if(s.scene==1||s.scene==2){
        label(o,12,3,s.scene==1?"POCKET QUEST":"TRY AGAIN");
        label(o,12,16,s.scene==1?(State::hasUserSaved()?"CONTINUE":"NEW GAME"):"CONTINUE");
        label(o,12,24,s.scene==1?"SILENT":"TITLE");
        if(s.scene==1&&State::hasUserSaved())label(o,12,32,"CLEAR SAVE");
        label(o,4,16+game.row()*8,"X");return;
    }
    if(s.scene==3){
        label(o,0,0,"ITEMS");label(o,40,0,"MAP");
        const char* names[]={"BOOM","BOMB","RING"};
        for(int i=0;i<s.items&&i<3;i++){label(o,6,10+i*8,names[i]);if(i==game.row())label(o,0,10+i*8,"X");}
        if(!s.items)label(o,0,12,"NONE");
        if(s.dungeon<4)for(int y=0;y<8;y++)for(int x=0;x<(s.dungeon?8:7);x++){
            int n=y*(s.dungeon?8:7)+x;if(n>=64)continue;
            bool current=x==s.roomX&&y==s.roomY,visited=State::gameState.mapStates[s.dungeon][n/8]&(1<<(n%8));
            if(visited||current)for(int dy=0;dy<2;dy++)for(int dx=0;dx<2;dx++)put(o,40+x*4+dx,8+y*4+dy,!current||(frame/15)%2);
        }
        label(o,0,35,"ENTER CLOSE");return;
    }
    // Keep all seven columns/four rows visible. Omit the tiny original HUD.
    for(int y=0;y<34;y++)for(int x=0;x<72;x++){
        int sx=(x*112+56)/72,sy=(y*64+32)/34;
        put(o,x,y,(Arduboy2Base::sBuffer[(sy/8)*128+sx]&(1<<(sy%8)))!=0);
    }
    snprintf(text,sizeof(text),"H%d K%d %s%d",max(0,s.hp),s.keys,s.dungeon?"D":"R",s.dungeon?s.dungeon:s.roomY*7+s.roomX);
    label(o,0,35,text);
    if(game.toastText()){
        for(int y=0;y<7;y++)for(int x=0;x<72;x++)put(o,x,y,false);
        label(o,1,1,game.toastText());
    }
}
void ardSendState(){
    ArdStats s=ardStats();
    Serial.printf("{\"t\":\"ard\",\"x\":%d,\"y\":%d,\"rx\":%d,\"ry\":%d,\"dungeon\":%d,\"hp\":%d,\"maxhp\":%d,\"keys\":%d,\"sword\":%d,\"items\":%d,\"scene\":%d,\"attack\":%d,\"frames\":%lu,\"tiles\":[",s.x,s.y,s.roomX,s.roomY,s.dungeon,s.hp,s.maxHp,s.keys,s.sword,s.items,s.scene,s.attacking,(unsigned long)s.frames);
    for(int i=0;i<28;i++)Serial.printf("%s%d",i?",":"",TileRoom::rooms[TileRoom::currentRoomOffset+i]);
    Serial.print("],\"entities\":[");bool first=true;
    for(int i=0;i<MAX_ENTITIES;i++){Entity &e=game.entities[i];if(e.type==UNSET)continue;Serial.printf("%s[%d,%d,%d,%d]",first?"":",",e.type,e.x,e.y,e.health);first=false;}
    Serial.println("]}");
}
