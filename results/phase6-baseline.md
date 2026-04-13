# Phase 6 Baseline & Operational Plan

date: 2026-04-13
phase: 6 (운영/측정)
status: baseline 확정 + 1주 측정 plan

---

## 1. S64 세션 Baseline (설치 직전까지 누적)

| 지표 | 값 |
|------|:--:|
| 총 Turn 수 | 75 (진행 중) |
| CL 오류 인벤토리 I-* | 12 건 |
| [CORRECTION] hook 감지 | 14 회 |
| CORRECTION 발생률 | 18.7% (14/75) |
| 세션 jsonl 크기 | 19.6 MB |
| 세션 소요 | 약 3.5h (12:51~17:37) |

---

## 2. Baseline 오류 유형 분포 (12건)

| 유형 | 건수 | 비율 |
|------|:--:|:--:|
| E-9 (3요소 누락, [CORRECTION] 별도 집계) | 2건 명시 + 14 hook | 32% |
| E-7/E-8 (근거 없는 추정) | 3건 | 25% |
| 프로세스 이탈 (자율실행) | 2건 | 17% |
| 도구 미활용 | 1건 | 8% |
| 도구 부분 사용 | 1건 | 8% |
| 의사소통 실패 | 1건 | 8% |
| 방법론 오류 | 1건 | 8% |
| 자의 선언 | 1건 | 8% |

---

## 3. 설치 후 예상 효과 (가설, 실측 전)

| 대상 | 가설 | 측정 지표 |
|------|------|----------|
| I-10 도구 미활용 | MindVault 자동 주입으로 해결 | wiki/qmd/CVM 사용 빈도 |
| I-7 Mason 의도 오해 | mindvault query로 과거 컨텍스트 사전 확보 | 재질문 빈도 |
| I-1/I-2/I-9 근거없는 추정 | presend_check + mindvault 근거 찾기 | FLAG/REWRITE verdict |
| I-11 E-9 반복 | presend_check V1 차단 | CORRECTION 감소율 |

---

## 4. 운영 측정 plan (1주)

### 4-A. 데이터 수집
- 매 세션 jsonl 누적 (auto)
- presend_check.py verdict 로그 (수동)
- [CORRECTION] hook 발생 카운트
- mindvault query 호출 빈도

### 4-B. 일별 점검
- Turn 종료 시 CL 자가 인벤토리 append
- 매일 종료 시 results/daily-*.md 작성

### 4-C. 주간 리포트 (D7)
- CORRECTION 발생률 전후 비교
- 인벤토리 유형별 증감
- 3객체 주간 검증 소환
- v6 완성도 평가
- Mason 최종 승인

---

## 5. 측정 스크립트 후속 필요 (P6 TODO)

- scripts/metrics/count-corrections.py — jsonl에서 CORRECTION 패턴 카운트
- scripts/metrics/presend-log-aggregate.py — presend_check verdict 통계
- scripts/metrics/weekly-report.py — 위 데이터 종합

---

## 6. 최종 Goal 달성 기준

| 기준 | 측정 | 목표 |
|------|------|------|
| 안정화 | CORRECTION 발생률 감소 | Baseline 18.7% → 목표 <10% |
| 자동화 | MindVault query 활용 빈도 | 세션 턴당 ≥1회 |
| 실행률 | presend_check 자동 루틴화 | 응답 전 100% 실행 |
| 마이그레이션 | MindVault 기존 도구 보완 (대체 X) | 3-way 공존 유지 |

---

## 7. Phase 6 현 시점 완료 선언 기준

- [x] Baseline 확정
- [x] 측정 plan 문서화
- [ ] 측정 스크립트 구현 (후속)
- [ ] 1주 운영
- [ ] 주간 리포트 + 3객체 검증
- [ ] 최종 Mason 승인

**현 Phase 6 Status: RUNNING (운영 진입, 1주 측정 대기)**

---

## 참조

- session log: cl-v6-lab/docs/session_v5-reassessment_discussion_log.md
- 인벤토리: cl-v6-lab/wiki/ClErrorPatterns.md
- URL 정책: cl-v6-lab/docs/url-policy.md
- R2 handoff: cl-v6-lab/docs/handoff-to-r2.md
- fork 브랜치: https://github.com/frankenmason/cl-mindvault/tree/cl-security-patches
