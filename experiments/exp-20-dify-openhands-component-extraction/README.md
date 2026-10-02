# EXP-20 — Dify/OpenHands Component Extraction

Status: PLANNED

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
