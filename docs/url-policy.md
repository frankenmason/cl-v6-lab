# URL Ingest 정책 (S64)

> 확정일: 2026-04-13
> 승인: Mason (TG 1341)
> 범위: mindvault ingest + 직접 조회/다운로드 포함

---

## 0. 정의

"외부 URL" = HTTP/HTTPS 리소스로 외부 서버에서 콘텐츠를 가져오는 모든 행위.

대상 도구:
- `mindvault ingest <URL>`
- Exa web_search / web_fetch
- firecrawl scrape / crawl
- curl / wget / requests / httpx
- mcp__plugin_ecc_exa__* / mcp__firecrawl__*

---

## 1. URL 출처 3경로

| 경로 | 설명 | 예시 |
|------|------|------|
| **A. Mason 직접 입력** | Mason이 TG/터미널로 CL에게 전달한 URL | "https://youtube.com/watch?v=cNlvrU-KcRg" |
| **B. CL 검색 결과** | CL이 Exa/Gemini/firecrawl로 찾은 URL | Exa search → top result URL |
| **C. 문서 내 링크** | Mason 제공 문서/기존 wiki 내 링크 | mmp.md 속 `https://...` |

---

## 2. 처리 정책

### 경로 A (Mason 입력)
- **자유**: 별도 승인 없이 즉시 ingest/fetch 가능
- 단 Mason 원문 인용과 함께 처리 이력 기록

### 경로 B (CL 검색 결과)
- **Mason 승인 필수**
- 절차:
  1. CL이 검색 수행
  2. 발견된 URL 목록 + 각 URL의 출처 메타데이터(검색어/랭킹/snippet) TG 보고
  3. Mason 승인 수신 후 ingest
  4. Mason 거부 시 skip

### 경로 C (문서 내 링크)
- **Mason 승인 필수**
- 절차:
  1. CL이 문서에서 링크 추출
  2. 링크 목록 + 포함 문서 출처 TG 보고
  3. Mason 승인 수신 후 ingest

---

## 3. 사전 차단 도메인 (화이트리스트 외)

화이트리스트 (경로 B/C 자동 승인 허용 검토 대상):
- github.com, gist.github.com
- arxiv.org
- anthropic.com, openai.com, google.com (공식 docs)
- karpathy.github.io
- pypi.org, npmjs.com, crates.io (공식 패키지 저장소)
- Mason 지정 기업 도메인

화이트리스트 도메인도 **최초 승인은 Mason 확인** 권장. 이후 반복 시 자동 승인 가능.

**모든 기타 도메인은 경로 무관 Mason 승인 필수.**

---

## 4. 금지 대상 (어떤 경로든 불가)

- 내부 네트워크 (Tailscale, localhost, 127.0.0.1, 192.168.*, 10.*)
  - 예외: mindvault 자체 MCP endpoint 등 공식 시스템
- 로컬 파일 경로 (file://)
- 민감 정보 추정 도메인 (banking, health, internal corporate)

---

## 5. Auto-Context Hook 정책

MindVault Auto-context hook은 **기본 OFF**.

Opt-in 조건:
- repo 루트에 `.mindvault-auto-context` marker 파일 존재 시만 작동
- 현재 세션에서는 `/home/ubuntu/cl-v6-lab/` 와 `/home/ubuntu/.cokacdir/workspace/` 에 한해 Mason 승인 후 on 예정

---

## 6. 승인 요청 TG 포맷

```
📥 URL Ingest 승인 요청
• 경로: B (CL 검색 결과) / C (문서 내 링크)
• URL: https://...
• 출처: [검색어 or 포함 문서]
• 목적: [ingest 후 어떻게 사용할지]
• 도메인 화이트리스트: O / X

승인(Y) / 거부(N) / 일괄 승인(AA) / 다음 Q
```

---

## 7. 위반 시 대응

- 무단 ingest 발견 → 즉시 wiki/인덱스 해당 엔트리 삭제
- 인벤토리에 I-* 오류로 기록
- reasoning_gate 검사 강화

---

## 8. 로그

- 모든 ingest 요청/승인/거부는 results/url-log.jsonl에 추가
- Phase 6(1주 효과 측정)에서 통계 산출

---

## 9. 관련

- MindVault README (취약점 맥락)
- docs/model-benchmarks.md
- session_v5-reassessment_discussion_log.md

## 상태

- [x] 정책 초안 작성
- [ ] Mason 최종 승인
- [ ] Phase 1 착수
