# EXP-07 evidence directory (Strix security-validation retry)

This directory holds **sanitized** EXP-07 experiment evidence only.

## Hard rule

`RAW_STRIX_OUTPUT_NEVER_COMMITTED`

Raw penetration-test material — Strix reports and console output, `strix_runs/**`,
agent transcripts, exploit payloads, proofs of concept, exploitable endpoint
details, source excerpts that enable an attack, secrets, tokens, credentials and
configuration fragments — must never be committed here or anywhere else in this
repository. It stays in access-controlled temporary/local storage on the operator
machine and is referenced from committed evidence by `sha256` digest at most.
`.gitignore` blocks `strix_runs/`, `.strix/`, `raw-pentest/`, `*.har` and `*.pcap`.

Committed artifacts may describe a finding only at the level of: sanitized
summary, vulnerability class, affected component/path (without exploit details),
severity, reproduction status, whether tests/linters/security checks/existing
issues/ordinary review already detected it, remediation state, and a safe
evidence hash or reference. The full rule lives in
`docs/security/STRIX_PILOT.md` → *Evidence handling and raw-output boundary*.

## What lives here now

- `STRIX_RETRY_2026-09-28.json` — sanitized evidence for the 2026-09-28 retry:
  frozen target (`Murkin1980/mebeldocs-ai@2d6d60b240f8f4e2546cf451433c8f1ff0aad65a`),
  frozen scope and exclusions, executed baseline (install / tests / typecheck /
  build / API surface / existing checks / known issues / ordinary code-review
  baseline), Strix version and source, execution environment, scan status,
  finding counts, novelty comparison, sanitization statement, execution outcome
  (`BLOCKED`), canonical registry status (`HOLD`) and the recommendation.
  Every finding count is `0` because the scan never ran — `0` means `NOT_RUN`,
  never "nothing found".

## What lands here after a real scan

One sanitized artifact per run, named `STRIX_RUN_<frozen-sha-prefix>_<date>.json`,
carrying the same field set plus per-finding entries limited to: vulnerability
class, affected component/path, severity, validity
(`confirmed`/`false_positive`/`inconclusive`), novelty versus the frozen
baseline, actionability, remediation state and an optional safe evidence hash.
Raw output is **not** added, and no result is synthesized when a run is blocked.

## Guards

`tests/test_exp07_strix_retry.py` fails when the sanitization boundary, the
frozen target/baseline record, the outcome→registry-status mapping or the
registry entry drift out of agreement with this evidence.
