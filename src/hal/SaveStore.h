// SPDX-License-Identifier: MIT
#pragma once
#include <Preferences.h>
#include <string.h>
// Separate namespace and versioned record; never touches Doom or pet saves.
class AdventureSaveStore {
    uint8_t bytes[256]={};
    bool loaded=false;
    void load(){if(loaded)return;loaded=true;Preferences p;if(p.begin("ard-quest",true)){if(p.getBytesLength("save-v1")==sizeof(bytes))p.getBytes("save-v1",bytes,sizeof(bytes));p.end();}}
public:
    template<class T> void get(size_t at,T &v){load();memset(&v,0,sizeof(v));if(at+sizeof(v)<=sizeof(bytes))memcpy(&v,bytes+at,sizeof(v));}
    void write(size_t at,uint8_t v){load();if(at<sizeof(bytes))bytes[at]=v;}
    template<class T> void put(size_t at,const T &v){load();if(at+sizeof(v)>sizeof(bytes))return;memcpy(bytes+at,&v,sizeof(v));Preferences p;if(p.begin("ard-quest",false)){p.putBytes("save-v1",bytes,sizeof(bytes));p.end();}}
};
extern AdventureSaveStore adventureSave;
