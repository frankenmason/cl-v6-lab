---
title: V6Direction
type: concept
tags: [v6, m2-plan, design-direction, wip, compile-not-retrieve]
last_updated: 2026-04-13
status: draft
---

## 개요

m2-plan v5 폐기 후 v6 진짜 정체. S64 PDCA archive 재발견 결과 = 신규 설계 X, 기존 PDCA 재실행/보완.

## v6 본질

- **v6 ≠ 신규 GATE 추가**
- **v6 = cl-reasoning-gate + cl-assumption-prevention 보완 + Karpathy compile-not-retrieve 운영화**
- **v6 = CL 사고 워크플로우의 "검색 → 합성 → 발화" 디폴트 내재화**

## 5개 보완 방향 (S64 도출)

| # | 방향 | 출처 |
|---|------|------|
| 1 | cl-reasoning-gate Layer 1/3 완전 검증 | report 미수행 항목 |
| 2 | cl-assumption-prevention F-4 해결 (라벨+내용 정합성) | report 후속 과제 |
| 3 | 자기 학습 루프 (Hook 차단 → 학습 → 다음 턴 강도 증가) | S64 인벤토리 분석 |
| 4 | autoresearch ↔ PDCA 통합 (지속 개선) | mmp.md Phase 3 |
| 5 | m2-plan 자체를 학습 루프에 포함 | 도구가 본업 잡아먹는 패턴 깨기 |

## 보조 장치 (D8/D9 — 주 해결책 X, 보조)

- D8: V1 (3요소 Stop hook 재생성)
- D9: V2/V3/V4 (별도 fresh LLM pass)

## Mason 본업과의 관계

- mmp.md 궁극 목표: **바이브코딩 자동화 (compile-not-retrieve)**
- Phase 1 (지식베이스): mason-second-brain로 91% 완료 (2026-04-08)
- Phase 2 (OSBA): 대기
- Phase 3 (자동화): 미시작

→ v6 = Phase 3 일부 (m2-plan PDCA 자동화)
→ but CL 오류로 도구 디버깅 늪 = Mason 본업 3달+ 지연 직접 원인
→ v6 진짜 목적: **CL 자율도/정확도 향상으로 Mason을 본업으로 해방**

## 디폴트 워크플로우 (S64 Mason 지시 Turn 52)

매 발화/판단 전 다음을 자동 수행:
1. **검색**: qmd / CVM / wiki / archive — 관련 정보 조회
2. **합성**: 발견 결과를 현재 문맥과 결합
3. **발화**: TYPE-1/2/3 라벨 + 3요소 + Selector
4. **갱신**: wiki ingest (이번 발화/결정도 wiki에 누적)

이게 Karpathy compile-not-retrieve 패턴의 실제 운영. v6 = 이 워크플로우의 강제/내재화.

## 다음 단계 (Mason 승인 후)

1. 두 PDCA design.md 추가 정독 → Layer 1/3 재현 절차 확보
2. F-4 (라벨+내용 정합성) 의미 분석 메커니즘 설계
3. 자기 학습 루프 프로토타입
4. autoresearch ↔ PDCA 연결 점 식별
5. v6.plan.md 작성 → bkit PDCA Plan 단계로 진입

## 관련

- [[s64-v5-reassessment]]
- [[ClErrorPatterns]]
- [[cl-pdca-loopholes]]
- [[MasonSecondBrain]]
- [[CompileNotRetrieve]]
- [[LlmWikiAgent]]
