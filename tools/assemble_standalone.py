"""Stage the module source under Arduino's recursive src build directory."""
from pathlib import Path
from stage_source import stage
ROOT=Path(__file__).resolve().parents[1]
stage(ROOT/'firmware/ArduboyQuest/src')
print(ROOT/'firmware/ArduboyQuest')
