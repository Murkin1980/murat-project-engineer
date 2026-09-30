# EXP-09 pre-run boundary review — 2026-09-30

**RESULT: NEEDS_REVIEW**
**Checkpoint:** EXP-09 — Personalized Assessment Engine v0
**Previous result:** REWORK (RUN-09; recorded 2026-08-15)
**Branch/base inspected:** `arena/01a0f188-murat-project-engineer` at `66dc1c57ef894586677b200274d06e6003699fe2`
**Run type:** Read-only pre-run inspection and repository validation. No Stage-2 assessment scenarios or external provider calls were run.

## Decision

The four boundary findings are **not closed**. This review stops before implementation or controlled evaluation. The experiment contract describes a bounded deterministic-plus-AI pattern, but does not specify enough of the external-provider contract to establish a safe, testable boundary. The implementation and frozen scenario artifacts named by RUN-09 are not present in this checkout, so the claimed runtime boundaries and input preservation cannot be independently verified here.

No provider policy, missing implementation, or missing frozen input was inferred or recreated. No source contract was changed. This is an additive blocker record, not a new evaluation result and not a PASS.

## Reconstructed RUN-09 state

Canonical historical evidence read:

- `experiments/EXPERIMENT_REGISTRY.json` — EXP-09 is `READY_TO_TEST`; its next action says resolve the four findings before another run; result summary says Stage-2 was REWORK.
- `evidence/stage2/RUN-09_REPORT.json` — `judge_verdict` and `outcome` are `REWORK`; deterministic classification (12/12), reported 35 tests, typecheck, lint and build were marked PASS, but unresolved risks include unavailable production pricing, unevaluated external LLM output, missing target Git metadata, and a placeholder target master instruction.
- `evidence/stage2/RUN-09_EXPERIMENT_RECORD.json` — records two rework cycles and retains the REWORK outcome.
- `docs/evaluations/PERSONALIZED_ASSESSMENT_ENGINE_V0.md` — says no external LLM generation was run; it describes the fallback composer only and keeps the terminal decision at HOLD.
- `STATUS.md` — explicitly retains RUN-09 as REWORK pending the four findings.

No separate EXP-09 `FINDINGS` file, `experiments/exp-09` implementation, assessment tests, or frozen scenario input files were found in the tracked repository at the inspected base. The prior report lists assessment sources/tests in `salamat-kitchen-configurator`, but that target tree and its Git metadata are not available in this checkout. The only present synthetic-scenario material is descriptive documentation and retrospective statements; it is not a hashable 12-scenario fixture.

## Boundary dispositions

| Boundary | Gate | Evidence and reason |
|---|---|---|
| Production rule | **FAIL — not proven** | The experiment contract excludes production release, real-customer use and unsupported production prices. However, no implementation is present to test for automatic production action, and the contract does not itself identify a code-level MPE approval gate. Prior evidence explicitly says approved production pricing was unavailable. This does not prove a production action occurred; it means the required separation cannot be verified. |
| External LLM | **FAIL — contract ambiguous** | The contract permits an AI explanation/outcome stage, says the model may improve wording but may not invent rules or authoritative numbers, and defines a structured conceptual flow. It does not unambiguously state whether an external provider is permitted, the exact allowed/disallowed payload, prohibited data, the required behavior when no provider exists, or an enforceable output contract preventing assessment-state mutation. Historical evidence says no external LLM was run. Per the pre-run instruction, no policy was invented and evaluation stops. |
| Git boundary | **FAIL — ownership not established** | RUN-09 itself records that the target directory had no Git metadata. Assessment implementation/tests and frozen scenarios are absent from this repository. The current MPE checkout therefore cannot prove experiment-owned paths, production exclusions, allowable changes, or frozen-input identity. No source artifacts were copied or modified. |
| Source of truth | **FAIL — canonical artifact not established** | The contract establishes a conceptual sequence (`input → deterministic facts → AI outcome`) and says deterministic facts own authoritative numbers, while historical documentation says the composer cannot mutate those facts. Neither the code nor a canonical assessment-state artifact is available here; the contract does not name one artifact as the sole authority. Prompt, generated output, UI and cached-state precedence cannot be tested. |

**Frozen inputs:** Preservation is **not established**. No frozen scenario fixture or baseline hash is present in the tracked tree. This branch made no changes to any scenario input, but that alone cannot prove the missing target inputs were preserved.

## Scope and change record

- Production files/code changed: **No**.
- Experiment contract, historical RUN-09 evidence, status, or unrelated experiments rewritten: **No**.
- New service, dependency, SaaS/API, scheduler, daemon, persistent service, repository, or production rollout: **No**.
- Deep architectural change: **No**.
- Additive files created by this review: this report and `BASELINE_SHA256SUMS.txt` only.
- Bounded Stage-2 validation: **not run**; the boundary gate is unmet.
- EXP-09 scenario-specific tests/regression tests: **not available** in this checkout; none were fabricated or added against absent code.

## Validation performed (repository baseline only)

These checks do not close EXP-09 boundaries and are not a Stage-2 evaluation:

- `python scripts/validate_package.py .` — **PASS** (4 experts, 3 teams, 5 playbooks, contracts and 20 gates).
- `python -m unittest discover -s tests -p 'test_contracts.py' -v` — **PASS**, 12 tests.
- `python -m unittest discover -s tests -v` — **FAIL**, 343 tests run, 8 failures, 1 skipped. Failures are outside EXP-09: committed portfolio views do not match the current registry for EXP-18 (`test_rendered_dashboard_text_tracks_registry_ids_names_and_next_steps`), and generated Reladraw artifacts are stale (`test_committed_mobile_views_are_fresh`, `test_committed_diagram_is_fresh`). No files had been changed before this baseline suite; failures were not modified as unrelated.
- `python -m pytest --version` — unavailable (`No module named pytest`); the repository unittest runner was used instead.

## Baseline hashes

`BASELINE_SHA256SUMS.txt` contains hashes for the registry entry source, experiment contract, prior evaluation report and RUN-09 report/record as inspected at the base commit. These files were not edited by this review.

## Required next decision (not performed here)

Before an implementation change or controlled run, an authorized owner decision must resolve the gaps without changing frozen inputs implicitly:

1. Identify the authorized Git repository/path containing the assessment implementation and exact frozen scenario fixture, or explicitly approve a Git-boundary change.
2. Clarify the external LLM boundary in the governing contract: provider permission, exact input/output, excluded data, no-provider behavior, and whether/how the system rejects any attempt to alter canonical assessment state.
3. Name the single canonical assessment-state artifact and its input-to-derived-output lineage.
4. Provide or identify an enforceable MPE production decision boundary, then verify it against the implementation.

Until those items have evidence and regression coverage, do not rerun Stage-2. EXP-09 remains **NEEDS_REVIEW / not ready for controlled run**. This review does not change the historical REWORK result or claim PASS.
