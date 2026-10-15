# 사이트의 작업물 렌더를 의상 카드(둥근 모서리 PNG) 28장으로 나눕니다.
# 사용: python3 prep_cards.py <사이트 assets 폴더>
#   → cards/c00.png … c27.png, cards/cards.json
import sys, os, json
from PIL import Image, ImageDraw

ASSETS = sys.argv[1]
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cards')
os.makedirs(OUT, exist_ok=True)

# (파일, 회색 렌더 패널 crop(글자 영역 제외), 열 개수, 쓸 열, 열 안에서 가로로 남길 비율)
SPEC = [
    ('portfolio/01_shinano_katana.jpg', (29, 207, 1971, 692), 4, [0, 3], .72),
    ('portfolio/02_rurune_sameholic.jpg', (29, 207, 1971, 692), 4, [0, 3], .72),
    ('portfolio/03_lasyusha_phantomflare.jpg', (29, 175, 1971, 660), 4, [0, 3], .72),
    ('portfolio/07_chocolat_elphelt.jpg', (29, 240, 1971, 725), 4, [0, 3], .72),
    ('portfolio/04_milltina_closet.jpg', (24, 190, 1976, 518), 6, range(6), 1.0),
    ('portfolio/05_milltina_fitting.jpg', (24, 165, 1976, 492), 6, range(6), 1.0),
    ('works-outfits.jpg', None, 4, range(4), 1.0),
    ('works-closet.jpg', None, 4, range(4), 1.0),
]

out, n = [], 0
for f, box, cols, use, keep in SPEC:
    im = Image.open(os.path.join(ASSETS, f)).convert('RGB')
    if box: im = im.crop(box)
    W, H = im.size; cw = W / cols
    inset = 2 if keep == 1.0 and box else 0
    for c in use:
        x0 = c * cw + cw * (1 - keep) / 2; x1 = x0 + cw * keep
        t = im.crop((round(x0) + inset, 0, round(x1) - inset, H))
        s = 900 / max(t.size); t = t.resize((round(t.width * s), round(t.height * s)), Image.LANCZOS)
        w, h = t.size; r = round(min(w, h) * .07); b = 8
        card = Image.new('RGBA', (w + 2 * b, h + 2 * b), (0, 0, 0, 0))
        m = Image.new('L', card.size, 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, card.width - 1, card.height - 1], r + b, fill=255)
        card.paste(Image.new('RGBA', card.size, (155, 131, 255, 255)), (0, 0), m)   # 보라 테두리
        m2 = Image.new('L', (w, h), 0); ImageDraw.Draw(m2).rounded_rectangle([0, 0, w - 1, h - 1], r, fill=255)
        card.paste(t, (b, b), m2)
        name = f'c{n:02d}.png'; card.save(os.path.join(OUT, name))
        out.append({'path': name, 'w': card.width, 'h': card.height}); n += 1

json.dump(out, open(os.path.join(OUT, 'cards.json'), 'w'))
print(n, 'cards →', OUT)
