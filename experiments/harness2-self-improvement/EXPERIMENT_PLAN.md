# MPE Self-Improvement Lab — Harness2

Status: PROPOSED / DESIGN ONLY
Date: 2026-10-19
New Idea Filter: EXPERIMENT
Repository: Murkin1980/murat-project-engineer
Upstream: https://github.com/google-research/harness2
Scope: bounded series of isolated experiments; no production integrations.

## Purpose
Test whether recursive Propose-Probe-Compose and cross-task reflection improve the quality, efficiency and transferability of an existing MPE agent while preserving all governance safeguards. Extract reusable components only after independent evidence.

## Existing capabilities and placement
MPE already has coordinator, typed handoffs, source-of-truth policy, test/evidence gates and compute budget preflight. EXP-29 Arena bootstrap provides fresh context packets, not a self-improvement mechanism. Reuse existing evaluation and evidence patterns, do not duplicate memory, scheduler, Router, agent runtime, or infrastructure. This research is lower priority than shipping MPE/Business Discovery MVPs and must be budget capped.

## E0 — Audit and isolation
Pin upstream commit SHA and review current code, dependencies, licenses, network, sandbox, subprocess, cost, memory and persistence. The official upstream README warns that executor networking is unrestricted and the Codex sandbox is disabled. Never execute those defaults on the user's machine with secrets. Use a disposable isolated environment with outbound access denied, read-only sanitized fixtures, write access only to scratch, no project credentials, no live Git or deployment, capped time/compute/cost. Run only the deterministic no-credentials demo initially. If isolation cannot be independently confirmed, STOP.

## Dataset / oracle controls
Select 5-10 completed MPE cases with reproducible inputs and historical outcomes; reconstruct state at the point before the original fix. Freeze independent test rubric and outputs. Keep correct historical code, hidden tests and grading criteria inaccessible to the tested agent, including through Git history, network and caches. Partition exploratory vs held-out tasks; redact secrets. Pin versions, configuration, model and seeds. Repeat when budget permits.

## E1 — Reproduce solved work
Compare frozen baseline agent versus Harness2 with k=1 using identical task, model, tools, budget and scoring. Evaluate working result, independent correctness, retries, human corrections, wall time, token use and monetary cost. Do not assume a repeated result is learning.

## E2 — Improvement depth
Compare no recursion, k=1, k=3, k=5 and parallel/sequential. Control for extra compute. Report marginal benefit per token, cost and time; record negative or non-monotonic outcomes.

## E3 — Transfer between tasks
Run an ordered task stream with reflection from earlier tasks. Evaluate only on unseen held-out cases. Ablations: no memory; reflection only; harness changes only; both. The held-out solutions, tests and later tasks must not leak into the improvement context. Compare results at equal budget and against a non-learning baseline.

## E4 — Safe self-improvement
Use synthetic adversarial cases attempting to change governance, exfiltrate sensitive data, override immutable rubric, access network, alter canonical source, or bypass human review. Confirm prevention and immutable audit trace. Candidate prompt/tool/memory edits only in disposable scratch; never edit real AGENTS.md, governance, source of truth, credentials, Router or production settings.

## E5 — Reusable mechanisms
If evidence supports it, propose the smallest portable primitives: proposal/probe/comparison, reflection with scope-aware lessons, evaluation gate, rollback, contamination defense. Prefer existing MPE components. Integration, persistent service, new dependencies or changing authority requires a separate owner-approved deep-change checkpoint.

## Checkpoints
CP-SI-01: Read governance, inspect pinned upstream and existing MPE experiments, produce technical audit, sandbox threat model, fixture selection, frozen evaluator, run matrix and fixed budget. Documentation-only. STOP for review.
CP-SI-02: Independently verify isolation; deterministic demo and baseline reproducibility.
CP-SI-03: E1 baseline vs k=1 replay.
CP-SI-04: E2 recursion depth comparative matrix.
CP-SI-05: E3 cross-task transfer with ablations and held-out tasks.
CP-SI-06: E4 governance and security adversarial testing.
CP-SI-07: E5 extraction report with optional proposed owner gate.

## Metrics / decision
Primary: independently verified held-out task success, cost per correct task, and critical security/governance violations (required zero). Secondary: time-to-verified completion, retries, regressions, lesson reuse, human rework, reproducibility and confidence. Evaluate whether improvements exceed run-to-run variance. Do not count prospective benefits as Verified Relief Units until genuine relief is implemented and measured. If no robust gain, record NO_GAIN and do not extract.

## Evidence
Record run and upstream/MPE commits, fixtures and hashes, model, executor, k, mode, seed, egress/sandbox settings, actual token/cost metrics, evaluator ID, blinded rubrics, output hashes, logs, test results, safety findings, deviations, reviewer, result PASS/FAIL/PARTIAL/BLOCKED/UNVERIFIED, rollback and next action. Use existing repository evidence conventions.

## CP-SI-01 Arena / Codex instruction
Repository: Murkin1980/murat-project-engineer
Branch: experiment/harness2-self-improvement-lab (or a separate checkpoint branch from main, preserving this proposal).
Read AGENTS.md and docs/governance/SCOPE-CHANGE-CONTROL.md before anything else. Read NEW_IDEA_FILTER_POLICY, GLOBAL_MPE_ENFORCEMENT, OPINIONATED_WORKSPACE_POLICY, HUMAN_VALUE_DELIVERY_PRINCIPLES, VALUE_UNIT_ECONOMICS and this plan. Inspect current EXP-29 and existing experiments for safe reuse. Pin upstream google-research/harness2 SHA. Perform read-only code analysis, threat modeling, design of 5-10 case fixtures with protected oracles, fairness/cost plan, dependency and license assessment. Create only experiment documentation/evidence in a minimal-diff PR. No code execution of upstream with network permissions, no model-backed/paid run, no broad implementation, no source policy or Router edits, no credentials, no merges or deployment. STOP at CP-SI-01 and request owner approval for any deep change or new security boundary.
