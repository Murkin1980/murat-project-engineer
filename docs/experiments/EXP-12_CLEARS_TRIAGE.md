# EXP-12 — CLEARS Triage / Executability Engine

Status: ACTIVE — retrospective backtest PASS; prospective validation pending  
Date: 2026-08-18  
New Idea Filter disposition: `EXPERIMENT`  
Execution tier: `VERIFIED`

## Work log

- 2026-08-18: Repository inspected and fast-forwarded to current `origin/main`; pre-existing untracked ZIP preserved.
- 2026-08-18: Runs 01–11, contracts, Stage 2 plan, status, operating model and deep-change boundaries reviewed.
- 2026-08-18: Codex Router (`opencode-go/deepseek-v4-pro`) completed an independent read-only extension-point and corpus review.
- 2026-08-18: Chosen implementation is a stateless deterministic Python helper with versioned JSON contracts, fixtures, tests and evidence. No service or authority change.

## Hypothesis

A small deterministic triage extension can classify task execution risk and mandatory human gates consistently enough to reduce under-triage, without adding runtime authority or changing Option A+ architecture.

## Scope

- Versioned input/output JSON contracts.
- Reproducible scores for Execution Confidence, Complexity, Risk, Blast Radius, Affected Repositories, Architectural Impact, Data Sensitivity, Unknowns, Deep-change Probability and Human Approval Requirement.
- One stateless Python function and CLI.
- A curated 20-case retrospective dataset sourced from RUN-01–11, versioned project history and explicit architecture-boundary counterfactuals.
- Automated tests and a committed backtest report.

## Non-scope

- No LLM classification, adaptive weights, database, service, daemon, queue, scheduler or UI.
- No automatic execution, approval, routing, portfolio disposition or architecture change.
- No claim that retrospective labels are prospective ground truth.
- No change to Codex Router authority.

## Baseline

Current triage is a human application of `FAST`, `VERIFIED` and `DEEP-CHANGE` rules. It is auditable but lacks one canonical machine-readable scorecard. Historical RUN tiers are the available baseline labels; cases without a RUN label are conservatively curated from versioned evidence and identified by `source_ref`.

## Scoring schema

All ordinal dimensions use `0` (none) through `4` (very high). Execution Confidence and Deep-change Probability use `0–100`. Inputs are explicit evidence ratings/signals; the engine does not infer from prose.

- Execution Confidence starts at 100 and deducts for unknowns, absent acceptance criteria, unknown rollback and missing affected repositories.
- Blast Radius is derived from repository count plus shared-component and production signals.
- Architectural Impact and Data Sensitivity take the maximum of supplied ratings and hard safety signals.
- Risk is the maximum of supplied risk, blast radius, architecture and data sensitivity.
- Deep-change Probability is a bounded transparent sum; any hard deep-change signal always selects `DEEP-CHANGE`.
- Human approval is mandatory for hard deep-change, destructive, production, security/permissions or sensitive-data-write signals. High computed sensitivity/probability also raises a gate.

Scores are conservative triage evidence, not calibrated probabilities.

## PASS / FAIL criteria

PASS for the first backtest requires:

1. At least 20 traceable cases.
2. At least 80% exact match on `(risk tier, approval required)`.
3. Zero false negatives for expected `DEEP-CHANGE` cases.
4. 100% deterministic repeatability for identical input.
5. Contracts, package validation and unit tests pass.
6. No prohibited architecture element is introduced.

FAIL if any safety criterion (3–6) fails. A result below the accuracy threshold is `REWORK`, not justification for autonomous or learned classification.

## Metrics

- exact match rate
- approval match rate
- deep-change false negatives
- case count and source traceability
- deterministic test result
- package/unit-test result

## Result log

### Prospective P-003 registration — 2026-08-18

- First non-self-hosting product case: MebelDocs AI company-profile edit UI, already listed in project roadmap/progress.
- Target baseline: `Murkin1980/mebeldocs-ai@477bb57`; target tree clean and synchronized before registration.
- Human label registered before engine execution: `VERIFIED`, approval not required.
- Registration evidence: `evidence/exp-12/prospective/P-003_PRE_REGISTRATION.json`.
- State: `REGISTERED`; result fields remain `null` until separate execution/evaluation checkpoints.
- PDF Cyrillic was considered and deferred because external font acquisition and visual rendering form a distinct risk scope.

### Prospective P-002 registration — 2026-08-18

- Real task: deterministically generate `EXECUTED` evidence and evaluate that frozen artifact instead of rerunning the current scorer.
- Human label registered before engine execution: `VERIFIED`, approval not required.
- Baseline commit: `19b7532`.
- Registration evidence: `evidence/exp-12/prospective/P-002_PRE_REGISTRATION.json`.
- State: `REGISTERED`; result fields remain `null` until subsequent checkpoints.
- Engine result: `VERIFIED`, approval not required, confidence 85, deep-change score 17.
- Implementation adds a deterministic execution CLI and changes evaluation to consume frozen EXECUTED evidence with registration/execution/scorer hashes instead of rerunning the scorer.
- Observed final classification: `VERIFIED`, approval not required; all three agreement checks are `true`.
- Verification: 44 total tests, including 42 passes and 2 privilege skips; package validator PASS.
- P-002 outcome: `PASS`; prospective progress: `2/10`.
- Independent Codex Router review: `PASS`; evaluation was verified not to rerun the scorer. Methodology note: P-001 and P-002 are self-hosting tooling tasks, so P-003 should be real product work or a genuine high-approval/deep-change case.

### Prospective P-001 registration — 2026-08-18

- Real task: add the prospective validation protocol, registry contract and deterministic evaluator.
- Human label registered before engine execution: `VERIFIED`, approval not required.
- Baseline commit: `0ef64aa`.
- Pre-registration evidence: `evidence/exp-12/prospective/P-001_PRE_REGISTRATION.json`.
- State at registration: `REGISTERED`; engine output and observed final classification were intentionally `null` in commit `2f72e8c`.
- First implementation check: unit tests passed, but direct CLI execution exposed a module import-path defect that tests had not represented. The fix adds direct-script import compatibility and a CLI regression test; this is recorded as P-001 rework rather than hidden.
- `REGISTERED`, `EXECUTED` and `EVALUATED` are separate evidence states. Registration was not rewritten; registration and scorer SHA-256 values are preserved so engine drift is visible.
- Engine: `VERIFIED`, approval not required, confidence 85, deep-change score 17.
- Observed final classification: `VERIFIED`, approval not required.
- Human ↔ engine, engine ↔ observed and human ↔ observed agreement: all `true`.
- Final checks before review: 42 total tests, including 40 passes and 2 privilege skips; package validator PASS.
- P-001 outcome: `PASS` with one useful rework. Prospective progress: `1/10` cases.
- Independent Codex Router review and final re-review: `PASS`; no blocker, no Option A+ or Router authority change.

### Backtest v1 — 2026-08-18

- Engine: `0.1.0`; dataset: `exp-12-v1`.
- 20 traceable cases.
- Retrospective fixture agreement for tier + approval: 20/20 (`1.0`); prospective accuracy is `NOT_OBSERVABLE` from this dataset.
- Approval match: `1.0`.
- Expected DEEP-CHANGE false negatives: `0`.
- Final unit-test run: 37 passed; 2 existing Windows symlink tests skipped because the account lacks symlink privilege.
- Package validator: PASS.
- Full-suite rerun initially exposed a repeatable Windows junction cleanup error in an existing RUN-11 test. The test already proved junction rejection, but left the junction for `TemporaryDirectory` to remove incorrectly. A bounded `finally: os.rmdir(junction)` cleanup was added and is included in the final rerun evidence.
- Architecture boundary: PASS; no service, persistence, autonomous execution or Router authority change.
- Outcome: `PASS` for deterministic mechanics and retrospective fixture consistency.
- Independent Codex Router review initially returned `REWORK`: maximum architectural impact could be under-triaged without a duplicate signal, schemas were not enforced at runtime, and the 20/20 result was framed too close to accuracy. Rework now forces `architectural_impact=4` to `DEEP-CHANGE + human approval`, validates the full input vocabulary/types/ranges, adds regression tests, removes two post-hoc historical signals, and labels prospective accuracy `NOT_OBSERVABLE`.
- Final independent Codex Router re-review: `PASS`; all requested safety/framing fixes reproduced, 37 tests passed with 2 privilege skips, no remaining blocker.

Important limitation: inputs and expected labels were curated from already-known evidence. The perfect retrospective fit is not evidence of generalization. EXP-12 remains ACTIVE until prospective cases are pre-registered and evaluated.

## Experiment record template

- Dataset/engine version:
- Case count:
- Exact match rate:
- Approval match rate:
- Deep-change false negatives:
- Determinism evidence:
- Contract/test evidence:
- Reviewer findings/rework:
- Outcome: `PASS | REWORK | BLOCKED | HUMAN_REQUIRED`
- Known limitations:
- Next experiment:

## Continuation instructions

1. Add prospective tasks before execution; do not relabel them after seeing the engine output.
2. Preserve inputs, expected human label, output and final observed tier.
3. Review disagreements manually; change weights only in a new dataset/engine version.
4. After 10 prospective cases, compare under-triage, over-triage and approval recall.
5. Do not connect the engine to automatic execution or Router authority without a new filter and explicit DEEP-CHANGE approval.
6. Register the next case only when a real task is selected; do not fill the prospective dataset with hypothetical outcomes.

Run locally:

```powershell
python scripts/triage_engine.py datasets/exp-12-backtest.json --backtest
python -m unittest discover -s tests -v
python scripts/validate_package.py .
```
