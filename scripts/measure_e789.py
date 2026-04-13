#!/usr/bin/env python3
"""
measure_e789.py — E-7/8/9 prevalence 실측 (v2 external validation)

Design (Gemini 2.5 Pro + codex:codex-rescue 검증 반영):
- baseline 비교 제거 → 절대 prevalence + 95% CI
- 층화 무작위 샘플링 (세션당 max N턴 → 과대표 방지)
- E-7/8/9 독립 측정 (집계 금지)
- 세션 단위 bootstrap 1000회 (턴 내 클러스터 고려)
- Fast-Path 예외 (user 단답 제외)
- 사전 등록 결정 규칙 (threshold 파라미터화)
- 현재 세션 자동 제외 (측정 오염 방지)

Usage:
    python3 measure_e789.py --run 1 --seed 42
    python3 measure_e789.py --run 2 --seed 43
"""
import json
import re
import random
import os
from pathlib import Path
from collections import defaultdict
import argparse

SESSIONS_DIR = Path("/home/ubuntu/.claude/projects/-home-ubuntu--cokacdir-workspace")
SIZE_MIN = 5 * 1024
TURNS_MIN = 10
CURRENT_SESSION_MARK = "5d893ed4-9652-4bca-9ecf-482e6bf49936"

INFERENCE_VERBS = re.compile(r"(따라서|이므로|즉\s|결국|그래서)")
TYPE1_LABEL = re.compile(r"TYPE-?1")
INTENT_BLOCK = re.compile(r"(^|\n)INTENT:|(^|\n)\s*WHAT:")
SELECTOR_BLOCK = re.compile(r"\[Selector\]|\(Selector\)")
STATUS_CONF = re.compile(r"(^|\n)CONFIDENCE:")
STATUS_ACT = re.compile(r"(^|\n)ACTION:")
STATUS_USES = re.compile(r"(^|\n)USES:")
FAST_PATH_USER = re.compile(
    r"^\s*(1|2|3|ㅇ|o|ok|OK|@승인|@모두\s*승인|네|응|맞음|수용|동의함?|허용|yes|Yes|Y|y)\s*$"
)


def parse_text(content):
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = []
        for p in content:
            if isinstance(p, dict) and p.get("type") == "text":
                parts.append(p.get("text", ""))
        return "\n".join(parts)
    return ""


def is_fast_path(user_text):
    if not user_text:
        return True
    first_line = user_text.strip().split("\n", 1)[0].strip() if user_text.strip() else ""
    return bool(FAST_PATH_USER.match(first_line))


def detect_e7_e8(text):
    return bool(INFERENCE_VERBS.search(text)) and bool(TYPE1_LABEL.search(text))


def detect_e9(text):
    has_intent = bool(INTENT_BLOCK.search(text))
    has_selector = bool(SELECTOR_BLOCK.search(text))
    has_status = bool(STATUS_CONF.search(text)) and bool(STATUS_ACT.search(text)) and bool(STATUS_USES.search(text))
    return not (has_intent and has_selector and has_status)


def load_sessions(exclude_current=True):
    sessions = []
    for f in SESSIONS_DIR.glob("*.jsonl"):
        if exclude_current and CURRENT_SESSION_MARK in f.name:
            continue
        if f.stat().st_size < SIZE_MIN:
            continue
        recs = []
        try:
            with open(f, "r", encoding="utf-8") as fh:
                for line in fh:
                    try:
                        recs.append(json.loads(line))
                    except json.JSONDecodeError:
                        continue
        except Exception:
            continue
        asst_count = sum(1 for r in recs if (r.get("type") or r.get("role")) == "assistant")
        if asst_count < TURNS_MIN:
            continue
        sessions.append((f.name, recs))
    return sessions


def extract_pairs(recs):
    pairs = []
    last_user = None
    for r in recs:
        kind = r.get("type") or r.get("role")
        msg = r.get("message") or r
        content = msg.get("content") if isinstance(msg, dict) else None
        text = parse_text(content)
        if kind == "user":
            last_user = text
        elif kind == "assistant" and last_user is not None:
            if not is_fast_path(last_user):
                pairs.append({"user": last_user, "assistant": text})
            last_user = None
    return pairs


def measure(sessions, max_per_session, seed):
    random.seed(seed)
    results = []
    for sname, recs in sessions:
        pairs = extract_pairs(recs)
        if max_per_session and len(pairs) > max_per_session:
            pairs = random.sample(pairs, max_per_session)
        for p in pairs:
            results.append({
                "session": sname,
                "e78": detect_e7_e8(p["assistant"]),
                "e9": detect_e9(p["assistant"]),
            })
    return results


def bootstrap_ci(by_session, metric, n_boot, seed):
    random.seed(seed)
    sessions = list(by_session.keys())
    if not sessions:
        return 0.0, 0.0, 0.0
    means = []
    for _ in range(n_boot):
        sample = random.choices(sessions, k=len(sessions))
        labels = []
        for s in sample:
            labels.extend([x[metric] for x in by_session[s]])
        if labels:
            means.append(sum(labels) / len(labels))
    means.sort()
    n = len(means)
    lo = means[int(n * 0.025)]
    hi = means[int(n * 0.975)]
    mid = means[n // 2]
    return mid, lo, hi


def decide(lo, hi, threshold_pct):
    t = threshold_pct / 100.0
    if lo > t:
        return "IMPLEMENT"
    if hi < t:
        return "SKIP"
    return "NEED_MORE_DATA"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", type=int, default=1)
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--max-per-session", type=int, default=50)
    ap.add_argument("--n-bootstrap", type=int, default=1000)
    ap.add_argument("--threshold", type=float, default=1.0)
    ap.add_argument("--output", default=None)
    args = ap.parse_args()

    effective_seed = args.seed + args.run
    out_path = args.output or f"/tmp/measure_e789_run{args.run}.json"

    print(f"[Run {args.run}] seed={effective_seed}")
    sessions = load_sessions(exclude_current=True)
    print(f"  eligible sessions: {len(sessions)}")

    labels = measure(sessions, args.max_per_session, effective_seed)
    total = len(labels)
    print(f"  measured turns (Fast-Path excluded): {total}")

    n_e78 = sum(1 for x in labels if x["e78"])
    n_e9 = sum(1 for x in labels if x["e9"])

    by_session = defaultdict(list)
    for x in labels:
        by_session[x["session"]].append(x)

    e78_pt, e78_lo, e78_hi = bootstrap_ci(by_session, "e78", args.n_bootstrap, effective_seed + 1000)
    e9_pt, e9_lo, e9_hi = bootstrap_ci(by_session, "e9", args.n_bootstrap, effective_seed + 2000)

    result = {
        "run": args.run,
        "seed": effective_seed,
        "threshold_pct": args.threshold,
        "config": {
            "size_min_bytes": SIZE_MIN,
            "turns_min": TURNS_MIN,
            "max_per_session": args.max_per_session,
            "n_bootstrap": args.n_bootstrap,
            "current_session_excluded": CURRENT_SESSION_MARK,
        },
        "n_sessions": len(sessions),
        "n_turns": total,
        "e7_e8": {
            "count": n_e78,
            "raw_rate_pct": round(100 * n_e78 / total, 4) if total else 0,
            "bootstrap_median_pct": round(100 * e78_pt, 4),
            "ci_95_lo_pct": round(100 * e78_lo, 4),
            "ci_95_hi_pct": round(100 * e78_hi, 4),
            "decision": decide(e78_lo, e78_hi, args.threshold),
        },
        "e9": {
            "count": n_e9,
            "raw_rate_pct": round(100 * n_e9 / total, 4) if total else 0,
            "bootstrap_median_pct": round(100 * e9_pt, 4),
            "ci_95_lo_pct": round(100 * e9_lo, 4),
            "ci_95_hi_pct": round(100 * e9_hi, 4),
            "decision": decide(e9_lo, e9_hi, args.threshold),
        },
    }

    with open(out_path, "w") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    print(f"  → {out_path}")
    print(f"  E-7/8: {n_e78}/{total} = {result['e7_e8']['raw_rate_pct']}% "
          f"(CI {result['e7_e8']['ci_95_lo_pct']}-{result['e7_e8']['ci_95_hi_pct']}%) "
          f"→ {result['e7_e8']['decision']}")
    print(f"  E-9:   {n_e9}/{total} = {result['e9']['raw_rate_pct']}% "
          f"(CI {result['e9']['ci_95_lo_pct']}-{result['e9']['ci_95_hi_pct']}%) "
          f"→ {result['e9']['decision']}")


if __name__ == "__main__":
    main()
