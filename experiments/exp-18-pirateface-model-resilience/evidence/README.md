# EXP-18 evidence layout

The harness writes its evidence into this directory with fixed file names, so a
later run overwrites an earlier one. Layout:

| Location | Run | Status |
| --- | --- | --- |
| `./` (flat files) | the most recent run | authoritative for `../FINDINGS.md` |
| `run-36670736828/` | 2026-09-30 04:51–05:08 UTC, commit `bef8985` | valid; all three retrievals hash-identical to canonical |
| `run-36672153216/` | 2026-09-30 05:10–05:19 UTC, commit `5dcfacc` | **invalid** — harness defect aborted the transfer; kept as a defect record |

File names:

| File | Meaning |
| --- | --- |
| `00_run_transcript.log` | timestamped stage transcript of the run |
| `01_environment.txt` | runner, tool versions, pinned budgets, run id / commit / branch |
| `02_hf_model_metadata.json`, `03_hf_model_at_revision.json` | Hugging Face API records for the repository and the pinned revision |
| `04_hf_license_evidence.json` | license and gating fields |
| `05_hf_tree_at_revision.json` | Hugging Face file list at the pinned revision (with recorded LFS `sha256`) |
| `06_canonical_manifest.json` | canonical artifact: every path, size and SHA-256 computed from bytes downloaded over the normal Hugging Face path |
| `06b_hash_crosscheck.json` | HF-recorded LFS SHA-256 and Pirate-Face-published checksums vs the computed manifest |
| `07_pirateface_page.html`, `07b_tracker_announce_before.json` | Pirate Face listing, magnet, and the swarm the tracker reported before retrieval |
| `07_<stage>.torrent`, `07_<stage>_aria2c.log`, `07_<stage>_peers.json`, `07_<stage>_client_status.txt` | metainfo and client record for each retrieval stage |
| `08_pf_normal_manifest.json` | manifest after the advertised-magnet retrieval |
| `09_source_loss_proof.txt` | proof that the Hugging Face zone and Pirate Face web layer were unreachable during stage E |
| `10_swarm_only_manifest.json` | manifest after the primary-source-loss retrieval (swarm + tracker) |
| `11_dht_only_manifest.json` | manifest after the trackerless (DHT) retrieval |
| `12_piece_reverify.log` | aria2 piece-table verification of the retrieved payload |
| `13_comparison.json`, `13b_dht_only_comparison.json` | deterministic path-set and SHA-256 comparison against the canonical manifest |
| `14_torrent_identity.json` | bencoded metainfo of each stage: info hash, piece table, file list, web seeds |
| `15_exp18_run_summary.json` | aggregation of the above (no inferred values) |

Interpretation notes:

- A `.torrent` file saved by the client is metainfo, not payload, and is excluded
  from the payload comparison.
- `exit_code=124` means the stage was stopped by the harness budget; the client
  log, the metainfo and the manifests say whether the payload was complete.
  `07_<stage>_client_status.txt` records the explicit check for the client's own
  "Download complete: <payload path>" line (the magnet's metadata job prints a
  similar line with `[MEMORY][METADATA]` and is not a payload completion).
