#include "../hal/Arduboy2.h"
#include "inGameMenu.h"
#include "spriteBitmaps.h"
#include "tileBitmaps.h"
#include "util.h"
#include "state.h"
#include "strings.h"
#include "hud.h"
#include "itemSprites.h"
#include "renderer.h"

extern Renderer renderer;
extern Arduboy2Base arduboy;

void InGameMenu::update(byte frame) {
    bool up=arduboy.pressed(UP_BUTTON)||arduboy.pressed(LEFT_BUTTON);
    bool down=arduboy.pressed(DOWN_BUTTON)||arduboy.pressed(RIGHT_BUTTON);
    int8_t direction=up==down?0:down?1:-1;
    if(!direction){heldDirection=0;heldFrames=0;return;}
    if(direction!=heldDirection){heldDirection=direction;heldFrames=0;}
    else if(heldFrames<255)++heldFrames;
    if(heldFrames==0||heldFrames>=18){
        row=QuestInventory::move(row,direction);
        if(heldFrames>=18)heldFrames=13;
    }
}

void InGameMenu::render(Player& player, uint8_t frame) {
    renderer.translateX = WIDTH - 16;
    renderer.translateY = 0;
    Hud::render(player);
    renderer.translateX = 0;

    const uint8_t x = 20;

    renderer.drawString(x + 4, 2, equip_string);

    // sword
    if (State::gameState.hasSword) {
        renderer.drawPlusMask(6, HEIGHT - 20, swordIcon_plus_mask, 0, 0, Invert);
    }

    // items
    for (uint8_t i = 0; i < State::gameState.numAcquiredItems; ++i) {
        if (i == row) {
            renderer.drawOverwrite(x + 4, 10 + 15 * i, hudBFrame_tiles, 0);
        }

        const uint8_t* itemBmp = (uint8_t*)pgm_read_ptr(secondaryItem_sprites + i + 1);
        renderer.drawPlusMask(x + 10, 12 + 15 * i, itemBmp, 0, 0, Invert);
    }

}
