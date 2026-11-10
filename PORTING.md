# 포팅 상태와 계획 / Porting status and plan

## 확인된 사항 / Confirmed

- 코드·그래픽 라이선스 분리와 고정 소스 inventory를 확인했습니다. / Code/artwork terms and the pinned source inventory have been reviewed.
- 원본 논리 화면은 128×64이며 SSD1306 페이지 형식 버퍼는 1,024바이트입니다. 목표 출력은 72×40, 360바이트입니다. / The source logical display is 128×64 (1,024 bytes in page format); the target is 72×40 (360 bytes).
- `drawBitmap.cpp`에는 AVR 전용 렌더링이 있으며 ESP32에서 직접 실행할 수 없습니다. / The bitmap renderer contains AVR-specific code and needs replacement.
- `pgm_read_word`로 포인터를 읽는 경로는 ESP32의 32비트 포인터에 맞춰 수정해야 합니다. / Pointer reads using `pgm_read_word` need a 32-bit-safe replacement.

## 미완료 작업 / Outstanding work

| 작업 / Work | 적용 위치 / Location |
|---|---|
| 자체 1비트 스프라이트·타일·폰트 및 제목 / Original one-bit sprites, tiles, font and title | Excluded `spriteBitmaps.h`, `tileBitmaps.h`, `tinyfontSprite.h`, `strings.h` replacements |
| Arduboy 입력·프레임 버퍼 호환 계층 / Arduboy input/framebuffer compatibility | New ESP32 HAL for `Arduboy2Base` |
| AVR 어셈블리 대신 클리핑된 C++ 렌더러 / Clipped portable C++ bitmap renderer | `drawBitmap.cpp` |
| 포인터 크기와 부호 있는 속도값 검토 / Pointer-width and signed velocity audit | `game.cpp`, `loadEntity.cpp`, `hud.cpp`, `entities/skeleton.cpp` |
| 게임 영역 축소 또는 카메라, 읽을 수 있는 HUD / Downsampled or camera-based playfield and readable HUD | Renderer and menu/HUD |
| 오디오 제거 / Silent sound implementation | `sfx` replacement |
| EEPROM 대신 NVS 저장 / NVS-backed persistence | `state.cpp` and platform storage |
| USB 버튼 매핑·입력 타임아웃 / USB controls and input timeout | Same controller protocol as Pocket World |
| 별도 펌웨어 빌드·실물 검증 / Standalone build and real-board tests | Boot, room transition, enemies, items, saves, reset |
| 검증 후 Pocket World 게임 목록 통합 / Add controller mode after verification | Parent application |

128×64를 단순히 72×40으로 축소하면 작은 글자와 공격 판정이 잘 보이지 않을 수 있습니다. 출력 해상도 변경만으로 게임 플레이 품질을 보장할 수 없으므로 새 에셋·HUD와 함께 검증해야 합니다.

Simply reducing 128×64 to 72×40 can obscure text and combat cues. A changed framebuffer size alone does not establish playability; replacement art and HUD need real display testing.

전체 펌웨어의 RAM/Flash 수치, 프레임 속도, 던전 완주 여부는 아직 측정하지 않았습니다. / Full-port RAM/flash use, frame rate and dungeon completion have not been measured yet.
