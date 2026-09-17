# AGENTS.md

Status: MANDATORY DEVELOPMENT INSTRUCTIONS
Project: Murat Project Engineer

## Required startup reading

Before substantial work in this repository, coding agents and developers MUST read the source-of-truth documents relevant to the task.

For any work involving human-facing automation, process discovery, onboarding, workflow recommendations, AI agents acting on user work, usage limits, monetization, or user engagement mechanics, the following document is mandatory reading before implementation:

- `docs/HUMAN_VALUE_DELIVERY_PRINCIPLES.md`

For any new substantial idea, product, feature, service, agent, plugin, integration, automation, or repository decision, also read and apply:

- `docs/NEW_IDEA_FILTER_POLICY.md`
- `docs/GLOBAL_MPE_ENFORCEMENT.md`
- `docs/OPINIONATED_WORKSPACE_POLICY.md`

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

If an implementation materially conflicts with `docs/HUMAN_VALUE_DELIVERY_PRINCIPLES.md` or other mandatory MPE governance, stop and surface the conflict for the appropriate human/deep-change decision rather than silently weakening the rule.

## Scope

These instructions apply to human contributors and coding agents, including Arena, Codex, Claude Code, and other automated coding systems operating on this repository.
