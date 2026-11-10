"""Import MIT C++ code only from a pinned Ardynia checkout.

Original artwork, font bitmaps, bundled sounds and the original game binary are
excluded. This produces source material for a port, not a buildable game.
"""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
REVISION = 'e07fafd1d076481c6fe3c0f85695c98e2dc976d6'
UPSTREAM = 'https://github.com/Pharap/ardynia'
EXCLUDED = {'spriteBitmaps.h', 'tileBitmaps.h', 'tinyfontSprite.h', 'strings.h', 'sfx.cpp', 'sfx.h'}

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('checkout', type=Path, nargs='?')
    parser.add_argument('--check', action='store_true', help='Verify the committed source inventory without importing')
    args = parser.parse_args()
    target = ROOT / 'vendor/ardynia'
    manifest_path = ROOT / 'UPSTREAM_MANIFEST.json'
    if args.check:
        manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
        actual = {p.relative_to(target).as_posix(): digest(p) for p in target.rglob('*') if p.is_file()}
        if actual != manifest['sha256']:
            raise SystemExit('Source inventory changed; review and regenerate intentionally.')
        if any(Path(p).name in EXCLUDED for p in actual):
            raise SystemExit('Excluded asset/audio file is present.')
        print('PASS: pinned source inventory and excluded asset headers')
        return
    if args.checkout is None:
        parser.error('A pinned upstream checkout is required for import.')
    revision = subprocess.check_output(['git', '-C', str(args.checkout), 'rev-parse', 'HEAD'], text=True).strip()
    if revision != REVISION:
        raise SystemExit('Unexpected revision. Expected ' + REVISION)
    dirty = subprocess.check_output(['git', '-C', str(args.checkout), 'status', '--porcelain'], text=True).strip()
    if dirty:
        raise SystemExit('Upstream checkout has local changes; import requires a clean checkout.')
    source = args.checkout / 'ardynia/src'
    target.mkdir(parents=True, exist_ok=True)
    for path in source.rglob('*'):
        if path.is_file() and path.suffix in ('.h', '.cpp') and path.name not in EXCLUDED:
            dest = target / 'src' / path.relative_to(source)
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(path.read_bytes().replace(b'\r\n', b'\n'))
    (target / 'LICENSE').write_bytes((args.checkout / 'LICENSE').read_bytes().replace(b'\r\n', b'\n'))
    files = {p.relative_to(target).as_posix(): digest(p) for p in sorted(target.rglob('*')) if p.is_file()}
    if any(Path(p).name in EXCLUDED for p in files):
        raise SystemExit('Excluded files already exist in destination; inspect them before publishing.')
    manifest_path.write_text(json.dumps({
        'upstream': UPSTREAM, 'revision': REVISION,
        'status': 'Source preparation only; no playable ESP32 firmware yet.',
        'excluded': sorted(EXCLUDED), 'sha256': files,
    }, indent=2) + '\n', encoding='utf-8')
    print('Imported', len(files), 'source/license files; original graphics and sounds excluded.')

if __name__ == '__main__':
    main()
