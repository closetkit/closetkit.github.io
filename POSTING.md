# Closet Kit 홍보 키트

## 어떤 주소를 쓰나

| 대상 | 주소 | 미리보기 |
|---|---|---|
| 한국 커뮤니티 | `https://closetkit.github.io/` | 한국어 카드 (`assets/og-ko.jpg`) |
| 일본 커뮤니티 | `https://closetkit.github.io/ja/` | 일본어 카드 (`assets/og-ja.jpg`), 열면 일본어 사이트 |
| 특정 섹션 바로 | `…/#pricing` · `…/#portfolio` · `…/#order` | `/ja/#order` 처럼 일본어에도 붙일 수 있음 |

> 미리보기 이미지를 바꾼 직후 X·디스코드에 예전 이미지가 뜨면 캐시입니다. 디스코드는 주소 끝에 `?v=2` 같은 걸 붙이면 새로 읽고, 카카오톡은 [카카오 공유 디버거](https://developers.kakao.com/tool/debugger/sharing)에서 캐시를 지울 수 있습니다.

## 1. 먼저 한 번만 할 일 (검색 등록)

- **네이버 서치어드바이저** — 한국 검색 유입의 핵심. 사이트 등록 → 소유 확인(HTML 태그) → 요청 › 사이트맵 제출에 `https://closetkit.github.io/sitemap.xml`
- **Google Search Console** — 속성 추가(URL 접두어) → HTML 태그로 확인 → Sitemaps 에 `sitemap.xml` 제출
- 소유 확인용 `<meta …>` 태그를 받으면 사이트 `<head>` 에 넣어야 합니다 (Claude 에게 태그만 붙여 주면 반영 가능)

## 2. 프로필에 링크 걸기

- X(트위터) 프로필 웹사이트 칸, BOOTH 샵 소개글, 디스코드 프로필 About Me 에 사이트 주소
- 홍보 영상 게시물을 X 프로필 상단에 고정

## 3. 게시글 문안

### X — 한국어 (영상 `closetkit_9x16_ko.mp4` 또는 `16x9_ko` 첨부)

```
BOOTH에서 산 옷, 아직 못 입혔나요? 👗

VRChat 옷 입히기 · 옷장 메뉴 세팅 커미션 받습니다.
✓ 미리보기 보고 결제
✓ 비밀번호 안 받아요
✓ 원본 그대로 (Modular Avatar 비파괴)

15,000원부터 👉 https://closetkit.github.io/

#VRChat #VRChat커미션 #브이알챗
```

### X — 日本語 (`closetkit_9x16_ja.mp4` 添付)

```
BOOTHで買った衣装、まだ着せられてない？👗

VRChatの衣装着せ替え・メニュー切替セットアップを代行します。
✓ プレビューを見てからお支払い
✓ パスワード不要
✓ 非破壊（Modular Avatar）

15,000ウォン〜（約¥1,580）👉 https://closetkit.github.io/ja/

#VRChat #VRChat改変 #改変代行
```

### 디스코드 · 네이버 카페 홍보 채널 (한국어, 긴 버전)

> 각 서버·카페의 홍보 규칙(홍보 채널, 주기)을 먼저 확인하세요.

```
[커미션] VRChat 옷 입히기 · 옷장 세팅 — Closet Kit

BOOTH에서 산 옷·헤어를 아바타에 입히고, 메뉴에서 바로 갈아입을 수 있게 세팅해 드려요.

• 옷이 분홍색 / 소품이 안 꺼짐 / 용량 초과 / 메뉴 엉킴 → 해결
• 업로드 용량(비압축 500MB · 다운로드 200MB) 실측 리포트
• 워터마크 미리보기 보고 마음에 들면 결제
• VRChat 비밀번호는 받지 않고, 업로드는 직접 (가이드 제공)
• 상호구매 원칙 — 작업자가 보유한 아바타·의상이면 작업비만

STANDARD 15,000원 · DELUXE 39,000원 · PREMIUM 69,000원
작업물 · 신청서 👉 https://closetkit.github.io/
```

### 쇼츠 · 릴스 · 틱톡 설명란

```
산 옷, 입혀 드립니다 👗 VRChat 옷 입히기 · 옷장 세팅 커미션
👉 closetkit.github.io
#VRChat #브이알챗 #VRChat커미션 #shorts
```
```
買った衣装、着せます 👗 VRChat 衣装の着せ替え・改変代行
👉 closetkit.github.io/ja/
#VRChat #VRChat改変 #改変代行 #shorts
```

음악은 각 앱의 라이브러리에서 고르세요 (저작권 문제 없음). 장면 전환: 2.5초 · 6초 · 11초 · 15초.

## 4. 꾸준히 올릴 것

- 작업 하나 끝날 때마다 **전/후 이미지 1장 + 사이트 링크** — 사이트 "작업물" 이미지를 그대로 써도 됩니다 (의뢰인 허락, 제작자 표기)
- "용량 400MB → 180MB" 같은 **숫자가 있는 결과**가 반응이 좋습니다
- 후기를 받으면 사이트 `window.REVIEWS` 에 추가 (허락받은 것만)
- 같은 글을 여러 곳에 동시에 올리기보다, 채널마다 1~2주 간격으로
