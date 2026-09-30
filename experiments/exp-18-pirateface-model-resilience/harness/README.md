# EXP-18 harness (bounded, temporary)

This directory holds the retrieval harness for EXP-18. It is experiment tooling,
not production code: nothing here is imported by the application, no dependency
is added to the repository, and the CI wrapper that runs it
(`.github/workflows/exp18-harness.yml`) is deleted once the experiment has
recorded its evidence.

## Why a CI runner is the test host

The agent sandbox used to author this experiment has an allow-listed network
egress: `huggingface.co` and `pirateface.co` are not reachable from it, while
GitHub and package registries are (see `METHOD.md`). A GitHub-hosted runner is
therefore used as the bounded, ephemeral test host, because it can reach both
distribution paths. The runner holds no credentials, publishes nothing, and is
destroyed after the job.

## What the harness does

`run_exp18.sh` executes seven recorded stages against one pinned model:

| Stage | Action | Evidence file |
| --- | --- | --- |
| 0 | environment / tool versions / run id | `01_environment.txt` |
| A | pin HF repo, revision (`sha`), license, expected file list | `02`–`05_*.json` |
| B | download canonical artifact through the normal HF path, hash every file | `06_canonical_manifest.json` |
| C | record the Pirate Face distribution reference (page, magnet, badges) | `07_pirateface_page.html`, `07_*` |
| D | retrieve through the Pirate Face path (advertised magnet, unmodified) | `08_pf_normal_manifest.json` |
| E | bounded primary-source loss: `/etc/hosts` blocks HF **and** Pirate Face's web layer; the magnet's `ws=` web-seed is stripped; retrieval may use only the swarm + Pirate Face tracker + DHT | `09_source_loss_proof.txt`, `10_swarm_only_manifest.json` |
| F | deterministic comparison (exact path sets, exact SHA-256) plus piece re-verification against torrent metadata | `12_comparison.json`, `13_torrent_identity.json` |
| – | aggregated run summary | `14_exp18_run_summary.json` |

Helpers: `manifest.py` (sorted path/size/SHA-256 manifest), `compare.py`
(exact-equality verdicts), `torrent_identity.py` (bencode + info-hash identity of
the torrent metainfo captured in stages D and E), `summarize.py` (aggregation
only — it reads recorded files and infers nothing).

## Honesty rules encoded in the harness

- The canonical artifact is the source of truth; the comparison is exact
  equality of SHA-256 digests and path sets, with no tolerance.
- Stage E does not merely block the *model page*: DNS for the whole
  `huggingface.co` zone, `hf.co` and the Xet bridge are pointed at `0.0.0.0`,
  and the fetching client is given a magnet with any web-seed removed, so bytes
  can only arrive from peers.
- The `.torrent` metainfo captured in stages D and E is compared (piece table +
  file list + info-hash) so the swarm-only run is provably the same torrent that
  Pirate Face advertises, not a different one.
- Peer addresses are recorded only as masked `/16` networks to avoid publishing
  full IPs of third-party seeders.

## Run log

- attempt 01 (run 36667540675, commit 6d8d807): harness executed end to end. The
  weight-file SHA-256 already matched across the Hugging Face and swarm-only
  retrievals, but two harness defects made the recorded evidence incomplete:
  `torrent_identity.py` raised `TypeError: Object of type bytes is not JSON
  serializable` while dumping the metainfo (the file was left truncated), and the
  manifest comparison did not normalise the torrent's payload directory, so the
  path sets were reported as disjoint. Both defects were fixed before attempt 02;
  the raw attempt-01 evidence remains in git history at commit 6d8d807.
- attempt 02 (run 36667763061): aborted by the job timeout. Starting aria2c with
  `--enable-rpc` keeps its RPC server alive after the download completes, so each
  stage waited for its own wrapper timeout; no evidence was committed.
- attempt 03 (2026-09-30): the RPC sampler now issues `aria2.shutdown` when the
  download reports complete, and the per-stage budget is 6 minutes without
  progress.
