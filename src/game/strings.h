// SPDX-License-Identifier: MIT
#pragma once
#include <Arduino.h>
#define QUEST_TEXT(name,value) static const uint8_t name##_string[]=value
QUEST_TEXT(gameOver,"TRY AGAIN");
QUEST_TEXT(continue,"CONTINUE");
QUEST_TEXT(quitFromGameOver,"TITLE");
QUEST_TEXT(newGame,"NEW GAME");
QUEST_TEXT(sfxOn,"SILENT");
QUEST_TEXT(sfxOff,"SILENT");
QUEST_TEXT(deleteSave,"CLEAR SAVE");
QUEST_TEXT(congrats,"QUEST COMPLETE");
QUEST_TEXT(equip,"ITEMS");
QUEST_TEXT(map,"MAP");
QUEST_TEXT(gotKey,"KEY FOUND");
QUEST_TEXT(gotBoomerang,"BOOMERANG");
QUEST_TEXT(gotBombs,"BOMBS");
QUEST_TEXT(gotRing,"MAGIC RING");
QUEST_TEXT(gotSword,"SWORD FOUND");
QUEST_TEXT(gotHeartContainer,"MORE HEALTH");
QUEST_TEXT(gotBossKey,"BOSS KEY");
#undef QUEST_TEXT
