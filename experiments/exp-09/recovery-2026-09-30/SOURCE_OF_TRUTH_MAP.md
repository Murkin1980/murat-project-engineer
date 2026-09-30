# EXP-09 Source-of-Truth Recovery

**Checkpoint:** EXP-09-SOURCE-OF-TRUTH-RECOVERY
**Review date:** 2026-09-30
**Result:** **SOURCE_OF_TRUTH_MISSING**
**Repository:** `Murkin1980/murat-project-engineer`
**Inspected main:** `66dc1c57ef894586677b200274d06e6003699fe2`
**Inspected session branch:** `arena/01a0f188-murat-project-engineer` at `698d6352cc3c5c5a4090b49ce82bd79f3399e9f3`

## Executive finding

Accessible repository evidence recovers the governing contract, a historical RUN-09 report/record, and a narrative evaluation report. It does **not** recover the assessment implementation, the 12 frozen scenario inputs, a canonical assessment-state artifact, per-scenario outputs, or the experiment tests themselves. The historical narrative therefore cannot be reproduced from the recovered artifacts.

This is a finding about what was recoverable in the inspected repository refs and history—not a claim that the missing material never existed. No missing input or implementation was reconstructed.

## Search performed

### Current repository

- Inspected `main`, the session branch, and the `experiments/`, `docs/`, `evidence/`, `tests/`, `scripts/`, `contracts/`, and package-manifest areas.
- Searched repository text and tracked paths for `EXP-09`, `Personalized Assessment Engine`, `assessment`, `Stage-2`, `frozen`, `scenario`, `assessment state`, and `evaluation`.
- Current governing/reference artifacts are the experiment contract, registry entry, status entry, evaluation narrative, RUN-09 report/record, and the previous additive boundary review in PR #44.
- The target implementation and the scenario/test paths listed in RUN-09 are not present in the current MPE worktree.

### Branches and GitHub history

- Local clone reports **shallow = true** and contains only the session commits plus the grafted `main` tip; local `git log` alone is not a complete history.
- Queried GitHub's branch list and recursive tip trees: **46 branch names / 45 unique tips**. No branch tip contains the target source/test paths named in RUN-09 (`salamat-kitchen-configurator/src/assessment`, `tests/assessment/assessment.test.ts`) or a path matching the EXP-09/assessment/scenario/frozen/Salamat terms searched. Relevant matches are the MPE experiment contract/evaluation documentation and the unrelated frozen EXP-002 IR; the session branch additionally contains its EXP-09 recovery/review evidence.
- GitHub path history for the contract, evaluation report, RUN-09 report, and RUN-09 record identifies the Stage-2 checkpoint commits listed below.
- GitHub pull-request/issue search found no earlier dedicated EXP-09 implementation PR or RUN-09 issue. PR #44 is the current pre-run boundary-review PR and contains no review comments. Issue #22 / PR #23 establish the portfolio registry and list Personalized Assessment as an experiment seed; they do not provide implementation or evaluation payloads.
- A full unreachable-object or external/local-disk search was not possible. The historical RUN-09 report itself says its implementation target was `C:\Projects\salamat-kitchen-configurator` and that the target directory had no Git metadata.

## Artifact inventory

`YES` means an artifact is present in an inspected revision. A narrative reference to another file is not counted as that file being recovered.

| Artifact | Found | Location | Revision | Hash | Status |
|---|---|---|---|---|---|
| Governing contract | YES | `CODEX_PERSONALIZED_ASSESSMENT_ENGINE_V0_EXPERIMENT.md` | `main` `66dc1c5`; introduced in `ad6364e`, adjusted in `2e6a4d9` | See `RECOVERY_HASHES.txt` | **Canonical governing reference**: registry points to this experiment path. |
| Registry / experiment identity | YES | `experiments/EXPERIMENT_REGISTRY.json` | `main` `66dc1c5` | See `RECOVERY_HASHES.txt` | Canonical MPE registry; records EXP-09 as `READY_TO_TEST` while requiring resolution of the findings before another run. |
| Implementation | NO | Historical report references `C:\Projects\salamat-kitchen-configurator\src\assessment` and its app files; no MPE Git path/revision | NOT RECOVERED | NONE | **Reported, not recovered.** No source file, commit, branch, PR artifact, or implementation revision was found in the inspected MPE refs/history. |
| Frozen scenarios | NO | No fixture path is recorded; historical report only says 12 synthetic scenarios were defined before source was copied | NOT RECOVERED | NONE | **MISSING.** No scenario bytes, revision, or baseline hash; do not reconstruct. |
| Canonical assessment state | NO | No separate assessment-state artifact in the inspected refs/history | NOT FOUND | NONE | **NOT FOUND.** No artifact distinguishes actual canonical state from input or presentation. |
| Derived/per-scenario outputs | NO | RUN-09/evaluation reports contain aggregate claims, not the 12 scenario outputs | NOT RECOVERED | NONE | **MISSING.** No input-to-state-to-output rows or output payloads. |
| Historical evaluation | YES, narrative only | `docs/evaluations/PERSONALIZED_ASSESSMENT_ENGINE_V0.md`; `evidence/stage2/RUN-09_REPORT.json` | Both introduced in `ad6364e`; current `main` `66dc1c5` | See `RECOVERY_HASHES.txt` | **Historical aggregate evidence, not reproducible.** Includes reported 12/12 classifications, claimed test/quality metrics and limitations, but no underlying scenario/output set. |
| Historical duplicate evaluation report | YES, historical path | `PERSONALIZED_ASSESSMENT_ENGINE_V0_REPORT.md` | Added in `ad6364e`, removed in `2e6a4d9` | Same Git blob as the evaluation document; see hashes | **Duplicate narrative**, byte-identical to `docs/evaluations/...` at `ad6364e`; not a separate result/evidence set. |
| Previous Stage-2 report | YES | `evidence/stage2/RUN-09_REPORT.json` | Added in `ad6364e` | See `RECOVERY_HASHES.txt` | Historical report states RUN-09 outcome `REWORK`; does not record implementation or scenario commit/hash. |
| Experiment record | YES | `evidence/stage2/RUN-09_EXPERIMENT_RECORD.json` | Added in `2e6a4d9` | See `RECOVERY_HASHES.txt` | Historical run summary; records `rework_count: 2` and outcome note, not implementation/input lineage. |
| Experiment-specific tests | NO, test files not recovered | RUN-09 report references `salamat-kitchen-configurator/tests/assessment/assessment.test.ts` | No Git revision available | NONE | **Reported test claim only.** Evaluation narrative says `npm.cmd run check`, typecheck/lint/build and 35/35 tests passed, but neither test source nor run log is in the MPE repository refs/history. |
| Findings | YES, embedded only | `evidence/stage2/RUN-09_REPORT.json` `unresolved_risks`; evaluation narrative `Failures and limitations` | `ad6364e` / current `main` | Same hashes as parent artifacts | **Historical findings are embedded prose/JSON.** No standalone EXP-09 `FINDINGS.md` was recovered. |
| Previous pre-run boundary review | YES | `experiments/exp-09/pre-run-2026-09-30/BOUNDARY_REVIEW.md` | Session branch `698d635` (PR #44) | See `RECOVERY_HASHES.txt` | Additive current review; not historical Stage-2 evidence. |

## Frozen-input status

- Scenario count: **12 is reported**, not independently inspectable.
- Exact scenario/fixture location: **not recorded/recovered**.
- Revision and hash: **not available**.
- Prior-run reference to exact frozen bytes: **none found**.
- Current-vs-prior hash comparison: **not possible**.
- State: **MISSING** (not `FROZEN_VERIFIED`; not reconstructed).

The contract says scenarios should be created before implementation and specifies expected groups. Those instructions are not the missing scenario inputs and were not used to regenerate them.

## Previous Stage-2 run reconstruction

| Field | Recovered evidence |
|---|---|
| Run ID | `RUN-09` |
| Reported time | 2026-08-15 00:00–01:00 `+05:00`, from `RUN-09_REPORT.json` |
| Reported result | `REWORK` (`judge_verdict` and `outcome` in RUN-09 report) |
| Separate experiment decision | `PERSONALIZED_ASSESSMENT_ENGINE_DECISION: HOLD` in evaluation narrative; this is not the Stage-2 run verdict. |
| Report artifact revision | Added to MPE at `ad6364e5642e41ff0cb52660cbcee181eb325fb4` (checkpoint commit `wip(stage2): checkpoint runs 07-11 and runtime coordination`). |
| Experiment record revision | Added to MPE at `2e6a4d9e25dba4601b42071a232aabf77e5c2873` (follow-up Stage-2 normalization commit). |
| Implementation revision | **Not recorded / not recovered.** The report names a local target path and explicitly says it had no Git metadata. |
| Scenario revision | **Not recorded / not recovered.** No fixture path or hash. |
| Outputs | Aggregate metrics/claims only; no per-scenario input, state, or output artifact. |
| Reproducible now? | **NO.** Missing implementation source/revision, frozen scenarios, experiment test sources/logs, and per-scenario outputs prevent replay and independent derivation of the evaluation. |

The narrative reports 12/12 expected classifications, 35/35 tests, quality averages and a `REWORK` run. These are historical recorded claims, not newly rerun or independently reproduced results.

## Canonical assessment state

**CANONICAL_ASSESSMENT_STATE: NOT_FOUND**

The contract describes `calculateAssessment(input) → DeterministicFacts`, followed by an AI outcome/composition stage, and says deterministic facts own authoritative numeric/business facts. The evaluation narrative claims the composer could not calculate or mutate those facts. No actual assessment-state artifact, source implementation, schema, runtime record, or persisted/serialized object is available to establish which artifact held canonical state. The conceptual description does not make any prompt, LLM response, generated JSON, UI object, or cache canonical.

## Lineage

| Link | Status | Basis |
|---|---|---|
| Governing contract → frozen inputs | **UNKNOWN** | Contract specifies scenario groups/acceptance; report says 12 scenarios were defined, but no exact fixture, path, revision, or hash links them. |
| Frozen inputs → implementation | **SUPPORTED** | Evaluation narrative says the scenarios were defined before assessment source was copied into the target. Both actual inputs and source are missing, so the assertion is not independently proven. |
| Implementation → assessment state | **SUPPORTED** | Contract/report describe deterministic facts and a bounded composer; no code or actual state artifact exists to prove the runtime mapping. |
| Assessment state → derived output | **UNKNOWN** | A structured result page is described, but no canonical state or per-scenario derived-output artifact is available. |
| Derived output → evaluation | **SUPPORTED** | Aggregate scenario/quality results are recorded in the report, but no output-to-scenario mapping or raw evaluation worksheet/log is present. |

No `SUPPORTED` link is upgraded to `PROVEN`.

## Boundary recovery (inspection only)

- **PRODUCTION_DECISION_BOUNDARY: PARTIAL.** The governing contract/evaluation report prohibit public/production rollout, real customer use and reliance on unavailable production pricing; RUN-09 claims local-only/no production exposure. No implementation or explicit enforceable separate-MPE-decision artifact was found. This is not proof of an automated production decision.
- **EXTERNAL_LLM_BOUNDARY: PARTIAL.** The contract bounds AI to explanation/presentation and disallows inventing authoritative price/rules. The evaluation says no external LLM was run and no LLM is required for reproducible v0. Provider identity, actual request/response, exact permitted payload, prohibited-data list, fallback behavior in code, and mutation proof are not recovered.
- **GIT_BOUNDARY: PARTIAL.** MPE governing/evaluation evidence is versioned, and all accessible MPE branch tips were inspected. The claimed target is a local Windows path whose report says it had no Git metadata; no experiment-only implementation or frozen-input revision can be established. No production file list/diff for the target exists in MPE evidence.
- **SOURCE_OF_TRUTH: UNKNOWN.** Deterministic facts are described as authoritative conceptually, but there is no recoverable canonical state artifact or lineage implementation.

## Findings / PR / issue references

- No standalone EXP-09 `FINDINGS` artifact was found in current paths, the inspected branch-tip trees, or the relevant path history. Historical limitations are embedded in the evaluation report; RUN-09 unresolved risks are in its report JSON.
- No earlier dedicated EXP-09 PR or RUN-09 issue was found in the accessible MPE PR/issue search. Current PR #44 is the prior boundary-review PR and is not the original Stage-2 implementation PR.
- Issue #22 and PR #23 are registry-governance artifacts. They include Personalized Assessment among experiment seeds but do not contain the implementation or raw run evidence.
- The prior report's references to the target assessment source/tests were verified as references only; corresponding files were not found in MPE GitHub history/branch tips.

## Missing artifacts

1. The actual assessment implementation and its Git repository/commit.
2. The 12 frozen synthetic-scenario input fixtures and their original hash/revision.
3. The canonical serialized assessment state and its schema/lineage.
4. Per-scenario derived outputs and raw evaluation records.
5. The experiment-specific test files and original test/build logs.
6. An implementation/source diff proving the production boundary and an actual external-provider request/response (historical narrative says no external LLM was called).
7. A standalone historical findings artifact; only embedded risks/limitations were recovered.

## Limitations

- The local Git checkout is shallow. GitHub API path history and all 45 unique remote branch-tip trees were inspected, but that cannot establish whether unreachable/deleted Git objects or material outside this repository ever existed. Branch-tree inspection was by path/name; GitHub code search returned zero matches with `incomplete_results: true`, so neither result rules out differently named blobs on a non-default branch.
- The Windows local path in RUN-09 was not accessible from this checkout. Its report states it lacked Git metadata; that assertion is preserved as a historical report claim.
- No other repository was searched because the governing task/repository is MPE and the historical report supplies no GitHub URL for the target directory.
- Missing means not found in inspected, accessible sources; it does not mean “never existed.”

## Scope confirmation

Recovery evidence only. No implementation, test, schema, contract, frozen input, production code, LLM call, Stage-2 run, dependency, service, repository, or architecture component was created or changed.
