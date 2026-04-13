#!/bin/bash
# rollback-helper.sh — v7 execution layer 프로토타입
# 목적: atomic 롤백 통합 (git + file + marker)
#
# Usage:
#   rollback-helper.sh snapshot <label>    # 현재 상태 스냅샷
#   rollback-helper.sh restore <label>     # 스냅샷으로 복구
#   rollback-helper.sh list                # 스냅샷 목록
set -u

SNAP_DIR="${HOME}/.cl-rollback"
mkdir -p "$SNAP_DIR"

cmd="${1:-}"
label="${2:-auto}"

case "$cmd" in
    snapshot)
        ts=$(date +%Y%m%d_%H%M%S)
        snap="$SNAP_DIR/${label}_${ts}"
        mkdir -p "$snap"
        # git head 기록
        if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
            git rev-parse HEAD > "$snap/git_head" 2>/dev/null
            git status --porcelain > "$snap/git_status" 2>/dev/null
            git stash create > "$snap/stash_sha" 2>/dev/null || echo "clean" > "$snap/stash_sha"
        else
            echo "not-a-git-repo" > "$snap/git_head"
        fi
        pwd > "$snap/cwd"
        echo "[OK] snapshot: $snap"
        ;;
    restore)
        latest=$(ls -d "$SNAP_DIR/${label}_"* 2>/dev/null | tail -1)
        if [ -z "$latest" ]; then
            echo "[ERR] no snapshot for label: $label" >&2
            exit 1
        fi
        head=$(cat "$latest/git_head" 2>/dev/null)
        if [ -n "$head" ] && [ "$head" != "not-a-git-repo" ]; then
            git reset --hard "$head" 2>&1 | head -2
            echo "[OK] restored to $head"
        else
            echo "[WARN] git rollback unavailable. manual intervention needed."
        fi
        ;;
    list)
        ls -la "$SNAP_DIR/" | tail -n +2
        ;;
    *)
        echo "Usage: rollback-helper.sh {snapshot|restore|list} [label]"
        exit 1
        ;;
esac
