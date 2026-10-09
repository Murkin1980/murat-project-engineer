# EXP-28 — Agent Workflow Skills: evidence-gated retrospective

Status: **COMPLETED — PASS**
Decision: **EXPERIMENT**
Adoption: **ADOPT_WITH_CHANGES** (manual, evidence-gated pattern only)
Owner: Murat Project Engineer
Repository: `Murkin1980/murat-project-engineer`

## Question

Can a deterministic, post-run retrospective identify real sources of wasted work and propose small, verifiable changes to navigation, instructions, or checks—without adding a second governance layer?

## Scope

This is a read-only reconstruction of three already completed Arena runs, plus one narrowly scoped instruction improvement for the still-authorized EXP-24 Phase 2 task:

1. **EXP-24 HyperFrames PR → Video, Phase 1 — PARTIAL** (2026-10-06). Phase 2 is not treated as a completed run.
2. **EXP-25 Atomic CRM component extraction — PASS** (2026-10-06).
3. **EXP-27 Paperclip orchestration patterns — PASS** (2026-10-06).

Primary records are each run's `ARENA_TASK.md`, `README.md`, `RESULTS.md`, and linked evidence. The source-of-truth and change boundary remain the existing MPE files; this experiment adds no runtime, service, agent, database, automation, persistent memory, production integration, or automatic post-run trigger.

## Reference

Reference extraction is pinned to `mattpocock/skills@b0618bc436ad893b3c5e84e55fba86586d34a404` (2026-10-08). Only the mechanics of `/retro`, `/pr`, and instruction review were inspected; no third-party skill was copied, installed, or integrated. The decisions and evidence are in [`RESULTS.md`](RESULTS.md).

## Method

For each run, reconstruct:

`task → executor actions → delays/errors → evidenced cause (or unknown) → smallest prevention`

Check five classes: context/file navigation; wrong or unnecessary execution path; errors a deterministic check could catch; instruction under/over-specification; repeated environment/tooling friction. A recommendation is eligible only when it has run-specific evidence, a root cause, a minimal change, an expected effect, a false-improvement risk, and a verification method. An isolated low-cost event defaults to `NO_CHANGE` unless it caused material cost or has strong evidence of recurrence.

## Outcome

The evidence supports **ADOPT_WITH_CHANGES**: keep a user-invoked, evidence-first review; adapt its candidate format to MPE's existing source-of-truth and change-control rules; never auto-write a rule or run it after every session. One task-local EXP-24 Phase 2 preflight clarification was applied. The measured navigation benefit is a previously recorded no-packet vs. context-packet comparison in EXP-27, not a claim that this retrospective itself saved wall-clock time. See [`RESULTS.md`](RESULTS.md) for exact limits and findings.
