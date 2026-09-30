#!/usr/bin/env python3
"""Assemble the EXP-18 run summary from the recorded evidence files.

Aggregation only: every value is read from a file written by the harness, and
nothing is inferred or filled in. Missing evidence stays null.

Usage: summarize.py <evidence_dir> <work_dir> <repo>
"""
from __future__ import annotations

import json
import os
import re
import sys
from datetime import datetime, timezone

PRIMARY_ARTIFACT = "model.safetensors"


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


def hashes(manifest) -> dict:
    if not manifest:
        return {}
    return {entry["path"]: entry["sha256"] for entry in manifest.get("files", [])}


def find_hash(manifest_hashes: dict, suffix: str):
    for path, digest in manifest_hashes.items():
        if path.endswith(suffix):
            return {"path": path, "sha256": digest}
    return None


def main() -> int:
    evid, work, repo = sys.argv[1], sys.argv[2], sys.argv[3]
    j = lambda name: read_json(os.path.join(evid, name))  # noqa: E731
    t = lambda name: read_text(os.path.join(evid, name))  # noqa: E731

    hf_meta = j("02_hf_model_metadata.json") or {}
    license_ev = j("04_hf_license_evidence.json") or {}
    canonical = j("06_canonical_manifest.json") or {}
    crosscheck = j("06b_hash_crosscheck.json") or {}
    pf_manifest = j("08_pf_normal_manifest.json") or {}
    swarm_manifest = j("10_swarm_only_manifest.json") or {}
    dht_manifest = j("11_dht_only_manifest.json") or {}
    comparison = j("13_comparison.json") or {}
    dht_comparison = j("13b_dht_only_comparison.json") or {}
    identity = j("14_torrent_identity.json") or {}
    tracker = j("07b_tracker_announce_before.json") or {}
    pf_html = t("07_pirateface_page.html")

    canonical_hashes = hashes(canonical)
    default_artifact = find_hash(canonical_hashes, PRIMARY_ARTIFACT)

    def run_block(tag: str, manifest: dict) -> dict:
        peers = j(f"07_{tag}_peers.json") or {}
        return {
            "manifest_file_count": manifest.get("file_count"),
            "manifest_total_bytes": manifest.get("total_bytes"),
            "zero_byte_files": manifest.get("zero_byte_files"),
            "exit_code": read_text(os.path.join(work, f"{tag}_rc")).strip(),
            "wall_seconds": read_text(os.path.join(work, f"{tag}_seconds")).strip(),
            "primary_artifact_sha256": find_hash(hashes(manifest), PRIMARY_ARTIFACT),
            "peer_sample": {
                "distinct_peer_networks": peers.get("distinct_peer_network_count"),
                "max_seeders": peers.get("max_seeders"),
                "max_connections": peers.get("max_connections"),
                "max_download_speed_bps": peers.get("max_download_speed_bps"),
                "sample_count": peers.get("sample_count"),
                "info_hash_reported_by_client": peers.get("info_hash"),
            },
            "webseed_mentions_in_client_log": (
                (lambda text: len(re.findall(r"webseed", text, re.I)))(t(f"07_{tag}_aria2c.log"))
            ),
        }

    summary = {
        "generated_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "harness": "experiments/exp-18-pirateface-model-resilience/harness/run_exp18.sh",
        "github_run_id": (re.search(r"github_run_id=(\S+)", t("01_environment.txt")) or [None, None])[1],
        "model_repo": repo,
        "hf_revision_pinned": read_text(os.path.join(work, "REV")).strip(),
        "hf_revision_reported_by_api": hf_meta.get("sha"),
        "hf_license_evidence": license_ev.get("license"),
        "hf_tags_license": [tag for tag in (hf_meta.get("tags") or []) if tag.startswith("license:")],
        "canonical": {
            "file_count": canonical.get("file_count"),
            "total_bytes": canonical.get("total_bytes"),
            "primary_artifact": default_artifact,
        },
        "hash_crosscheck": crosscheck.get("figures"),
        "hash_crosscheck_detail": {
            "computed_manifest_matches_hf_recorded_lfs": crosscheck.get("computed_manifest_matches_hf_recorded_lfs"),
            "pirateface_page_hashes_matching_canonical_bytes": crosscheck.get(
                "pirateface_page_hashes_matching_canonical_bytes"
            ),
            "files_whose_hash_is_published_by_pirateface": crosscheck.get(
                "files_whose_hash_is_published_by_pirateface"
            ),
        },
        "pirateface_reference": {
            "page_url": f"https://pirateface.co/{repo}",
            "page_http_status_line": t("07_pirateface_page.html")[:0] or None,
            "magnet_advertised": read_text(os.path.join(work, "magnet_page.txt")).strip(),
            "magnet_swarm_only": read_text(os.path.join(work, "magnet_swarm_only.txt")).strip(),
            "infohash_from_magnet": read_text(os.path.join(work, "infohash.txt")).strip(),
            "magnet_has_web_seed_parameter": "ws=" in read_text(os.path.join(work, "magnet_page.txt")),
            "sha256_values_published_on_page": len(crosscheck.get("pirateface_page_sha256_values_found") or []),
            "checksum_badge_text": sorted(set(re.findall(r">\s*([0-9]+ checksums)\s*<", pf_html))) or None,
        },
        "tracker_observation_before_retrieval": tracker.get("announce"),
        "runs": {
            "D_pirateface_normal": run_block("D_pf_normal", pf_manifest),
            "E_swarm_only_hf_blocked": run_block("E_swarm_only", swarm_manifest),
            "E2_dht_only_tracker_blocked": run_block("E2_dht_only", dht_manifest),
        },
        "torrent_metainfo": {
            "info_hash": (identity.get("normal_retrieval_metainfo") or {}).get("info_hash_sha1"),
            "file_count": (identity.get("normal_retrieval_metainfo") or {}).get("file_count"),
            "total_length": (identity.get("normal_retrieval_metainfo") or {}).get("total_length"),
            "piece_length": (identity.get("normal_retrieval_metainfo") or {}).get("piece_length"),
            "piece_count": (identity.get("normal_retrieval_metainfo") or {}).get("piece_count"),
            "announce_list": (identity.get("normal_retrieval_metainfo") or {}).get("announce_list"),
            "url_list_web_seeds": (identity.get("normal_retrieval_metainfo") or {}).get("url_list_web_seeds"),
            "has_web_seed_in_metainfo": (identity.get("normal_retrieval_metainfo") or {}).get("has_web_seed_in_metainfo"),
            "creator": (identity.get("normal_retrieval_metainfo") or {}).get("creator"),
            "creation_date_utc": (identity.get("normal_retrieval_metainfo") or {}).get("creation_date_utc"),
            "same_piece_table_and_file_list_across_runs": identity.get("same_piece_table_and_file_list"),
            "same_info_hash_across_runs": identity.get("same_info_hash"),
        },
        "comparison_vs_canonical": {
            "pirateface_normal": {
                "file_set_identical": (comparison.get("pirateface_normal_vs_canonical") or {}).get("file_set_identical"),
                "shared_files_hash_identical": (
                    comparison.get("pirateface_normal_vs_canonical") or {}
                ).get("all_shared_files_hash_identical"),
                "files_compared": (comparison.get("pirateface_normal_vs_canonical") or {}).get("files_compared"),
                "sha256_matched": (comparison.get("pirateface_normal_vs_canonical") or {}).get("sha256_matched"),
                "sha256_mismatched": len(
                    (comparison.get("pirateface_normal_vs_canonical") or {}).get("sha256_mismatched") or []
                ),
                "missing_in_candidate": (comparison.get("pirateface_normal_vs_canonical") or {}).get(
                    "missing_in_candidate"
                ),
                "additional_in_candidate": (comparison.get("pirateface_normal_vs_canonical") or {}).get(
                    "additional_in_candidate"
                ),
            },
            "pirateface_swarm_only": {
                "file_set_identical": (comparison.get("pirateface_swarm_only_vs_canonical") or {}).get(
                    "file_set_identical"
                ),
                "shared_files_hash_identical": (
                    comparison.get("pirateface_swarm_only_vs_canonical") or {}
                ).get("all_shared_files_hash_identical"),
                "files_compared": (comparison.get("pirateface_swarm_only_vs_canonical") or {}).get("files_compared"),
                "sha256_matched": (comparison.get("pirateface_swarm_only_vs_canonical") or {}).get("sha256_matched"),
                "sha256_mismatched": len(
                    (comparison.get("pirateface_swarm_only_vs_canonical") or {}).get("sha256_mismatched") or []
                ),
                "missing_in_candidate": (comparison.get("pirateface_swarm_only_vs_canonical") or {}).get(
                    "missing_in_candidate"
                ),
                "additional_in_candidate": (comparison.get("pirateface_swarm_only_vs_canonical") or {}).get(
                    "additional_in_candidate"
                ),
            },
        },
        "dht_only_extra_check": {
            "manifest_present": bool(dht_manifest),
            "file_set_identical": (dht_comparison.get("pirateface_swarm_only_vs_canonical") or {}).get(
                "file_set_identical"
            ),
            "shared_files_hash_identical": (dht_comparison.get("pirateface_swarm_only_vs_canonical") or {}).get(
                "all_shared_files_hash_identical"
            ),
            "exit_code": read_text(os.path.join(work, "E2_dht_only_rc")).strip(),
            "wall_seconds": read_text(os.path.join(work, "E2_dht_only_seconds")).strip(),
        },
        "piece_reverification_log_tail": t("12_piece_reverify.log").strip().splitlines()[-6:],
        "source_loss_proof": t("09_source_loss_proof.txt").strip(),
    }
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
