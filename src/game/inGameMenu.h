#ifndef ingamemenu_h
#define ingamemenu_h

#include "entityTypes.h"
#include "../hal/InventorySelection.h"
#include "state.h"
#include "entities/player.h"

typedef uint8_t Decision;

class InGameMenu {
    public:
        uint8_t row;
        int8_t heldDirection=0;
        uint8_t heldFrames=0;
        void open(EntityType equipped){row=QuestInventory::rowFor(equipped);chosenItem=equipped;heldDirection=0;heldFrames=0;}
        bool canEquip() const {return QuestInventory::owned(row,State::gameState.numAcquiredItems);}
        void select(){chosenItem=QuestInventory::equip(row,State::gameState.numAcquiredItems,chosenItem);}
        EntityType chosenItem;

        InGameMenu():
            row(0),
            chosenItem(UNSET)
        {}

        void update(uint8_t frame);
        void render(Player& player, uint8_t frame);
};

#endif
