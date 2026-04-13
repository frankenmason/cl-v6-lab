# 모델별 공식 벤치마크 & 가중치 산출 (S64)

> 수집일: 2026-04-13
> 출처: benchlm.ai, automatio.ai, pricepertoken.com, deepmind report, umesh-malik.com, openai/simple-evals
> 용도: 3객체 검증 시 각 모델 답변의 가중치 부여

---

## 1. 모델별 raw 벤치마크 (공식 수치)

### Claude Opus 4.6 (CL 본체, 기준)
- 출처: automatio.ai, benchlm.ai
- 종합 (benchlm): **85 / 100**
- GPQA: **91.3%**
- HumanEval: **95.4%** (Thinking 97.0%)
- MMLU: **91.3%**
- MMLU Pro: **82.1%**
- LiveCodeBench: **70.2%**
- SWE-Bench: **80.2%**
- HLE: **53%**
- AIME 2025: **94.2%**

### Claude Sonnet 4.5 (subagent 코딩용)
- 출처: pricepertoken.com HumanEval leaderboard
- HumanEval (Thinking): **97.6%** (전체 1위)
- 종합: 상세 없음, ~85 수준 추정 (Opus 4.6과 근접)

### Claude Haiku 4.5 (subagent 검색용)
- 출처: benchlm.ai
- 종합: **63 / 100**
- HumanEval (Thinking): 96.3%
- Coding: 48.5 (vs Opus 72)
- Knowledge: 54.4 (vs Opus 77.8)

### OpenAI GPT-5.4 mini (Codex CLI 내장)
- 출처: benchlm.ai, umesh-malik.com
- GPT-5.4 base 종합: **94 / 100** (1위)
- GPT-5.4 mini (프로비저널): **73 / 100**
- GDPval: 83.0% (base)
- OSWorld-Verified: 75.0% (base)
- SWE-Bench Pro: 57.7% (base)

### Gemini 2.5 Pro
- 출처: datatunnel.io, deepmind gemini_v2_5_report.pdf
- LiveCodeBench: **74.2%**
- GPQA Diamond: **86.4%**
- Aider Polyglot: **82.2%**
- AIME 2025: **88.0%**
- HLE: 21.6%
- FACTS Grounding: 87.8%
- 종합 추정: **~80 / 100**

---

## 2. 상대 가중치 계산 (Opus 4.6 기준 정규화)

| 모델 | 종합 점수 | Opus 대비 | 용도 |
|------|:--------:|:---------:|------|
| Claude Opus 4.6 | 85 | 1.00 | CL 본체 |
| Claude Sonnet 4.5 | ~85 | ~1.00 | subagent 코딩 |
| Claude Haiku 4.5 | 63 | 0.74 | subagent 검색 |
| GPT-5.4 mini | 73 | 0.86 | codex CLI |
| Gemini 2.5 Pro | ~80 | 0.94 | Gemini CLI |

---

## 3. 3객체 검증 시 가중치 제안 (Mason 조정 필요)

이번 세션 Turn 34에서 사용한 3객체:
- codex:codex-rescue → GPT-5.4 mini 기반 (Codex CLI)
- general-purpose subagent → Sonnet 계열 추정
- Gemini 2.5 Pro

### 방안 A: 능력치 정규화만
```
codex        = 0.86 → 25.7%
subagent     = 1.00 → 29.9%
Gemini       = 0.94 → 28.1%
  (합계 2.80 기준 정규화, 나머지 16.3% 합의 가중치)
```

### 방안 B: 독립성 가중 (codex 완전 독립 컨텍스트 +bonus)
```
codex        = 0.86 * 1.2 독립성보너스 = 1.03 → 32%
subagent     = 1.00 * 1.0 = 1.00 → 31%
Gemini       = 0.94 * 1.15 = 1.08 → 34%
  (합계 3.11)
```

### 방안 C: 균등 (1:1:1) — 단순 평균

---

## 4. 한계 명시

- Sonnet 4.5 종합 점수 미상 (~85 추정은 HumanEval 97.6% 단일 근거)
- GPT-5.4 mini는 base의 78% 추정 (mini 전용 상세 수치 부족)
- 독립성 보너스 (방안 B) 수치는 제 임의 (근거 없는 추정 위험)
- Mason 조정 필수

---

## 5. 참조 URL

- https://pricepertoken.com/leaderboards/benchmark/humaneval
- https://benchlm.ai/compare/claude-haiku-4-5-vs-claude-opus-4-6
- https://automatio.ai/models/claude-opus-4-6
- https://umesh-malik.com/blog/openai-gpt-5-4-complete-guide
- https://benchlm.ai/models/gpt-5-4
- https://datatunnel.io/product/gemini-2-5-pro-benchmark-results/
- https://storage.googleapis.com/deepmind-media/gemini/gemini_v2_5_report.pdf
