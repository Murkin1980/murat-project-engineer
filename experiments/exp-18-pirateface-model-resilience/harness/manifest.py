#!/usr/bin/env python3
"""Build a deterministic manifest (sorted path, size, sha256) for a directory.

Used by the EXP-18 harness so the canonical Hugging Face artifact and the
Pirate Face artifact are described by exactly the same procedure.
"""
from __future__ import annotations

import hashlib
import json
import os
import sys
from datetime import datetime, timezone


def sha256_of(path: str, chunk: int = 1024 * 1024) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        while True:
            block = fh.read(chunk)
            if not block:
                break
            h.update(block)
    return h.hexdigest()


def build(root: str) -> dict:
    files = []
    for dirpath, _dirnames, filenames in os.walk(root):
        for name in filenames:
            full = os.path.join(dirpath, name)
            rel = os.path.relpath(full, root).replace(os.sep, "/")
            if rel.endswith(".aria2"):
                continue
            files.append(
                {
                    "path": rel,
                    "size": os.path.getsize(full),
                    "sha256": sha256_of(full),
                }
            )
    files.sort(key=lambda entry: entry["path"])
    total = sum(entry["size"] for entry in files)
    missing_sizes = [entry["path"] for entry in files if entry["size"] == 0]
    return {
        "root": os.path.basename(root.rstrip("/")),
        "generated_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "file_count": len(files),
        "total_bytes": total,
        "zero_byte_files": missing_sizes,
        "files": files,
    }


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit("usage: manifest.py <directory> <output.json>")
    manifest = build(sys.argv[1])
    with open(sys.argv[2], "w", encoding="utf-8") as fh:
        json.dump(manifest, fh, indent=2, sort_keys=True)
        fh.write("\n")
    print(
        f"manifest: {sys.argv[2]} files={manifest['file_count']} "
        f"bytes={manifest['total_bytes']} zero_byte={len(manifest['zero_byte_files'])}"
    )
