# v5 plan 독립 검토 (외부 시각)

- date: 2026-04-13
- reviewer: CL (4일 전 세션, v4→v5 결정 과정 개입 없음)
- source: `docs/01-plan/features/m2-plan.plan.v5.md` (265줄 실독)
- 보조 근거: `~/.claude/hooks/reasoning_gate_v3.sh` (5355 bytes 실측), `~/.claude/skills/m2-plan/SKILL.md` (462줄 실측), 이번 세션 [GATE v3] CORRECTION 실작동 관찰

---

## TL;DR

v5는 방향은 옳으나 실현 가능성에서 2건의 치명적 결함, 설계에서 2건의 모순, 실측 근거 부재 1건을 확인.
승인 전 **"현재 v3 hook에서 E-7/8/9 발생률 n=100턴 실측"** 수행 권장.

| 분류 | 건수 |
|------|------|
| 🔴 Critical | 2 |
| 🟡 High | 2 |
| 🟢 Medium | 3 |
| ✅ 우수한 점 | 4 |

---

## 🔴 치명적 결함 (Critical)

### C1. Stop hook 기반 "차단"은 구조적 불가능

**v5 제안 (§OUTPUT-GATE 2차 구현)**
```
~/.claude/hooks/output_gate.sh (Stop hook, 신규 제안)
IF NOT (has_intent AND has_selector AND has_status):
  HALT + 재작성 요구
```

**문제**
- Claude Code Stop hook은 응답 **송출 후** 실행. 이미 사용자에게 전달됨
- "HALT + 재작성"을 구조적으로 달성 불가. 경고(log) 수준만 가능
- 실측 증거: 이번 세션 [GATE v3]에 포함된 `[CORRECTION] 직전 턴 BARE 감지`도 "**직전** 턴" 교정만 가능. 즉 이미 송출됨

**근본 원인**
- OUTPUT-GATE는 검증(validation) 역할이 아니라 억제(enforcement) 역할이 필요
- Stop hook으로는 enforcement 불가

**개선안 3가지 (택일)**
1. **PreToolUse 기반 재설계**: 응답 송출 직전 단계에서 text 검사 → 실패 시 블록. 단 Claude Code API가 응답 송출을 가로채는 hook 제공 여부 확인 필요
2. **의미 재정의**: "차단"이 아닌 "**다음 턴 페널티**"로 재정의. 이전 턴이 3요소 누락이면 다음 턴의 UserPromptSubmit hook에 강제 CORRECTION 주입 (v3 hook에 이미 일부 구현 — 활용 확장)
3. **책임 분리**: SKILL 내부 self-check만 강제 (hook 제거). SKILL 실행 PHASE마다 체크리스트로 3요소 확인

**권장**: 2안 (다음 턴 페널티). v3 hook 이미 유사 패턴 있어 최소 변경

---

### C2. EVIDENCE-GATE 판별 = LLM 의미 이해 필요 작업

**v5 제안 (§EVIDENCE-GATE)**
```
IF 응답에 "따라서|이므로|즉|결국|그래서" 존재 AND EVIDENCE에 "TYPE-1" 존재:
  IF 추론 결론 자체가 TYPE-1로 라벨됨:
    HALT + "추론 결론은 TYPE-1 불가"
```

**문제**
- bash hook은 정규식 텍스트 매칭만 가능
- "TYPE-1 라벨이 실제 추론 결론인지 vs 데이터 관찰인지" 판별은 **의미 분석** 필요
- 예: "TYPE-1 (파일 X에 Y가 있다)"는 정상. "따라서 Z가 원인이다 (TYPE-1)"은 위반. 둘 다 같은 grep 패턴에 걸림
- 오탐(false positive) 높음 → 정상 응답까지 HALT → SKILL 사용성 저하

**개선안: 2단계 구조**
```
1차 (bash, 저비용): 추론 동사 + TYPE-1 공존 여부 플래그만 설정
  → 공존 시: 플래그 세팅 후 응답 허용
  
2차 (LLM self-check, 의미 이해): 플래그 세팅된 경우에만 응답 송출 전 CL에게
  "직전 응답에서 TYPE-1 라벨이 추론 결론에 붙었는지 자가 검사. 예=수정 요청, 아니오=그대로"
  질의 → CL 답변에 따라 응답 수정 or 유지
```

**리스크**: 2단계 self-check가 LLM 토큰 증가. 1일 수백 턴이면 비용 고려 필요

---

## 🟡 설계 모순 (High)

### H1. CRITIC과 GATE 역할 중복

**현황**
- v4/v4.5: PLANNER / EXECUTOR / **CRITIC** (codex:codex-rescue) 3역할 분리
- v5: 여기에 OUTPUT-GATE + EVIDENCE-GATE 2개 추가

**문제**
- CRITIC이 이미 "독립 컨텍스트 검증" 역할. GATE 2개가 또 검증
- 책임 경계 불명확: 
  - OUTPUT-GATE는 형식? CRITIC은 논리?
  - EVIDENCE-GATE는 라벨? CRITIC은 내용?
- 통합 오케스트레이션 없이 중복 검증 → 성능 저하 + 혼란

**개선안: 역할 명시적 분리**
```
GATE (매 응답/발화 단위):
  - OUTPUT-GATE: Interface Mode 3요소 형식 체크 (매 응답)
  - EVIDENCE-GATE: TYPE 라벨 무결성 (매 발화)
  
CRITIC (PHASE 완료 시, 1회):
  - codex review: 논리/설계 검증 (독립 컨텍스트)
  - gap-detector: 설계 ↔ 구현 갭
  - design-validator: 문서 완결성
```

**추가 권장**: v5 §연결 섹션에 역할 경계 표로 명시

---

### H2. 실측 미비 — v5 정당성 근거 약함

**현황**
- v5 §Context에 E-7/8/9 **발견 사실**은 있음
- **재발 빈도 데이터 없음**: 몇 턴 중 몇 건에서 E-7/8/9 발생했는지 실측 없음
- v5 §SC 기준 "매 응답에 3요소 존재"를 강제하려면 현재 미충족률 알아야 함

**대비 (v1→v2 전례)**
- v1 분석 시 n=992턴 파싱 → BARE ACTION 59.6% 실측 → v2 설계 정당화
- 그 실측이 없었으면 v2의 범위 결정 불가능

**v5의 위험**
- 발생률 미측정 → 과잉 설계 or 미달 설계 확률 50/50
- 가능성 A: 실제 <5% → v5 OUTPUT-GATE는 오버엔지니어링
- 가능성 B: 실제 >30% → v5 EVIDENCE-GATE까지 필요
- 지금은 B 가정하고 구현 계획 중 — A일 경우 낭비

**개선안**
1. Phase 0 신설: "v3 hook 환경에서 E-7/8/9 발생률 n=100~500턴 실측"
2. 결과 기반 범위 조정:
   - <5% → v5 구현 보류 (기록만)
   - 5-20% → OUTPUT-GATE만 구현 (경량)
   - >20% → v5 전체 구현 정당

---

## 🟢 작은 개선점 (Medium)

### M1. Fast-Path 예외 범위 협소

**v5 §OUTPUT-GATE Fast-Path**
```
예외: 승인("1", "@승인"), 단순 확인("ㅇ", "ok") 응답은 SKIP
```

**문제**
- 일반 Read-only 팩트 응답도 3요소 강제 시 overhead
- 예: "X 파일 있나요?" → "네, /path/to/X" 한 줄 답이 정상인데 3요소 강제하면 과잉

**개선안: Fast-Path 카테고리 추가**
```
기존 + 추가:
- 단일 팩트 응답 (존재 여부, 개수, 경로 등 bool/scalar)
- 위험도 LOW + 범위 명확한 Read-only 작업
- ctx_execute 결과 단순 출력
```

### M2. SC-10 오탐 대비 없음

**v5 §SC-10**: "따라서/이므로/즉" + TYPE-1 공존 시 HALT

**문제**
- 정상 추론-기록 문장에도 "따라서"는 등장
- 예: "A 확인. B 확인. 따라서 두 파일 모두 존재 (TYPE-1)" — 정상이나 걸림

**개선안: 컨텍스트 윈도우 감지**
```
"따라서" 이후 N토큰 내에 TYPE-1 라벨이 나오면 위반
vs
"따라서" 이전에 먼저 나온 TYPE-1 라벨은 무관
```

### M3. V-11/12/13 검증 시나리오 모호

**v5 §검증 테이블**
```
V-11 의도적으로 추론 결론에 TYPE-1 부여 → Gate 차단
```

**문제**
- "의도적으로"의 재현 절차 없음
- 누가, 어떻게 부여? 자동/수동?
- PASS/FAIL 판정 기준 정량화 안 됨

**개선안: 구체 테스트 케이스**
```bash
# test_v5_v11.sh
echo '# 의도 위반 샘플
CONFIDENCE: 높음
ACTION: test
EVIDENCE: TYPE-1 (따라서 이것이 원인이다)  # 추론을 TYPE-1로 잘못 라벨
' > /tmp/test_v11.txt

# 예상: EVIDENCE-GATE가 차단 (exit != 0 또는 HALT 신호)
bash ~/.claude/hooks/output_gate.sh < /tmp/test_v11.txt
[ $? -ne 0 ] && echo "V-11 PASS" || echo "V-11 FAIL"
```

---

## ✅ 우수한 점

1. **v4/v4.5 구조 계승**: SC-1~8 재사용 → 재발명 회피
2. **E-7/8/9 명확히 번호화 + 조치 매핑**: 문제 ↔ 해결이 1:1 추적 가능
3. **Delta 요약 표 (v4 → v4.5 → v5)**: 변화 추적 쉬움
4. **SC/V 매핑 일관 (SC-9↔V-11 등)**: 검증 설계 깔끔

---

## 💡 핵심 권장사항 (우선순위)

### P1 (필수, v5 승인 전)
**현재 v3 hook에서 E-7/8/9 발생률 실측** (n=100~500턴)
- 스크립트: `scripts/m2-plan/measure_e789.py` (다른 세션에서 작성 예정)
- 결과: `docs/logs/m2-plan_e789_measurement_result.md`
- 판정:
  - <5% → v5 구현 보류
  - 5-20% → OUTPUT-GATE만
  - >20% → v5 전체 구현

### P2 (구조적, v5 설계 단계)
**Stop hook "차단" 설계 재검토**
- C1 개선안 2안 (다음 턴 페널티) 채택 권장
- Stop hook은 로그/경고용으로 격하
- 차단은 "다음 UserPromptSubmit hook에 강제 주입" 방식

### P3 (비용/사용성, 구현 단계)
**EVIDENCE-GATE 2단계 분리**
- 1차: bash 패턴 감지 (저비용, 플래그만)
- 2차: LLM self-check (플래그 세팅 시만)
- 오탐 최소화 + 비용 제어

---

## 🔗 참조 경로

| 경로 | 용도 |
|------|------|
| `docs/01-plan/features/m2-plan.plan.v5.md` | 본 검토 대상 |
| `docs/01-plan/features/m2-plan.plan.v4.md` | 계승 원본 (SC-1~5) |
| `docs/01-plan/features/m2-plan.plan.v4.5.md` | 계승 원본 (SC-6~8) |
| `~/.claude/skills/m2-plan/SKILL.md` | 실행 정의 |
| `~/.claude/hooks/reasoning_gate_v3.sh` | 현재 매 턴 hook |
| `~/.claude/hooks/reasoning_gate_stop.sh` | 현재 Stop hook |
| `docs/logs/m2-plan_cl-auto-workframe_test_run1.md` | v1 실측 n=992 전례 |
| `docs/logs/m2-plan_cl-auto-workframe_v2_3rd.md` | v2 설계 (제 이전 세션) |
| `docs/logs/m2-plan_e789_measurement_prompt.md` | 실측 가이드 (이번 세션 작성) |

---

## 결론

v5는 올바른 문제 의식(E-7/8/9)을 짚었으나 해결 도구(Stop hook, bash regex)가 문제 성격과 미스매치.
**실측 선행 + 아키텍처 소폭 재설계** 후 구현 권장.
