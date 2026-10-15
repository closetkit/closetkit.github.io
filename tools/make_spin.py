# Unity 촬영본(PNG) → 사이트용 360° 이미지(WebP)
# 사용: python3 make_spin.py <촬영 폴더> <사이트 assets/spin/아바타id> [높이px=900] [품질=82]
#   촬영 폴더 구조: <촬영 폴더>/<옷 id>/00.png … NN.png  (ClosetKitTurntable.cs 가 만드는 구조 그대로)
# 모든 옷·각도의 투명 영역을 합쳐 한 번만 잘라서, 옷을 바꾸거나 돌려도 위치가 흔들리지 않습니다.
import sys, os, glob, json
from PIL import Image

src, dst = sys.argv[1], sys.argv[2]
H = int(sys.argv[3]) if len(sys.argv) > 3 else 900
Q = int(sys.argv[4]) if len(sys.argv) > 4 else 82
outfits = sorted(d for d in os.listdir(src) if os.path.isdir(os.path.join(src, d)))
frames = {o: sorted(glob.glob(os.path.join(src, o, '*.png'))) for o in outfits}
counts = {len(v) for v in frames.values()}
assert len(counts) == 1 and counts != {0}, f'옷마다 장 수가 같아야 합니다: { {o: len(v) for o, v in frames.items()} }'
N = counts.pop()

box = None
for o in outfits:
    for f in frames[o]:
        b = Image.open(f).getchannel('A').getbbox()
        if b: box = b if box is None else (min(box[0], b[0]), min(box[1], b[1]), max(box[2], b[2]), max(box[3], b[3]))
W0, H0 = Image.open(frames[outfits[0]][0]).size
pad = round(0.03 * (box[3] - box[1]))
box = (max(0, box[0] - pad), max(0, box[1] - pad), min(W0, box[2] + pad), min(H0, box[3] + pad))
# 뷰어 칸(3:4)에 맞게 가로를 넓혀서 가운데 정렬
cw = max(box[2] - box[0], round((box[3] - box[1]) * 3 / 4)); cx = (box[0] + box[2]) / 2
box = (round(cx - cw / 2), box[1], round(cx + cw / 2), box[3])

total = 0
for o in outfits:
    os.makedirs(os.path.join(dst, o), exist_ok=True)
    for i, f in enumerate(frames[o]):
        im = Image.open(f).convert('RGBA').crop(box)
        s = H / im.height; im = im.resize((round(im.width * s), H), Image.LANCZOS)
        p = os.path.join(dst, o, f'{i:02d}.webp'); im.save(p, 'WEBP', quality=Q, method=6, alpha_quality=90)
        total += os.path.getsize(p)
print(json.dumps({'frames': N, 'outfits': outfits, 'crop': box, 'size': f'{im.width}x{im.height}', 'total_kb': round(total / 1024)}, ensure_ascii=False))
print('window.SPIN 예시:', json.dumps({'id': os.path.basename(dst.rstrip('/')), 'ko': '', 'ja': '', 'path': dst.rstrip('/').split('assets/', 1)[-1].join(['assets/', '/']) if 'assets/' in dst else dst, 'frames': N,
      'outfits': [{'id': o, 'ko': o, 'ja': o} for o in outfits]}, ensure_ascii=False))
