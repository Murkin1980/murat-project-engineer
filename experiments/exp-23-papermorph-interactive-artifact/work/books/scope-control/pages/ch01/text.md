# Smallest Sufficient Change

## page 1

MPE Scope & Change Control
Status: MANDATORY
Version: 2026-09-24
Canonical source:
`Murkin1980/murat-project-engineer/docs/governance/SCOPE-CHANGE-CONTROL.md`
This policy defines the default execution discipline for Murat Project
Engineer repositories and coding agents.
Project-specific rules MAY be stricter. They MUST NOT silently weaken this
policy.
1. Primary principle
Perform the task with the smallest sufficient correct change.
The goal is the requested behavior with the minimum necessary new code,
dependencies, infrastructure, configuration, abstractions, and unrelated
edits.
Simplicity first.
Explicit current owner instructions take priority unless they conflict with
fundamental project rules, security requirements, an approved architecture
invariant, or the deep-change gate.
2. Source of truth
For the current task, use this priority order:
1. Explicit current owner instruction.
2. Current approved checkpoint/spec.
3. Repository-local mandatory governance and project instructions.
4. Existing architecture/product/domain contracts.
5. Existing code and tests.
6. Historical conventions and prior decisions.
If sources materially conflict, do not silently choose the convenient
interpretation. Surface the conflict and follow the higher-priority source
unless a deep-change decision is required.
3. Checkpoint is the task boundary

## page 2

When work is governed by a checkpoint/spec:
    implement only that checkpoint;
    do not invent the next checkpoint;
    do not prebuild later work;
    do not turn a discovered opportunity into current scope;
    stop when the approved checkpoint is complete;
    if the spec says `STOP`, stop.
A new checkpoint begins only after an owner instruction or committed
owner-approved spec authorizes it.
4. Before editing
Inspect only the code and call paths needed to make the change safely.
Do not explore the whole repository for a small task.
Determine:
    where the behavior lives;
    which call path is relevant;
    which existing component/pattern already solves similar work;
    which tests cover the behavior;
    which architecture constraints apply.
Make a small obvious fix directly. Use a short plan only when the approach is
unclear, multiple subsystems are affected, or consequences are substantial.
Resolve ordinary implementation details independently.
5. New Idea Filter
Before implementing any new substantial idea, product, feature, service,
agent, plugin, integration, automation, or repository, evaluate:
    can an active project be extended;
    can an existing component be reused;
    does this duplicate existing capability or infrastructure;
    is there measurable business value;
    can it be tested as a minimal experiment/MVP;
    what is its priority relative to active projects;
    is it a deep-change.
