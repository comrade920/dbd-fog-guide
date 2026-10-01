#!/bin/bash
# 최신 데이터 받기 + 페이지 다시 만들기 (패치 후 실행)
cd "$(dirname "$0")"
bash fetch.sh && python3 build2.py raw
