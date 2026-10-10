# New Idea Filter Policy

Status: ACTIVE / MANDATORY  
Updated: 2026-10-05  
Scope: All Murat AI Stack projects and repositories

## Rule

Every new product, feature, service, agent, plugin, integration, automation, repository, or substantial technical idea must be evaluated through Murat Project Engineer before implementation starts.

No implementation or repository creation should begin from an unfiltered idea. The idea must pass this filter and receive a recorded disposition adhering to `contracts/NEW_IDEA_FILTER.md`.

---

## Required Filter Checks

For each candidate idea, Murat Project Engineer must execute these nine checks in strict order:

1. **Existing active project:** Does an existing active project already solve the same problem fully or partially?
2. **Extension possibility:** Can the idea be implemented as a bounded extension of an existing project without violating its foundation, architecture, scope, or deep-change-gate?
3. **Reusable component:** Can an existing component, module, skill, integration, or external pattern be reused instead of building a new system?
4. **Duplicate capability/infrastructure:** Does the idea create duplicate functionality, redundant infrastructure, or a competing product inside the current portfolio?
5. **Measurable business value:** What concrete, measurable user or business outcome justifies implementation now?
6. **Smallest useful experiment/MVP:** What is the smallest test or MVP that can validate the idea before deeper development?
7. **Priority versus current portfolio:** How does this idea rank against active portfolio priorities (e.g. active P0 commitments)? Does it justify the opportunity cost?
8. **Deep-change impact:** Does the idea touch protected architecture boundaries (MASTER, Router authority, credentials, persistent agents, central runtime, memory governance)?
9. **Explicit "do not build" constraints (Anti-roadmap):** Does the idea violate any explicit anti-roadmap constraints?

---

## Anti-Roadmap Layer ("Do Not Build" Constraints)

To prevent architectural drift and premature complexity, the following constraints are non-negotiable across MPE:

1. **No Unnecessary Repositories:** Do not create a new repository when an existing active repository can be extended or component reused.
2. **No Persistent Runtime Daemons:** Do not introduce daemons, schedulers, generic workflow engines, persistent agent runtimes, background services, or MCP servers into MPE.
3. **No Heavy Storage/Vector DBs:** Do not add Vector DBs, Knowledge Graphs, or external database engines for agent memory; use Git-native artifacts.
4. **No External Source-of-Truth Sync:** Do not move MPE source of truth into Notion, Airtable, or external platforms; Git remains the canonical source of truth.
5. **No Premature Digital Employee / Dots Abstractions:** Do not introduce ungrounded digital employee abstractions or complex persona topologies until simpler role contracts are proven insufficient.
6. **No Auto-Merge:** Do not enable autonomous or automated merging into `main`; human review and governed gates remain required.
7. **No Private Personal Data in Public Repositories:** Anti-roadmap constraints and idea records must be represented without embedding private personal data into public project files.
8. **No Assertions Over Evidence:** Never accept an agent claim as evidence of task completion without verifiable command/system artifacts.

---

## Terminal Decisions

Murat Project Engineer must return exactly one primary terminal disposition from the canonical seven:

- `EXTEND_EXISTING` — add the idea as a bounded feature or extension to an existing active project.
- `REUSE_COMPONENT` — reuse an existing internal or external component/pattern without new construction.
- `MERGE` — consolidate the idea with an overlapping project or workstream.
- `EXPERIMENT` — run a bounded, pre-registered validation experiment before product development.
- `HOLD` — record the idea with rationale, but defer development until defined prerequisites are met.
- `NEW_REPOSITORY` — create a new repository only when the idea cannot reasonably live inside an existing active project and satisfies the New Repository Gate.
- `REJECT` — do not pursue because it violates anti-roadmap constraints, duplicates capabilities, or lacks sufficient measurable value.

---

## Fail-Closed Rule

The filter must fail closed:
- If a **deep-change impact** or **fundamental architectural conflict** is detected during evaluation, the filter must NOT return `EXTEND_EXISTING` or `NEW_REPOSITORY` without explicit prior human approval.
- If an idea violates any **anti-roadmap constraint**, the disposition must immediately resolve to `REJECT` or `HOLD`.
- If required evidence or portfolio priority is ambiguous, the decision must default to `HOLD`, never to speculative development.

---

## New Repository Gate

Creating a new repository is the exception, not the default.

Before `NEW_REPOSITORY` is authorized, the evaluation must prove:
- no suitable existing active repository can be extended;
- a clearly distinct product or system boundary;
- a measurable outcome and verifiable validation path;
- no unnecessary duplication of data models, infrastructure, auth, AI gateways, UI systems, or agent orchestration;
- compatibility with current Murat AI Stack architecture and portfolio priorities.

---

## Portfolio Priority Rule

When a new idea competes for development capacity with an active P0 project, Murat Project Engineer must explicitly compare expected value, urgency, dependencies, and opportunity cost before recommending development.

Default rule: Until the portfolio is intentionally re-prioritized, new ideas should preferentially strengthen or validate current core projects rather than create parallel systems.
