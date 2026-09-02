# EXP-14 — OpenClaw Runtime Patterns for MPE

Status: QUEUED / NOT_STARTED  
Disposition: EXTEND_EXISTING  
Added: 2026-09-03

## Purpose

Evaluate selected OpenClaw 2.0 / 2026.8.1 runtime patterns as bounded extensions to Murat Project Engineer. Do not create a parallel platform and do not make OpenClaw a production dependency during this experiment.

Primary user scenario:

`smartphone -> MPE Dashboard -> Task Packet -> cloud/remote worker -> GitHub -> verification -> durable visual status`

## Hypothesis

MPE can improve remote execution visibility and smartphone-first control by reusing a small set of architectural patterns demonstrated by OpenClaw, while preserving the existing MPE coordinator, gates, evidence model, Git boundaries, and deep-change rules.

## First experiment scope

Priority 1:

1. Cloud / Remote Session pattern.
2. Durable Progress Card pattern.
3. Map the result onto the existing Task Packet -> execution -> verification -> checkpoint flow.

Target progress states for evaluation:

- QUEUED
- RUNNING
- TESTING
- BROWSER_VERIFY
- GIT_DIFF
- CHECKPOINT
- PASS
- UNVERIFIED
- BLOCKED

The experiment must determine whether this can be represented as bounded state/evidence around existing MPE execution rather than as a new workflow runtime.

## Secondary candidates

Evaluate only after the first experiment is complete:

- Browser Evidence integration patterns.
- Secret Boundary / destination-scoped credential handling.
- Persistent operation permissions with separate READ / WRITE / DEPLOY / MONEY / DEEP_CHANGE scopes.
- Skillization Workshop: repeated successful workflows -> skill candidates -> review -> approval.
- Model Router contract for selecting provider/model/runtime without moving orchestration authority into the router.

## Reuse targets

Prefer existing components before adding anything new:

- MPE Task Packet / execution workflow.
- `dashboard/` project status surface.
- existing Browser Evidence and Git diff/checkpoint rules.
- existing runtime coordination contracts and helpers.
- existing New Idea Filter and DEEP-CHANGE gate.
- existing skillization policy and skills structure.
- existing Codex Router boundaries.

## Explicit non-goals

- No new repository.
- No full OpenClaw migration.
- No production OpenClaw dependency.
- No daemon, scheduler, generic DAG/workflow engine, persistent autonomous agent runtime, shared orchestration database, or independent memory service.
- No change of Router authority.
- No automatic credential exposure to model context.
- No autonomous deployment or money-spending permissions.

## Deep-change guard

STOP and request explicit approval before any implementation that introduces or requires:

- persistent orchestration state beyond the bounded evidence/status model;
- daemon/poller/retry worker/scheduler;
- generic workflow runtime;
- persistent agents;
- shared runtime database/message bus;
- adaptive routing authority;
- Prime Agent runtime integration;
- core architecture redesign.

## Minimum experiment / MVP

Use one existing MPE-controlled project and one bounded Task Packet.

Success path:

1. Create/preview Task Packet.
2. Start a bounded remote/cloud execution session.
3. Surface durable execution state in a Progress Card.
4. Record tests and Browser Evidence where applicable.
5. Record Git diff/checkpoint state.
6. Confirm that any post-verification change resets PASS to UNVERIFIED.
7. Confirm cancel/stop remains possible before irreversible action.

## Success criteria

PASS only if the experiment shows measurable improvement over the current flow in at least three of these dimensions:

- smartphone usability;
- execution visibility;
- interruption recovery;
- verification traceability;
- lower manual status checking;
- lower coordination overhead;

And only if it does so without violating the existing MPE boundaries.

## Failure / hold criteria

HOLD or REJECT the pattern if it:

- duplicates existing MPE functionality without measurable benefit;
- requires a new orchestration platform to be authoritative;
- makes OpenClaw a mandatory production dependency;
- weakens evidence, Git, credential, or approval boundaries;
- introduces deep-change without explicit approval.

## Expected output

Produce a short evaluation containing:

- architecture mapping: OpenClaw pattern -> existing MPE component;
- what can be reused unchanged;
- smallest required extension;
- measured result;
- risks;
- final disposition for each tested pattern: REUSE_COMPONENT, EXTEND_EXISTING, HOLD, or REJECT.

Do not proceed to secondary candidates until Priority 1 has an evidence-backed result.
