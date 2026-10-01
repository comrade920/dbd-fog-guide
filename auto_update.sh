#!/bin/bash
# 안개 도감 자동 갱신: 데이터 받기 → 페이지 만들기 → 바뀐 게 있으면 GitHub에 올리기
cd "$(dirname "$0")"
export PATH="/Library/Frameworks/Python.framework/Versions/Current/bin:/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin"
mkdir -p logs
exec >> logs/auto_update.log 2>&1
echo "===== $(date '+%Y-%m-%d %H:%M:%S')"
if ! bash update.sh; then echo "실패: 데이터 받기 또는 빌드 오류 (사이트는 그대로 유지)"; exit 1; fi
git add index.html data.json
if git diff --cached --quiet; then
  echo "변경 없음"
else
  git commit -q -m "자동 갱신 $(date +%F)" && git push -q && echo "올림 완료"
fi
