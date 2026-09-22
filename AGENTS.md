<!-- MPE:SCOPE-CHANGE-CONTROL:START -->
## Mandatory first read — MPE Scope & Change Control

Before planning, coding, refactoring, dependency changes, testing strategy, deployment, or checkpoint execution, read:

- `docs/governance/SCOPE-CHANGE-CONTROL.md`

Read it before project-specific source-of-truth documents. Then follow this repository's local rules and the current checkpoint/spec.

The scope policy governs minimal change, reuse, checkpoint boundaries, deep-change, testing, evidence, merge/deploy authority, and stopping conditions.

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
