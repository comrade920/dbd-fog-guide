# 안개 도감

데드 바이 데이라이트(Dead by Daylight)의 기술, 애드온, 아이템, 공물, 캐릭터를 한국어로 빠르게 찾는 비공식 팬 사이트입니다.

**사이트:** https://comrade920.github.io/dbd-fog-guide/

## 주요 기능

- 초성(`ㅈㄱㅅㄱ`), 영문명(`dead hard`), 줄임말(`bbq`, `noed`) 검색
- 캐릭터별 보기: 고유 기술, 살인마 능력과 애드온
- 설명 속 수치 강조: 기술 1/2/3단계 수치를 색으로 구분
- 상태 효과 사전: 설명 속 효과 이름을 누르면 뜻과 관련 기술 목록
- 효과 태그 필터: 발전기, 치료, 오라, 추격, 은신 등
- 빌드 짜기와 링크 공유, 즐겨찾기, 최근 본 항목
- 이번 주 신전, 패치 변경점
- 추천 세팅 탭: 살인마 44명의 추천 기술·애드온 조합 (원문: 라스쿠 님, 출처 표기)

## 데이터 갱신

맥에서 매일 09:30에 자동으로 갱신됩니다(`com.dbdfog.update.plist` → `auto_update.sh`).

자동 실행을 못 한 날은 터미널에서 직접 실행합니다.

```bash
cd ~/Dev/dbd-wiki && bash auto_update.sh
tail -5 logs/auto_update.log   # '올림 완료' 또는 '변경 없음'이면 정상
```

| 파일 | 하는 일 |
|---|---|
| `fetch.sh` | 게임 데이터(한국어·영어)와 신전 정보를 받아 `raw/`에 저장 |
| `build2.py` | 데이터를 정리해 `data.json`을 만들고 `template.html`에 넣어 `index.html` 생성. 이전 버전과 비교해 패치 변경점 기록 |
| `update.sh` | `fetch.sh` + `build2.py` |
| `auto_update.sh` | `update.sh` 후 바뀐 내용이 있으면 GitHub에 올림 |
| `make_icons.py` | 아이콘 이미지를 묶음 파일(`icons/*.webp`)로 생성 |

## 출처

- 추천 세팅: 라스쿠 님 [자주쓰는 살인마 세팅 업데이트(v2026_2차)](https://gall.dcinside.com/mgallery/board/view/?id=dbd&no=2606672) (디시인사이드 데드바이데이라이트 마이너 갤러리). 원문 이미지를 텍스트로 옮기고 이름을 게임 표기로 맞춤. 원문이 바뀌면 `settings_src/raw.txt`를 고친 뒤 `python3 settings_src/match.py` 결과를 `settings.json`에 반영

- 게임 데이터: [dbd.tricky.lol](https://dbd.tricky.lol)
- 아이콘: [Icon-Pack-Provider/Dead-by-daylight-Default-icons](https://github.com/Icon-Pack-Provider/Dead-by-daylight-Default-icons)

- 앱 아이콘: 배경 사진 "Night trees forest"(Jon Sullivan, 퍼블릭 도메인), 글꼴 Cinzel(SIL OFL 1.1). 자세한 내용은 `appicon_src/CREDITS.md`

## 저작권

- 추천 세팅 내용의 저작권은 원작자(라스쿠 님)에게 있습니다.
- 소스 코드, 디자인, 직접 작성한 내용: © 2026 [comrade920](https://github.com/comrade920). All rights reserved. 허락 없이 복제·수정·재배포할 수 없습니다. 자세한 내용은 [LICENSE](LICENSE)를 보세요.
- Dead by Daylight의 게임 텍스트와 이미지 저작권은 Behaviour Interactive Inc.에 있습니다. 이 사이트는 Behaviour Interactive와 관련이 없는 비공식 팬 사이트입니다.
