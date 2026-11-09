# EXP-41 — DeepSeek SuperAgent / Harness research intake

Status: PLANNED / RESEARCH ONLY
Date: 2026-11-09
Primary disposition: EXTEND_EXISTING
Owner: Murat Project Engineer
Canonical parent: EXP-41 — Harness² self-improvement lab
Existing plan: experiments/harness2-self-improvement/EXPERIMENT_PLAN.md
Reference: https://pimenov.ai/knowledge/superagent-deepseek-harness-perevod/#section-1-superagent

## Registration and deduplication

DeepSeek SuperAgent architecture is a research case within registered EXP-41, **not** a new EXP-47, separate agent runtime, or independent self-improvement experiment. Registry already assigns EXP-41 to Harness², EXP-45 to MCC bounded agents, and EXP-46 to HackerTube; EXP-34 remains retired/unassigned. Preserve all existing experiment identities and FIFO history.

Reuse EXP-29's canonical Git-derived bootstrap, existing MPE approval/evidence/guardrails, and existing MCC bounded-agent research. Do not duplicate a Router, scheduler, watchdog, memory store, dashboard or infrastructure.

## Candidate ideas for comparison (not authorization to implement)

- Central routing vs existing MPE coordination and typed handoffs.
- Event-driven handoffs vs existing GitHub/CI/checkpoint workflows.
- Worker isolation and watchdog safety vs existing evidence gates and review processes.
- Session-independent task state vs EXP-29 bootstrap and scoped lessons.
- Asynchronous orchestration and MCC visibility vs EXP-45 (security-first) research.

## Minimal work and allocation

Route this intake through the **existing** EXP-41 CP-SI-01 (upstream audit and design-only review). Compare DeepSeek against Harness² and present MPE capabilities. Assess upstream authenticity, code/license provenance, dependencies, secrets/network permissions, sandbox risks and operating cost before any installation. Identify overlapping mechanisms, measurable user benefit, and the smallest safe read-only test.

EXP-29: source of reusable bootstrap components, not reopened or renumbered.
EXP-45: MCC-related comparison/reuse only, not a subproject with modified permissions.

No separate CP numbers are created. Any extension to CP-SI-02…07 needs its own scope review and authorization under the existing plan.

## Success measures

Baseline vs proposed mechanism: time needed to resume a stopped Codex/Work task, rediscovery steps, factual handoff errors, human corrections, verified task completion and total cost. No Verified Relief Unit is claimed from a proposal or analysis.

## Explicit boundaries

No autonomous agent launch, event subscription, networked upstream execution, credentials, new repository, persistent runtime, production code changes, policy changes, merge or deploy. No changes to permissions or canonical source-of-truth. Deep-change triggers STOP and require explicit owner approval. No PASS claim without measured evidence.

Next action: CP-SI-01 read-only technical audit, report for owner review; no activation of subsequent checkpoints.
