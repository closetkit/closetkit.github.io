# 360° 회전 뷰어용 촬영 도구

사이트의 "360° 돌려 보기" 섹션은 **각도별 렌더 이미지**만 씁니다. 3D 모델 파일(GLB/VRM)은 웹에 올리면
누구나 내려받을 수 있어 BOOTH 아바타·의상 약관(재배포 금지)에 걸리므로 올리지 않습니다.

## 1. Unity 에서 촬영 — `ClosetKitTurntable.cs`

1. `Assets/Editor/` 폴더에 `ClosetKitTurntable.cs` 를 넣습니다 (폴더가 없으면 만들기)
2. 메뉴 **Tools › Closet Kit › 360° 촬영**
3. **아바타 루트**에 아바타를 끌어 넣습니다
4. **옷 목록**에 아바타 안의 옷 오브젝트들을 **+ 옷 추가**로 넣습니다
5. **목록 전부 촬영** — 옷을 하나씩만 켜 가며 전부 찍고, 끝나면 원래 상태로 돌려 놓습니다.
   크기는 가장 큰 옷 기준으로 한 번 정해서 모든 옷에 같게 씁니다.
6. 열린 `ClosetKitTurntable/<아바타 id>` 폴더를 압축해서 보내면 끝 (`spin.json` 사이트 설정도 같이 들어 있음)

- 옷 목록 없이 지금 보이는 상태만 찍으려면 아래쪽 **이 상태로 촬영** (옷 id 입력)
- 업로드 결과와 똑같이 찍으려면 Play 모드(Modular Avatar/NDMF 의 Apply on Play)에서 Hierarchy 의 Play 중인 아바타를 넣고 촬영하세요.
- 카메라가 아바타 주위를 돌기 때문에 PhysBone(머리카락 등)이 흔들리지 않습니다. 촬영 중에는 아바타만 찍힙니다.
- 투명 배경이 이상하게 나오면(셰이더에 따라 반투명하게 찍히는 경우) **투명 배경**을 끄고 찍으세요.

## 2. 사이트용으로 변환 — `make_spin.py`

```bash
python3 make_spin.py <ClosetKitTurntable/아바타id 폴더> <사이트>/assets/spin/<아바타id>
```

모든 옷·각도의 여백을 같은 크기로 잘라 WebP 로 줄입니다 (옷 1벌 36장 ≈ 1–2MB). 마지막 줄에 `window.SPIN` 에 넣을 설정이 나옵니다 (촬영 폴더의 `spin.json` 이름을 그대로 사용).

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
