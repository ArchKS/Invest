#!/bin/bash
# 用法: fetch.sh <jobs文件> —— 每行: api|ticker|params_json_不含file_path|outfile
cd "/Users/zendu/Library/Application Support/kimi-desktop/daimon-share/daimon/runtime/kimi-code/home/plugins/managed/ifind"
D="/Users/zendu/Documents/invest/医药/华电国际研究/data"
while IFS='|' read -r api ticker params outfile; do
  [ -z "$ticker" ] && continue
  if [ -s "$D/$outfile" ]; then echo "SKIP $outfile"; continue; fi
  ok=0
  for attempt in 1 2; do
    out=$(python3 scripts/ifind_tool.py call --api-name "$api" --params-json "{\"ticker\":\"$ticker\",$params,\"file_path\":\"$D/$outfile\"}" 2>&1 | tail -c 150)
    if [ -s "$D/$outfile" ]; then echo "OK   $outfile"; ok=1; break; fi
    echo "RETRY($attempt) $outfile :: $out"
    sleep 12
  done
  [ $ok -eq 0 ] && echo "FAIL $outfile"
  sleep 5
done < "$1"
