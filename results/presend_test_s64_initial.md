# presend_check.py 초기 테스트 결과 (S64)

date: 2026-04-13
version: v0.1 (프로토타입)

## 결과 요약

| 테스트 | 기대 | 실측 verdict | Exit | 평가 |
|--------|------|:-----------:|:----:|------|
| 1. BARE (61자) | REWRITE | **PASS** (short bypass) | 0 | ⚠️ 오탐 — V1 개선 필요 |
| 2. 정상 (358자, 3요소 완비) | PASS | PASS | 0 | ✅ |
| 3. E-7/E-8 (추론+TYPE-1+수치무근거) | FLAG | FLAG (2 flags) | 1 | ✅ |
| 4. Fast-path (단답) | PASS | PASS | 0 | ✅ |

## 한계 발견

- V1 단답 판별 길이 150자 cut이 너무 큼 (테스트 1 오탐)
- 길이 대신 문장 수 기반 또는 user context 기반 판별 필요
- MIN_LENGTH 조정 또는 sentence count 로직 추가 필요

## 정량 지표 (초기)

- 검출률 (V2/V3 FLAG): E-7/E-8 테스트에서 2/2 패턴 감지 ✅
- FP 위험 (V1): 짧은 BARE 놓침 → 검출 누락 가능성
- 실행 시간: 즉시 (Python 단일 파일, < 100ms)
