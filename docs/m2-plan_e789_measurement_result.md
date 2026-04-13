# E-7/8/9 발생률 실측 결과

**date:** 2026-04-13
**method:** Python transcript parsing + session-clustered bootstrap (v2 external-validated design)
**script:** `scripts/m2-plan/measure_e789.py`
**design validation:** Gemini 2.5 Pro + codex:codex-rescue 독립 검증 반영

---

## 측정 설계 (외부 검증 반영)

1. Baseline 비교 제거 (절대 prevalence + 95% CI만)
2. 대상: 2026-04-13 기준 전체 jsonl 중 size ≥ 5KB + assistant 턴 ≥ 10
3. 현재 세션(5d893ed4) 자동 제외 (측정 오염 방지)
4. 층화 무작위 샘플링: 세션당 max 50턴
5. Fast-Path 제외: user 단답 승인/확인 (`1/2/ㅇ/ok/@승인/네/맞음/수용/동의함/허용/yes/y`)
6. E-7/8/9 독립 측정 (집계 금지)
7. 세션 단위 bootstrap 1000회 → 95% CI
8. 사전 등록 결정 규칙: CI 하한 > threshold% → IMPLEMENT

---

## 결과 표

| 항목 | Run1 (seed=43) | Run2 (seed=45) | 평균 | 안정성 |
|------|---------------:|---------------:|-----:|:-------|
| 적격 세션 | 85 | 85 | 85 | 동일 |
| 측정 턴 (Fast-Path 제외) | 2571 | 2571 | 2571 | 동일 |
| E-7/E-8 count | 4 | 3 | 3.5 | — |
| E-7/E-8 raw % | 0.1556 | 0.1167 | 0.1362 | Δ=0.04% (PASS) |
| E-7/E-8 CI 95% | 0.00–0.4249 | 0.00–0.3205 | — | 겹침 |
| E-7/E-8 **판정** | **SKIP** | **SKIP** | **SKIP** | 일치 |
| E-9 count | 2570 | 2570 | 2570 | — |
| E-9 raw % | 99.9611 | 99.9611 | 99.9611 | Δ=0% (PASS) |
| E-9 CI 95% | 99.8746–100.0 | 99.8747–100.0 | — | 완전 일치 |
| E-9 **판정** | **IMPLEMENT** | **IMPLEMENT** | **IMPLEMENT** | 일치 |

threshold = 1.0% (사전 등록)

---

## 판정 기준 (사전 등록)

- CI 95% 하한 > 1% → IMPLEMENT (구현 정당)
- CI 95% 상한 < 1% → SKIP (구현 보류)
- 1%가 CI 내 → NEED_MORE_DATA

---

## 재현성 검증

| 지표 | 기준 | 실측 | PASS/FAIL |
|------|-----:|-----:|:---------|
| E-7/8 \|Run1-Run2\| | < 2×SE | 0.04% | PASS |
| E-9 \|Run1-Run2\| | < 2×SE | 0.00% | PASS |
| E-7/8 CI 겹침 | 있어야 함 | 있음 | PASS |
| E-9 CI 겹침 | 있어야 함 | 있음 | PASS |

재현성 안정. 결과 신뢰 가능.

---

## 해석 주의사항 (중요)

### E-7/E-8: 0.1% — 과소 감지 가능성

- regex 패턴 (`따라서|이므로|즉|결국|그래서` + `TYPE-1`)으로만 감지
- 의미 분석(추론 결론 vs 데이터 관찰)은 미수행
- 진짜 E-7/E-8은 의미 해석 필요 → 추가 검증 권장
- 현재 값은 **보수적 하한**으로 해석

### E-9: 99.96% — 해석 극단적, 원인 분석 필요

- 과거 세션들이 INTENT/Selector/CONFIDENCE 규칙을 **아예 몰랐을 가능성**
- CLAUDE.md 04조 Interface Mode 3요소 규칙은 **최근 도입**
- 과거 세션에는 규칙 자체가 없었으므로 "누락률 99.9%"는 자연스러움
- 이 값은 "과거 미준수율"이지 "현재 준수 실패율"이 아님
- **현재 규칙 하의 재발률 측정**을 위해서는:
  - (A) 대상을 규칙 도입 이후 세션으로 제한
  - (B) 또는 **최근 N턴**만 측정 (예: 최근 7일)

---

## 결정 권고

### v5 OUTPUT-GATE (E-9 대응)
- 형식적 판정: **IMPLEMENT** (CI 하한 99.87% >> 1%)
- 실질 판정: **재측정 필요** (과거 데이터 오염)
- 권장: 최근 7일 세션만 재측정 후 결정

### v5 EVIDENCE-GATE (E-7/E-8 대응)
- 판정: **SKIP** (CI 상한 0.42% < 1%)
- 단 regex 기반 하한치. 의미 분석 기반 재측정 시 상승 가능
- 권장:
  - 현재 결과(과소 감지)만으로는 SKIP 결정 보류
  - Phase 1차: 의심 턴(위 0.1%)에 대해 LLM self-check로 재분류 → 실제 비율 확인

---

## 권장사항 (재측정)

1. **최근 7일 세션만** 재측정 → E-9 규칙 강화 이후 실제 준수 실패율 확인
2. **E-7/E-8 의심 턴 LLM 재분류** → regex 한계 보정
3. **결과 확정 후** v6 plan 설계 착수

---

## 참조

- 설계: `scripts/m2-plan/measure_e789.py`
- 원본 데이터: `/home/ubuntu/.claude/projects/-home-ubuntu--cokacdir-workspace/*.jsonl` (140개)
- Run1 JSON: `/tmp/measure_e789_run1.json`
- Run2 JSON: `/tmp/measure_e789_run2.json`
- 검토 원본: `docs/logs/m2-plan_v5_independent_review.md`
- 측정 가이드: `docs/logs/m2-plan_e789_measurement_prompt.md`
- 외부 검증: Gemini 2.5 Pro + codex:codex-rescue
