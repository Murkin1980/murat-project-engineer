#!/usr/bin/env python3
"""Deterministic file-set and SHA-256 comparison for EXP-18.

Comparison rules (fixed before the run, no tolerance):
  * paths are compared after stripping a single common top-level directory that
    the BitTorrent client creates for the torrent payload, and after excluding
    `.torrent` metainfo files (which are evidence, not payload);
  * every remaining path must exist on both sides;
  * SHA-256 digests and byte sizes must be exactly equal - a mismatch is a
    failure, never a warning.

Usage: compare.py <canonical.json> <pf_normal.json> <swarm_only.json> <out.json>
"""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone

META_SUFFIX = ".torrent"


def load(path: str) -> dict:
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def normalized_index(manifest: dict) -> tuple[dict, dict]:
    """Return (index_by_normalized_path, normalization_info)."""
    raw_paths = [entry["path"] for entry in manifest["files"]]
    excluded = sorted(p for p in raw_paths if p.endswith(META_SUFFIX))
    payload = [p for p in raw_paths if not p.endswith(META_SUFFIX)]
    tops = {p.split("/", 1)[0] for p in payload}
    strip = None
    if len(tops) == 1 and any("/" in p for p in payload):
        strip = next(iter(tops))
    index = {}
    for entry in manifest["files"]:
        path = entry["path"]
        if path.endswith(META_SUFFIX):
            continue
        if strip and path.startswith(strip + "/"):
            path = path[len(strip) + 1 :]
        index[path] = entry
    info = {
        "excluded_metainfo_files": excluded,
        "stripped_top_level_directory": strip,
        "payload_file_count": len(index),
    }
    return index, info


def compare(reference: dict, candidate: dict) -> dict:
    ref, ref_info = normalized_index(reference)
    cand, cand_info = normalized_index(candidate)
    ref_paths, cand_paths = set(ref), set(cand)
    matched, mismatched, size_mismatch = [], [], []
    for path in sorted(ref_paths & cand_paths):
        if ref[path]["sha256"] == cand[path]["sha256"]:
            matched.append(path)
        else:
            mismatched.append(
                {
                    "path": path,
                    "reference_sha256": ref[path]["sha256"],
                    "candidate_sha256": cand[path]["sha256"],
                    "reference_size": ref[path]["size"],
                    "candidate_size": cand[path]["size"],
                }
            )
        if ref[path]["size"] != cand[path]["size"]:
            size_mismatch.append(path)
    return {
        "normalization": {"reference": ref_info, "candidate": cand_info},
        "reference_file_count": len(ref_paths),
        "candidate_file_count": len(cand_paths),
        "file_set_identical": ref_paths == cand_paths,
        "missing_in_candidate": sorted(ref_paths - cand_paths),
        "additional_in_candidate": sorted(cand_paths - ref_paths),
        "files_compared": len(ref_paths & cand_paths),
        "sha256_matched": len(matched),
        "sha256_mismatched": mismatched,
        "size_mismatched_paths": size_mismatch,
        "all_shared_files_hash_identical": (
            len(ref_paths & cand_paths) == len(ref_paths) and not mismatched and len(ref_paths) > 0
        ),
        "identical_artifact": ref_paths == cand_paths and not mismatched and len(ref_paths) > 0,
        "reference_total_bytes": reference["total_bytes"],
        "candidate_total_bytes": candidate["total_bytes"],
        "zero_byte_files_in_candidate": candidate.get("zero_byte_files", []),
        "per_file_hashes": {
            path: {"reference": ref[path]["sha256"], "candidate": cand[path]["sha256"]}
            for path in sorted(ref_paths & cand_paths)
        },
    }


def main() -> int:
    if len(sys.argv) != 5:
        sys.exit("usage: compare.py <canonical.json> <pf_normal.json> <swarm_only.json> <out.json>")
    canonical, pf_normal, swarm_only = (load(p) for p in sys.argv[1:4])
    result = {
        "generated_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "method": (
            "exact normalized path-set equality + exact sha256 equality per file; "
            "torrent root directory stripped; .torrent metainfo excluded from payload comparison"
        ),
        "pirateface_normal_vs_canonical": compare(canonical, pf_normal),
        "pirateface_swarm_only_vs_canonical": compare(canonical, swarm_only),
    }
    result["all_shared_files_hash_identical_normal"] = result["pirateface_normal_vs_canonical"][
        "all_shared_files_hash_identical"
    ]
    result["all_shared_files_hash_identical_swarm_only"] = result["pirateface_swarm_only_vs_canonical"][
        "all_shared_files_hash_identical"
    ]
    with open(sys.argv[4], "w", encoding="utf-8") as fh:
        json.dump(result, fh, indent=2, sort_keys=True)
        fh.write("\n")
    for label, key in (
        ("Pirate Face (normal)", "pirateface_normal_vs_canonical"),
        ("Pirate Face (swarm only)", "pirateface_swarm_only_vs_canonical"),
    ):
        block = result[key]
        print(
            f"{label}: shared_files_identical={block['all_shared_files_hash_identical']} "
            f"file_set_identical={block['file_set_identical']} "
            f"compared={block['files_compared']} matched={block['sha256_matched']} "
            f"mismatched={len(block['sha256_mismatched'])} "
            f"missing={block['missing_in_candidate']} additional={block['additional_in_candidate']}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
