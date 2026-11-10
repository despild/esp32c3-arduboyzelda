# ESP32-C3 Arduboy Zelda-style Adventure

[한국어](README.md) · [User guide / 사용 가이드](USER_GUIDE.md) · [Porting notes](PORTING.md)

An independent repository preparing an Arduboy-style top-down adventure for the ESP32-C3 mini's **0.42-inch, 72×40, 1-bit OLED**. The requested repository name is `esp32c3-arduboyzelda`. This is not Nintendo's Zelda or an NES emulator.

**Current status: source preparation only. There is no playable ESP32 port, game binary or controller mode yet.** Pocket World's current dungeon is a separate original mini game.

## Selected source

The source material is [Ardynia](https://github.com/Pharap/ardynia), originally by Matt Greer, pinned to revision `e07fafd1d076481c6fe3c0f85695c98e2dc976d6`. It targets the 128×64 Arduboy and includes game logic, entities, maps and inventory code.

Its license distinguishes **MIT code from restricted graphics**. A ROM-free project does not automatically grant permission to modify and redistribute its artwork. Original sprite, tile and font images and game binaries are excluded here. Original replacement assets and a silent platform layer must be implemented before integrating a playable port.

## Included material

- `vendor/ardynia/src/`: Unmodified MIT C++ source at the pinned revision, including remaining AVR dependencies.
- `vendor/ardynia/LICENSE`: Full original terms, including the graphics restriction and MIT license.
- `tools/prepare_sources.py`: Code import/verification tool that excludes graphics and audio files.
- `UPSTREAM_MANIFEST.json`: Revision, exclusion list and per-file SHA256 hashes.
- `PORTING.md`: Work needed for 32-bit pointers, display, input, storage and distribution.

Some C++ files reference excluded headers, so **this snapshot does not build as a game yet**. Source preparation and successful board execution are tracked separately.

## Verify the snapshot

```powershell
python tools/prepare_sources.py --check
```

This checks file integrity and excluded files. It does not test gameplay on an ESP32. The working Doom/controller project is available in [esp32-micro-world](https://github.com/despild/esp32-micro-world/tree/main/esp32c3mini-oled0.42-72x40).

New preparation tools are MIT-licensed; imported code retains the original MIT terms. This project is unaffiliated with Nintendo and includes no Nintendo ROMs or assets.
