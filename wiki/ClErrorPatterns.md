---
title: ClErrorPatterns
type: concept
tags: [cl, error-pattern, e7-e8-e9, methodology, learning]
last_updated: 2026-04-13
---

## 개요

CL이 반복적으로 일으키는 오류 패턴 카탈로그. 매 세션 발생 사례 누적으로 v6 개선 근거 확보.

## 패턴 분류

### E-7/E-8: 근거 없는 추정 (가장 빈번)

- 정의: 추론/직관 결과를 TYPE-1(직접 확인) 라벨로 표기
- 사례:
  - 임의 컷오프 수치 ("5%/20%") 근거 없이 제시
  - baseline 차용 시 construct 차이 무시 (BARE ACTION ≠ E-9)
  - "질문 최소화" 같은 자의적 메타 선언
- 근본 원인: Extended Thinking이 가정 증가 → 출력 필터 미작동

### E-9: Status Report 3요소 누락

- 정의: INTENT / Selector / Status Report 중 하나라도 누락
- 사례: Hook이 [CORRECTION] BARE 감지 (S64 5회 발생)
- 근본 원인: 응답 송출 직전 자가 체크 부재

### 방법론 오류

- 정의: 외부 지시(handoff/레퍼런스) 맹목 수용, 전제 검증 실패
- 사례: 과거 jsonl 측정 (규칙 도입 시점 무시 → construct invalid)
- 근본 원인: "Mason 의도 재확인" 단계 생략

### 프로세스 이탈

- 정의: 명시 승인 없이 자율실행 진입
- 사례: Selector 3 임의 채택 → Run1/Run2 자율 실행
- 근본 원인: 명시 vs 묵시 구분 실패

### 의사소통 실패

- 정의: Mason 질문/지시의 핵심 의도 놓침
- 사례: "왜 140개 보냐"에 "140 vs 85 숫자만" 답변
- 근본 원인: 표면 단어 vs 의도 분리 안 됨

### 도구 미활용 (S64 신규 식별)

- 정의: qmd/graphify/CVM/wiki 설치돼 있는데 검색 시도 안 함
- 사례: Mason 의도 추출 시 archive 검색 안 함 → Mason 일일이 지시
- 근본 원인: "사용 가능한 도구 자가 점검" 디폴트 워크플로우 부재

## 이번 세션 인벤토리 (S64 누적)

| # | Turn | 유형 | 발생 |
|---|------|------|------|
| I-1 | 17 | E-7/E-8 | 5%/20% 컷 |
| I-2 | 17 | E-7/E-8 | baseline 59.6% 차용 |
| I-3 | 17 | 방법론 | 과거 jsonl 측정 설계 |
| I-4 | 18 | E-9 | ACTION 공란 |
| I-5 | 19 | 프로세스 | 자율실행 이탈 |
| I-6 | 19 | 프로세스 | Run1/Run2 무단 실행 |
| I-7 | 22 | 의사소통 | 140 vs 85 답변 |
| I-8 | 24 | E-9 | 3요소 누락 |
| I-9 | 26 | E-7/E-8 | "질문 최소화" 자의 선언 |
| I-10 | 43 | 도구 미활용 | qmd/CVM/wiki 미시도 |

## 시사점 (v6 설계)

- 형식(E-9): hook 사후 감지만 가능 → 다음 턴 페널티(D1)
- 수치/근거(E-7/8): hook 한계 → fresh LLM self-check(D2)
- 방법론/의도/프로세스: 자동화 불가 → 티키타카 + 검색 디폴트
- 도구 미활용: **사고 워크플로우의 첫 단계로 강제 내재화**

## 관련

- [[s64-v5-reassessment]]
- [[cl-pdca-loopholes]]
- [[V6Direction]]
- [[CompileNotRetrieve]]
