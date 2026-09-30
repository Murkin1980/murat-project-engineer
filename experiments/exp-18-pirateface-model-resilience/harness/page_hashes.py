#!/usr/bin/env python3
"""Cross-check the three independent hash statements in EXP-18.

1. Hugging Face's own recorded LFS SHA-256 (`lfs.oid` in the tree API) versus
   the SHA-256 we computed from the bytes we downloaded - proves our canonical
   manifest describes the revision HF itself recorded.
2. The SHA-256 values Pirate Face publishes on the model page versus the
   canonical manifest - shows whether its checksum list refers to the same
   bytes.

Usage: page_hashes.py <tree.json> <canonical_manifest.json> <page.html> <out.json>
"""
from __future__ import annotations

import json
import re
import sys
from datetime import datetime, timezone

HEX64 = re.compile(r"\b[0-9a-f]{64}\b")


def main() -> int:
    tree_path, manifest_path, page_path, out_path = sys.argv[1:5]
    with open(tree_path, encoding="utf-8") as fh:
        tree = json.load(fh)
    with open(manifest_path, encoding="utf-8") as fh:
        manifest = json.load(fh)
    with open(page_path, encoding="utf-8", errors="replace") as fh:
        page = fh.read()

    hf_recorded = {
        entry["path"]: entry["lfs"]["oid"]
        for entry in tree
        if entry.get("type") == "file" and isinstance(entry.get("lfs"), dict) and entry["lfs"].get("oid")
    }
    computed = {entry["path"]: entry["sha256"] for entry in manifest["files"]}

    hf_matches, hf_mismatches = [], []
    for path, oid in sorted(hf_recorded.items()):
        if computed.get(path) == oid:
            hf_matches.append(path)
        else:
            hf_mismatches.append({"path": path, "hf_recorded": oid, "computed": computed.get(path)})

    published = sorted(set(HEX64.findall(page)))
    canonical_values = set(computed.values())
    matched_hashes = sorted(set(published) & canonical_values)
    files_confirmed_by_page = {
        path: digest for path, digest in sorted(computed.items()) if digest in matched_hashes
    }

    result = {
        "generated_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "hf_recorded_lfs_sha256_count": len(hf_recorded),
        "computed_manifest_matches_hf_recorded_lfs": len(hf_recorded) == len(hf_matches) and bool(hf_recorded),
        "hf_recorded_lfs_matched": hf_matches,
        "hf_recorded_lfs_mismatched": hf_mismatches,
        "pirateface_page_sha256_values_found": published,
        "pirateface_page_sha256_count": len(published),
        "pirateface_page_hashes_matching_canonical_bytes": matched_hashes,
        "files_whose_hash_is_published_by_pirateface": files_confirmed_by_page,
        "figures": {
            "hf_lfs_files": len(hf_recorded),
            "pirateface_page_hashes": len(published),
            "pirateface_page_hashes_confirmed_against_canonical": len(matched_hashes),
        },
    }
    with open(out_path, "w", encoding="utf-8") as fh:
        json.dump(result, fh, indent=2, sort_keys=True)
        fh.write("\n")

    tree_entries = [
        e for e in tree if e.get("type") == "file" and not str(e.get("path", "")).endswith((".onnx", ".xml", ".bin", ".h5", ".ot"))
    ]
    print(
        "hash cross-check: "
        f"hf_recorded_lfs={len(hf_recorded)} matched={len(hf_matches)} mismatched={len(hf_mismatches)}; "
        f"pirateface_page_hashes={len(published)} "
        f"confirmed_against_canonical={len(matched_hashes)} "
        f"files_confirmed={len(files_confirmed_by_page)}; "
        f"hf_tree_files(excl. exported formats)={len(tree_entries)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
