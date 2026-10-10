<!-- MPE:SCOPE-CHANGE-CONTROL:START -->
## Mandatory first read — MPE Scope & Change Control

Before planning, coding, refactoring, dependency changes, testing strategy, deployment, or checkpoint execution, read:

- `docs/governance/SCOPE-CHANGE-CONTROL.md`

Read it before project-specific source-of-truth documents. Then follow this repository's local rules and the current checkpoint/spec.

The scope policy governs minimal change, reuse, checkpoint boundaries, deep-change, testing, evidence, change-size/merge-pressure, merge/deploy authority, and stopping conditions.

If a local rule appears to conflict with the scope policy, apply the documented source-of-truth priority. Do not silently weaken either rule; surface a deep-change conflict when required.
<!-- MPE:SCOPE-CHANGE-CONTROL:END -->

# AGENTS.md

Status: MANDATORY DEVELOPMENT INSTRUCTIONS
Project: Murat Project Engineer

## Required startup reading

Before substantial work in this repository, coding agents and developers MUST read the source-of-truth documents relevant to the task.

For any work involving human-facing automation, process discovery, onboarding, workflow recommendations, AI agents acting on user work, usage limits, monetization, or user engagement mechanics, the following document is mandatory reading before implementation:

- `docs/HUMAN_VALUE_DELIVERY_PRINCIPLES.md`

For any work involving automation value, ROI, prioritization, process decomposition, unit economics, MVP selection, reusable automation primitives, or comparing candidate improvements, also read and apply:

- `docs/VALUE_UNIT_ECONOMICS.md`

For any new substantial idea, product, feature, service, agent, plugin, integration, automation, or repository decision, also read and apply:

- `docs/NEW_IDEA_FILTER_POLICY.md`
- `docs/GLOBAL_MPE_ENFORCEMENT.md`
- `docs/OPINIONATED_WORKSPACE_POLICY.md`

For work involving Composio social-media publishing or moving ChatGPT-managed media into a publishing connector, also read and apply:

- `playbooks/composio-social-publishing.md`

## Mandatory human-value rules

Preserve these principles unless an explicit approved deep change says otherwise:

1. Human involvement should be rewarded with visible relief.
2. Observe real work where appropriate; do not rely only on self-reported process descriptions.
3. Find friction before choosing technology.
4. Gamification must represent real relief, not artificial engagement.
5. Prove value before pay whenever a safe bounded improvement can be delivered.
6. First-session value should include one completed improvement when safely possible.
7. Never stop substantial work at an unusable state; create a resumable handoff.
8. Resume without rediscovery whenever the necessary context/evidence was already captured.
9. Process observation must not silently become employee productivity scoring.
10. Do not claim relief or completed automation when only analysis/recommendation was produced.

## Mandatory value-unit rules

For substantial automation/value work:

1. Decompose the process toward the smallest useful `Work Atom`.
2. Distinguish a detected opportunity from a delivered `Relief Atom`.
3. Count a `Verified Relief Unit (VRU)` only after implemented relief is verified on a real or production-like outcome.
4. Track `Unlock Value` when one small fix enables downstream work.
5. Track `Reuse Multiplier` when a solved primitive can benefit multiple workflows/projects.
6. Prefer verified relief over activity metrics such as prompts, agent runs, model calls, feature count, or lines of code.
7. Do not invent project-specific incompatible value units when the canonical VRU model is sufficient.

## Graceful handoff contract

When execution must stop because of quota, credentials, approvals, unavailable integrations, external dependencies, budget, model/context boundaries, or other blockers, preserve at minimum:

- STATE
- EVIDENCE
- CHANGES
- RESULT
- BLOCKER
- NEXT ACTION
- HANDOFF

Where code or artifacts changed, preserve the applicable diff, commit, artifact, test, and rollback evidence required by the project's existing governance.

## Conflict rule

If an implementation materially conflicts with `docs/HUMAN_VALUE_DELIVERY_PRINCIPLES.md`, `docs/VALUE_UNIT_ECONOMICS.md`, or other mandatory MPE governance, stop and surface the conflict for the appropriate human/deep-change decision rather than silently weakening the rule.

## Scope

These instructions apply to human contributors and coding agents, including Arena, Codex, Claude Code, and other automated coding systems operating on this repository.


## Chat handoff format for Arena / Codex / coding-agent tasks

When the owner asks for instructions for Arena, Codex, Claude Code, or another coding agent:

1. Put the **complete authoritative instruction** in the relevant project repository, experiment directory, checkpoint file, or task file.
2. In chat, provide only a **short handoff block intended for copy/paste**.
3. The chat handoff block must include at minimum:
   - repository;
   - branch, when applicable;
   - exact path to the full instruction;
   - concise objective;
   - starting checkpoint/action;
   - critical stop/deep-change boundary when relevant.
4. Format the short handoff as a fenced code block so it can be copied directly.
5. Do not paste the full repository instruction into chat unless the owner explicitly asks for the full text.
6. If the repository instruction has not yet been created or updated, do that first; then return the short copyable handoff.
7. This rule applies even when the full instruction was just written during the same conversation.

The repository version is authoritative; the chat block is only a compact launch pointer.

### Reusable derived-artifact pattern rule

For tasks that transform an authoritative source into visual, media, interactive, training, presentation, or similar derived artifacts, read and evaluate:

- `docs/REUSABLE_DERIVED_ARTIFACT_PATTERN.md`

Prefer reuse of its stable source→beats/work-units→marks/cues/timings→asset-slots→QA→minimal-diff revision contract before designing a new parallel pipeline. Do not apply it to unrelated work where the structure adds no value.

### Reusable UI reconstruction pattern rule

For screenshot-to-code, UI parity, or reference-screen reconstruction tasks, read and evaluate:

- `docs/REUSABLE_UI_RECONSTRUCTION_PATTERN.md`

Default budget: 1 initial render + up to 3 targeted correction cycles, with early stop on diminishing returns. Prefer localized minimal-diff fixes, protect stabilized regions, validate mobile when applicable, and do not use 5 cycles by default.

### Arena bootstrap rule

For **Arena** tasks that are context-heavy, resume prior work, depend on multiple repository sources, or rely on accumulated experiment lessons, prepare the handoff with the validated EXP-29 bootstrap pattern before giving Arena the chat instruction.

Use:

- `experiments/exp-29-arena-bootstrap-harness/harness/bootstrap_builder.py`
- generated `ARENA_CONTEXT.json` / `ARENA_CONTEXT.md` as **derived, non-authoritative views only**
- canonical Git files as the source of truth

Required behavior:

1. Generate the bootstrap from the current canonical repository state for the target experiment/checkpoint.
2. Verify the packet is `FRESH` before referencing or handing it to Arena.
3. Include the bootstrap path in the short Arena handoff when the task is context-heavy or resumptive.
4. If verification returns `STALE` or `REJECTED`, regenerate or stop and resolve the source conflict; never let the packet override canonical Git.
5. Keep lessons scoped as `GLOBAL`, `PROJECT`, `TASK`, or `NO_CHANGE`; do not promote a one-off task lesson globally without evidence.
6. Do **not** require a bootstrap for a small self-contained task where it would add more context than it saves.

Until a separately approved shared helper replaces it, the EXP-29 harness is the reference implementation for Arena bootstrap generation and verification.
