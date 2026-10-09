# EXP-29 — Arena Bootstrap Harness

## Primary disposition

**REUSE_COMPONENT**

Work only inside `Murkin1980/murat-project-engineer`.

This is a bounded experiment. Do not create a new repository, service, database, vector store, daemon, scheduler, persistent agent runtime, or parallel governance/memory layer.

## Start condition

**Do not execute EXP-29 until the owner explicitly starts it after EXP-20 is completed.**

Until then this file is the authoritative queued task specification only.

## Goal

Build and test a deterministic **Arena Bootstrap Harness** that gives a fresh Arena session the smallest useful context needed to begin a real MPE task without rediscovering information already present in canonical Git sources.

Mental model:

`canonical Git sources → deterministic bootstrap builder → derived ARENA_CONTEXT.md/json → fresh Arena session`

The bootstrap is not memory authority. It is a temporary derived view.

## Main question

Can a fresh executor reach useful work faster and with less rediscovery when given a compact, source-linked bootstrap packet, while preserving MPE governance and Git as the only source of truth?

## Required packet layers

The prototype should support only the smallest useful set:

1. **NOW** — project, task, branch/base SHA when known, current checkpoint, nearest action.
2. **RULES** — only task-relevant mandatory rules and stop/deep-change boundaries.
3. **KNOWN LESSONS** — evidence-backed lessons relevant to this task.
4. **REUSABLE COMPONENTS** — already accepted reusable patterns relevant to the task.
5. **KNOWN TRAPS** — verified environment/tooling/task-specific hazards.
6. **RESUME** — last known state, evidence, changes, blocker, next action, handoff when available.

Every item must point back to canonical sources. Prefer source path + digest/hash where practical.

## Knowledge scope

Classify each included lesson as exactly one of:

- `GLOBAL` — repeatedly useful across unrelated MPE tasks;
- `PROJECT` — applies to one project/product line;
- `TASK` — applies only to one experiment/checkpoint;
- `NO_CHANGE` — observed but not promoted into the bootstrap.

Do not infer `GLOBAL` from a single low-cost incident.

## Phase 0 — audit before coding

Read and reconcile:

- `AGENTS.md`;
- `docs/governance/SCOPE-CHANGE-CONTROL.md`;
- `STATUS.md`;
- `experiments/EXPERIMENT_REGISTRY.json`;
- EXP-27 results/evidence on context packets and resumable execution;
- EXP-28 results on evidence-gated retrospective;
- existing runtime/handoff/context helpers before introducing any new helper.

Map existing components first. If an existing helper can be extended, extend it instead of creating a parallel mechanism.

## CP-01 — Existing capability map

Produce:

`need → existing MPE component → reusable? → gap → decision`

At minimum cover:

- task genealogy/context packets;
- graceful handoff;
- source digests;
- experiment registry;
- status/next action;
- task-local instructions;
- accepted lessons from experiment results.

Output dispositions:

- `KEEP_EXISTING`
- `REUSE`
- `EXTEND`
- `REJECT_DUPLICATE`

If a separate memory subsystem appears necessary, stop with `DEEP_CHANGE_REQUIRED`.

## CP-02 — Deterministic bootstrap builder

Implement the smallest possible experiment-only prototype that can derive a packet from repository files.

Preferred form:

- one small script or harness inside EXP-29;
- deterministic output for identical inputs;
- no network requirement;
- no LLM needed for packet construction;
- no persistent store;
- no automatic writes back into canonical sources.

Generate both:

- `ARENA_CONTEXT.json` — machine-readable;
- `ARENA_CONTEXT.md` — human-readable launch brief.

The generated artifacts must identify their canonical source refs and expose staleness when source digests no longer match.

## CP-03 — Fresh-session comparison

Use one real, already completed context-heavy MPE task as the frozen fixture.

Run two isolated arms:

### Arm A — normal rediscovery
Fresh executor receives only the task pointer and normal repository access.

### Arm B — bootstrap
Fresh executor receives the same task pointer plus the generated Arena bootstrap packet.

Measure at minimum:

- number of files read before first useful task action;
- bytes of context read;
- rediscovery steps;
- tool calls before first useful task action;
- wrong/redundant paths entered;
- whether task genealogy and stop conditions are reproduced correctly;
- whether packet contents remain consistent with canonical sources.

Do not claim wall-clock savings unless time is actually measured reproducibly.

## CP-04 — stale/unsafe packet negative controls

Prove fail-closed behaviour for at least:

1. canonical source changed after packet generation;
2. source digest mismatch;
3. missing critical stop/deep-change rule;
4. stale NEXT ACTION;
5. packet attempts to override canonical Git source;
6. task-local lesson incorrectly promoted as GLOBAL.

Expected outcome: packet is rejected, flagged stale, or degraded to a non-authoritative hint. It must never silently override canonical files.

## CP-05 — Result and adoption decision

Return one of:

- `PASS / ADOPT_WITH_CHANGES`
- `PASS / REUSE_COMPONENT`
- `PARTIAL`
- `FAIL`
- `DEEP_CHANGE_REQUIRED`

PASS requires:

- deterministic packet generation;
- source-linked provenance;
- stale-packet detection;
- fresh-session comparison;
- no second source of truth;
- no new runtime/service/database;
- measurable reduction in rediscovery or context/tool overhead;
- no governance weakening.

## Promotion rule

The harness must not automatically learn from every completed experiment.

A lesson can enter a future bootstrap source only when it has:

- explicit evidence;
- a known scope (GLOBAL/PROJECT/TASK);
- a minimal reusable formulation;
- a verification path;
- no conflict with current governance.

Otherwise use `NO_CHANGE`.

## Required validation

Run the project-standard validation available at execution time, including:

- package validator;
- full unittest baseline before/after;
- EXP-29 proof tests;
- `git diff --check`;
- scope check;
- secrets check when applicable.

Pre-existing unrelated failures must be recorded, not repaired inside EXP-29 unless required for the experiment.

## Scope stop rules

Stop before implementation and return `DEEP_CHANGE_REQUIRED` if the solution needs any of:

- memory database/vector store;
- daemon/scheduler;
- automatic persistent learning;
- Router authority;
- autonomous promotion of rules;
- shared orchestration state;
- new canonical source of truth;
- generic workflow engine.

## PR/result

One bounded PR.

Return:

- RESULT;
- disposition;
- capability map;
- packet schema/fields;
- fixture;
- Arm A vs Arm B measurements;
- stale/negative-control results;
- changed files;
- tests;
- commit SHA;
- PR;
- rollback.

Open the PR but do not merge.

## CP-06 — First real-use repair checkpoint (owner authorized 2026-10-09)

Trigger: EXP-22 first real-use bootstrap run returned `REJECTED` twice with matching source digests and `matches_rebuild=true`. Evidence: `experiments/exp-22-colibri-local-inference/evidence/bootstrap/FIRST_REAL_USE.md`.

This checkpoint is limited to the three confirmed harness defects from that run:

- **H-1** — stop-rule parser misses real boundary sections such as `## Boundaries` and `## Failure / stop criteria`, causing false `REJECTED`.
- **H-2** — markdown renderer hardcodes EXP-27 labels instead of describing the actual packet source/semantics.
- **H-3** — checkpoint-chain/disposition parsing ignores README-declared fields, producing incomplete genealogy for EXP-22.

### Required repair

1. Reproduce all three defects against the committed EXP-22 evidence before editing.
2. Make the smallest additive/targeted changes inside the existing EXP-29 harness only. Do not add a second parser, memory layer, registry, or new source of truth.
3. Preserve fail-closed behavior: broader parsing must not turn missing or ambiguous safety boundaries into silent `FRESH`.
4. Add regression tests for H-1/H-2/H-3 using EXP-22-shaped fixtures plus the existing EXP-27 fixture.
5. Rebuild a packet for **EXP-22 / CP-01** from current canonical Git and require verifier result **FRESH**.
6. Confirm the repaired packet contains:
   - non-empty checkpoint chain covering CP-01…CP-03;
   - disposition `EXPERIMENT` from canonical source;
   - applicable EXP-22 stop/boundary rules;
   - correct non-hardcoded markdown labels;
   - source refs/digests that verify against current Git.
7. Re-run the original EXP-29 negative controls and prove all six still fail closed as designed.
8. Record before/after real-use measurements and whether any extra rediscovery remains necessary for EXP-22 startup.

### Scope

Allowed changes:
- `experiments/exp-29-arena-bootstrap-harness/harness/**`;
- EXP-29 tests/evidence/results needed for CP-06;
- generated EXP-29/EXP-22 bootstrap evidence needed to prove the repair;
- registry/result metadata if required by the established experiment ritual.

Do not change EXP-22 Colibri conclusions, production code, governance, Router, contracts, gates, or unrelated experiments.

If fixing H-1/H-2/H-3 requires changing canonical source priority, safety authority, or adding persistent memory/orchestration, STOP with `DEEP_CHANGE_REQUIRED`.

### CP-06 PASS

PASS only if the same EXP-22/CP-01 case that previously returned `REJECTED` now returns **FRESH**, H-1/H-2/H-3 have regression coverage, EXP-27 remains valid, all six CP-04 negative controls still fail closed, and no production/governance boundary changes.

Open one bounded PR and do not merge.

## CP-07 — Canonical current-state gap (owner authorized 2026-10-09)

Trigger: CP-06 made the EXP-22/CP-01 bootstrap technically `FRESH`, but the packet still carried stale task state because the canonical EXP-22 registry entry remained `PLANNED` with a pre-run next action while `FINDINGS.md` recorded CP-01…CP-03 as already executed.

Primary decision: **EXTEND_EXISTING**.

This checkpoint must close the gap using the **existing canonical experiment state mechanisms first**. Do not add a new bootstrap source role, memory store, generic findings index, or automatic state inference unless the existing registry/results path is proven insufficient.

### Goal

A fresh Arena session receiving a verified EXP-22 bootstrap must correctly understand that:

- EXP-22 has already executed CP-01…CP-03;
- the result is `PARTIAL` / recommendation `HOLD`;
- structural compatibility was proven, but decision quality was not measured against released weights;
- the next authorized action is the bounded released-weight quality run on a weights-available suitable machine;
- CP-01 must **not** be repeated.

### Required order

1. Reproduce the state-gap on current `main` before editing:
   - build + verify EXP-22 bootstrap;
   - show that it is `FRESH` yet reports stale `PLANNED` / "execute CP-01" state;
   - confirm `FINDINGS.md` records CP-01…CP-03 as already run.
2. Audit the existing canonical state path:
   - `experiments/EXPERIMENT_REGISTRY.json`;
   - target experiment `README.md` / `RESULTS.md` convention;
   - EXP-29 builder's existing target-results source role;
   - dashboard/Reladraw regeneration ritual for registry changes.
3. Prefer the smallest canonical repair:
   - update the existing EXP-22 registry entry to the truthful terminal/current state;
   - add `experiments/exp-22-colibri-local-inference/RESULTS.md` only if needed to express the already-established experiment result in the repository's normal result format;
   - derive its content from the committed EXP-22 evidence/FINDINGS; do not reinterpret the experiment.
4. Rebuild EXP-22 / CP-01 bootstrap from current canonical sources and require `FRESH`.
5. Prove a fresh-session consumer can answer the current-state questions correctly **without reading FINDINGS.md**:
   - status/result;
   - completed checkpoints;
   - recommendation;
   - current limitation/blocker;
   - next authorized action;
   - whether CP-01 should run again (expected: **NO**).
6. Measure remaining rediscovery. The packet may point to canonical evidence for detail, but it must not require rediscovery merely to determine what has already been completed or what action comes next.
7. Re-run EXP-29 regression/negative-control tests and verify EXP-27 remains `FRESH`.
8. If the registry/results path cannot represent the current state without changing bootstrap source semantics, STOP and report the exact gap before adding any new source role.

### Canonical EXP-22 state to preserve

Use only already-committed EXP-22 evidence. Do not change its conclusion:

- `RESULT: PARTIAL`
- `RECOMMENDATION: HOLD`
- `DEEP_CHANGE: NO`
- structural decision-path proof: 66/66 HTTP 200, 0 malformed constrained outputs, 22/22 deterministic, 7–13 ms tiny-model latency at ~48 MB RSS;
- released-weight decision quality: **NOT measured** because the released checkpoint was unavailable in the original sandbox;
- next action: run the frozen fixtures against the released Laya checkpoint on a weights-available suitable machine; no production integration is authorized.

### Scope

Allowed:

- EXP-22 `RESULTS.md` / README status metadata if required for truthful canonical state;
- EXP-22 entry in `experiments/EXPERIMENT_REGISTRY.json`;
- required registry-driven Reladraw/dashboard artifacts;
- EXP-29 tests/evidence/results needed to prove CP-07;
- regenerated derived bootstrap packets.

Do not:

- rerun Colibri quality claims without released weights;
- change EXP-22 fixtures/conclusions;
- add a new source-of-truth or findings database;
- make FINDINGS.md automatically authoritative;
- change production code, governance, Router, contracts or gates;
- implement production Colibri integration.

### CP-07 PASS

PASS only if:

1. the pre-change `FRESH-but-stale-state` condition is reproduced;
2. the canonical EXP-22 state is corrected through existing registry/results mechanisms;
3. rebuilt EXP-22 bootstrap is `FRESH` and reports the truthful current result + next action;
4. a fresh isolated consumer does not propose repeating CP-01;
5. no new bootstrap source role or second source of truth was required;
6. EXP-29 negative controls and EXP-27 regression remain green;
7. registry/dashboard ritual and project validation pass.

Open one bounded PR and do not merge.
