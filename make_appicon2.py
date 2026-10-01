"""안개 도감 앱 아이콘 v2: 안개 사진 배경 + 가운데 'DBD' 글자"""
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageChops
import sys, os
FOG, FONT, OUT = sys.argv[1], sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else 'appicon'
S = 1024
fog = Image.open(FOG).convert('RGB')
# 안개 사진을 정사각형 아래쪽에 크게 깔기 (저해상도라 키운 뒤 살짝 흐리게)
w = int(S * 1.25); h = int(fog.height * w / fog.width)
fog = fog.resize((w, h), Image.LANCZOS).filter(ImageFilter.GaussianBlur(6))
canvas = Image.new('RGB', (S, S), (6, 6, 8))
canvas.paste(fog, ((S - w)//2, S - h + 40))
# 위쪽은 검정으로 자연스럽게
grad = Image.new('L', (S, S), 0); gd = ImageDraw.Draw(grad)
for y in range(S): gd.line([(0, y), (S, y)], fill=int(255 * min(1, max(0, (y - S*0.18) / (S*0.45)))))
canvas = Image.composite(canvas, Image.new('RGB', (S, S), (6, 6, 8)), grad)
# 붉은 빛 번짐
glow = Image.new('RGB', (S, S), (0, 0, 0)); ImageDraw.Draw(glow).ellipse([S*0.2, S*0.28, S*0.8, S*0.62], fill=(120, 14, 24))
glow = glow.filter(ImageFilter.GaussianBlur(90))
canvas = ImageChops.add(canvas, glow)
# 글자
font = ImageFont.truetype(FONT, 330)
txt = Image.new('L', (S, S), 0); td = ImageDraw.Draw(txt)
bb = td.textbbox((0, 0), 'DBD', font=font)
tw, th = bb[2]-bb[0], bb[3]-bb[1]
pos = ((S - tw)/2 - bb[0], S*0.43 - th/2 - bb[1])
td.text(pos, 'DBD', font=font, fill=255)
shadow = txt.filter(ImageFilter.GaussianBlur(14))
canvas = Image.composite(Image.new('RGB', (S, S), (0, 0, 0)), canvas, shadow.point(lambda v: v*0.8))
canvas = Image.composite(Image.new('RGB', (S, S), (238, 232, 234)), canvas, txt)
# 앞쪽 안개: 글자 아랫부분을 살짝 덮음
front = Image.open(FOG).convert('L').resize((w, h), Image.LANCZOS).filter(ImageFilter.GaussianBlur(10))
mask = Image.new('L', (S, S), 0); mask.paste(front, ((S - w)//2 + 60, int(S*0.40)))
mask = mask.point(lambda v: int(v * 0.55))
canvas = Image.composite(Image.new('RGB', (S, S), (215, 214, 218)), canvas, mask)
os.makedirs(OUT, exist_ok=True)
canvas.save(f'{OUT}/icon-1024.png')
for n, size in [('apple-touch-icon.png', 180), ('icon-192.png', 192), ('icon-512.png', 512), ('favicon-32.png', 32)]:
    canvas.resize((size, size), Image.LANCZOS).save(f'{OUT}/{n}', optimize=True)
print('ok', OUT)
