#!/bin/bash
# 안개 도감: tricky.lol API에서 최신 한국어/영어 데이터를 받아 raw/ 폴더에 저장합니다.
cd "$(dirname "$0")"
mkdir -p raw
UA="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0 Safari/537.36"
ok=0; fail=0
for ep in perks addons characters items offerings versions; do
  for loc in ko en; do
    out="raw/${ep}_${loc}.json"
    code=$(curl -s -A "$UA" -o "$out" -w "%{http_code}" "https://dbd.tricky.lol/api/${ep}?locale=${loc}")
    size=$(wc -c < "$out" | tr -d ' ')
    if [ "$code" = "200" ] && head -c 1 "$out" | grep -q '[{[]'; then
      echo "OK   $out  (${size} bytes)"; ok=$((ok+1))
    else
      echo "FAIL $out  (HTTP $code)"; fail=$((fail+1))
    fi
    sleep 1
  done
done
# 이번 주 신전 (언어 무관)
code=$(curl -s -A "$UA" -o raw/shrine.json -w "%{http_code}" "https://dbd.tricky.lol/api/shrine")
if [ "$code" = "200" ] && head -c 1 raw/shrine.json | grep -q '[{[]'; then echo "OK   raw/shrine.json"; ok=$((ok+1)); else echo "FAIL raw/shrine.json  (HTTP $code)"; fail=$((fail+1)); fi
echo "완료: 성공 $ok / 실패 $fail"
