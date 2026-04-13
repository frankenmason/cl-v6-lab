# E-7/8/9 발생률 실측 가이드 — 신규 세션용 프롬프트

> **이 문서를 새 Claude Code 세션의 첫 입력으로 복사해서 붙여넣으시면 됩니다.**
> 작성일: 2026-04-13
> 작성 근거: v5 plan 독립 검토 결과 "현재 v3 hook에서 E-7/8/9 재발 빈도 실측 없음 → v5 구현 전 n=100 기준 측정 필요"
> 선행 근거: v1→v2 전환 시 n=992턴 BARE 59.6% 실측으로 전환 정당성 확보했던 전례

---

## 당신(CL)이 받은 임무

v5 plan의 OUTPUT-GATE / EVIDENCE-GATE 구현 전에, **현재 v3 hook 환경에서 E-7/8/9 패턴 재발 빈도를 실측**하세요. 추론이 아닌 파싱 기반 정량 측정입니다.

### E-7/8/9 정의 (v5 plan §Context 참조)

| ID | 정의 | 감지 방법 |
|----|------|----------|
| E-7 | 파일 확인(TYPE-1) 근거로 인과관계 결론도 TYPE-1 라벨링 | 응답 내 `EVIDENCE:` 라인에 `TYPE-1` + `따라서\|이므로\|즉\|결국\|그래서` 공존 |
| E-8 | reasoning_gate 실행되나 추론→단정 차단 못 함 | 위 E-7과 동일 패턴의 재발 턴 카운트 |
| E-9 | INTENT + Selector + Status Report 3요소 일부 생략 | 응답에서 `INTENT:` / `[Selector]` / `CONFIDENCE:` 존재 여부 |

---

## 매 턴 자동 기록되는 데이터 (중요 — 기존 세션들이 모르는 부분)

### 1. UserPromptSubmit hook 주입 데이터
- 경로: `~/.claude/settings.json` UserPromptSubmit Block1
- 매 user 입력마다 `reasoning_gate_v3.sh` 실행 → `[GATE v3]` 블록이 당신 컨텍스트에 주입됨
- 주입 내용: SERVICES / CACHE / WORKFLOW / DUTY / RESOURCES / PLAN_HINT / CORRECTION
- **핵심**: `[CORRECTION] 직전 턴 BARE 감지` 블록이 나타나면 = E-8 발생 증거

### 2. 세션 transcript 자동 저장
- 경로: `/home/ubuntu/.claude/projects/-home-ubuntu--cokacdir-workspace/{session_id}.jsonl`
- 매 턴 user 입력 + assistant 응답이 JSON Lines 형식으로 append
- 이 파일을 Python으로 파싱해서 E-7/8/9 패턴 grep 가능

### 3. hook 스크립트 위치
- `~/.claude/hooks/reasoning_gate_v3.sh` (UserPromptSubmit, 매 턴)
- `~/.claude/hooks/reasoning_gate_stop.sh` (Stop, 응답 후)
- `~/.claude/hooks/cl_session_cache.sh` (SessionStart, 1회)

---

## 수행 절차

### Step 1: 측정 스크립트 작성 (파일 생성)

경로: `/home/ubuntu/.cokacdir/workspace/scripts/measure_e789.py`

다음 기능 포함:
```python
# 입력: 최근 N개 세션 .jsonl 파일 (>5KB, assistant 턴 ≥10)
# 출력: 턴별 E-7/E-8/E-9 감지 여부 + 전체 집계

# E-7/E-8 감지 (동일 패턴):
#   assistant 턴 텍스트에 "TYPE-1" 포함 AND ("따라서"|"이므로"|"즉"|"결국"|"그래서") 포함
#
# E-9 감지:
#   assistant 턴에 다음 3개 중 하나라도 누락:
#     - "INTENT:" 또는 "WHAT:"
#     - "[Selector]" (또는 옵션 답변은 예외 — Fast-Path)
#     - "CONFIDENCE:" AND "ACTION:" AND "USES:"
#
# Fast-Path 예외 (계산에서 제외):
#   user 입력이 "1"/"2"/"ㅇ"/"ok"/"@승인"/"@모두 승인" 단독
```

### Step 2: 측정 실행

- 대상: 최근 10개 세션 .jsonl (각 >5KB, assistant 턴 ≥10)
- 기준: v1→v2 실측과 동일 (n≈500~1000턴 확보)
- 2회 독립 실행(Run1, Run2) → 재현성 확인 (차이 <0.5%면 안정)

### Step 3: 결과 기록

경로: `/home/ubuntu/.cokacdir/workspace/docs/logs/m2-plan_e789_measurement_result.md`

포맷:
```markdown
# E-7/8/9 발생률 실측 결과

date: 2026-04-XX
method: Python transcript parsing
target: 최근 10개 세션 .jsonl (>5KB)
total_turns: {N}

| 항목 | Run1% | Run2% | 평균 | 안정성 | 판정 |
|------|-------|-------|------|--------|------|
| E-7/E-8 (추론-단정 공존) | X.X | X.X | X.X | VARY/PASS | ... |
| E-9 (3요소 누락) | X.X | X.X | X.X | ... | ... |

## 판정 기준

- E-9 <5% → v5 OUTPUT-GATE 불필요 (과잉 설계)
- E-9 10-30% → OUTPUT-GATE만 구현 (EVIDENCE-GATE 보류)
- E-9 >30% → v5 전체 구현 정당화

## 권장사항

...
```

### Step 4: v5 plan 업데이트

측정 결과를 근거로 `docs/01-plan/features/m2-plan.plan.v5.md`의 `## Context` 섹션에 실측 데이터 추가. 범위 조정(축소/전체 구현) 제안.

---

## 주의사항

1. **측정 자체가 오염을 만들지 않도록**: 측정 스크립트 실행 턴은 계산에서 제외
2. **CLAUDE.md Hard Constraints 준수**: H-3(스킬 수정은 백업 필수), H-7(CLAUDE.md 수정 금지)
3. **Fast-Path 예외 정확히 반영**: "1"/"ㅇ" 등 단답 승인은 3요소 강제 대상 아님
4. **추정 금지**: 모든 수치는 파싱 결과. "대략 X%" 발화 금지
5. **보고는 Status Report 형식 준수** (CLAUDE.md 04조 + v5 OUTPUT-GATE)

---

## 선행 참조 문서

| 경로 | 용도 |
|------|------|
| `docs/01-plan/features/m2-plan.plan.v5.md` | v5 plan 본문 (E-7/8/9 정의) |
| `docs/01-plan/features/m2-plan.plan.v4.5.md` | v4.5 계승 (SC-6~8) |
| `docs/01-plan/features/m2-plan.plan.v4.md` | v4 원본 (SC-1~5) |
| `docs/logs/m2-plan_cl-auto-workframe_test_run1.md` | v1→v2 때 n=992 실측 전례 |
| `docs/logs/m2-plan_cl-auto-workframe_test_run2.md` | 재현성 검증 방법 |
| `~/.claude/skills/m2-plan/SKILL.md` | m2-plan 실행 정의 |
| `~/.claude/hooks/reasoning_gate_v3.sh` | 현재 매 턴 hook |
| `~/.claude/hooks/reasoning_gate_stop.sh` | Stop hook |

---

## 완료 기준

- [ ] `scripts/measure_e789.py` 작성 + 실행 2회
- [ ] `docs/logs/m2-plan_e789_measurement_result.md` 작성
- [ ] v5 plan에 실측 근거 반영 제안
- [ ] Mason에게 결과 보고 (Status Report 형식)

완료 후 Mason 승인 받으면 v5 구현 단계로 전환.
