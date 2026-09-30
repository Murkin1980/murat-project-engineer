# EXP-18 harness (bounded, temporary)

This directory holds the retrieval harness for EXP-18. It is experiment tooling,
not production code: nothing here is imported by the application, no dependency
is added to the repository, and the CI wrapper that runs it
(`.github/workflows/exp18-harness.yml`) is temporary and is removed once the
experiment has recorded its evidence.

The scripts in this directory were started by the earlier EXP-18 execution
session on branch `arena/01a0f07b-murat-project-engineer`; this session adopted
them, hardened the stage/timeout handling, and recorded its own run. Evidence
files under `../evidence/` come from the run listed in the run log below.

## Why a CI runner is the test host

The agent sandbox used to author this experiment has an allow-listed network
egress: `huggingface.co` and `pirateface.co` are not reachable from it, while
GitHub and package registries are (see `../METHOD.md`). A GitHub-hosted runner is
therefore used as the bounded, ephemeral test host, because it can reach both
distribution paths. The runner holds no credentials, publishes nothing, and is
destroyed after the job.

## What the harness does

`run_exp18.sh` executes the recorded stages against one pinned model:

| Stage | Action | Evidence file |
| --- | --- | --- |
| 0 | environment / tool versions / run id / budgets | `01_environment.txt` |
| A | pin HF repo, revision (`sha`), license, expected file list | `02`–`05_*.json` |
| B | download canonical artifact through the normal HF path, hash every file | `06_canonical_manifest.json` |
| C | record the Pirate Face distribution reference (page, magnet, badges, endpoint probes) | `07_pirateface_page.html`, `07b_*` |
| D | retrieve through the Pirate Face path (advertised magnet, unmodified) | `08_pf_normal_manifest.json` |
| E | bounded primary-source loss: `/etc/hosts` blocks HF **and** Pirate Face's web layer; the magnet's `ws=` web-seed is stripped; retrieval may use only the swarm + Pirate Face tracker + DHT | `09_source_loss_proof.txt`, `10_swarm_only_manifest.json` |
| E2 | same with the Pirate Face tracker blocked too → swarm/DHT only | `11_dht_only_manifest.json` |
| F | deterministic comparison (exact path sets, exact SHA-256) plus piece re-verification and torrent-metainfo identity | `12_piece_reverify.log`, `13_comparison.json`, `13b_*`, `14_torrent_identity.json` |
| – | aggregated run summary | `15_exp18_run_summary.json` |

Helpers: `manifest.py` (sorted path/size/SHA-256 manifest), `compare.py`
(exact-equality verdicts with payload-directory normalisation), `page_hashes.py`
(cross-check of HF's recorded LFS SHA-256 and the hashes Pirate Face publishes
against the downloaded bytes), `peer_sample.py` (aria2 RPC sampler that also
stops aria2c when the transfer ends), `torrent_identity.py` (bencode + info-hash
identity of the torrent metainfo captured in stages D and E), `tracker_announce.py`,
`summarize.py` (aggregation only — it reads recorded files and infers nothing).

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
- A stage that stalls is ended by its budget and recorded as incomplete; missing
  evidence stays null in the summary instead of being inferred.

## Run log

- attempt 01 (run 36667540675, prior session, commit 6d8d807): harness executed
  end to end; the weight-file SHA-256 already matched across the Hugging Face and
  swarm-only retrievals, but two harness defects left the recorded comparison
  incomplete (`torrent_identity.py` bytes-vs-JSON serialisation, and no
  payload-directory normalisation in the path comparison). That raw evidence
  remains in git history at commit 6d8d807.
- attempt 02 (run 36667763061, prior session): aborted by the job timeout —
  aria2c started with `--enable-rpc` keeps its RPC server alive after a transfer
  ends, so stages waited for their wrapper timeouts.
- attempt 03 (run 36669718210, prior session, commit 6d236b6): RPC shutdown added;
  superseded by this session's run before evidence was committed.
- attempt 04 (run 36670736828, commit `bef8985`, this session): the stage runner
  gained a hard harness budget and per-stage budgets, and the RPC sampler was
  made responsible for stopping aria2c. All three retrievals produced
  byte-identical payloads, but each torrent stage then sat until its budget
  timeout because the sampler stopped sampling as soon as the magnet's metadata
  job was replaced by the payload job (new GID, old GID answers
  `400 Bad Request`). Evidence archived in `../evidence/run-36670736828/`.
- attempt 05 (run 36672153216, commit `5dcfacc`): **defect**. The sampler had
  been changed to treat the `400 Bad Request` as "the transfer is over" and shut
  aria2c down 21 s into the transfer, so every retrieval was truncated
  (`INPR`, `281MiB/0.9GiB`). Evidence kept as a defect record in
  `../evidence/run-36672153216/`.
- attempt 06 (run 36672975009, commit `e408717`): fix — the sampler re-reads the
  active download list every poll, never pins a GID, and shuts the client down
  only after 20 consecutive polls with no active download; the stage runner now
  records the client's own payload "Download complete" line, the result-block
  status counts and the sampler byte counters. All three retrievals completed
  cleanly (`exit=0`) and verified byte-identical to the canonical artifact.
  This is the authoritative evidence set; results are in `../FINDINGS.md`.

## Temporary CI wrapper

`.github/workflows/exp18-harness.yml` is deleted once the experiment has recorded
its evidence (as it now has). A verbatim copy is kept at
`exp18-harness.workflow.yml` in this directory so the run can be reproduced by
placing it back under `.github/workflows/` with the branch filter adjusted.
