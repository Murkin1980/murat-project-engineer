# Murat Project Engineer — Stage 2 Experiment Plan

Date: 2026-08-11  
Status: ACTIVE  
Purpose: validate whether Murat Project Engineer v1.0 improves real project execution enough to justify keeping or expanding the architecture.

## Decision boundary

Stage 2 is an evidence-gathering phase, not an architecture expansion.

Do **not** add a daemon, scheduler, generic workflow engine, persistent runtime agents, autonomous memory promotion, Router task orchestration, or Prime Agent runtime integration during this stage.

A move toward Option B (Pattern Hybrid) requires evidence from the experiment and a separate deep-change RFC/approval.

## Primary question

Does the v1.0 disciplined coordinator improve correctness, review quality, interruption recovery, and execution clarity at acceptable overhead compared with the simpler baseline Codex workflow?

## Experiment size

Run 20 representative tasks across real Murat AI Stack projects.

Target split:

- 6 FAST runs
- 10 VERIFIED runs
- 4 DEEP-CHANGE classification exercises or approved deep-change runs

Include at least 5 baseline runs using the prior simpler Codex approach on comparable task classes.

## Representative project mix

Use real work where practical:

1. Murat Project Engineer
2. MebelDocs KZ / mebeldocs-ai
3. MebelLegal KZ
4. Furniture Layout / Configurator
5. Furniture Production or related operational tooling
6. Furniture Sales / customer-facing workflow
7. Codex Router maintenance tasks that do not change Router authority

Do not force equal representation. Prefer actual work that would have been done anyway.

## Task classes to cover

At minimum, include examples of:

- small documentation/configuration change
- isolated bug fix
- feature implementation
- refactor with regression risk
- repository/release readiness review
- external research feeding an engineering decision
- UI or interaction change
- data/schema-sensitive change
- security/permissions-sensitive change
- interrupted task resumed from handoff/context artifacts

## Run procedure

For every Murat Project Engineer run:

1. Read source-of-truth files for the target project.
2. Classify risk as FAST, VERIFIED, or DEEP-CHANGE.
3. Select the smallest sufficient Expert or temporary Team.
4. Select the matching Playbook.
5. Record route profile/model resolution when observable.
6. Execute the task.
7. Run mandatory deterministic gates before semantic review.
8. Use an independent Reviewer/Judge only where the playbook/risk requires it.
9. Record rework and human intervention.
10. Emit one terminal state: PASS, REWORK, BLOCKED, or HUMAN_REQUIRED.
11. Complete one Experiment Record and one compact Run Report.

For baseline runs, record the same measurable fields where possible, but do not retroactively simulate Expert/Team behavior.

## Required evidence per run

Each run should preserve observable evidence, not hidden reasoning:

- task and acceptance criteria
- source-of-truth references
- risk classification
- selected playbook
- Expert/Team used
- model/route resolution if observable
- files changed
- deterministic gate results
- reviewer findings
- rework count
- human intervention
- interruption/recovery issue, if any
- escaped defect discovered after PASS, if any
- rollback information
- approximate usage/cost if observable

## Success metrics

Track these across the 20 runs:

### Quality

- deterministic gate failure rate before final PASS
- defects escaped after PASS
- reviewer findings that caused useful rework
- reviewer false positives
- acceptance criteria missed before final review

### Efficiency

- rework count
- human interventions
- obvious redundant expert/reviewer calls
- approximate token/cost overhead when observable
- whether the selected risk tier was judged excessive or insufficient afterward

### Recoverability

- can a run be resumed from source-of-truth + handoff + Run Report without reconstructing hidden context?
- did interruption cause duplicated work or contradictory decisions?

### Architecture pressure

Explicitly mark whether a run showed a real need for:

- fan-out/fan-in coordination
- durable runtime state beyond versioned files
- machine-readable workflow state
- generic workflow execution
- persistent agents

A single preference for convenience is not sufficient evidence for architecture expansion.

## Stage 2 exit criteria

After 20 runs, produce `STAGE2_EXPERIMENT_REVIEW.md` containing:

1. run matrix and task distribution
2. baseline vs coordinator comparison
3. quality findings
4. overhead findings
5. interruption/recovery findings
6. reviewer value and false-positive rate
7. repeated fan-out/fan-in evidence
8. architecture-pressure evidence
9. recommendation: KEEP A+ | ADJUST A+ | RFC OPTION B | STOP

## Option B trigger

Recommend an RFC for Option B only if repeated evidence shows that human-readable runbooks and versioned handoffs are insufficient, for example:

- gates are repeatedly skipped or inconsistently applied despite correct use
- multiple real tasks require recurring fan-out/fan-in that becomes error-prone
- interruption recovery repeatedly fails because state cannot be reconstructed
- orchestration bookkeeping becomes a material source of defects or excessive overhead

Any Option B proposal remains subject to the deep-change-gate.

## First five suggested runs

Use these as the starting queue unless real work provides better candidates:

1. Murat Project Engineer — documentation/status hygiene (FAST)
2. Furniture Configurator — small bounded UI/interaction change (VERIFIED)
3. MebelDocs KZ — isolated document-generation or validation bug (VERIFIED)
4. MebelLegal KZ — research-backed legal workflow change with deterministic checks (VERIFIED)
5. Murat Project Engineer — interrupted/resumed maintenance task to test recoverability (VERIFIED)

## Guardrails

- No architecture expansion during measurement.
- No automatic memory promotion.
- No secrets in reports or handoffs.
- No hidden chain-of-thought in artifacts.
- No permanent model binding to Expert roles.
- Router remains inference/protocol/credential gateway only.
- Project source-of-truth files override stale session notes.
