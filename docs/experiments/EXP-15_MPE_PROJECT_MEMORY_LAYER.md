# EXP-15 — MPE Project Memory Layer

## Status

QUEUED

## New Idea Filter

**Decision: EXTEND_EXISTING**

This experiment extends Murat Project Engineer. It must not create a second memory authority, a parallel project-management system, or a new repository.

## Goal

Test whether a bounded project-memory layer can improve continuity between Task Packets, coding-agent executions, PR/evidence verification, and later tasks without weakening MPE source-of-truth rules.

The experiment compares the current MPE approach against a MemoryOS-inspired local-first pattern and borrows provenance/write-gating ideas from MemoryWiki.

## Hypothesis

A compact, structured project-memory context will reduce repeated rediscovery, contradictory decisions, and loss of rationale between agent sessions while preserving Git/project artifacts as the canonical source of truth.

## Scope

Prototype only inside the existing MPE architecture.

Candidate memory classes:

- decisions;
- outcomes;
- constraints;
- lessons;
- failed attempts;
- provenance/source references.

Before task execution, the agent should receive only relevant project memory, not the full historical transcript.

After execution, the agent may propose a bounded **Memory Delta**:

- `ADD`
- `UPDATE`
- `SUPERSEDE`
- `DELETE`
- `NO_CHANGE`

A proposed delta must not silently become canonical memory.

## Integration target

The experiment should fit the existing flow:

`Project Memory → Task Packet → Agent → PR/Evidence → Verification → Memory Delta → Approval → Project Memory`

It should reuse the existing MPE Task Packet, experiment/evidence conventions, and current project storage/index components where possible.

## Architectural constraints

1. Git/project files remain the source of truth.
2. No autonomous memory promotion during this experiment.
3. Memory writes are provenance-aware and write-gated.
4. No new repository.
5. No separate production memory service unless a later experiment proves the need.
6. The prototype must fail closed when provenance or write authorization is missing.
7. The memory layer must remain compatible with MPE Earned Autonomy levels; write authority cannot exceed the active autonomy level.

## Comparison baseline

Compare:

### A. Current MPE baseline

Task Packet + repository/docs/evidence without a dedicated bounded project-memory context.

### B. Memory-layer prototype

Same task flow plus:

- compact relevant-memory retrieval;
- decision/outcome/constraint recall;
- provenance metadata;
- proposed Memory Delta;
- approval-gated canonical update.

## Acceptance tests

The prototype is not considered ready until all six tests pass:

1. **RECALL** — returns the relevant fact/decision for a task.
2. **UPDATE** — a newer approved fact supersedes the old one correctly.
3. **DELETE** — an approved deletion removes the fact from future recall.
4. **ISOLATION** — unrelated projects/users/scopes do not leak into each other.
5. **PROVENANCE** — recalled facts expose their source/evidence.
6. **FAILURE** — if the memory/index layer is unavailable or inconsistent, MPE does not fabricate memory and falls back safely to canonical project artifacts.

## Minimal experiment

Use a small sample of real MPE development tasks that already have prior decisions/evidence.

For each task, measure baseline vs memory-layer prototype on:

- whether the correct prior decision was recalled;
- whether contradictory guidance was produced;
- time/tokens spent rediscovering context;
- number of unnecessary repo/document reads;
- provenance correctness;
- whether the proposed Memory Delta was valid;
- whether any unauthorized canonical write occurred.

## PASS criteria

PASS only if:

- all six acceptance tests pass;
- provenance is present for every promoted memory item;
- no cross-project memory leakage occurs;
- no unauthorized canonical memory write occurs;
- the prototype materially improves continuity or reduces rediscovery versus baseline;
- the experiment does not introduce a second source of truth.

## FAIL / REJECT criteria

Reject the layer if it:

- duplicates existing MPE artifacts without measurable benefit;
- becomes a second authority beside Git/project files;
- requires autonomous promotion to be useful;
- leaks memory across project/user scopes;
- cannot preserve provenance;
- adds operational complexity greater than the measured benefit.

## Reference patterns to study

- MemoryOS (vetrovk): local-first project/coding-agent memory, Markdown + index pattern, session/task continuity.
- MemoryWiki: provenance, conflict/history handling, episodic/semantic/procedural separation, write-gated memory changes.
- Graphiti: temporal/relationship ideas only as later research; do not add it to this MVP unless the simpler layer proves insufficient.

## Expected outcome

A decision on whether MPE should keep a minimal project-memory layer, reuse only selected patterns, or reject the added layer and stay with the current artifact-only approach.
