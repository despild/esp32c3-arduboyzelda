# ESP32-C3 Arduboy Zelda-style Adventure

[English](README.en.md) · [사용 가이드 / User guide](USER_GUIDE.md) · [포팅 계획 / Porting notes](PORTING.md)

ESP32-C3 mini의 **0.42인치 72×40 1비트 OLED**에 Arduboy 계열 젤다 스타일 모험 게임을 가져오기 위한 독립 저장소입니다. 저장소 이름은 요청한 `esp32c3-arduboyzelda`를 사용합니다. 닌텐도 원작 젤다나 NES 에뮬레이터는 아닙니다.

**현재 단계: 소스 준비. 아직 실행 가능한 ESP32 포트·게임 바이너리·컨트롤러 게임 모드가 없습니다.** 현재 Pocket World의 ‘던전’은 별도의 자체 미니 게임입니다.

## 선정한 기반

[Ardynia](https://github.com/Pharap/ardynia)의 C++ 게임 코드를 기반 자료로 보관했습니다. 원작자 Matt Greer, 고정 revision `e07fafd1d076481c6fe3c0f85695c98e2dc976d6`입니다. 원본 대상은 128×64 Arduboy이며, 게임 로직·엔티티·맵·인벤토리 코드를 포함합니다.

원작 라이선스는 **코드 MIT / 그래픽 별도 제한**입니다. 따라서 ‘ROM이 필요 없다’는 사실만으로 기존 그래픽을 수정해 배포할 수 있는 것은 아닙니다. 이 저장소에는 원본 스프라이트·타일·폰트 이미지·게임 바이너리를 넣지 않았습니다. 자체 에셋과 무음 플랫폼 계층을 작성한 뒤 실행 포트로 통합해야 합니다.

## 포함한 자료

- `vendor/ardynia/src/`: 고정 버전의 MIT C++ 게임 코드. 원본 그대로이며 AVR 의존 코드도 남아 있습니다.
- `vendor/ardynia/LICENSE`: 그래픽 제한과 MIT 조항을 포함한 원문 전체.
- `tools/prepare_sources.py`: 원본 그림·소리 관련 파일을 제외하는 소스 가져오기/검증 도구.
- `UPSTREAM_MANIFEST.json`: 원본 revision, 제외 목록, 파일별 SHA256.
- `PORTING.md`: 32비트 포인터, 디스플레이, 입력, 저장, 배포 작업 목록.

제외된 헤더를 참조하는 C++ 코드가 있으므로 **현재 상태 그대로는 빌드되지 않습니다.** 소스가 준비되었다는 사실과 보드 실행 검증을 구분해 관리합니다.

## 검증

```powershell
python tools/prepare_sources.py --check
```

파일 무결성과 제외 대상 유무를 확인합니다. ESP32 게임 실행 검증은 아직 하지 않았습니다. Doom과 현재 컨트롤러는 [esp32-micro-world](https://github.com/despild/esp32-micro-world/tree/main/esp32c3mini-oled0.42-72x40)에서 사용할 수 있습니다.

새 포팅 도구 코드는 MIT, 가져온 코드는 원저작자의 MIT 조건을 따릅니다. 닌텐도와 무관한 팬 프로젝트 준비 작업이며 닌텐도 ROM이나 에셋을 포함하지 않습니다.
