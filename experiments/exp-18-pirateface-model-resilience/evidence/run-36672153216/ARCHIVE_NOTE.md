# Archived evidence — harness run 36672153216 (INVALID retrieval, kept as a defect record)

This directory is a verbatim copy of the evidence produced by GitHub Actions run
[36672153216](https://github.com/Murkin1980/murat-project-engineer/actions/runs/36672153216)
(commit `5dcfacc`, 2026-09-30 05:10–05:19 UTC).

**This run must not be read as an availability result.** Every stage ended after
~25 s and the payload is incomplete; the recorded SHA-256 values
(`dfe9eb79…`, `bdeb8598…`, `d5527a44…` for `model.safetensors`) are hashes of
*truncated* files and do not match the canonical artifact.

What actually happened (observed):

- A magnet download in aria2 is first a metadata-only job
  (`Download complete: [MEMORY][METADATA]fed3a1e2…`), which is then replaced by
  the real payload job under a **new GID**; queries for the old GID return
  `400 Bad Request`.
- The harness had been changed, for this run only, to interpret an RPC error as
  "the transfer is over" and to shut aria2c down. It therefore stopped the client
  21 s into the transfer.
- The client log records the truth: `[#9c205d 281MiB/0.9GiB(30%) …]`,
  `Download GID#9c205d3163a3c15e not complete`, `INPR` in the results block.
- The evidence is kept because it is the counter-example that forced the sampler
  to be rewritten (follow the active download list every poll instead of pinning
  the first GID) and because it shows what an aborted Pirate Face retrieval looks
  like in this harness.

The last run in the flat `evidence/` directory is the authoritative one for
`../../FINDINGS.md`.
