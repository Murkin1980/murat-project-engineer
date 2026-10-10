#!/usr/bin/env python3
"""Field-level diff between two JSON contract snapshots (minimal-diff proof)."""
import json, sys

def walk(a, b, path, out):
    if isinstance(a, dict) and isinstance(b, dict):
        for k in sorted(set(a) | set(b)):
            walk(a.get(k, "<absent>"), b.get(k, "<absent>"), f"{path}.{k}" if path else k, out)
    elif isinstance(a, list) and isinstance(b, list) and len(a) == len(b) and all(isinstance(x, dict) for x in a + b):
        for i, (x, y) in enumerate(zip(a, b)):
            walk(x, y, f"{path}[{i}]", out)
    elif a != b:
        out.append((path, a, b))

if __name__ == "__main__":
    old, new = json.load(open(sys.argv[1])), json.load(open(sys.argv[2]))
    changes = []
    walk(old, new, "", changes)
    for p, a, b in changes:
        print(f"CHANGED {p}: {json.dumps(a, ensure_ascii=False)} -> {json.dumps(b, ensure_ascii=False)}")
    print(f"TOTAL_FIELD_CHANGES {len(changes)}")
