"""안개 도감 앱 아이콘 v3: 무료 사진(CC0/퍼블릭 도메인) 배경 + 가운데 'DBD'
사용: python3 make_appicon3.py <배경 사진> <글꼴> <출력 폴더> [crop_x 0~1] [tint r,g,b] [text_y 0~1]
"""
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageEnhance, ImageChops, ImageOps
import sys, os
SRC, FONT, OUT = sys.argv[1:4]
cx = float(sys.argv[4]) if len(sys.argv) > 4 else 0.5
tint = tuple(int(v) for v in (sys.argv[5] if len(sys.argv) > 5 else '120,18,28').split(','))
ty = float(sys.argv[6]) if len(sys.argv) > 6 else 0.42
col = tuple(int(v) for v in (sys.argv[7] if len(sys.argv) > 7 else '240,234,236').split(','))
stroke = int(sys.argv[8]) if len(sys.argv) > 8 else 0
S = 1024
im = Image.open(SRC).convert('RGB')
side = min(im.size); left = int((im.width - side) * cx); top = (im.height - side)//2
im = im.crop((left, top, left + side, top + side)).resize((S, S), Image.LANCZOS)
# 색 보정: 채도 낮추고 어둡게, 붉은 기운
im = ImageEnhance.Color(im).enhance(0.25)
im = ImageEnhance.Brightness(im).enhance(0.62)
im = ImageEnhance.Contrast(im).enhance(1.25)
gray = ImageOps.grayscale(im)
red = ImageOps.colorize(gray, black=(4, 3, 5), white=(225, 214, 218), mid=tint)
im = Image.blend(im, red, 0.55)
# 비네트
vig = Image.new('L', (S, S), 0); vd = ImageDraw.Draw(vig)
vd.ellipse([-S*0.25, -S*0.2, S*1.25, S*1.3], fill=255)
vig = vig.filter(ImageFilter.GaussianBlur(160))
im = Image.composite(im, Image.new('RGB', (S, S), (0, 0, 0)), vig)
# 글자 뒤 붉은 빛
glow = Image.new('RGB', (S, S), (0, 0, 0)); ImageDraw.Draw(glow).ellipse([S*0.18, S*(ty-0.17), S*0.82, S*(ty+0.17)], fill=tint)
im = ImageChops.add(im, glow.filter(ImageFilter.GaussianBlur(80)))
# 글자
txt = Image.new('L', (S, S), 0); td = ImageDraw.Draw(txt)
size = 400
while True:  # 글자 폭을 아이콘 폭의 78%에 맞춤
    font = ImageFont.truetype(FONT, size); bb = td.textbbox((0, 0), 'DBD', font=font)
    if bb[2]-bb[0] <= S*0.78 or size < 120: break
    size -= 10
tw, th = bb[2]-bb[0], bb[3]-bb[1]
td.text(((S - tw)/2 - bb[0], S*ty - th/2 - bb[1]), 'DBD', font=font, fill=255)
im = Image.composite(Image.new('RGB', (S, S), (0, 0, 0)), im, txt.filter(ImageFilter.GaussianBlur(16)).point(lambda v: int(v*0.85)))
if stroke:
    ring = Image.new('L', (S, S), 0); ImageDraw.Draw(ring).text(((S - tw)/2 - bb[0], S*ty - th/2 - bb[1]), 'DBD', font=font, fill=255, stroke_width=stroke, stroke_fill=255)
    im = Image.composite(Image.new('RGB', (S, S), (8, 4, 6)), im, ring)
im = Image.composite(Image.new('RGB', (S, S), col), im, txt)
# 앞쪽 엷은 안개
fog = Image.new('L', (S, S), 0); fd = ImageDraw.Draw(fog)
for i, y in enumerate([0.60, 0.68, 0.76]):
    fd.ellipse([-S*0.3 + i*80, S*y, S*1.2 + i*60, S*y + 140], fill=55)
im = Image.composite(Image.new('RGB', (S, S), (200, 196, 204)), im, fog.filter(ImageFilter.GaussianBlur(45)))
os.makedirs(OUT, exist_ok=True)
im.save(f'{OUT}/icon-1024.png')
for n, size in [('apple-touch-icon.png', 180), ('icon-192.png', 192), ('icon-512.png', 512), ('favicon-32.png', 32)]:
    im.resize((size, size), Image.LANCZOS).save(f'{OUT}/{n}', optimize=True)
print('ok', OUT)
