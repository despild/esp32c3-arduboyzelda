# 포팅 내역 / Porting notes

원본 MIT 코드는 `vendor/ardynia/`에 유지하며 `tools/assemble_port.py`로 `src/game/`를 생성합니다. 플랫폼·렌더러·에셋은 `src/hal/`, `src/ArdAdventure.*`, 자체 game 파일에서 관리합니다.

The unchanged MIT snapshot remains in `vendor/ardynia/`; `tools/assemble_port.py` generates adapted `src/game/` files. Platform, rendering and new assets are maintained separately.

| 변경 / Change | 위치 / Location |
|---|---|
| 32비트 포인터 / 32-bit pointer reads | game, loadEntity, HUD |
| AVR 어셈블리 교체 / Portable clipped bitmap renderer | drawBitmap.cpp |
| NVS 저장 / Separate versioned save record | hal/SaveStore.h |
| 자체 스프라이트·타일·폰트 / Original replacement artwork | make_assets.py, hal/Font.h |
| 무음 / No audio allocations or assets | game/sfx.h |
| 정수형·부호·콜백 수정 / Integer, signed velocity and callback corrections | entityTemplates, skeleton, torch, player |
| 맵 경계·압축 길이·빈 엔티티 슬롯 검사 / Bounds checks | tileRoom, game |
| 네이티브 HUD·장비·지도 / Native OLED menus | ArdAdventure.cpp |
| Arduino 빌드 단위 통합 / Single-unit staging to reduce header discovery | stage_source.py |

게임 좌표와 맵은 유지합니다. 112×64 게임 영역을 72×34로 축소하고, 아래 6줄에 HUD를 표시합니다. 자체 그림은 어두운 배경과 밝은 물체로 통일하여 원본 던전의 반전을 제거했습니다.

Logical coordinates and maps are retained. The 112×64 playfield is sampled to 72×34 with a native six-row HUD. Replacement art uses dark backgrounds and bright objects; original dungeon inversion is removed.

`tools/check_maps.py`: 필드 42 + 던전 64 = 106개 방이 각각 28개의 유효 타일로 해석되는지 검사 / validates all 106 compressed rooms.

`tools/qa_board.py`: USB 입력으로 이동·방 전환·검 획득/공격·장비 메뉴·라이브 뷰·잠금 일시 정지 검사 / exercises real USB gameplay, menus, readback and pause.

`tools/qa_inventory.py`: 저장 초기화 없이 장비가 없는 상태의 커서 이동, 길게 누르기, 미획득 장착 차단, 메뉴 재진입, 라이브 뷰 OFF 중 입력을 검사합니다. / Checks inventory navigation, key repeat, locked-item rejection, reopening and input while readback is off, without resetting progress.

2026-11-11: 보조 장비가 없으면 메뉴가 고정되어 보이던 문제를 수정했습니다. 세 슬롯을 항상 표시하고 장착 가능 여부를 구분합니다. 메뉴 재진입 시 현재 장착 슬롯을 유지합니다. / The menu now displays three browsable slots even with no secondary items, rejects unowned equipment and reopens on the equipped slot. Compile-time regressions cover empty, partial and full inventories in `hal/InventorySelection.h`.

전체 퍼즐·보스 완주는 아직 검증하지 않았습니다. / A complete playthrough of all puzzles and bosses has not been verified.
