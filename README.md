# Closet Kit 홍보 영상

사이트(`main` 브랜치)와 분리된 홍보 영상 소스입니다. 이 브랜치는 GitHub Pages 에 배포되지 않습니다.

게시글 문안 · 해시태그 · 검색 등록 방법은 [POSTING.md](POSTING.md).
사이트 360° 뷰어용 Unity 촬영 도구는 [tools/](tools/README.md).

## 완성본 — `promo/videos/`

| 파일 | 비율 | 용도 |
|---|---|---|
| `closetkit_9x16_ko.mp4` | 1080×1920 | 쇼츠 · 릴스 · 틱톡 (한국어) |
| `closetkit_9x16_ja.mp4` | 1080×1920 | 쇼츠 · 릴스 · 틱톡 (일본어) |
| `closetkit_16x9_ko.mp4` | 1920×1080 | 유튜브 · X · 디스코드 (한국어) |
| `closetkit_16x9_ja.mp4` | 1920×1080 | 유튜브 · X · 디스코드 (일본어) |

18초, 30fps, 무음 오디오 트랙 포함. 장면 전환은 **2.5초 · 6초 · 11초 · 15초** — 음악 박자를 여기에 맞추면 좋습니다.

## 구성

| 시간 | 장면 |
|---|---|
| 0–2.5s | 훅 — "BOOTH에서 산 옷, 아직 못 입혔나요?" |
| 2.5–6s | 문제 칩 4개 → 취소선 → 가운데 점으로 모임 |
| 6–11s | 아이리스 전환 → Blender 3D 옷장 레일 + "산 옷, 입혀 드립니다." |
| 11–15s | 색 막대 와이프 → 가격 오도미터 + 체크 3개 |
| 15–18s | 줌 스루 → 엔드카드 (로고 · URL · 신청서 버튼 · 저작권 표기) |

## 파일

- `promo/prep_cards.py` — 사이트 `assets/` 의 작업물 렌더를 의상 카드 28장으로 자름 (글자 영역 제외)
- `promo/make_grain.py` — 필름 그레인 타일
- `promo/closet_scene.py` — Blender 3D 샷 (두 줄 옷장 레일, 피사계 심도, 보케). Cycles CPU + OIDN 디노이저
- `promo/promo.html` — 문구·모션그래픽 레이어. `?aspect=v|h&lang=ko|ja`, `window.seek(frame)` 으로 프레임 단위 재현
- `promo/render_frames.js` — Playwright 로 프레임을 찍어 ffmpeg 로 인코딩 (서브프레임 2장 평균 = 모션 블러)
- `promo/build.sh` — 전체 빌드

## 다시 만들기

```bash
# 준비: python3 + Pillow/numpy, ffmpeg, node + playwright, Noto Sans CJK 폰트
python3 -m venv ~/bpyenv && ~/bpyenv/bin/pip install bpy   # Blender 5.x (Python 3.13)
git worktree add ../site main                              # 사이트 이미지가 필요
cd promo && PY_BPY=~/bpyenv/bin/python ./build.sh ../../site/assets
```

문구는 `promo.html` 의 `TXT` (ko / ja), 가격은 `TXT.num` / `RATE`(엔 환산) 에서 바꿉니다.
문구만 바꿀 때는 3D 렌더(`blend/`)를 다시 할 필요가 없습니다 — `blend/` 폴더가 있으면 build.sh 가 건너뜁니다.

미리보기: `node render_frames.js --stills v ko 60,200,400` → `stills/`

작례 아바타·의상의 저작권은 각 제작자에게 있습니다.
