# EXP-27 — Paperclip orchestration patterns

Status: PLANNED

## Decision

Primary MPE disposition: REUSE_COMPONENT.

Paperclip is a donor/reference for orchestration patterns. Do not adopt it wholesale, do not create a parallel control plane, and do not move MPE governance or project source-of-truth into Paperclip.

## Sources

- Paperclip: https://github.com/paperclipai/paperclip
- Habr overview: https://habr.com/ru/articles/1012490/

## Fit for Murat stack

Estimated overall usefulness: **82% as a pattern/component donor**, not as a product to deploy.

Component-level estimate:

| Pattern | Usefulness |
|---|---:|
| Goal context / ancestry | 95% |
| Atomic task checkout / lease | 92% |
| Persistent task/run history | 90% |
| Approval / governance gates | 88% |
| Budget + runaway protection | 85% |
| Heartbeats / routines | 80% |
| Runtime skills injection | 78% |
| Paperclip wholesale deployment | 42% |

Expected actual reuse is closer to 20–30% of Paperclip concepts/mechanics.

## Primary target

Reuse should land primarily in **murat-ai-orchestrator** and be surfaced by MPE/dashboard rather than becoming a separate Paperclip service.

Priority chain:

`task lease → goal context → persistent evidence → budget guard → approval gate`

## Hypothesis

For an existing MPE/Arena/Codex workflow, a small set of Paperclip-inspired control-plane patterns can reduce duplicate execution and context loss while improving resumability, evidence quality and runaway protection without creating a second orchestration system.

## Bounded experiment

Use one existing MPE engineering workflow with a small number of agent runs.

### CP-01 — Goal context
Pass the executor a compact chain:

`project → goal → experiment/CP → task`

Measure whether the executor can state the parent goal and preserve it through completion.

### CP-02 — Atomic task lease
Ensure only one executor can own the same task at a time. A second attempt must fail or return an explicit already-owned state.

### CP-03 — Persistent evidence
Persist plan, run state, blockers, outputs and terminal status next to the task so a fresh executor can resume without reconstructing the full chat history.

### CP-04 — Budget / runaway guard
Apply bounded limits for retries, wall time, tool calls and, where observable, token/cost usage. Crossing a hard limit must stop or block execution rather than silently continuing.

### CP-05 — Approval gate
A task that reaches an integration-sensitive boundary must return READY/WARNING/BLOCKED and require the existing MPE approval path before merge/deploy/deep-change.

## Measurements

- duplicate task executions;
- context rediscovery steps;
- resume success from persisted evidence;
- retries/tool calls/wall time;
- human review burden;
- evidence completeness;
- compatibility with existing READY/WARNING/BLOCKED governance;
- incremental complexity versus current MPE/orchestrator mechanisms.

## Acceptance criteria

1. No new repository.
2. No permanent Paperclip service.
3. No production source-of-truth change.
4. MPE remains the governance/decision layer.
5. Existing project repositories remain canonical for their artifacts.
6. Atomic lease behavior is demonstrated.
7. Goal ancestry is available to the executor.
8. A fresh executor can resume from persisted evidence without relying on chat history.
9. At least one hard resource/runaway boundary is demonstrated.
10. Approval/deep-change boundaries remain under existing MPE rules.
11. Any adopted mechanism maps to an existing component before implementation.
12. Source-code reuse requires a separate license/dependency review.

## Success outcome

PASS does **not** mean “install Paperclip”.

PASS means there is evidence to implement the smallest useful subset inside existing systems, prioritizing:

1. task lease;
2. goal context;
3. persistent evidence;
4. budget guard;
5. approval gate.

## Next action

Arena performs CP-01 through CP-05 against one existing MPE engineering workflow and returns PASS/PARTIAL/FAIL plus exact component-level adoption guidance for murat-ai-orchestrator.
