# 사용 가이드 / User guide

## 한국어

이 저장소는 아직 플레이용 펌웨어가 아닙니다. 현재 ESP32에서 사용하는 펫·미니 던전·Doom은 [Pocket World](https://github.com/despild/esp32-micro-world/tree/main/esp32c3mini-oled0.42-72x40)의 컨트롤러와 펌웨어를 사용하세요. 이 저장소를 업로드해 기존 보드를 교체하지 마세요.

### 소스 확인

```powershell
git clone https://github.com/despild/esp32c3-arduboyzelda.git
cd esp32c3-arduboyzelda
python tools/prepare_sources.py --check
```

### 원본에서 다시 가져오기

Python 3.10+와 Git을 사용합니다. 원본 checkout은 수정하지 않은 고정 버전이어야 합니다.

```powershell
git clone https://github.com/Pharap/ardynia downloads/ardynia
git -C downloads/ardynia checkout e07fafd1d076481c6fe3c0f85695c98e2dc976d6
python tools/prepare_sources.py downloads/ardynia
python tools/prepare_sources.py --check
```

가져오기 도구는 그래픽/폰트/음원 헤더를 제외합니다. 원본 `spritePngs`, `tilePngs`, 완성 게임 이미지 및 바이너리를 이 포트의 배포물에 추가하지 마세요. 남은 구현 작업은 [PORTING.md](PORTING.md)에 기록합니다.

## English

This repository is not playable firmware yet. Use the controller and firmware in [Pocket World](https://github.com/despild/esp32-micro-world/tree/main/esp32c3mini-oled0.42-72x40) for the working pet, mini dungeon and Doom. Do not replace your board firmware with this preparation snapshot.

### Inspect the source

```powershell
git clone https://github.com/despild/esp32c3-arduboyzelda.git
cd esp32c3-arduboyzelda
python tools/prepare_sources.py --check
```

### Reimport from upstream

Use Python 3.10+ and Git. The upstream checkout must be clean and at the pinned revision.

```powershell
git clone https://github.com/Pharap/ardynia downloads/ardynia
git -C downloads/ardynia checkout e07fafd1d076481c6fe3c0f85695c98e2dc976d6
python tools/prepare_sources.py downloads/ardynia
python tools/prepare_sources.py --check
```

The importer excludes graphics/font/audio headers. Do not add original `spritePngs`, `tilePngs`, complete game images or binaries to the derivative port's distribution. Remaining implementation work is documented in [PORTING.md](PORTING.md).
