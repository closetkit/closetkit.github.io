#!/bin/bash
# Closet Kit 홍보 영상 전체 빌드 (4편: 9:16 / 16:9 × 한국어 / 일본어)
# 사용: ./build.sh <사이트 assets 폴더>   예) ./build.sh ../site/assets
# 필요: python3 (Pillow, numpy), bpy 5.x (pip install bpy — Python 3.13), node + playwright, ffmpeg
# 시간: 4코어 CPU 기준 3D 렌더 약 50분 + 영상 인코딩 약 1시간
set -euo pipefail
P="$(cd "$(dirname "$0")" && pwd)"
ASSETS="${1:?사이트 assets 폴더 경로를 넣어 주세요}"
PY_BPY="${PY_BPY:-python3}"   # bpy 가 설치된 파이썬 (예: PY_BPY=~/bpyenv/bin/python)

python3 "$P/prep_cards.py" "$ASSETS"
python3 "$P/make_grain.py"
for a in v h; do
  [ "$(ls "$P/blend/$a" 2>/dev/null | wc -l)" -ge 150 ] || "$PY_BPY" "$P/closet_scene.py" -- "$a" "$P/blend/$a" 1 150 75 32
done
mkdir -p "$P/out" "$P/videos"
for a in v h; do for l in ko ja; do
  r=$([ $a = v ] && echo 9x16 || echo 16x9)
  node "$P/render_frames.js" $a $l "$P/out/closetkit_${r}_$l.mp4"          # 원본 (CRF 17)
  ffmpeg -v error -y -i "$P/out/closetkit_${r}_$l.mp4" -c:v libx264 -preset slow -crf 21 -pix_fmt yuv420p \
    -profile:v high -c:a copy -movflags +faststart "$P/videos/closetkit_${r}_$l.mp4"   # 공유용 (~8MB)
done; done
ls -la "$P/videos"
