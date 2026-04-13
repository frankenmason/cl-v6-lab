# cl-v6-lab

CL v6 improvement workbench.

## Context

S64 (2026-04-13) v5 재평가 세션에서 도출. 
m2-plan v5 폐기 → v6 진짜 정체 = 이전 PDCA(cl-reasoning-gate, cl-assumption-prevention) 보완 + CL RAG 디폴트 워크플로우 운영화.

## 구조

- `docs/` — 현재 논의 자료 (S64 log, 인벤토리, PDCA 분석, YouTube R2 요약)
- `scripts/presend/` — Pre-send self-check 프로토타입
- `wiki/` — LLM Wiki 사본 (compile-not-retrieve 참조)
- `hooks/` — reasoning gate 개선 실험물
- `results/` — raw data 누적 (PASS/FLAG/REWRITE 로그, 비용)

## 참조

- Karpathy LLM Wiki: https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f
- YouTube 핵심 레퍼런스: https://youtube.com/watch?v=cNlvrU-KcRg
- masonmasterplan.md (바이브코딩 자동화 로드맵)

## 진행 상태

- [x] S64 논의 자료 복사
- [x] wiki 4개 페이지 ingest (ClErrorPatterns, V6Direction, cl-pdca-loopholes, s64-v5-reassessment, YouTube R2 요약)
- [x] measure_e789.py (E-9 실측, 세션당 13.8% CORRECTION 발생)
- [ ] presend_check.py 프로토타입
- [ ] 모델별 능력치 조사 (Opus 4.6 / Sonnet / Haiku / GPT-5.4 mini / Gemini 2.5 Pro)
- [ ] 3객체 검증
- [ ] reasoning gate 통합
