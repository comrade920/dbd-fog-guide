"""아이콘 스프라이트 생성: 기본 아이콘 저장소(Icon-Pack-Provider/Dead-by-daylight-Default-icons) -> icons/*.webp + icons.json
사용: python3 make_icons.py <아이콘 저장소 경로> <raw 폴더> [2022 데이터 폴더(초상화 매핑용)]
"""
import json, os, sys, glob, math
from PIL import Image
REPO, RAW = sys.argv[1], sys.argv[2]
OLD = sys.argv[3] if len(sys.argv) > 3 else None
CELL = 64
idx = {}
for p in glob.glob(os.path.join(REPO, '**/*.png'), recursive=True):
    idx.setdefault(os.path.splitext(os.path.basename(p))[0].lower(), p)
def base(img): return os.path.splitext(os.path.basename(img or ''))[0].lower()
L = lambda n, loc='ko': json.load(open(os.path.join(RAW, f'{n}_{loc}.json')))
sheets = {'perk': [], 'addon': [], 'misc': [], 'char': []}
icmap = {}   # 키: 이미지 파일 기본이름(소문자) 또는 'char:<캐릭터 id>'
def add(sheet, key, path):
    if key in icmap or not path: return
    icmap[key] = [sheet, len(sheets[sheet])]; sheets[sheet].append(path)
for v in L('perks').values(): add('perk', base(v['image']), idx.get(base(v['image'])))
for v in L('addons').values(): add('addon', base(v['image']), idx.get(base(v['image'])))
for n in ('items', 'offerings'):
    for v in L(n).values(): add('misc', base(v['image']), idx.get(base(v['image'])))
# 캐릭터 초상화: 2022 데이터의 영문 이름 -> charSelect 초상화 파일
if OLD:
    old = {}
    for f in ('killers', 'survivors'):
        for c in json.load(open(os.path.join(OLD, 'en', f + '.json'))):
            old[c['name'].lower()] = c['image'].lower()
    for c in L('characters', 'en').values():
        add('char', 'char:' + c['id'], idx.get(old.get(c['name'].lower(), '')))
os.makedirs('icons', exist_ok=True)
for name, paths in sheets.items():
    if not paths: continue
    cols = math.ceil(math.sqrt(len(paths)))
    rows = math.ceil(len(paths) / cols)
    sheet = Image.new('RGBA', (cols * CELL, rows * CELL), (0, 0, 0, 0))
    for i, p in enumerate(paths):
        im = Image.open(p).convert('RGBA')
        bb = im.getbbox() if name == 'char' else None
        im = im.resize((CELL, CELL), Image.LANCZOS)
        sheet.paste(im, ((i % cols) * CELL, (i // cols) * CELL), im)
    sheet.save(f'icons/{name}.webp', 'WEBP', quality=82, method=6)
    print(name, len(paths), f'{cols}x{rows}', os.path.getsize(f'icons/{name}.webp') // 1024, 'KB')
meta = {n: [math.ceil(math.sqrt(len(p))), math.ceil(len(p) / math.ceil(math.sqrt(len(p))))] for n, p in sheets.items() if p}
json.dump({'cell': CELL, 'cols': meta, 'map': icmap}, open('icons.json', 'w'), separators=(',', ':'))
print('icons.json', len(icmap))
