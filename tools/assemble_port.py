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
    if p.name=='game.cpp':
        s=s.replace('min(titleRow + 1, rows)', 'min(titleRow + 1, (int)rows)')
        s=s.replace('    uint8_t** rowPtr', '    if(x>=pgm_read_byte(TileRoom::map+2)||y>=pgm_read_byte(TileRoom::map+3)) return;\n    uint8_t** rowPtr')
        s=s.replace('    lastRoomWasLit = roomIsLit();','    if(nextRoomX>=pgm_read_byte(TileRoom::map+2)||nextRoomY>=pgm_read_byte(TileRoom::map+3)){player.undoMove();return;}\n    lastRoomWasLit = roomIsLit();')
        s=s.replace('    uint8_t e = spawnNewEntity(CHEST, player);','    int8_t e = spawnNewEntity(CHEST, player);\n    if(e<0) return;')
    if p.name=='game.h':
        s=s.replace('            holdACount(0),','            holdACount(0),\n            toastCount(0),\n            toastString(NULL),')
        s=s.replace('    public:\n        RoomType', '''    public:
        void beginPlay(){loadSave(true);}
        Player& hero(){return player;}
        int scene() const {return currentUpdate==&Game::updateTitle?1:currentUpdate==&Game::updateGameOver?2:currentUpdate==&Game::updateMenu?3:currentUpdate==&Game::updatePlay?0:4;}
        int row() const {return scene()==3?menu.row:titleRow;}
        const char* toastText() const {return toastCount&&toastString?(const char*)toastString:nullptr;}
        void toggleMenu(){if(scene()==3){player.bButtonEntityType=menu.chosenItem;player.entities[1].type=UNSET;currentUpdate=&Game::updatePlay;currentRender=&Game::renderPlay;}else if(scene()==0){menu.row=0;menu.chosenItem=player.bButtonEntityType;prevUpdate=currentUpdate;prevRender=currentRender;currentUpdate=&Game::updateMenu;currentRender=&Game::renderMenu;}}
        RoomType''')
        # No include dependency on State is needed for toggling the menu.
    if p.name in ('drawBitmap.cpp','renderer.cpp'):continue
    s='\n'.join(line.rstrip() for line in s.splitlines()).rstrip()+'\n'
    if not target.exists() or target.read_text(encoding='utf-8')!=s:target.write_text(s,encoding='utf-8')
subprocess.run([sys.executable,str(ROOT/'tools/make_assets.py')],check=True)
print('Assembled ESP32-compatible game source')
