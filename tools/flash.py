"""Flash only the standalone host; retain NVS and the reserved upper flash."""
from pathlib import Path
import argparse,subprocess,sys
ROOT=Path(__file__).resolve().parents[1]
def main():
    p=argparse.ArgumentParser();p.add_argument('--port',required=True);p.add_argument('--build',type=Path,default=ROOT/'build/firmware');a=p.parse_args()
    files=[(0,'bootloader.bin',0x8000),(0x8000,'partitions.bin',0x1000),(0x10000,'bin',0x100000)]
    command=[sys.executable,'-m','esptool','--chip','esp32c3','--port',a.port,'--baud','115200','write-flash','--flash-mode','dio','--flash-freq','80m','--flash-size','4MB']
    for address,suffix,limit in files:
        path=a.build/('ArduboyQuest.ino.'+suffix)
        if not path.is_file() or not 0<path.stat().st_size<=limit:raise SystemExit('Missing/oversize firmware: '+str(path))
        command.extend([hex(address),str(path)])
    subprocess.run(command,check=True)
if __name__=='__main__':main()
