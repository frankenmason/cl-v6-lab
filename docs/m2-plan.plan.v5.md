# M2-PLAN (MASON PLAN) — 통합 워크프레임 SKILL 설계 v5.0

> 기반: v4.md + v4.5.md 병합 + 2026-04-13 세션 신규 발견(E-7/8/9) 반영
> 작성일: 2026-04-13
> 상태: Draft (Mason 승인 대기)

---

## 참조 경로 (필수 동반 확인)

| 구분 | 경로 | 용도 |
|------|------|------|
| 선행 plan | `docs/01-plan/features/m2-plan.plan.v4.md` | v4 원본 (SC-1~5, 기본 플로우) |
| 선행 plan | `docs/01-plan/features/m2-plan.plan.v4.5.md` | v4.5 원본 (SC-6~8, ROLLBACK/LOG) |
| 실행 SKILL | `~/.claude/skills/m2-plan/SKILL.md` | m2-plan 실제 실행 파일 (v4.5 기반, PREFLIGHT 체크리스트화 반영됨) |
| 시스템 헌법 | `/home/ubuntu/.cokacdir/workspace/CLAUDE.md` | 04조 Interface Mode 3요소, C2 Evidence-First |
| reasoning gate (매 턴) | `~/.claude/hooks/reasoning_gate_v3.sh` | UserPromptSubmit hook (E-8 대상) |
| reasoning gate (stop) | `~/.claude/hooks/reasoning_gate_stop.sh` | Stop hook (E-8 대상) |
| 추론 기준서 | `docs/cl_reasoning_reference.md` | Clarification Gate 기준 |
| MEMORY 인덱스 | `/home/ubuntu/.claude/projects/-home-ubuntu--cokacdir-workspace/memory/MEMORY.md` | RULES 12항 (feedback 참조) |

---

## Context

### v4/v4.5 기존 문제 (계승)
- S61 4건 모두 Mason 직접 체크로 오류 발견 (sbr 하드코딩, qmd reindex, vault-memory wasm, 환경변수 뒤바뀜)
- 자기 검증 형식적 (파일 존재 = 검증 착각), 독립 CRITIC 부재
- 3개 계획 시스템(bkit PDCA, GSD, Superpowers) 분산

### 2026-04-13 세션 신규 재발 문제 (v5 신설)
S62 stop hooks 문제 해결 과정에서 3가지 품질 결함 재발:
1. **E-7**: 파일 확인(TYPE-1)을 근거로 인과관계 결론도 TYPE-1로 라벨링 (`cursor-hooks/hooks.json 존재 확인` → `claude-mem이 원인`을 TYPE-1로 표기)
2. **E-8**: `reasoning_gate_stop.sh` 실행은 되나 추론→단정 패턴을 차단하지 못함 (Gate 통과하지만 발화 전 자가 검증 부실)
3. **E-9**: CLAUDE.md 04조 "INTENT + Selector + Status Report 3개 모두 필수"인데 일부 생략된 응답 송출

---

## 목표

bkit PDCA + GSD + Superpowers → `@M2-PLAN` 단일 SKILL.
PLANNER→EXECUTOR→CRITIC 역할 분리로 실행 품질 구조적 보장.
**v5 추가**: EVIDENCE 라벨 무결성 + reasoning_gate 추론-단정 차단 + Interface Mode 3요소 강제화.

---

## 성공 기준

### v4 계승 (SC-1~5)
| ID | 기준 | 검증 방법 |
|----|------|----------|
| SC-1 | `@M2-PLAN [task]` 단일 트리거로 전체 순차 진행 | COMPLETE까지 도달 |
| SC-2 | CRITIC에서 codex:codex-rescue가 **독립 컨텍스트**로 검증 | Agent 호출 로그 subagent_type 확인 |
| SC-3 | Karpathy Check 4항목 + verification-loop 6-phase 통과해야 전환 | 미충족 시 블록 동작 확인 |
| SC-4 | CRITIC 실패 시 fail_target(planner/executor) 복귀 (max 3) | 의도적 실패 → 복귀 확인 |
| SC-5 | `--optimize` 플래그로 autoresearch 선택적 활성화 | 플래그 유무별 실행/미실행 |

### v4.5 계승 (SC-6~8)
| ID | 기준 | 검증 방법 |
|----|------|----------|
| SC-6 | 미실측 4회 시 PHASE ROLLBACK 동작 | miss_count 증가 → ROLLBACK 확인 |
| SC-7 | 정체 감지: 동일 오류 3회 연속 시 HALT | STALL DETECTED 메시지 출력 |
| SC-8 | 실행 품질 LOG 생성 | `docs/logs/m2-plan_{task}_execution_log.md` 존재+내용 확인 |

### v5 신규 (SC-9~11)
| ID | 기준 | 검증 방법 |
|----|------|----------|
| SC-9 | EVIDENCE 라벨이 근거 유형과 일치 | 추론 결론을 TYPE-1로 표기 시 Gate 차단 |
| SC-10 | reasoning_gate가 추론-단정 패턴 차단 | "따라서/이므로/즉" + TYPE-1 조합 시 Gate HALT |
| SC-11 | 매 응답에 INTENT + Selector + Status Report 3개 모두 존재 | 출력 검증 hook 또는 SKILL OUTPUT-GATE 차단 |

---

## 전체 플로우 (v5 — v4.5 기반 + OUTPUT-GATE 추가)

```
@M2-PLAN [task] [--optimize] [--code|--infra|--skill]
  │
  ├─ PREFLIGHT (체크리스트 먼저 출력 → 병렬 실측 → raw 표)
  │   CHECK-1: codex CLI (which codex)
  │   CHECK-2: qmd MCP (mcp__qmd__status)
  │   CHECK-3: graphify-mcp pm2 (pm2 list | grep graphify)
  │   CHECK-4: .planning/ 디렉토리
  │   CHECK-5: vault-memory CLI (ls obsidian-ai-agent/dist/cli.js)
  │   CHECK-6: git repo (IF --code 필수, --skill/infra SKIP)
  │
  ├─ PRE-GATE: Karpathy #1 Think + #2 Simplicity
  │
  ├─ @논의모드 ON (docs/logs/sessionN_discussion_log.md)
  │
  ├─ PLANNER: Plan Plus → bkit PDCA → GSD plan-phase → Superpowers writing-plans
  │
  ├─ EXECUTOR:
  │   --code  → Skill("superpowers:subagent-driven-development")
  │   --infra → /gsd:execute-phase
  │   --skill → 직접 Write/Edit (H-3 백업 필수)
  │
  ├─ POST-GATE-A: Karpathy #3 Surgical + #4 Goal-Driven
  ├─ POST-GATE-B: verification-loop 6-phase (--code만)
  │   Build/Types/Lint/Tests(≥80%)/Security/Diff
  │
  ├─ CRITIC (mode별 분기 — v4.5):
  │   Step1 codex review
  │     --code  → codex review --base {branch}
  │     --skill → codex review SKILL.md 파일 단위
  │     --infra → SKIP
  │   Step2 gap-detector + design-validator
  │     --skill → gap-detector만 (design SKIP)
  │     --code  → 둘 다 병렬
  │     --infra → gap-detector만
  │   Step3 codex challenge (선택적, advisory)
  │
  ├─ 【NEW v5】OUTPUT-GATE (매 응답 전 — E-9 대응):
  │   체크 3항목 (모두 PASS 필수):
  │   [O1] INTENT 블록 존재? (WHAT/WHY/PLAN/HOW/GOAL)
  │   [O2] Selector 존재? (현재상태/Scope/옵션/[Selector])
  │   [O3] Status Report 존재? (CONFIDENCE/ACTION/USES/EVIDENCE/Not Used/💡)
  │   IF 1개라도 누락 → 출력 중단 + 재작성
  │
  ├─ 【NEW v5】EVIDENCE-GATE (매 단정 발화 전 — E-7/E-8 대응):
  │   체크 2항목:
  │   [V1] EVIDENCE TYPE 라벨이 근거 유형과 일치?
  │     - TYPE-1 = 직접 확인한 데이터 (Read/CLI 출력)
  │     - TYPE-2 = 사전 조사/문서
  │     - TYPE-3 = Mason 의도/지시
  │     - 추론/인과관계 결론은 TYPE-1 금지 (TYPE-2 최대)
  │   [V2] 추론 동사 + 단정 결합 감지:
  │     "따라서/이므로/즉/결국" + TYPE-1 라벨 → Gate HALT
  │   IF 미충족 → 응답 수정 또는 "확인 후 답변" 전환
  │
  ├─ 실측 정책 / ROLLBACK 매트릭스 / 정체 감지 (v4.5 계승)
  │
  ├─ 실행 품질 LOG (v4.5 계승)
  │   docs/logs/m2-plan_{task}_execution_log.md
  │
  ├─ IF --optimize → autoresearch
  │
  ├─ COMPLETE
  │   Step1 GSD discuss-phase (입력: 실행 품질 LOG)
  │   Step2 bkit PDCA Report
  │   Step3 Archive (vault Summary + vault-memory CLI + qmd reindex 알림
  │                  + graphify + LLM Wiki + 논의모드 LOG 링크)
  │
  └─ @논의모드 OFF
```

---

## v5 신규 섹션 — 상세 설계

### OUTPUT-GATE (E-9 대응)

**목적**: CLAUDE.md 04조 "Interface Mode 통합 출력 3개 모두 필수" 강제화.

**구현 위치**:
- 1차: m2-plan SKILL.md 내부 체크 섹션 (자가 검증)
- 2차: `~/.claude/hooks/output_gate.sh` (Stop hook, 신규 제안)

**검사 로직** (pseudocode):
```
FOR 매 응답 송출 전:
  has_intent    = grep "^INTENT:" AND grep "WHAT:|WHY:|PLAN:|HOW:|GOAL:"
  has_selector  = grep "현재 상태:" AND grep "\[Selector\]:"
  has_status    = grep "^CONFIDENCE:" AND grep "^ACTION:" AND grep "^USES:" AND grep "^EVIDENCE:"

  IF NOT (has_intent AND has_selector AND has_status):
    HALT + 재작성 요구
```

**예외**: Execution Mode 자율 실행 중 / 완료 보고 (Selector 생략 허용).
**Fast-Path**: 승인("1", "@승인"), 단순 확인("ㅇ", "ok") 응답은 SKIP.

### EVIDENCE-GATE (E-7/E-8 대응)

**목적**: 근거 없는 추론을 TYPE-1로 라벨링하는 패턴 차단.

**구현 위치**:
- 1차: `~/.claude/hooks/reasoning_gate_v3.sh` 강화 (기존 hook 확장)
- 2차: m2-plan SKILL.md 내부 체크

**TYPE 판별 매핑표**:
| 발화 패턴 | 허용 TYPE |
|----------|----------|
| "Read 결과 파일 X에 Y가 있다" | TYPE-1 |
| "CLI 실행 결과 출력이 Z다" | TYPE-1 |
| "문서 D에 명시되어 있다" | TYPE-2 |
| "Mason이 지시했다" | TYPE-3 |
| "따라서 A가 원인이다" | **TYPE-2 최대** (TYPE-1 금지) |
| "이므로 B가 발생한다" | **TYPE-2 최대** |
| "즉 C다" | **TYPE-2 최대** |

**검사 로직**:
```
IF 응답에 "따라서|이므로|즉|결국|그래서" 존재 AND EVIDENCE에 "TYPE-1" 존재:
  IF 추론 결론 자체가 TYPE-1로 라벨됨:
    HALT + "추론 결론은 TYPE-1 불가. TYPE-2로 변경 또는 '확인 후 답변'"
```

### 연결 — 기존 RULES와의 관계

| 기존 규칙 | v5 추가 대응 |
|----------|-------------|
| MEMORY.md RULES: evidence_only | EVIDENCE-GATE가 실제 차단 (기존은 권고) |
| CLAUDE.md C2 Evidence-First | EVIDENCE-GATE가 hook 레벨로 승격 |
| CLAUDE.md 04조 3요소 필수 | OUTPUT-GATE가 실제 차단 (기존은 권고) |
| reasoning_gate_v3.sh | 추론 동사 감지 패턴 추가 필요 |

---

## 발견된 이슈 (v5 추가 — E-7/8/9)

| ID | 유형 | 이슈 | 조치 | 상태 |
|----|------|------|------|------|
| E-7 | 품질 | 파일 확인(TYPE-1) 근거로 인과관계 결론도 TYPE-1 라벨링 | EVIDENCE-GATE 신설 | 설계 완료, 구현 대기 |
| E-8 | hook | reasoning_gate 실행되나 추론-단정 패턴 차단 안 됨 | reasoning_gate_v3.sh 추론 동사 매핑 추가 | 설계 완료, 구현 대기 |
| E-9 | 출력 | INTENT+Selector+Status Report 3요소 일부 생략 | OUTPUT-GATE 신설 (SKILL 내부 + hook 2단) | 설계 완료, 구현 대기 |

---

## 검증 (SC 매핑 v5 추가)

| # | 검증 항목 | SC | 명령/확인 방법 | 기대 결과 |
|---|---------|-----|--------------|----------|
| V-11 | EVIDENCE 라벨 무결성 | SC-9 | 의도적으로 추론 결론에 TYPE-1 부여 | Gate 차단 |
| V-12 | reasoning_gate 패턴 차단 | SC-10 | "따라서 A가 원인 (TYPE-1)" 응답 시도 | HALT + 수정 요구 |
| V-13 | 3요소 강제 | SC-11 | INTENT 생략 응답 시도 | OUTPUT-GATE HALT |

---

## v4 → v4.5 → v5 Delta 요약

| 항목 | v4 | v4.5 | v5 |
|------|----|----|----|
| SC 개수 | 5 | 8 | **11** |
| CRITIC mode 분기 | code only | code/skill/infra | 계승 |
| miss_count 리셋 조건 | 미명시 | 3조건 | 계승 |
| 실행 품질 LOG | 없음 | 있음 | 계승 |
| OUTPUT-GATE (3요소) | 없음 | 없음 | **신설** |
| EVIDENCE-GATE (라벨 무결성) | 없음 | 없음 | **신설** |
| reasoning_gate 추론 동사 매핑 | 없음 | 없음 | **신설** |

---

## Out of Scope (v5 유지)

- Hub L2 자동 기록
- TG 완료 알림
- 다른 에이전트(클로라/FRANKEN) 지원
- executing-plans 직접 사용 (SDD 대체)

---

## 다음 단계 (승인 후)

1. `~/.claude/skills/m2-plan/SKILL.md`에 OUTPUT-GATE / EVIDENCE-GATE 섹션 추가 (H-3 백업 선행)
2. `~/.claude/hooks/reasoning_gate_v3.sh` 추론 동사 매핑 로직 확장
3. (선택) `~/.claude/hooks/output_gate.sh` 신규 Stop hook 작성
4. V-11/12/13 검증 시나리오 실행 → SC-9/10/11 충족 확인

---

## 외부 참조 (v4/v4.5 계승 R-1~R-9 유지)

세부: v4.md / v4.5.md의 "외부조사 근거" 표 참조.
