# Overnight C — v7 execution layer 3 script 프로토타입

date: 2026-04-13
status: drafted, NOT registered

## 생성 파일

| 파일 | 역할 | 상태 |
|------|------|:----:|
| scripts/execution/rollback-helper.sh | git snapshot/restore/list | ✅ 실행 가능 |
| scripts/execution/auto-ingest-session.sh | 세션 jsonl → vault Summary → mindvault ingest | ✅ 실행 가능 |
| scripts/execution/stop-learn.sh | Stop hook 후보 (marker opt-in) | ⏸️ 미등록 |

## 테스트 지침 (수동)

### rollback-helper
```bash
cd /tmp/test && git init -q && echo test > a.txt && git add . && git commit -qm init
bash rollback-helper.sh snapshot test1
echo change > a.txt && git add . && git commit -qm change
bash rollback-helper.sh restore test1  # HEAD 복귀 확인
```

### auto-ingest
```bash
bash auto-ingest-session.sh /path/to/session.jsonl
# → obsidian-vault/30-Claude/31-Summaries/ 에 md 생성 확인
```

### stop-learn
```bash
touch ~/.cl-stop-learn
bash stop-learn.sh
ls ~/.cl-stop-learn.log
```

## Mason 승인 대기 사항

1. settings.json Stop hook에 stop-learn.sh 등록 여부
2. auto-ingest-session을 cron/주기 실행 여부
3. rollback-helper를 m2-plan SKILL EXECUTOR에 통합 여부
