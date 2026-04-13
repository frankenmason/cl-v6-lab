# Overnight D — cl-mindvault 보안 패치 회귀 테스트

date: 2026-04-13
status: 8/8 PASS

## 생성 파일

- `cl-mindvault/tests/test_security.py` (commit 87718cf, cl-security-patches 브랜치)

## 테스트 결과 (pytest)

```
tests/test_security.py::test_p1_extraction_prompt_has_untrusted_boundary PASSED [ 12%]
tests/test_security.py::test_p2_source_file_forced_for_nodes PASSED      [ 25%]
tests/test_security.py::test_p2_source_file_forced_for_edges PASSED      [ 37%]
tests/test_security.py::test_p3_safe_roots_path_validation PASSED        [ 50%]
tests/test_security.py::test_p3_path_traversal_attack_skipped PASSED     [ 62%]
tests/test_security.py::test_p4_safe_label_exists_and_sanitizes PASSED   [ 75%]
tests/test_security.py::test_p5_hook_has_marker_optin PASSED             [ 87%]
tests/test_security.py::test_p5_hook_version_marker_bumped PASSED        [100%]
============================== 8 passed in 0.16s ===============================
```

## 커버리지

| 패치 | 테스트 | 유형 | 결과 |
|------|--------|------|:----:|
| P1 | extraction_prompt untrusted boundary | 소스 grep | PASS |
| P2 node | source_file forced (node) | 소스 grep | PASS |
| P2 edge | source_file forced (edge) | 소스 grep | PASS |
| P3 structure | safe_roots/is_relative_to 존재 | 소스 grep | PASS |
| P3 functional | /etc/passwd 공격 차단 | runtime 호출 | PASS |
| P4 structure | _safe_label 동작 | runtime 호출 | PASS |
| P5 marker | .mindvault-auto-context 체크 | 소스 grep | PASS |
| P5 version | HOOK_VERSION=4 | 소스 grep | PASS |

## 실행 방법 (Mason 재현)

```bash
cd /home/ubuntu/cl-mindvault
PIPX_PY=/home/ubuntu/.local/share/pipx/venvs/mindvault-ai/bin/python
$PIPX_PY -m pytest tests/test_security.py -v
```

## 기술 노트

- pytest 실행은 pipx 가상환경 python 필요 (networkx 등 의존성)
- P3 functional 테스트: `/etc/passwd`를 source_file로 넣은 node로 _collect_key_facts 호출 시 빈 결과 확인 — path traversal 차단 검증
- P4 runtime: `\n\r\n` 연속 replace로 공백 2개 생성 (예상된 동작)

## 상태

- [x] tests/test_security.py 추가
- [x] 8/8 PASS
- [x] push (cl-security-patches 브랜치)
- [ ] main 머지 — Mason 승인 후
