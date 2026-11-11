# Pocket Quest 사용 가이드 / User guide

## 한국어

통합 펌웨어를 설치한 뒤 Pocket World 컨트롤러에서 **Arduboy · 포켓 퀘스트**를 선택하세요. 기존 ‘던전’ 버튼과 별도 게임입니다. **새 모험**은 Arduboy 저장만 초기화합니다. 이어서 하려면 모드만 선택하세요.

| 입력 | 동작 |
|---|---|
| 방향키 / WASD | 이동 |
| Ctrl / Z | 검 공격, 메뉴 확인 |
| Space | 장착한 보조 아이템 |
| Enter / Tab | 장비·지도 열기/닫기 |
| Ctrl 길게 | 원본 장비 메뉴 방식 |

장비 화면은 보조 장비 세 칸을 항상 표시합니다. 방향키를 누르거나 길게 눌러 탐색하고, `-`는 미획득, `B`는 장착 중입니다. 보유한 장비에서 Ctrl 또는 Enter를 누르면 장착하고 닫습니다. 미획득 장비에서 Ctrl을 누르면 그대로이며, Enter/Tab으로 현재 장비를 유지한 채 닫을 수 있습니다. 검은 이 목록에서 선택하지 않고 플레이 중 Ctrl로 사용합니다. 오른쪽 지도는 방문 기록 표시이며 선택 커서가 없습니다.

시작 방에서 오른쪽으로 두 방 가면 검 상자가 있습니다. 아래에서 위로 접근해 검을 얻으세요. **모험 진행 저장**은 아이템·방 클리어 진행을 별도 `ard-quest` NVS에 저장합니다. 위치·적 상태 전체를 저장하지 않으며 재시작은 지역 입구에서 합니다. 라이브 뷰를 꺼도 OLED와 입력은 계속 동작합니다. Windows 잠금 시 모험은 멈추고 통합 호스트의 펫이 움직입니다.

### 단독 빌드와 업로드

Arduino CLI, Espressif Arduino core 3.1.1, Python 3.10+가 필요합니다. SSD1306 연결은 SDA5/SCL6, 주소 0x3C입니다. 원본 ROM이나 WAD는 필요하지 않습니다.

```powershell
python tools/prepare_sources.py --check
python tools/check_maps.py
./tools/build.ps1
python -m pip install 'esptool>=5,<6' pyserial Pillow
python tools/flash.py --port COM4
```

CLI가 기본 Arduino IDE 경로와 다르면 `-ArduinoCli 'C:/path/arduino-cli.exe'`를 사용합니다. 산출물은 `build/firmware/ArduboyQuest.ino.*`입니다. 업로드 전 컨트롤러를 닫고 기존 보드를 백업하세요. 단독 버전은 모험 게임만 포함하며 잠금이나 연결 단절 시 일시 정지합니다. 펫·Doom을 함께 사용하려면 [상위 통합 프로젝트](https://github.com/despild/esp32-micro-world/tree/main/esp32c3mini-oled0.42-72x40)를 사용하세요.

미리 빌드한 단독 파일은 `bin/`에 있습니다. `python tools/flash.py --port COM4 --build bin`으로 업로드할 수 있으며 [SHA256](bin/BUILD_INFO.json)을 제공합니다. 단독 파일은 빌드 검증을, 동일 게임 소스의 통합 버전은 실물 플레이 검증을 완료했습니다.

### 검사

```powershell
python tools/qa_board.py --port COM4 --inspect
python tools/qa_board.py --port COM4
```

첫 명령은 현재 상태와 화면을 저장합니다. 두 번째 명령은 **새 모험으로 저장을 초기화하고** 실제 키 입력을 검사합니다. 컨트롤러를 닫고 실행하며 결과는 `output/board-qa/`에 저장합니다.

## English

After installing integrated firmware, select **Arduboy · 포켓 퀘스트 (Pocket Quest)** in the Pocket World controller. It is separate from the original mini-dungeon button. **새 모험 (New adventure)** clears only Arduboy progress. Select just the mode to continue.

| Input | Action |
|---|---|
| Arrows / WASD | Move |
| Ctrl / Z | Sword attack, menu confirm |
| Space | Equipped secondary item |
| Enter / Tab | Open/close inventory and map |
| Hold Ctrl | Original inventory shortcut |

Inventory always shows all three secondary-item slots. Tap or hold the arrows to browse; `-` means unowned and `B` means equipped. Ctrl or Enter equips an owned selection and closes the menu. Ctrl on an unowned slot leaves the menu open; Enter/Tab closes it without changing equipment. The sword is used directly with Ctrl during play and is not selected here. The map on the right displays visited rooms and has no selection cursor.

The sword chest is two rooms to the right of the start. Approach from below. **모험 진행 저장 (Save adventure)** stores items and room completion in the separate `ard-quest` NVS namespace. It does not preserve exact positions or all actors; restarts begin at the region entrance. Live view can be disabled while OLED gameplay and controls continue. On Windows lock the adventure pauses while the integrated host displays the pet.

### Standalone build and upload

Requires Arduino CLI, Espressif Arduino core 3.1.1 and Python 3.10+. SSD1306 wiring: SDA5/SCL6, address 0x3C. No original ROM or WAD is required.

```powershell
python tools/prepare_sources.py --check
python tools/check_maps.py
./tools/build.ps1
python -m pip install 'esptool>=5,<6' pyserial Pillow
python tools/flash.py --port COM4
```

Use `-ArduinoCli 'C:/path/arduino-cli.exe'` if the CLI is not at the default Arduino IDE path. Outputs are `build/firmware/ArduboyQuest.ino.*`. Close the controller and back up existing firmware before uploading. Standalone firmware contains only the adventure and pauses on lock/disconnection. Use the [parent integrated project](https://github.com/despild/esp32-micro-world/tree/main/esp32c3mini-oled0.42-72x40) to retain pet and Doom modes.

Prebuilt standalone files are in `bin/`. Flash with `python tools/flash.py --port COM4 --build bin`; [SHA256 hashes](bin/BUILD_INFO.json) are provided. Standalone files passed compilation; real-board gameplay was tested using the integrated build of the same game source.

### Verify

```powershell
python tools/qa_board.py --port COM4 --inspect
python tools/qa_board.py --port COM4
```

The first command records current state and display. The second **starts a new adventure and clears its save** before testing real controls. Close the controller first. Results go to `output/board-qa/`.

## USB protocol / USB 프로토콜

115200 baud, newline commands: `HELLO`, `MODE 3`, `KEY n` every ~80ms, `LOCK 0/1`, `MIRROR 0/1`, `ARD STATE`, `ARD SAVE`, `ARD NEW`. Key bits: 0 secondary item / 보조 아이템, 1 sword / 검, 4/5 up/down / 위아래, 6/7 left/right / 좌우, 8/9 inventory / 장비.

`ard` JSON reports position, room and inventory / 좌표·방·아이템 상태. `frame.hex` is the 360-byte SSD1306 page buffer / OLED 페이지 버퍼. The separate source snapshot is in `vendor/`; the port is in `src/`. Reapply adaptations with `tools/assemble_port.py`; regenerate original art with `tools/make_assets.py`.
