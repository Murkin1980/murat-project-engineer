#!/usr/bin/env python3
"""Assemble the EXP-18 run summary from the evidence files produced by run_exp18.sh.

Pure aggregation: every value is read from a recorded file, nothing is inferred.
"""
from __future__ import annotations

import json
import os
import re
import sys
from datetime import datetime, timezone


def read_json(path: str):
    try:
        with open(path, encoding="utf-8") as fh:
            return json.load(fh)
    except Exception:
        return None


def read_text(path: str) -> str:
    try:
        with open(path, encoding="utf-8", errors="replace") as fh:
            return fh.read()
    except Exception:
        return ""


def main() -> int:
    evid, work, repo = sys.argv[1], sys.argv[2], sys.argv[3]

    hf_meta = read_json(os.path.join(evid, "02_hf_model_metadata.json")) or {}
    license_ev = read_json(os.path.join(evid, "04_hf_license_evidence.json")) or {}
    canonical = read_json(os.path.join(evid, "06_canonical_manifest.json")) or {}
    pf_manifest = read_json(os.path.join(evid, "08_pf_normal_manifest.json")) or {}
    swarm_manifest = read_json(os.path.join(evid, "10_swarm_only_manifest.json")) or {}
    comparison = read_json(os.path.join(evid, "12_comparison.json")) or {}
    identity = read_json(os.path.join(evid, "13_torrent_identity.json")) or {}

    magnet_page = read_text(os.path.join(work, "magnet_page.txt")).strip()
    magnet_swarm = read_text(os.path.join(work, "magnet_swarm_only.txt")).strip()
    infohash = read_text(os.path.join(work, "infohash.txt")).strip()
    rev = read_text(os.path.join(work, "REV")).strip()
    pf_html = read_text(os.path.join(evid, "07_pirateface_page.html"))

    page_seeders = re.findall(r"\U0001F331\s*([0-9,]+)", pf_html)
    page_checksum_badge = re.findall(r"(\d+)\s+checksums", pf_html)
    summary = {
        "generated_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "harness": "experiments/exp-18-pirateface-model-resilience/harness/run_exp18.sh",
        "model_repo": repo,
        "hf_revision_pinned": rev,
        "hf_revision_reported_by_api": hf_meta.get("sha"),
        "hf_license_evidence": license_ev.get("license"),
        "hf_last_modified": hf_meta.get("lastModified"),
        "canonical_file_count": canonical.get("file_count"),
        "canonical_total_bytes": canonical.get("total_bytes"),
        "canonical_file_hashes": {
            entry["path"]: entry["sha256"] for entry in canonical.get("files", [])
        },
        "pirateface_page_url": f"https://pirateface.co/{repo}",
        "pirateface_magnet_advertised": magnet_page,
        "pirateface_magnet_swarm_only": magnet_swarm,
        "pirateface_infohash": infohash,
        "pirateface_page_seeders_observed": page_seeders,
        "pirateface_page_checksum_badges_observed": page_checksum_badge,
        "pirateface_normal_file_count": pf_manifest.get("file_count"),
        "pirateface_normal_total_bytes": pf_manifest.get("total_bytes"),
        "pirateface_normal_file_hashes": {
            entry["path"]: entry["sha256"] for entry in pf_manifest.get("files", [])
        },
        "swarm_only_file_count": swarm_manifest.get("file_count"),
        "swarm_only_total_bytes": swarm_manifest.get("total_bytes"),
        "swarm_only_file_hashes": {
            entry["path"]: entry["sha256"] for entry in swarm_manifest.get("files", [])
        },
        "pirateface_normal_exit_code": read_text(os.path.join(work, "D_pf_normal_rc")).strip(),
        "pirateface_normal_wall_seconds": read_text(os.path.join(work, "D_pf_normal_seconds")).strip(),
        "swarm_only_exit_code": read_text(os.path.join(work, "E_swarm_only_rc")).strip(),
        "swarm_only_wall_seconds": read_text(os.path.join(work, "E_swarm_only_seconds")).strip(),
        "comparison": comparison,
        "torrent_identity": {
            "same_piece_table_and_file_list": identity.get("same_piece_table_and_file_list"),
            "same_info_hash": identity.get("same_info_hash"),
            "info_hash_from_metainfo": (identity.get("normal_retrieval_metainfo") or {}).get("info_hash_sha1"),
            "has_url_list_in_metainfo": (identity.get("normal_retrieval_metainfo") or {}).get("has_url_list"),
            "piece_count": (identity.get("normal_retrieval_metainfo") or {}).get("piece_count"),
            "announce_list": (identity.get("normal_retrieval_metainfo") or {}).get("announce_list"),
        },
    }
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
