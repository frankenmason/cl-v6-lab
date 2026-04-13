# V6 Execution Layer 설계 (Phase 6 후속)

> 3객체 verdict: "RAG는 memory layer만. plan→execute→verify loop 별도 필요"

---

## 현재 Stack

| Layer | 도구 | 역할 |
|-------|------|------|
| Memory | qmd(BM25) + CVM(semantic) + mindvault(graph+wiki) | 과거 지식 retrieval |
| Gate | reasoning_gate_v3 + presend_check (P5) + mindvault hook (opt-in) | 발화 전 검증 |
| Skill | m2-plan + bkit:plan-plus + /gsd:* | 계획/실행 명령 |

**누락: plan→execute→verify 자동 loop (Memory 위에 구동하는 실행 엔진)**

---

## 제안 — v7 Execution Layer 골격

### 단계

1. **Plan**: 요청 → mindvault query로 과거 유사 케이스 retrieve → plan 생성
2. **Execute**: plan 단위 (파일/명령/API)별 atomic 실행 + side-effect 캡처
3. **Verify**: 기대값 vs 실제값 비교 (test/codex/human)
4. **Rollback**: Verify FAIL 시 atomic rollback (git revert, file restore, DB transaction)
5. **Learn**: Verify 결과를 mindvault/wiki에 ingest → 다음 plan에 feedback

### 기존 스킬과의 매핑

- Plan 단계: bkit:plan-plus + /pdca plan + mindvault 회고 = 기존 활용
- Execute 단계: m2-plan EXECUTOR + superpowers:subagent-driven-development = 기존 활용
- Verify 단계: m2-plan POST-GATE-B (verification-loop) = 기존 활용
- **Rollback 단계: 누락** → 신규 필요
- **Learn 단계: 누락** → mindvault ingest 수동, 자동화 필요

### 신규 도구 후보

1. `scripts/execution/rollback-helper.sh` — git/file/DB rollback 통합
2. `scripts/execution/auto-ingest-session.sh` — 세션 종료 시 자동 mindvault ingest
3. `~/.claude/hooks/stop-learn.sh` — Stop hook에서 세션 데이터 wiki로 컴파일

---

## Plan→Execute→Verify 실전 flow (예시)

```
[User 요청]
  ↓
[Plan] mindvault query --global → retrieve 5건 → plan 초안 → Mason 승인
  ↓
[Execute] subagent driven development (git worktree 격리)
  ↓
[Verify] build + test + 3객체 검증
  ↓ PASS
[Learn] 결과를 vault/wiki/s{N}-{feature}.md 생성 → mindvault ingest
  ↓ FAIL
[Rollback] git stash + 원래 branch 복귀 + issue 생성
```

---

## v6 완료 + v7 착수 기준

- v6: Memory + Gate 레이어 안정화 (완료)
- v7: Execution + Rollback + Learn 레이어 (신규)
- 착수 조건: Mason 승인 + baseline 1주 누적 데이터

---

## 참조

- https://github.com/frankenmason/cl-mindvault
- https://github.com/frankenmason/cl-v6-lab
- docs/session_v5-reassessment_discussion_log.md
- results/phase6-baseline.md
