---
title: "YouTube 핵심 레퍼런스 — 카파시 LLM Wiki × Claude Code × Obsidian × Graphify"
type: source
tags: [youtube, karpathy, llm-wiki, graphify, obsidian, claude-code, second-brain, core-reference]
date: 2026-04-12
url: https://youtube.com/watch?v=cNlvrU-KcRg
title_full: "카파시의 LLM Wiki로 나만의 AI 세컨드 브레인 만들기, 이것만 보세요— 클로드 코드 × 옵시디언 × Graphify"
summarizer: R2 (Hermes agent)
sources: []
last_updated: 2026-04-13
mason_designation: "핵심 레퍼런스이자 실제 너가 작용/수행/실행 되도록 하는 것이 목표"
---

## 개요

Mason이 v6 핵심 레퍼런스로 지정한 YouTube 영상. R2가 요약 전달.

영상 핵심 주제:
- Obsidian + LLM Wiki + Graphify로 개인용 AI 세컨드 브레인 구축
- 지식그래프 + 위키 + Obsidian 뷰로 구조화
- "이것만 보세요" = 표준 운영 가이드

## Graphify 핵심 (영상 시연)

- Claude Code용 스킬 (`/graphify`)
- 폴더 읽고 → 지식그래프 빌드 → graph.html / Obsidian vault / wiki 출력
- 멀티모달: code, pdf, markdown, 이미지, 스크린샷, 다이어그램
- 캐시/업데이트 구조: 변경된 파일만 재처리 (SHA256)
- Edge 구분: EXTRACTED / INFERRED / AMBIGUOUS — 환각 감소

## 5가지 실무적 가치 (R2 요약)

| 항목 | 핵심 |
|------|------|
| 안정성 | 로컬 중심, SHA256 캐시, edge 분류로 환각 감소 |
| 최적화 | 토큰 절감, 그래프 재사용, 증분 갱신 (update/watch/hook) |
| 효율성 | 관계 탐색에 강함, Obsidian 그래프뷰 궁합, 위키 index.md 탐색성 |
| 활용성 | 코드베이스, 연구자료, PDF/이미지 포함 KB, 프로젝트 메모리 |
| 범용성 | Claude Code, Codex, OpenCode, Cursor, Gemini CLI, OpenClaw 등 |

## 주의점

- 문서 정리 도구가 아니라 그래프 기반 지식 추론 도구
- 입력 자료 품질이 그래프 품질 결정
- source 정리 미흡 시 환각 추정 증가

## 우리 환경과의 매핑 (실측)

| 영상 요소 | 우리 보유 자산 | 상태 |
|----------|---------------|------|
| Karpathy LLM Wiki | wiki/ 16페이지 (compile-not-retrieve) | ✅ 운영 |
| /graphify | graphify-mcp pm2 online | ✅ 운영 (5h uptime) |
| Obsidian vault | obsidian-vault/ 270노트 | ✅ |
| Claude Code 스킬 | mason-second-brain 4커맨드 | ✅ 완료 (91% match) |
| qmd 검색 | qmd MCP + CLI | ⚠️ MCP 끊김 (현재) |
| vault-memory CLI | OSBA semantic search | ✅ index 완료 (276 노트) |

→ **인프라 모두 갖춤. 운영 디폴트화가 v6 핵심**

## v6와의 직접 연결

영상이 보여주는 운영 흐름:
1. Web Clipper로 raw 수집
2. /wiki-ingest로 wiki에 합성
3. /graphify로 지식그래프 갱신
4. Obsidian 그래프뷰로 탐색
5. 새 질문 시 위키/그래프 조회 → 합성

CL이 매 발화 전 디폴트로 수행해야 할 워크플로우.

## 관련

- [[V6Direction]]
- [[ClErrorPatterns]]
- [[CompileNotRetrieve]]
- [[LlmWikiAgent]]
- [[MasonSecondBrain]]
- [[s64-v5-reassessment]]

## Mason 지정 의의

영상 = 단순 참조 X, **CL의 실제 작동/실행 표준**
즉 v6 = 이 영상의 운영 흐름을 CL이 디폴트로 수행하도록 내재화
