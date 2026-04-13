#!/usr/bin/env python3
"""Count [CORRECTION] 직전 턴 BARE hook injections (corrected v2)."""
import json
import sys

def count(jsonl_path):
    asst_turns = 0
    user_turns = 0
    correction_by_type = {}
    with open(jsonl_path, 'r', encoding='utf-8') as f:
        for line in f:
            try: rec = json.loads(line)
            except: continue
            t = rec.get('type', '')
            if t == 'assistant':
                asst_turns += 1
            elif t == 'user':
                user_turns += 1
            if '[CORRECTION] 직전 턴 BARE' in json.dumps(rec, ensure_ascii=False):
                correction_by_type[t] = correction_by_type.get(t, 0) + 1
    return asst_turns, user_turns, correction_by_type

if __name__ == '__main__':
    p = sys.argv[1] if len(sys.argv) > 1 else None
    if not p:
        print("Usage: count-corrections.py <jsonl>"); sys.exit(1)
    a, u, c = count(p)
    total = sum(c.values())
    unique_user = c.get('user', 0)
    print(f"assistant turns: {a}")
    print(f"user turns: {u}")
    print(f"CORRECTION by record type: {c}")
    print(f"unique user-turn CORRECTION injections: {unique_user}")
    print(f"rate (vs user turns): {100*unique_user/u if u else 0:.2f}%")
    print(f"rate (vs assistant turns): {100*unique_user/a if a else 0:.2f}%")
