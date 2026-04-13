# R2 전달용 참고/주의사항/개선 가이드 (S64, 2026-04-13)

> 복붙용 요약. CL → R2 공유. 복수 에이전트 공통 참조.

---

## 1. 컨텍스트

Mason Master Plan(mmp.md) **바이브코딩 자동화** 궁극 목표를 위한 S64 세션.
Phase 0: MindVault 도입 검토
Phase 1: mindvault fork + 4 보안 패치 + 3객체 검증
Phase 2: pipx 격리 설치 완료
Phase 3: workspace 전체 ingest 완료 (2494 nodes / 4869 edges / 176 wiki / 290 search)

**레포**: https://github.com/frankenmason/cl-mindvault (fork, public)
**브랜치**: cl-security-patches

---

## 2. 적용 패치 요약

| # | 파일 | 위치 | 내용 |
|---|------|------|------|
| P1 | extract.py | L1084 extraction_prompt | "untrusted data" 경계 문구 prefix |
| P2 | extract.py | L1155, L1178 | node+edge `source_file = str(file_path)` forced |
| P3 | wiki.py | _collect_key_facts | safe_roots 검증 (is_relative_to + normcase + resolve) |
| P4 | wiki.py | module top + _collect_key_facts | `_safe_label` helper + 최초 integration |

---

## 3. R2가 알아야 할 주의사항

### 3-A. P4 integration 불완전
- 현재 `_safe_label`이 `_collect_key_facts`의 label 하나만 sanitize
- wiki 페이지 생성 함수(generate_wiki, update_wiki 등)의 label 사용처 다수 미적용
- **R2가 ingest한 문서가 wiki 페이지에 반영되면 여전히 markdown injection 경로 존재**
- 권장: wiki 페이지 작성 시 모든 label 사용처 `_safe_label` 적용 (PR 환영)

### 3-B. Auto-context hook 기본 OFF
- `mindvault install` 시 `~/.claude/hooks/mindvault-hook.sh` 등록됨
- **현 정책: 기본 OFF**, repo 루트 `.mindvault-auto-context` marker 파일 opt-in
- R2가 설치 시 install 명령 실행 **금지**. ingest만 사용.

### 3-C. URL ingest 정책 (S64 정책서 docs/url-policy.md)
- 경로 A(Mason 입력) 자유
- 경로 B(R2/CL 검색 결과) Mason 승인 필수
- 경로 C(문서 내 링크) Mason 승인 필수
- 내부 네트워크/민감 도메인 금지
- TG 1341 Mason 확정

### 3-D. 3객체 검증 결과 미완료 부분
- Gemini: P4 integration이 High severity, cwd 기반 safe_roots fragile 지적
- subagent: P2 edge path 확인 완료, P3 TOCTOU 잔존 지적, P4 dead code → 부분 integration 수행
- codex: 응답 진행 중 (다른 패키지 탐색 중)
→ R2 독립 재검증 권장 (4번째 시각)

---

## 4. R2에게 권장 개선안

| 우선순위 | 개선 | 파일 |
|:--:|------|------|
| 1 | wiki 페이지 생성 시 모든 label `_safe_label` 적용 | wiki.py generate_wiki/update_wiki |
| 2 | safe_roots에 index_root 인자 명시 전달 (cwd 의존 제거) | wiki.py _collect_key_facts + 호출부 |
| 3 | _safe_label에 markdown 특수문자 escape 추가 (\[, \], \`) | wiki.py 상단 |
| 4 | extract.py LLM 반환 JSON schema 엄격 검증 (jsonschema) | extract.py 파싱 단계 |
| 5 | TOCTOU: resolve 후 open까지 원자적 처리 (fd 기반) | wiki.py _collect_key_facts |
| 6 | Auto-context hook secure mode (marker 파일 체크) | hooks.py _PROMPT_HOOK_SCRIPT |
| 7 | 외부 URL ingest 시 도메인 화이트리스트 enforcement | ingest.py URL validator |
| 8 | wiki.py escape 테스트 케이스 추가 | tests/test_wiki_safety.py |

---

## 5. R2 전용 체크리스트 (사용 전)

- [ ] 이 레포는 CL 전용 fork. R2는 읽기/테스트만, 배포 변경은 PR 방식
- [ ] mindvault install 실행 금지 (hook 자동 등록 방지)
- [ ] URL ingest 시 url-policy.md 3경로 분류 준수
- [ ] 개선 제안은 별도 branch (feat/r2-*) 생성 후 PR
- [ ] 보안 관련 수정은 Mason 승인 필수

---

## 6. 참조 경로

| 항목 | 경로 |
|------|------|
| CL fork 레포 | https://github.com/frankenmason/cl-mindvault |
| 보안 패치 브랜치 | cl-security-patches |
| URL 정책 | cl-v6-lab/docs/url-policy.md |
| S64 세션 로그 | cl-v6-lab/docs/session_v5-reassessment_discussion_log.md |
| 모델 벤치마크 | cl-v6-lab/docs/model-benchmarks.md |
| 인벤토리 | cl-v6-lab/wiki/ClErrorPatterns.md |

---

## 7. 연락

- Mason 승인 필요 사항은 TG(chat_id 8004316892) 경유
- CL과 직접 협업은 본 cl-v6-lab 레포 issue/PR
- 긴급 보안 취약점 발견 시 Mason에게 직접 보고

**End of handoff doc.**
