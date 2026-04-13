#!/usr/bin/env python3
"""Count [CORRECTION] occurrences in a session jsonl."""
import json
import sys
from pathlib import Path

def count(jsonl_path):
    corrections = 0
    turns = 0
    with open(jsonl_path, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                rec = json.loads(line)
            except:
                continue
            msg = rec.get('message', {})
            content = msg.get('content')
            if isinstance(content, str):
                text = content
            elif isinstance(content, list):
                text = '\n'.join(p.get('text', '') if isinstance(p, dict) else str(p) for p in content)
            else:
                text = ''
            if (rec.get('type') or rec.get('role')) == 'assistant':
                turns += 1
            if 'CORRECTION' in text and 'BARE' in text:
                corrections += 1
    return corrections, turns

if __name__ == '__main__':
    p = sys.argv[1] if len(sys.argv) > 1 else None
    if not p:
        print("Usage: count-corrections.py <jsonl>")
        sys.exit(1)
    c, t = count(p)
    print(f"CORRECTION: {c}")
    print(f"assistant turns: {t}")
    print(f"rate: {100*c/t if t else 0:.2f}%")
