# Murat Project Engineer — Operating Model

Status: ACTIVE
Updated: 2026-08-13
Architecture: Option A+ boundaries unchanged

## Purpose

This document connects the portfolio-level New Idea Filter with the existing per-task Murat Project Engineer execution model. It is policy/documentation only and does not create a runtime, queue, scheduler, persistent agent, memory service, or workflow engine.

## Lifecycle

### 1. Idea intake

Any new product, feature, service, agent, plugin, integration, automation, repository, or substantial technical idea first passes `docs/NEW_IDEA_FILTER_POLICY.md`.

The filter returns one primary disposition:

- `EXTEND_EXISTING`
- `REUSE_COMPONENT`
- `MERGE`
- `EXPERIMENT`
- `HOLD`
- `NEW_REPOSITORY`
- `REJECT`

No implementation starts before this disposition is recorded.

### 2. Project placement

If the disposition permits work, identify the target project's source-of-truth files and confirm that the idea fits the project's foundation, architecture, scope, priorities, and deep-change-gate.

`NEW_REPOSITORY` is exceptional and requires the evidence defined in the New Idea Filter Policy.

### 3. Execution classification

A concrete implementation task is classified using the existing MPE risk tiers:

- `FAST`
- `VERIFIED`
- `DEEP-CHANGE`

Portfolio disposition and execution risk are separate decisions. For example, an `EXTEND_EXISTING` idea can still be a `DEEP-CHANGE` task.

### 4. Bounded execution

For coordinator runs:

1. select the smallest sufficient Expert or temporary Expert Team;
2. use the applicable existing Playbook;
3. preserve observable handoffs where needed;
4. run deterministic gates before optional semantic review;
5. require explicit user approval for DEEP-CHANGE when applicable;
6. emit one terminal state: `PASS`, `REWORK`, `BLOCKED`, or `HUMAN_REQUIRED`.

### 5. Evidence

Measured Stage 2 work records:

- Run Report;
- Experiment Record;
- source/artifact references;
- rollback information;
- gate results;
- reviewer findings when used;
- architecture-pressure signals.

Do not store hidden chain-of-thought, secrets, agent lifecycle state, queue state, or invented metrics.

## Authority boundaries

- Codex remains the execution/orchestration environment.
- Murat Project Engineer remains a bounded coordinator and policy layer.
- Codex Router remains an inference/protocol/credential gateway only.
- Experts remain bounded roles, not persistent processes.
- Git/project files remain the source of truth.
- The deep-change-gate remains mandatory.

## Current Stage 2 rule

Continue validating this operating model through the 20-run evidence experiment before proposing architectural expansion.

A need for better ergonomics, batching, dashboards, or UI is not by itself evidence for a workflow engine, persistent agents, adaptive routing, or durable orchestration state.
