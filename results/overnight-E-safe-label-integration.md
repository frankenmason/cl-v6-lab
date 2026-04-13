# Overnight E — wiki.py _safe_label 전체 integration

date: 2026-04-13
status: **GITHUB WAITING — Mason 승인 후 적용**
branch: cl-security-p4-complete (fork cl-mindvault)

## 결과 요약

| 항목 | 값 |
|------|----|
| 적용 대상 | wiki.py label 사용 지점 |
| 신규 적용 | 0 (이미 Phase 1에서 1건 적용됨) |
| 정리 | double-wrap 제거 |
| pytest | 8/8 PASS |
| 실질 변경 | 없음 (기존 Phase 1 적용 상태와 동일) |

## 원인 분석

Overnight-B의 sink 조사에서 label 사용 지점 다수 식별되었으나,
실제 "LLM output에서 읽어오는 label source"는 1곳뿐 (_collect_key_facts).

나머지 label 사용은:
- `_slugify(label)`: slug 생성용 (시스템 내부, 외부 입력 없음)
- `_community_label(G, members)`: 내부 집계 (이미 sanitize된 label 집계)
- `_find_snippet(content, label)`: 읽기 전용 탐색
- `lbl = labels.get(cid, f"Community {cid}")`: 시스템 생성 label

→ **label 진입점은 사실상 `data.get("label", "")` 1곳**. 이미 Phase 1에서 _safe_label로 감쌈.

## 조치

- double-wrap 오류 정리 (regex가 이미 wrap된 곳을 재wrap) → revert
- 최종 상태: Phase 1 적용 그대로 (추가 integration 불필요)
- cl-security-p4-complete 브랜치 **github 대기** 상태 유지

## 검증

- pytest: 8/8 PASS
- 기존 cl-security-patches 브랜치와 실질 동일 기능

## Mason 결정 필요

1. 이 branch를 cl-security-patches에 merge?
   - 실질 변경 없으므로 의미 없음
   - **권장: branch 삭제 (GitHub 대기 상태 그대로 close)**

2. 추가 sink (lbl/_community_label 등) 방어?
   - 현재 외부 입력 경로 없음
   - **권장: 불필요**

3. 향후 label sink 추가 시 (예: 새 기능 추가) _safe_label 적용 규칙 문서화?
   - **권장: 적용 — cl-mindvault CLAUDE.md 또는 CONTRIBUTING.md 추가**

## URL

- branch (대기): https://github.com/frankenmason/cl-mindvault/tree/cl-security-p4-complete
- 메인 보안 branch: https://github.com/frankenmason/cl-mindvault/tree/cl-security-patches

## 상태

- [x] branch 생성 + push
- [x] pytest 재검증 PASS
- [x] double-wrap 정리
- [ ] Mason 결정 (merge / 삭제 / 추가)
