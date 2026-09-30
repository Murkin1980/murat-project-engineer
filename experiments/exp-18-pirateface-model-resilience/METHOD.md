# EXP-18 — Method, test host and evidence rules

This file records *how* the EXP-18 evidence is produced. The contract itself is
`README.md` (mirrored from PR #31) and is not modified by the execution.

## Test host: why a temporary CI runner, not the authoring sandbox

The authoring agent sandbox has an allow-listed network egress. Observed from
the sandbox on 2026-09-30 (probes recorded in the run transcript):

| Destination | Observed result |
| --- | --- |
| `huggingface.co:443` | TLS handshake reset (`SSL_ERROR_SYSCALL`), HTTP/80 also refused |
| `cdn-lfs.huggingface.co:443`, `cas-bridge.xethub.hf.co:443` | unreachable |
| `pirateface.co:443` / `:80` | TLS handshake reset / no HTTP response |
| `tracker.pirateface.co:6969` (UDP announce) | timeout |
| `tracker.pirateface.co:6969` (TCP) | connection reset |
| `github.com`, `api.github.com`, `codeload.github.com` | reachable |
| `pypi.org`, `files.pythonhosted.org`, `registry.npmjs.org` | reachable |
| arbitrary hosts (e.g. `example.com`, `1.1.1.1`) | blocked |

Neither distribution path is reachable from the sandbox, so the bounded test is
executed on an ephemeral GitHub-hosted runner instead. That runner is:

- temporary (destroyed at the end of the job);
- credential-free (no secrets are used; `/etc/hosts` is the only "outage"
  mechanism, applied to the runner itself);
- non-production (it publishes nothing, deploys nothing, and no repository code
  or runtime depends on it).

The workflows file `.github/workflows/exp18-harness.yml` is experiment tooling
and is removed once the evidence is recorded; the harness scripts stay under
`harness/` as the reproducible method.

## Stages

| Stage | Action | Evidence |
| --- | --- | --- |
| 0 | environment, tool versions, run id, budget | `01_environment.txt` |
| A | pin HF repository, revision (`sha`), license, expected file list | `02`–`05_*.json` |
| B | download the canonical artifact through the normal Hugging Face path and hash every file | `06_canonical_manifest.json` |
| C | record the Pirate Face distribution reference (page, magnet, endpoint probes) | `07_pirateface_page.html`, `07b_tracker_announce_before.json` |
| D | retrieve through the Pirate Face path using the advertised magnet unmodified | `08_pf_normal_manifest.json` |
| E | bounded primary-source loss: `/etc/hosts` blocks the HF zone, `hf.co`, the Xet bridge and Pirate Face's web layer; the magnet's `ws=` web-seed is stripped, so bytes can only come from the swarm + Pirate Face tracker + DHT | `09_source_loss_proof.txt`, `10_swarm_only_manifest.json` |
| E2 | same, with the Pirate Face tracker blocked as well → swarm/DHT only | `11_dht_only_manifest.json` |
| F | deterministic comparison (exact path sets, exact SHA-256), torrent metainfo identity, piece re-verification | `12_piece_reverify.log`, `13_comparison.json`, `13b_dht_only_comparison.json`, `14_torrent_identity.json` |
| – | aggregated summary, built only from recorded files | `15_exp18_run_summary.json` |

## Comparison rules (fixed before the run)

- The canonical Hugging Face manifest is the reference. Every candidate file
  must exist with byte-identical size and SHA-256; mismatches are failures, not
  warnings.
- Paths are compared after stripping the single common top-level directory the
  BitTorrent client creates for the payload, and after excluding `.torrent`
  metainfo files (evidence, not payload).
- Pirate Face's own published checksums and Hugging Face's recorded LFS
  `sha256` values are cross-checked against the bytes actually downloaded
  (`06b_hash_crosscheck.json`).
- Peer addresses are recorded only as masked `/16` networks; third-party seeder
  IPs are not published.

## Evidence discipline

- `OBSERVED` means a value read from a file produced by the run, a HTTP response,
  or a hash computed from downloaded bytes.
- `INFERRED` is stated as inference only.
- `UNKNOWN` is left empty rather than filled with an assumption.
- A magnet or listing is never treated as proof of availability; only a
  completed retrieval whose bytes hash to the pinned values counts.
