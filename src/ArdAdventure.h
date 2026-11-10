// SPDX-License-Identifier: MIT
#pragma once
#include <stdint.h>
struct ArdStats {
    int x,y,roomX,roomY,dungeon,hp,maxHp,keys,sword,items,scene,attacking;
    uint32_t frames;
};
void ardBegin();
void ardStep(uint16_t controllerKeys);
void ardRender(uint8_t output[360]);
ArdStats ardStats();
void ardNewGame();
void ardSave();
void ardSendState();
