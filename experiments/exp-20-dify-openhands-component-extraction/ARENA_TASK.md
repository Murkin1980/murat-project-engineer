# EXP-20 — ARENA_TASK (owner instruction, frozen at execution time)

Status: EXECUTED — see `RESULTS.md`
Repository: `Murkin1980/murat-project-engineer` (only)
Branch: `arena/6f37b26a-murat-project-engineer`
Base commit: `21ad8ba2b200f385372668715685f802148a2c83`
Instruction recorded: 2026-10-09

This file is the authoritative checkpoint instruction for EXP-20. `README.md` is the
earlier planning document (disposition `REUSE_COMPONENT`, candidate list); where the two
differ, this file governs.

## Boundary

Do **not** create: a new repository, a workflow platform, a control plane, a persistent
agent runtime, a database, or a separate orchestration service.

## Goal

Determine which individual components and architectural patterns from **Dify** and
**OpenHands** can be reused in existing Murat projects — primarily Murat Project Engineer,
Business Discovery, MebelFlow AI, `murat-ai-orchestrator`, and the existing
AI/transcription gateways.

Not a platform comparison ("which is better"). The only question is:

> What exactly can we extract and embed into existing tools without duplicating the
> architecture we already have?

## Phase 0 — audit

Read before changing anything: `AGENTS.md`; `STATUS.md`;
`docs/NEW_IDEA_FILTER_POLICY.md`; the EXP-20 README/task; existing MPE
Router/orchestrator/runtime material; the relevant EXP-11, EXP-25, EXP-27.

Pin the upstream Dify and OpenHands versions/commits. Install nothing wholesale.

## CP-01 — Component map

For both upstreams build:

```text
component → existing Murat equivalent → gap → disposition
```

Use only: `KEEP_EXISTING`, `BORROW`, `ADAPT`, `REJECT`.

Search at least these categories: tool execution; sandbox/executor isolation;
task/session state; human approval; retries/error recovery; context packaging;
observability; model/provider abstraction; workflow representation; plugin/tool registry.

If the function already exists in Murat — `KEEP_EXISTING` by default.

## CP-02 — Duplicate filter

Separately identify everything that duplicates: MPE governance; `murat-ai-orchestrator`;
Router; MiniBase; Paperclip-derived patterns; the existing approval/evidence model.

A component must not be transferred only because the upstream implemented it more
beautifully. It must show **measurable additional value**.

## CP-03 — Smallest bounded proof

Choose **at most 2** components with the greatest potential benefit. For each, build a
minimal isolated proof inside EXP-20. No production integration. Preferably use one real
MPE fixture/task.

Verify: correctness; deterministic behaviour where possible; failure mode; rollback;
overhead; volume of new code; conflict with the existing architecture.

## Special interest

Check with priority, if they really exist upstream:

1. OpenHands — sandbox/executor boundary and resumable execution.
2. Dify — typed tool/provider abstraction or workflow representation.

But **do not force** these options if the audit shows an equivalent already exists.

## Stop rules

If the best component requires: a new persistent runtime; a shared workflow DB; a Router
authority change; a separate scheduler/queue; a new canonical source of truth; a generic
DAG engine — stop for that component with `DEEP_CHANGE_REQUIRED` and do not implement it.

## Acceptance

PASS only if: both upstreams are really audited; a component map exists; duplicates are
explicitly filtered; at most 2 candidates reached proof; at least one shows measurable
benefit over the existing MPE; it is proven that full-platform adoption is not needed;
production was not changed.

If there are no useful components, `PASS / REJECT` is also an acceptable good result.

## Checks

Run: `python3 scripts/validate_package.py .`; the full unittest baseline before/after;
the specialized proof tests; `git diff --check`; secrets/scope checks.

Do not fix pre-existing failures inside EXP-20 without direct necessity.

## Result

Return: `RESULT: PASS / PARTIAL / FAIL`; the final recommendation; the
`KEEP_EXISTING / BORROW / ADAPT / REJECT` map; which 1–2 components were proven; the
measurable benefit; what was rejected as duplication; tests; changed files; commit SHA; PR.

**Open the PR, do not merge it.**
