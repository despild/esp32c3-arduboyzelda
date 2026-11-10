// SPDX-License-Identifier: MIT
// Standalone Pocket Quest host. Games and original assets run on the ESP32.
#include <Arduino.h>
#include <Wire.h>
#include "src/ArdAdventure.h"
static uint8_t display[360],address=0x3c;
static bool connected=false,mirror=true,locked=false,oledOk=false;
static uint16_t keys=0;
static uint32_t heartbeat=0,keyAt=0,tickAt=0,mirrorAt=0,stateAt=0;
static char input[128];static unsigned used=0;static bool overflow=false;
static void commands(const uint8_t* data,int n){Wire.beginTransmission(address);Wire.write(0);Wire.write(data,n);Wire.endTransmission();}
static void flush(){if(!oledOk)return;const uint8_t c[]={0x21,28,99,0x22,0,4};commands(c,sizeof(c));for(int i=0;i<360;i+=24){Wire.beginTransmission(address);Wire.write(0x40);Wire.write(display+i,24);if(Wire.endTransmission())oledOk=false;}}
static bool paused(){return locked||millis()-heartbeat>3500;}
static void frame(){if(!connected||!mirror||!Serial)return;char out[760];const char h[]="0123456789abcdef";int n=snprintf(out,sizeof(out),"{\"t\":\"frame\",\"hex\":\"");for(int i=0;i<360;i++){out[n++]=h[display[i]>>4];out[n++]=h[display[i]&15];}out[n++]='"';out[n++]='}';out[n++]='\n';Serial.write((uint8_t*)out,n);}
static void state(){if(!connected)return;ArdStats s=ardStats();Serial.printf("{\"t\":\"state\",\"id\":\"oled-doom\",\"v\":1,\"mode\":3,\"auto\":%s,\"lock\":%s,\"hp\":%d,\"ammo\":%d,\"map\":%d,\"frames\":%lu,\"heap\":%u,\"oled\":%s,\"fault\":false}\n",paused()?"true":"false",locked?"true":"false",s.hp,s.keys,s.dungeon,(unsigned long)s.frames,ESP.getFreeHeap(),oledOk?"true":"false");ardSendState();}
static void parse(char* s){
    if(!strcmp(s,"HELLO")){connected=true;heartbeat=millis();Serial.println("{\"t\":\"hello\",\"id\":\"oled-doom\",\"v\":1,\"width\":72,\"height\":40,\"native\":true,\"arduboy\":true,\"standalone_arduboy\":true}");state();return;}
    if(!connected)return;heartbeat=millis();unsigned v;
    if(sscanf(s,"KEY %u",&v)==1){keys=v&1023;keyAt=millis();}
    else if(sscanf(s,"LOCK %u",&v)==1){locked=v!=0;keys=0;if(locked)ardSave();}
    else if(sscanf(s,"MIRROR %u",&v)==1)mirror=v!=0;
    else if(sscanf(s,"LIGHT %u",&v)==1&&v<=255){const uint8_t c[]={0x81,(uint8_t)v};commands(c,2);}
    else if(!strcmp(s,"ARD NEW"))ardNewGame();
    else if(!strcmp(s,"ARD SAVE"))ardSave();
    else if(!strcmp(s,"ARD STATE"))ardSendState();
    else if(!strcmp(s,"STATE")){state();frame();}
}
void setup(){
    Serial.begin(115200);Serial.setTxTimeoutMs(20);Serial.setRxBufferSize(1024);
    Wire.begin(5,6);Wire.setClock(400000);Wire.beginTransmission(address);oledOk=Wire.endTransmission()==0;
    const uint8_t c[]={0xae,0xd5,0x80,0xa8,0x27,0xd3,0,0xad,0x30,0x8d,0x14,0x40,0xa6,0xa4,0x20,0,0xa1,0xc8,0xda,0x12,0x81,150,0xd9,0x22,0xdb,0x20,0x2e,0xaf};commands(c,sizeof(c));
    ardBegin();ardStep(0);ardRender(display);flush();heartbeat=millis()-4000;
}
void loop(){
    unsigned budget=512;while(Serial.available()&&budget--){char c=Serial.read();if(c=='\n'){if(!overflow){input[used]=0;parse(input);}used=0;overflow=false;}else if(c!='\r'){if(used<sizeof(input)-1)input[used++]=c;else overflow=true;}}
    if(millis()-keyAt>350)keys=0;
    if(millis()-tickAt>=16){tickAt=millis();if(!paused())ardStep(keys);ardRender(display);flush();}
    if(millis()-mirrorAt>=100){mirrorAt=millis();frame();}
    if(millis()-stateAt>=1000){stateAt=millis();state();}
    delay(1);
}
