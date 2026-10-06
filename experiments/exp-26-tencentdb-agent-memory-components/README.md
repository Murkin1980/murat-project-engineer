# EXP-26 — TencentDB Agent Memory component extraction

Status: PLANNED  
Decision: REUSE_COMPONENT  
Owner: Murat Project Engineer  
Repository: `Murkin1980/murat-project-engineer`  
Upstream: `TencentCloud/TencentDB-Agent-Memory`

## Purpose

Evaluate whether selected architectural patterns from TencentDB Agent Memory can measurably improve the already-proven EXP-15 MPE memory approach without introducing a second memory platform, new source of truth, persistent service, or parallel orchestration layer.

This is a donor-component experiment, not a platform adoption.

Primary question:

> Can symbolic short-term compaction and layered progressive-disclosure recall improve MPE memory efficiency or recall quality beyond the existing EXP-15 baseline, while preserving Git as canonical source of truth and current approval/isolation rules?

## New Idea Filter

Primary disposition: **REUSE_COMPONENT**

### Existing project fit

MPE already has EXP-15 memory evidence and a bounded file-backed memory model. Therefore TencentDB Agent Memory must not become a competing memory product.

### Reuse target

Evaluate only reusable patterns/components that can strengthen the existing approach:

1. **Symbolic short-term memory / compaction**
   - condense large tool/session outputs into a compact state representation;
   - preserve drill-down references to raw evidence;
   - avoid repeatedly loading raw logs.

2. **Layered long-term memory / progressive disclosure**
   - compare flat recall against layered recall;
   - preserve provenance and explicit source references;
   - retrieve the smallest useful amount of memory first, then drill down only when needed.

3. **Retrieval fallback ideas**
   - inspect BM25 / keyword / hybrid retrieval patterns only as references;
   - do not introduce embeddings or a vector database unless a later separately approved checkpoint proves they are necessary.

## Explicit non-goals

Do NOT:
- deploy MemoryCore, Memory Hub, Proxy, or the full TencentDB Agent Memory stack;
- create a new repository;
- create a new daemon/service;
- add a vector database;
- add a second canonical memory store;
- change MPE Router authority;
- migrate EXP-15 data;
- enable automatic cross-project sharing;
- add background memory extraction;
- add autonomous memory writes;
- add production persistence infrastructure;
- change the source of truth away from Git.

The upstream project is a donor/reference only.

## Existing baseline

Use EXP-15 as the baseline and source of frozen memory cases.

Read:
- `experiments/exp-15-memory/2026-09-30/README.md`
- `experiments/exp-15-memory/2026-09-30/RESULTS.md`
- `experiments/exp-15-memory/2026-09-30/BASELINE.md`
- `experiments/exp-15-memory/2026-09-30/ACCEPTANCE_TESTS.md`

Do not re-run unrelated EXP-15 work unless needed for direct comparison.

## Upstream facts to verify

Before implementation, verify against current upstream:
- license;
- current release/commit used;
- short-term symbolic memory architecture;
- layered memory structure;
- retrieval modes;
- local storage/runtime assumptions;
- security/isolation model;
- whether useful pieces can be reused conceptually or in a tiny isolated harness without running the full stack.

Record exact upstream commit/tag used.

## Checkpoint CP-01 — Architecture extraction

Produce a concise component map:

```text
TencentDB concept/component
→ problem it solves
→ EXP-15 equivalent
→ overlap
→ possible incremental value
→ adoption risk
→ keep / reject
```

At minimum evaluate:
- symbolic short-term compaction;
- layered L0/L1/L2/L3-style memory;
- progressive disclosure/drill-down;
- provenance/reference preservation;
- BM25/keyword/hybrid recall;
- agent/team visibility/isolation concepts.

CP-01 passes only if at least one donor mechanism offers plausible incremental value over EXP-15 without requiring a parallel runtime.

If none does, stop with FAIL / DO_NOT_ADOPT.

## Checkpoint CP-02 — Frozen comparison design

Use the same bounded EXP-15-style tasks or an equivalent frozen subset.

Create three modes:

### Mode A — EXP-15 baseline
Existing file-backed memory / current retrieval behavior.

### Mode B — symbolic compaction
Same source material, but raw/session/tool information is represented through a compact symbolic or structured top-level state with drill-down references.

### Mode C — layered recall
Same source material, organized into a small hierarchy that supports progressive disclosure rather than loading a flat result set.

Do not combine B and C until each is individually measurable.

## Checkpoint CP-03 — Minimal harness

Build the smallest experiment-only harness needed to compare A/B/C.

Prefer:
- standard library;
- existing repository dependencies;
- local files;
- deterministic fixtures.

Do not add a server if a script/test harness can prove the point.

Do not add a database unless the comparison is impossible without one. If a database becomes necessary, stop and report the deep-change implication instead of implementing it.

## Required measurements

For each mode measure where applicable:

- correct prior-decision recall;
- source/provenance accuracy;
- context lines loaded;
- approximate token footprint if deterministically measurable;
- number of document/raw-log reads;
- rediscovery steps;
- false-positive recall;
- isolation violations;
- unauthorized write attempts;
- drill-down operations required;
- implementation complexity.

Do not claim a VRU unless the experiment demonstrates actual verified relief on a real or production-like workflow.

## Acceptance

### PASS
At least one donor mechanism improves a meaningful EXP-15 metric while preserving recall correctness, provenance, isolation, and Git canonicality, with a small implementation footprint and no parallel infrastructure.

### PARTIAL
The donor mechanism shows useful signal but needs one bounded unresolved validation step, or the Arena environment prevents direct measurement.

### FAIL
No meaningful improvement over EXP-15, excessive complexity, weakened provenance/isolation, or dependence on a parallel runtime/service.

## Final adoption result

Return one:
- ADOPT
- ADOPT_WITH_CHANGES
- DO_NOT_ADOPT

If adopted, name the exact reusable mechanism(s). Do not recommend adopting the whole TencentDB Agent Memory platform unless a future separately authorized deep-change evaluation explicitly asks for that.

## Evidence

Keep experiment evidence under:

`experiments/exp-26-tencentdb-agent-memory-components/`

Minimum artifacts:
- `UPSTREAM_AUDIT.md`
- `COMPONENT_MAP.md`
- frozen fixtures or references
- comparison outputs
- `RESULTS.md`

If a harness is created, keep it experiment-local.

## Mandatory startup

Before work:
1. read `AGENTS.md`;
2. read `docs/governance/SCOPE-CHANGE-CONTROL.md`;
3. read mandatory New Idea / Global / Workspace governance;
4. read the EXP-15 baseline files listed above;
5. read this README;
6. read `ARENA_TASK.md`.

## Stop conditions

Stop and report before:
- deploying a persistent TencentDB memory service;
- adding a new database/vector store;
- introducing automatic writes or sharing;
- changing Git canonicality;
- changing Router authority;
- creating a new repo;
- adding recurring paid infrastructure;
- broad production integration.

## Completion boundary

Stop after:
- one bounded A/B/C comparison;
- PASS/PARTIAL/FAIL;
- ADOPT / ADOPT_WITH_CHANGES / DO_NOT_ADOPT;
- exact component-level recommendation.

Do not continue into production integration.
