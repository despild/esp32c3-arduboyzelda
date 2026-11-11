"""Generate the ESP32 game translation units from the intact pinned MIT source."""
from pathlib import Path
import shutil,subprocess,sys
ROOT=Path(__file__).resolve().parents[1]
DEST=ROOT/'src/game'
for p in (ROOT/'vendor/ardynia/src').rglob('*'):
    if not p.is_file():continue
    target=DEST/p.relative_to(ROOT/'vendor/ardynia/src')
    target.parent.mkdir(parents=True,exist_ok=True)
    s=p.read_text(encoding='utf-8')
    hal='../hal/Arduboy2.h' if target.parent==DEST else '../../hal/Arduboy2.h'
    s=s.replace('#include <Arduboy2.h>',f'#include "{hal}"')
    if p.name in ('game.cpp','loadEntity.cpp','hud.cpp'):
        # These files use word reads exclusively for pointers, unlike map decoding.
        s=s.replace('pgm_read_word','pgm_read_ptr')
    if p.name=='skeleton.cpp':s=s.replace('(int16_t)pgm_read_word','(int8_t)pgm_read_byte')
    if p.name=='state.cpp':
        s='#include "../hal/SaveStore.h"\n'+s.replace('EEPROM.', 'adventureSave.')
    if p.name=='entity.cpp':s=s.replace('State::isInDungeon() ? (type == BAT ? Xor : Invert) : Normal','Normal')
    if p.name=='tileRoom.cpp':
        s=s.replace('dontInvert ? Normal : Invert','Normal')
        s=s.replace('TileDef TileRoom::getTileAt(uint8_t px, uint8_t py) {','TileDef TileRoom::getTileAt(uint8_t px, uint8_t py) {\n    if(px>=112 || py>=64) return Stone;')
        s=s.replace('    uint16_t lengthOfMap = pgm_read_word(map);','    if(roomX>=pgm_read_byte(map+2) || roomY>=pgm_read_byte(map+3)) { for(int i=0;i<TILES_PER_ROOM;i++) rooms[offset+i]=Stone;return; }\n    uint16_t lengthOfMap = pgm_read_word(map);')
        s=s.replace('                rooms[offset++] = tileId;','                if(offset<maxOffset) rooms[offset++] = tileId;')
    if p.name=='player.cpp':
        s=s.replace('(DrawMode)State::isInDungeon()', 'Normal')
        s=s.replace('min(health + 1, State::gameState.totalHealth)', 'min(health + 1, (int)State::gameState.totalHealth)')
    if p.name=='entityTemplates.h':s=s.replace('return (width - 1) << 4 | (height - 1);', 'return uint8_t((uint8_t(width - 1) << 4) | uint8_t(height - 1));')
    if p.name in ('torch.cpp','torch.h'):s=s.replace('Entity* player','Entity& player')
    if p.name=='inGameMenu.h':
        s=s.replace('#include "entityTypes.h"','#include "entityTypes.h"\n#include "../hal/InventorySelection.h"\n#include "state.h"')
        s=s.replace('        uint8_t row;', '''        uint8_t row;
        int8_t heldDirection=0;
        uint8_t heldFrames=0;
        void open(EntityType equipped){row=QuestInventory::rowFor(equipped);chosenItem=equipped;heldDirection=0;heldFrames=0;}
        bool canEquip() const {return QuestInventory::owned(row,State::gameState.numAcquiredItems);}
        void select(){chosenItem=QuestInventory::equip(row,State::gameState.numAcquiredItems,chosenItem);}''')
    if p.name=='inGameMenu.cpp':
        start=s.index('    const int8_t maxRows =',s.index('void InGameMenu::update'))
        end=s.index('\n}',start)
        s=s[:start]+'''    bool up=arduboy.pressed(UP_BUTTON)||arduboy.pressed(LEFT_BUTTON);
    bool down=arduboy.pressed(DOWN_BUTTON)||arduboy.pressed(RIGHT_BUTTON);
    int8_t direction=up==down?0:down?1:-1;
    if(!direction){heldDirection=0;heldFrames=0;return;}
    if(direction!=heldDirection){heldDirection=direction;heldFrames=0;}
    else if(heldFrames<255)++heldFrames;
    if(heldFrames==0||heldFrames>=18){
        row=QuestInventory::move(row,direction);
        if(heldFrames>=18)heldFrames=13;
    }'''+s[end:]
    if p.name=='game.cpp':
        s=s.replace('min(titleRow + 1, rows)', 'min(titleRow + 1, (int)rows)')
        s=s.replace('    uint8_t** rowPtr', '    if(x>=pgm_read_byte(TileRoom::map+2)||y>=pgm_read_byte(TileRoom::map+3)) return;\n    uint8_t** rowPtr')
        s=s.replace('    lastRoomWasLit = roomIsLit();','    if(nextRoomX>=pgm_read_byte(TileRoom::map+2)||nextRoomY>=pgm_read_byte(TileRoom::map+3)){player.undoMove();return;}\n    lastRoomWasLit = roomIsLit();')
        s=s.replace('    uint8_t e = spawnNewEntity(CHEST, player);','    int8_t e = spawnNewEntity(CHEST, player);\n    if(e<0) return;')
        start=s.index('            if (player.bButtonEntityType != UNSET)',s.index('void Game::updatePlay'))
        end=s.index('            push(&Game::updateMenu',start)
        s=s[:start]+'            menu.open(player.bButtonEntityType);\n\n'+s[end:]
        s=s.replace('        // respond to the decision','        if(!menu.canEquip()) return;\n        menu.select();\n        // respond to the decision')
    if p.name=='game.h':
        s=s.replace('            holdACount(0),','            holdACount(0),\n            toastCount(0),\n            toastString(NULL),')
        s=s.replace('    public:\n        RoomType', '''    public:
        void beginPlay(){loadSave(true);}
        Player& hero(){return player;}
        int scene() const {return currentUpdate==&Game::updateTitle?1:currentUpdate==&Game::updateGameOver?2:currentUpdate==&Game::updateMenu?3:currentUpdate==&Game::updatePlay?0:4;}
        int row() const {return scene()==3?menu.row:titleRow;}
        const char* toastText() const {return toastCount&&toastString?(const char*)toastString:nullptr;}
        void toggleMenu(){if(scene()==3){menu.select();player.bButtonEntityType=menu.chosenItem;player.entities[1].type=UNSET;currentUpdate=&Game::updatePlay;currentRender=&Game::renderPlay;}else if(scene()==0){menu.open(player.bButtonEntityType);prevUpdate=currentUpdate;prevRender=currentRender;currentUpdate=&Game::updateMenu;currentRender=&Game::renderMenu;}}
        RoomType''')
        # No include dependency on State is needed for toggling the menu.
    if p.name in ('drawBitmap.cpp','renderer.cpp'):continue
    s='\n'.join(line.rstrip() for line in s.splitlines()).rstrip()+'\n'
    if not target.exists() or target.read_text(encoding='utf-8')!=s:target.write_text(s,encoding='utf-8')
subprocess.run([sys.executable,str(ROOT/'tools/make_assets.py')],check=True)
print('Assembled ESP32-compatible game source')
