// SPDX-License-Identifier: MIT
#pragma once
namespace QuestInventory {
constexpr int slots=3;
constexpr int rowFor(int equipped){return equipped>=1&&equipped<=slots?equipped-1:0;}
constexpr int move(int row,int direction){return row+direction<0?0:row+direction>=slots?slots-1:row+direction;}
constexpr bool owned(int row,int acquired){return row>=0&&row<slots&&row<acquired;}
constexpr int equip(int row,int acquired,int previous){return owned(row,acquired)?row+1:previous;}
// Regression cases: empty/partial inventories must be browsable without granting gear.
static_assert(move(0,1)==1&&move(1,1)==2&&move(2,1)==2,"All slots must be browsable");
static_assert(move(0,-1)==0&&move(2,-1)==1,"Cursor must stay within bounds");
static_assert(!owned(0,0)&&equip(2,0,255)==255,"Empty inventory cannot equip anything");
static_assert(equip(0,1,255)==1&&equip(2,1,1)==1,"Locked selection must preserve equipment");
static_assert(equip(2,3,1)==3&&rowFor(3)==2,"Reopening must keep the equipped slot");
}
