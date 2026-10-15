# 영상 "작업물" 장면용 패널 4장 (사이트 작업물 이미지에서 글자 없이 렌더 영역만)
# 사용: python3 make_panels.py <사이트 assets 폴더>  → panels/p0.jpg … p3.jpg
import sys, os
from PIL import Image
A = sys.argv[1]
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'panels'); os.makedirs(OUT, exist_ok=True)
for i, (f, box) in enumerate([('01_shinano_katana', (29, 207, 1971, 692)), ('02_rurune_sameholic', (29, 207, 1971, 692)),
                              ('03_lasyusha_phantomflare', (29, 175, 1971, 660)), ('07_chocolat_elphelt', (29, 240, 1971, 725))]):
    im = Image.open(os.path.join(A, 'portfolio', f + '.jpg')).convert('RGB').crop(box)
    im.resize((1600, round(im.height * 1600 / im.width)), Image.LANCZOS).save(os.path.join(OUT, f'p{i}.jpg'), quality=92)
print('panels →', OUT)
