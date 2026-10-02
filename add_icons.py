"""기존 아이콘 스프라이트에 빠진 아이콘 추가
사용: python3 add_icons.py <추가 PNG 폴더> <raw 폴더>
추가 폴더의 파일 이름: 게임 이미지 파일 기본이름(소문자).png, 캐릭터 초상화는 char_<캐릭터 id>.png
(공식 위키 deadbydaylight.wiki.gg 에서 받은 것: icons_src/wiki)
"""
import json, os, sys, math
from PIL import Image
SRC, RAW = sys.argv[1], sys.argv[2]
meta = json.load(open('icons.json')); CELL = meta['cell']; icmap = meta['map']
sheets = {}
for name, (cols, rows) in meta['cols'].items():
    sh = Image.open(f'icons/{name}.webp').convert('RGBA')
    n = sum(1 for v in icmap.values() if v[0] == name)
    sheets[name] = [sh.crop(((i % cols) * CELL, (i // cols) * CELL, (i % cols + 1) * CELL, (i // cols + 1) * CELL)) for i in range(n)]
def base(img): return os.path.splitext(os.path.basename(img or ''))[0].lower()
L = lambda n, loc='en': json.load(open(os.path.join(RAW, f'{n}_{loc}.json')))
added = 0
def add(sheet, key, path, crop=False):
    global added
    if key in icmap or not os.path.exists(path): return
    im = Image.open(path).convert('RGBA')
    if crop and im.getbbox(): im = im.crop(im.getbbox())
    im = im.resize((CELL, CELL), Image.LANCZOS)
    sheets.setdefault(sheet, []); icmap[key] = [sheet, len(sheets[sheet])]; sheets[sheet].append(im); added += 1
for n, sh in (('perks', 'perk'), ('addons', 'addon'), ('items', 'misc'), ('offerings', 'misc')):
    for v in L(n).values(): add(sh, base(v['image']), os.path.join(SRC, base(v['image']) + '.png'))
for c in L('characters').values(): add('char', 'char:' + c['id'], os.path.join(SRC, f"char_{c['id']}.png"), crop=True)
cols_meta = {}
for name, cells in sheets.items():
    cols = math.ceil(math.sqrt(len(cells))); rows = math.ceil(len(cells) / cols)
    out = Image.new('RGBA', (cols * CELL, rows * CELL), (0, 0, 0, 0))
    for i, im in enumerate(cells): out.paste(im, ((i % cols) * CELL, (i // cols) * CELL), im)
    out.save(f'icons/{name}.webp', 'WEBP', quality=82, method=6); cols_meta[name] = [cols, rows]
    print(name, len(cells), f'{cols}x{rows}', os.path.getsize(f'icons/{name}.webp') // 1024, 'KB')
json.dump({'cell': CELL, 'cols': cols_meta, 'map': icmap}, open('icons.json', 'w'), separators=(',', ':'))
print('추가', added, '/ 전체', len(icmap))
