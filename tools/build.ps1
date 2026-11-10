param([string]$ArduinoCli="$env:LOCALAPPDATA/Programs/Arduino IDE/resources/app/lib/backend/resources/arduino-cli.exe",[string]$Python='python')
$ErrorActionPreference='Stop'
$repoRoot=Split-Path -Parent $PSScriptRoot
& $Python (Join-Path $PSScriptRoot 'assemble_standalone.py')
if($LASTEXITCODE -ne 0){throw 'Source assembly failed'}
$config=Join-Path $repoRoot 'local-arduino.yaml'
$dataPath="$env:LOCALAPPDATA/Arduino15".Replace('\','/')
$userPath=(Join-Path $repoRoot 'build/arduino-user').Replace('\','/')
"directories:`n  data: $dataPath`n  user: $userPath" | Set-Content -LiteralPath $config -Encoding utf8
& $ArduinoCli --config-file $config compile --fqbn 'esp32:esp32:esp32c3:CDCOnBoot=cdc,FlashSize=4M' --build-path "$repoRoot/build/firmware" "$repoRoot/firmware/ArduboyQuest"
if($LASTEXITCODE -ne 0){throw 'Arduboy firmware build failed'}
