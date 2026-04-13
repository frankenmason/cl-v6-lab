#!/usr/bin/env python3
"""Inventory-based error rate (Mason v3 standard).

Counts all I-* entries in discussion log / wiki as raw errors,
regardless of whether externally detected or self-reported.

Usage: inventory-rate.py <discussion_log_md> <total_turns>
"""
import re, sys

if len(sys.argv) < 3:
    print("Usage: inventory-rate.py <log.md> <total_turns>"); sys.exit(1)

path = sys.argv[1]
total = int(sys.argv[2])
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

inv_matches = re.findall(r'^\| I-\d+', content, re.MULTILINE)
n = len(inv_matches)
rate = 100 * n / total if total else 0
print(f"inventory entries: {n}")
print(f"total turns: {total}")
print(f"error rate (Mason v3): {rate:.1f}%")
