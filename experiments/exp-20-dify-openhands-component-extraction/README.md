# EXP-20 — Dify/OpenHands Component Extraction

Status: COMPLETED — **PASS** (executed 2026-10-09, `REUSE_COMPONENT`, pattern level only)

## Execution record

- Authoritative checkpoint instruction: [`ARENA_TASK.md`](ARENA_TASK.md)
- Phase 0 + CP-01 upstream audit and pins: [`UPSTREAM_AUDIT.md`](UPSTREAM_AUDIT.md)
- CP-01 component map (`component → existing Murat equivalent → gap → disposition`):
  [`COMPONENT_MAP.md`](COMPONENT_MAP.md)
- CP-02 duplicate filter: [`DUPLICATE_FILTER.md`](DUPLICATE_FILTER.md)
- CP-03 bounded proofs and measurements: `harness/`, `evidence/`
- Result, checks, limitations, next action: [`RESULTS.md`](RESULTS.md)

Two components reached proof and both passed: crash-tolerant/idempotent event evidence
(OpenHands `EventLog` subset, `BORROW`) and deterministic failure classification onto the
existing gate vocabulary (OpenHands `error_classification` + Dify typed tool errors,
`BORROW`). The prioritized candidates were **not** forced: the OpenHands sandbox/executor
boundary and the Dify workflow representation are `REJECT — DEEP_CHANGE_REQUIRED`, and the
Dify typed tool/provider abstraction is `REJECT` for MPE (no consumer). No production file
was changed and neither platform was installed, deployed, or executed.

Vocabulary note: this planning document originally listed `KEEP / BORROW / ADAPT / IGNORE`.
The executed checkpoints use the four dispositions required by `ARENA_TASK.md` —
`KEEP_EXISTING / BORROW / ADAPT / REJECT` — which supersede that earlier list. The planning
text below is preserved unchanged as the pre-execution record.

## Decision

Primary MPE disposition: REUSE_COMPONENT.

Do not adopt Dify or OpenHands as full platforms and do not create a new repository. Treat both projects as external architecture/component references and identify only the capabilities that materially fill an existing gap in the Murat AI Stack.

## Sources

- Dify: https://github.com/langgenius/dify
- OpenHands: https://github.com/OpenHands/OpenHands

## Hypothesis

Useful capabilities from Dify and OpenHands can be extracted or adapted into existing MPE/AI-stack projects without introducing a parallel agent platform.

## Candidate capabilities

### Dify

- workflow orchestration patterns
- tool/MCP abstraction
- RAG and knowledge ingestion pipelines
- structured workflow outputs
- AI workflow observability

### OpenHands

- agent execution loop
- sandbox/workspace isolation
- repository/workspace abstraction
- task → agent → result lifecycle
- coding-agent execution patterns
- event/automation architecture

## Existing-system mapping

First compare each candidate capability against:

- Murat Project Engineer
- Business Discovery / Business Value Engine
- MebelFlow AI
- existing AI gateway
- existing transcription gateway
- existing agent/orchestration components

Classification for each candidate:

- KEEP — existing internal capability is sufficient.
- BORROW — reuse an architectural pattern or implementation where licensing permits.
- ADAPT — reproduce the useful behavior using the existing stack.
- IGNORE — no current measurable need.

## Acceptance criteria

1. No new repository is created.
2. No full Dify/OpenHands deployment is required for the experiment.
3. Existing components are checked before proposing new abstractions.
4. Candidate capabilities are mapped to concrete current gaps.
5. License compatibility is checked before copying source code.
6. At least one bounded proof demonstrates whether a selected capability provides measurable relief or reuse value.
7. No source-of-truth, security boundary, or approved MPE architecture invariant is changed.

## Next action

Perform a comparative architecture audit of Dify and OpenHands against the current MPE/AI-stack components, then select the smallest candidate capability for a bounded proof.

## Constraints

This experiment does not authorize a new agent platform, persistent autonomous runtime, new repository, production deployment, or replacement of MPE governance.
