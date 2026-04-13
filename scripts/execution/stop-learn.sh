#!/bin/bash
# stop-learn.sh — Stop hook 후보 (v7)
# 목적: 세션 종료 시 자동 ingest + wiki 갱신
# 주의: 현재 settings.json 등록 안 됨 (Mason 승인 후 등록)
#
# 실행 조건: marker .cl-stop-learn 존재 시만
set -u

CWD=$(pwd)
[ ! -f "$CWD/.cl-stop-learn" ] && [ ! -f "$HOME/.cl-stop-learn" ] && exit 0

# 현재 세션 jsonl 찾기
SESSION_ID=$(ls -t /home/ubuntu/.claude/projects/-home-ubuntu--cokacdir-workspace/*.jsonl 2>/dev/null | head -1)
[ -z "$SESSION_ID" ] && exit 0

# auto-ingest 호출
bash "$(dirname "$0")/auto-ingest-session.sh" "$SESSION_ID" >> "$HOME/.cl-stop-learn.log" 2>&1

# wiki reindex trigger (옵션)
if command -v mindvault >/dev/null 2>&1 && [ -d "$HOME/.mindvault" ]; then
    mindvault update >> "$HOME/.cl-stop-learn.log" 2>&1 || true
fi

exit 0
