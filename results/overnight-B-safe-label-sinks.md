# Overnight B — wiki.py _safe_label 적용 후보 sinks

## label 변수 사용 지점 (적용 후보)

| # | 줄 | 코드 | 위험도 | 적용 권장 |
|--|--:|------|:----:|:----:|
| 1 | 11 | `"""Sanitize label for markdown embedding.` | mid (write path) | Y |
| 2 | 138 | `key = f"{src}::{label}"` | high (f-string markdown) | Y |
| 3 | 263 | `nlabel = data.get("label", nid)` | source (변수 지정) | Y (source) |
| 4 | 267 | `page_lines.append(f"- **{nlabel}** ({src_file}) -- {deg} connections")` | mid (write path) | Y |
| 5 | 293 | `page_lines.append(f"- {ulabel} -> {rel} -> {vlabel} [{conf}]")` | mid (write path) | Y |
| 6 | 307 | `page_lines.append(f"- {ulabel} -> {rel} -> {vlabel} (-> [[{other_slug}]])")` | mid (write path) | Y |
| 7 | 366 | `concepts[node_label].append(filename)` | mid (write path) | Y |
| 8 | 496 | `nlabel = data.get("label", nid)` | source (변수 지정) | Y (source) |
| 9 | 499 | `page_lines.append(f"- **{nlabel}** ({src_file}) -- {deg} connections")` | mid (write path) | Y |
| 10 | 522 | `page_lines.append(f"- {ulabel} -> {rel} -> {vlabel} [{conf}]")` | mid (write path) | Y |
| 11 | 535 | `page_lines.append(f"- {ulabel} -> {rel} -> {vlabel} (-> [[{other_slug}]])")` | mid (write path) | Y |

## 요약
- 총 label 사용 지점: 11 (Y 권장 지점만)
- _safe_label 이미 적용된 곳: 1
- 적용 대기 지점: 11
