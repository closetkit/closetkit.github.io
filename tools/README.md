# 360° 회전 뷰어용 촬영 도구

사이트의 "360° 돌려 보기" 섹션은 **각도별 렌더 이미지**만 씁니다. 3D 모델 파일(GLB/VRM)은 웹에 올리면
누구나 내려받을 수 있어 BOOTH 아바타·의상 약관(재배포 금지)에 걸리므로 올리지 않습니다.

## 1. Unity 에서 촬영 — `ClosetKitTurntable.cs`

1. `Assets/Editor/` 폴더에 `ClosetKitTurntable.cs` 를 넣습니다 (폴더가 없으면 만들기)
2. 메뉴 **Tools › Closet Kit › 360° 촬영**
3. **아바타 루트**에 아바타를 끌어 넣고, **아바타 id**·**옷 id** 를 영문으로 적습니다 (예: `milltina`, `katana`)
4. 가장 큰 옷(날개·모자 등)을 입힌 상태에서 **담을 높이 › 자동**을 한 번 누릅니다 → 이 값을 모든 옷에 그대로 사용
5. **미리보기**로 구도 확인 → **촬영**
6. 옷을 바꾸고 옷 id 만 바꿔서 다시 **촬영** (옷 개수만큼 반복)

결과: `<프로젝트 폴더>/ClosetKitTurntable/<아바타 id>/<옷 id>/00.png …`

- 업로드 결과와 똑같이 찍으려면 Play 모드(Modular Avatar/NDMF 의 Apply on Play)에서 Gesture Manager 로 옷을 바꾸고,
  Hierarchy 의 Play 중인 아바타를 넣어 촬영하세요.
- 카메라가 아바타 주위를 돌기 때문에 PhysBone(머리카락 등)이 흔들리지 않습니다.
- 투명 배경이 이상하게 나오면(셰이더에 따라 반투명하게 찍히는 경우) **투명 배경**을 끄고 배경색을 사이트와 같은
  연보라(기본값)로 찍으세요.

## 2. 사이트용으로 변환 — `make_spin.py`

```bash
python3 make_spin.py <ClosetKitTurntable/아바타id 폴더> <사이트>/assets/spin/<아바타id>
```

모든 옷·각도의 여백을 같은 크기로 잘라 WebP 로 줄입니다 (옷 1벌 36장 ≈ 1–2MB). 마지막 줄에 `window.SPIN` 에 넣을 설정이 나옵니다.

## 3. 사이트에 등록 — `index.html` 의 `window.SPIN`

```js
window.SPIN = [
  { id: "milltina", ko: "밀티나", ja: "ミルティナ", path: "assets/spin/milltina/", frames: 36,
    outfits: [ { id: "katana", ko: "Project-KATANA", ja: "Project-KATANA" },
               { id: "devicute", ko: "DeviCute", ja: "DeviCute" } ],
    credit: "DOLOSart · velvetsky" }
];
```

> 촬영 폴더를 압축해서 Claude 에게 주면 2·3단계는 대신 해 줄 수 있습니다.
