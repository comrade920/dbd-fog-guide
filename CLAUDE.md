# DBD 도감 — Claude Code 작업 안내

Dead by Daylight(데바데) 기술·애드온·아이템·공물·캐릭터를 한국어로 검색하는 비공식 팬 사이트.
- 공개 사이트: https://comrade920.github.io/dbd-fog-guide/ (GitHub Pages, 저장소 comrade920/dbd-fog-guide, main 브랜치)
- 이력·사용자 선호·계정 인수인계: `HANDOFF.md` 참고
- 소유자: comrade920 (© 2026). 비상업 팬 사이트, BHVR 팬 콘텐츠 가이드라인 준수. 후원·광고 넣지 않음
- 대화는 한국어로. 설명은 짧게(사용자는 풀스택 개발자)

## 구조 (프레임워크 없음)
- `template.html` — 화면 전체(HTML/CSS/순수 JS 한 파일, 약 700줄). `__DATA__` 자리에 데이터 JSON이 들어감
- `build2.py` — `raw/` + `icons.json` + `settings.json` → `data.json` → `index.html`(사이트) + `dbd-fog-guide.html`(Claude 아티팩트용, git 제외)
  - 직전 `data.json`과 비교해 '패치 변경점'(data.changes) 생성
  - 아이콘 파일 md5 앞 8자리를 `icons.v`에 넣어 `icons/x.webp?v=...`로 캐시 방지
  - `{Tunable.X.y}` 치환, 키워드→한국어 용어 매핑, 신전 파싱, 추천 세팅 이름 검증
- `fetch.sh` — tricky.lol API(perks/addons/characters/items/offerings/versions × ko/en + shrine)를 `raw/`에 받음. 성공한 파일만 교체, 하나라도 실패하면 종료코드 1
- `update.sh` = fetch.sh + build2.py
- `auto_update.sh` — update.sh 후 `index.html data.json`만 add → 바뀌었으면 commit("자동 갱신 날짜") + push. 로그: `logs/auto_update.log`
- `com.dbdfog.update.plist` — launchd, 매일 09:30 auto_update.sh 실행
- 아이콘: `icons/{perk,addon,misc,char}.webp` 스프라이트(64px 칸) + `icons.json`(map: 이미지 기본이름 소문자 또는 `char:<캐릭터id>` → [시트, 칸번호])
  - `make_icons.py` — 처음부터 생성(원본 아이콘 저장소 필요, 지금은 안 씀)
  - `add_icons.py <PNG폴더> raw` — 기존 스프라이트에 빠진 것만 덧붙임. PNG 이름 = 게임 이미지 기본이름 소문자.png, 초상화는 char_<id>.png
  - `icons_src/wiki/` — 공식 위키에서 받은 PNG(git 제외)
- 추천 세팅: `settings_src/raw.txt`(라스쿠 님 디시 글을 옮겨 적은 원문) → `python3 settings_src/match.py` → `settings.json`. 별칭 표(PA/AA)로 원문 표기를 게임 데이터 이름에 연결. `settings_src/review.md`는 원문 대조용
- 앱 아이콘: `appicon/`, `make_appicon3.py`, `appicon_src/`(CREDITS.md에 출처), `manifest.webmanifest`
- `data.json` 항목: `{c, id, ko, en, d(설명 HTML), o(캐릭터/소유), ic}` — c는 sp(생존자 기술) kp(살인마 기술) ka(살인마 애드온) sa(아이템 애드온) it(아이템) of(공물)

## 지켜야 할 것
- localStorage 키 이름 `fog-fav`, `fog-recent`, `fog-build`, `fog-state`는 바꾸지 않기(사용자 저장 내용이 사라짐)
- 주소 해시 형식 유지: `#sp.<id>`(항목), `#b~...`(빌드 공유), `#set.<살인마id>`(추천 세팅)
- 저장소 이름·사이트 주소 `dbd-fog-guide` 유지. 앱 이름은 "DBD 도감"
- 하단 출처 표기 유지: tricky.lol, Icon-Pack-Provider 아이콘, 공식 DBD 위키(deadbydaylight.wiki.gg), 라스쿠 님 원문 링크, 비공식 고지
- 나무위키 내용은 가져오지 않음(검색 링크만)
- template.html이나 build2.py를 고친 뒤에는 반드시 `python3 build2.py raw`로 다시 만들고 확인
- 브라우저에서 확인: `python3 -m http.server 8000` 후 http://localhost:8000 (file://로 열면 아이콘이 안 보일 수 있음)
- commit/push는 사용자가 원할 때만. push 후 사이트 반영 1~2분, 페이지 캐시 최대 10분

## 자주 하는 일
- 지금 바로 갱신: `bash auto_update.sh && tail -3 logs/auto_update.log` (`올림 완료` / `변경 없음` / `실패`)
- 데이터 버전 확인: `curl -s https://dbd.tricky.lol/api/versions | python3 -m json.tool`, 현재 반영 버전: data.json의 version
  - 패치 직후엔 tricky.lol 반영이 며칠 늦을 수 있음. 09:30 이후에 올라오면 다음 날 자동 반영
- 빠진 아이콘 확인:
  ```
  python3 -c "
  import json,os
  m=json.load(open('icons.json'))['map']; b=lambda s:os.path.splitext(os.path.basename(s or ''))[0].lower()
  for n in ['perks','addons','items','offerings']:
      d=json.load(open(f'raw/{n}_en.json')); print(n,[v['name'] for v in d.values() if b(v['image']) not in m])
  c=json.load(open('raw/characters_en.json')); print('chars',[v['name'] for v in c.values() if 'char:'+v['id'] not in m])"
  ```
  - 새 아이콘 출처: 공식 위키 deadbydaylight.wiki.gg. 이미지 이름 규칙 IconPerks_xxx / IconAddon_xxx / IconItems_xxx / IconFavors_xxx(게임 경로의 T_UI_ 접두사, iconsPerks 등은 정규화 필요, 철자 차이 있음), 초상화 <id>_<이름>_Portrait.png. 위키 API: `/api.php?action=query&list=allimages&aiprefix=IconPerks&aiprop=url&ailimit=500&format=json`
  - 위키는 Cloudflare 때문에 curl이 막힐 수 있음 → 막히면 사용자가 브라우저로 받아 icons_src/wiki에 넣도록 안내
  - 현재 빈 것(위키에도 없음): @#Addon_GasBomb_19a/20a/20b(원본 데이터 미완성), Eyes In The Sky
- 추천 세팅 원문이 바뀌면: raw.txt 수정 → `python3 settings_src/match.py` → `python3 build2.py raw`

## 환경 메모
- 맥의 python.org 파이썬은 SSL 인증서 문제가 있어 HTTP 요청은 curl로 (fetch.sh도 curl 사용)
- 이미지 처리에 Pillow 필요(설치되어 있음)
- launchd 등록 확인: `launchctl list | grep dbdfog`
- 원본 데이터 한계: 일부 번역은 추정(Haste/Hindered → 이동 속도 증가/감소, Elusive → 회피), K32·K37·K38·K40 소개글이 원본에서 잘려 있음

## 앞으로 할 후보
1. 추천 세팅 원문 대조 검수(settings_src/review.md)
2. 내 보유 기술 체크(빌드·추천 세팅에서 없는 기술 표시)
3. 자동 갱신 실패 시 맥 알림(osascript display notification)
4. 폰 첫 로딩 줄이기(데이터를 별도 파일로 분리·캐시)
5. 랜덤 빌드 뽑기, 기술 2~3개 비교
