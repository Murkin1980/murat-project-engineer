# EXP-32 — OpenMuse component evaluation

Status: PLANNED (registration only)
Date: 2026-10-16
Owner: Murat Project Engineer
Primary New Idea Filter disposition: REUSE_COMPONENT
Source: https://www.copilotkit.ai/openmuse?ref=producthunt
Source code: https://github.com/CopilotKit/OpenMuse

## Goal

Evaluate specific reusable patterns from OpenMuse for the *existing* Murat AI Stack. This is not approval to deploy OpenMuse as a second personal agent, to add a runtime, or to create a repository.

## Existing projects / candidates

- `murat-ai-orchestrator`: browser session ownership, resumable task execution and AG-UI interoperability.
- MPE Control Center and `business-discovery`: interactive rich-message patterns and human approval surfaces.
- `minibase-cloudflare`: examine state/artifact handoff interfaces without replacing storage or source of truth.

## Bounded evaluation (next checkpoint: CP-01, not yet executed)

1. Confirm upstream repository, license, supported providers, dependencies, maintenance status and architecture from actual code at a pinned commit.
2. Compare browser control (observe / handoff), task checkpoint/recovery, and AG-UI rich-result rendering with *current* existing internal solutions.
3. Document precise reusable files/components, licensing obligations, integration cost, API/security and state boundaries, deployment compatibility (Cloudflare defaults), and rollback.
4. Run a local isolated synthetic proof only if the existing architecture permits it without new credentials, persistence or infrastructure; otherwise mark BLOCKED or HOLD.
5. Report component-by-component ADOPT / ADOPT_WITH_CHANGES / DO_NOT_ADOPT with evidence, not marketing claims.

## Success criteria

- At least one component/pattern demonstrates a measurable improvement in implementation effort, verified task recovery, or human-visible interaction quality against an existing baseline.
- No duplicate orchestrator, auth, storage, model router, persistent browser infrastructure, autonomous authority, or production dependency is introduced.
- Security / consent / cost and open-source license conditions are documented.
- Findings are reproducible with pinned upstream revision and minimal evidence.

## Safety / deep-change stop

STOP and request explicit owner approval before changing production architecture, persistent agent authority, browser access to live logged-in accounts, secrets or credentials, model routing, memory source of truth, infrastructure or paid services. Never perform account actions without explicit authority. This registration alone authorizes no execution, migration or integration.

## State

STATE: PLANNED
EVIDENCE: prior conceptual comparison; source implementation not yet verified
CHANGES: registration documentation only
RESULT: not tested
BLOCKER: none for read-only CP-01
NEXT ACTION: assign Arena the isolated CP-01 audit and record findings
HANDOFF: use this file and the mandatory MPE governance documents as the source of truth.
