#!/usr/bin/env python3
"""Deterministic file-set and SHA-256 comparison for EXP-18.

Inputs: canonical Hugging Face manifest, Pirate Face manifest, swarm-only manifest.
Output: JSON verdict object. Comparison is exact string equality of SHA-256 digests
and exact equality of relative path sets - no tolerance, no fuzzy matching.
"""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone


def load(path: str) -> dict:
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def index(manifest: dict) -> dict:
    return {entry["path"]: entry for entry in manifest["files"]}


def compare(reference: dict, candidate: dict) -> dict:
    ref, cand = index(reference), index(candidate)
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
        "reference_file_count": len(ref_paths),
        "candidate_file_count": len(cand_paths),
        "file_set_identical": ref_paths == cand_paths,
        "missing_in_candidate": sorted(ref_paths - cand_paths),
        "additional_in_candidate": sorted(cand_paths - ref_paths),
        "files_compared": len(ref_paths & cand_paths),
        "sha256_matched": len(matched),
        "sha256_mismatched": mismatched,
        "size_mismatched_paths": size_mismatch,
        "identical_artifact": (
            ref_paths == cand_paths
            and not mismatched
            and len(matched) == len(ref_paths)
            and len(ref_paths) > 0
        ),
        "reference_total_bytes": reference["total_bytes"],
        "candidate_total_bytes": candidate["total_bytes"],
        "zero_byte_files_in_candidate": candidate.get("zero_byte_files", []),
    }


def main() -> int:
    if len(sys.argv) != 5:
        sys.exit("usage: compare.py <canonical.json> <pf_normal.json> <swarm_only.json> <out.json>")
    canonical, pf_normal, swarm_only = (load(p) for p in sys.argv[1:4])
    result = {
        "generated_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "method": "exact path-set equality + exact sha256 equality per file",
        "pirateface_normal_vs_canonical": compare(canonical, pf_normal),
        "pirateface_swarm_only_vs_canonical": compare(canonical, swarm_only),
    }
    result["integrity_verified_normal"] = result["pirateface_normal_vs_canonical"]["identical_artifact"]
    result["integrity_verified_swarm_only"] = result["pirateface_swarm_only_vs_canonical"]["identical_artifact"]
    with open(sys.argv[4], "w", encoding="utf-8") as fh:
        json.dump(result, fh, indent=2, sort_keys=True)
        fh.write("\n")
    for label, key in (("Pirate Face (normal)", "pirateface_normal_vs_canonical"),
                       ("Pirate Face (swarm only)", "pirateface_swarm_only_vs_canonical")):
        block = result[key]
        print(
            f"{label}: identical={block['identical_artifact']} "
            f"files={block['files_compared']}/{block['reference_file_count']} "
            f"matched={block['sha256_matched']} mismatched={len(block['sha256_mismatched'])} "
            f"file_set_identical={block['file_set_identical']} "
            f"missing={len(block['missing_in_candidate'])} additional={len(block['additional_in_candidate'])}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
