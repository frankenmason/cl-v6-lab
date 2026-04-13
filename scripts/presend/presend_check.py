#!/usr/bin/env python3
"""
presend_check.py — S64 Mason 지시 구현 (option C)

목적: CL 응답 초안을 송출 전 정량 검증, E-7/E-8/E-9 재발 억제

검사 항목:
- V1: 3요소 존재 (INTENT/Selector/Status) — CLAUDE.md 04조
- V2: 추론동사 + TYPE-1 공존 (flag only, fresh LLM pass 필요 신호)
- V3: 수치 등장 시 근거 언급 흔적
- V5: 자의 선언 감지 (약한 필터)

Fast-Path 예외:
- 응답 < 150자 단답
- user 입력이 승인/확인/단답이면 3요소 생략 허용 (사전 메타로 전달 필요)

출력:
- stdout JSON
- exit 0 = PASS
- exit 1 = FLAG (경고, 수정 권장)
- exit 2 = REWRITE (3요소 누락, 재작성 요구)

Usage:
    echo "응답 초안" | python3 presend_check.py [--fastpath]
    python3 presend_check.py --file draft.txt
"""
import sys
import re
import json
import argparse

INTENT_BLOCK = re.compile(r"(^|\n)INTENT:")
SELECTOR_BLOCK = re.compile(r"\[Selector\]|\(Selector\)|Selector:")
STATUS_CONF = re.compile(r"(^|\n)CONFIDENCE:")
STATUS_ACT = re.compile(r"(^|\n)ACTION:")
STATUS_USES = re.compile(r"(^|\n)USES:")
STATUS_EVID = re.compile(r"(^|\n)EVIDENCE:")

INFERENCE_VERBS = re.compile(r"(따라서|이므로|즉\s|결국|그래서|so,|therefore)")
TYPE1_LABEL = re.compile(r"TYPE-?1")
NUMBER_PATTERN = re.compile(r"\d+(?:\.\d+)?%|\d+/\d+|\d+건|\d+회|\$\d+")
SOURCE_QUOTE = re.compile(r"['\"『「][^'\"』」\n]{3,}['\"』」]|원문|raw|실측|확인 결과|출력")
SELF_DECLARATION = re.compile(r"(최소화|재정의|재구성|태도.*재정립|정리할게요|정리하겠음)")


def check(text, fastpath=False):
    result = {
        "length": len(text),
        "fastpath": fastpath,
        "checks": {},
        "flags": [],
        "verdict": "PASS",
        "score": 0,
    }

    # Fast-Path 예외
    if fastpath or len(text) < 150:
        result["verdict"] = "PASS"
        result["note"] = "fast-path or short response — 3-element check skipped"
        return result

    # V1: 3요소 존재
    has_intent = bool(INTENT_BLOCK.search(text))
    has_selector = bool(SELECTOR_BLOCK.search(text))
    has_status = (
        bool(STATUS_CONF.search(text))
        and bool(STATUS_ACT.search(text))
        and bool(STATUS_USES.search(text))
    )
    result["checks"]["v1_intent"] = has_intent
    result["checks"]["v1_selector"] = has_selector
    result["checks"]["v1_status"] = has_status

    if not (has_intent and has_status):
        result["verdict"] = "REWRITE"
        if not has_intent:
            result["flags"].append("V1: INTENT 블록 없음")
        if not has_status:
            result["flags"].append("V1: Status Report(CONFIDENCE/ACTION/USES) 불완전")
        if not has_selector:
            result["flags"].append("V1: Selector 없음 (Interface Mode 전용, Execution에서는 허용)")

    # V2: 추론동사 + TYPE-1 공존 (flag)
    has_inference = bool(INFERENCE_VERBS.search(text))
    has_type1 = bool(TYPE1_LABEL.search(text))
    result["checks"]["v2_inference_type1"] = has_inference and has_type1
    if has_inference and has_type1:
        result["flags"].append(
            "V2: 추론동사 + TYPE-1 공존 — fresh LLM self-check 필요"
        )
        if result["verdict"] == "PASS":
            result["verdict"] = "FLAG"

    # V3: 수치 등장 시 근거 흔적
    has_numbers = bool(NUMBER_PATTERN.search(text))
    has_source = bool(SOURCE_QUOTE.search(text))
    result["checks"]["v3_numbers"] = has_numbers
    result["checks"]["v3_source"] = has_source
    if has_numbers and not has_source:
        result["flags"].append("V3: 수치 등장, 근거 원문 인용 흔적 없음")
        if result["verdict"] == "PASS":
            result["verdict"] = "FLAG"

    # V5: 자의 선언
    self_decl = SELF_DECLARATION.search(text)
    result["checks"]["v5_self_declaration"] = bool(self_decl)
    if self_decl:
        result["flags"].append(
            f"V5: 자의 선언 키워드 감지: '{self_decl.group(0)}' — Mason 지시 기반 여부 확인 필요"
        )
        if result["verdict"] == "PASS":
            result["verdict"] = "FLAG"

    # Score (0~100)
    checks_passed = sum(1 for v in result["checks"].values() if v)
    total = len(result["checks"])
    result["score"] = round(100 * checks_passed / total) if total else 0

    return result


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--file", help="파일 경로")
    ap.add_argument("--fastpath", action="store_true", help="단답 승인 턴 예외 모드")
    args = ap.parse_args()

    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            text = f.read()
    else:
        text = sys.stdin.read()

    result = check(text, fastpath=args.fastpath)
    print(json.dumps(result, ensure_ascii=False, indent=2))

    if result["verdict"] == "REWRITE":
        sys.exit(2)
    if result["verdict"] == "FLAG":
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
