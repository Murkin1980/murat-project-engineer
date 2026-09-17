# Global Murat Project Engineer Enforcement

Status: ACTIVE / MANDATORY

## Purpose

Make the Murat Project Engineer New Idea Filter, Opinionated Workspace defaults, Human-Centered Value Delivery Principles, and Value Unit Economics the default decision, product, and economic gates across ChatGPT, Codex, repository work, and MPE-governed human-facing automation instead of relying on one conversation or one repository context.

## Canonical rule

Before implementing any new product, feature, service, agent, plugin, integration, automation, repository, or substantial technical idea, first run the Murat Project Engineer New Idea Filter defined in `docs/NEW_IDEA_FILTER_POLICY.md`.

The filter must produce exactly one primary disposition before implementation starts:

- EXTEND_EXISTING
- REUSE_COMPONENT
- MERGE
- EXPERIMENT
- HOLD
- NEW_REPOSITORY
- REJECT

If the proposal triggers the deep-change gate, implementation must stop until the user explicitly approves the deep change.

After placement into an existing project or approved experiment, resolve and use the project's current workspace defaults according to `docs/OPINIONATED_WORKSPACE_POLICY.md`. Do not silently introduce parallel hosting, storage, auth, AI gateway, workflow, deployment, or verification paths when existing project defaults satisfy the task.

For human-facing automation, process discovery, onboarding, workflow recommendations, AI agents acting on user work, usage/plan limits, monetization, or engagement mechanics, also apply `docs/HUMAN_VALUE_DELIVERY_PRINCIPLES.md` as a mandatory product-design input.

For automation value, ROI, process decomposition, reusable primitives, portfolio prioritization, or unit-economics decisions, also apply `docs/VALUE_UNIT_ECONOMICS.md`.

The canonical human-value rule is:

> Human involvement should be rewarded with visible relief.

Where safely possible, first-time value should include one completed improvement rather than analysis alone. If substantial execution must stop, the system must preserve a safe resumable state and handoff rather than abandon work mid-process.

The canonical value-unit hierarchy is:

```text
PROCESS -> TASK -> STEP -> ACTION -> WORK ATOM -> RELIEF ATOM -> VERIFIED RELIEF UNIT (VRU)
```

A detected opportunity or recommendation is not a completed VRU. Completed VRUs require implemented and verified relief. MPE should track `Unlock Value` for bottleneck-breaking improvements and `Reuse Multiplier` for primitives that can create value across multiple workflows or projects.

## Enforcement layers

### Layer 1 — ChatGPT global custom instruction

Use the following instruction in ChatGPT Custom Instructions:

> MURAT PROJECT ENGINEER GLOBAL RULE: Before implementing or recommending implementation of any new product, feature, service, agent, plugin, integration, automation, repository, or substantial technical idea for my projects, first apply the Murat Project Engineer New Idea Filter. Check overlap with active projects, extension/reuse/merge opportunities, duplication, measurable value, smallest validation experiment, portfolio priority, and deep-change risk. Return exactly one primary disposition: EXTEND_EXISTING, REUSE_COMPONENT, MERGE, EXPERIMENT, HOLD, NEW_REPOSITORY, or REJECT. Do not begin implementation or create a new repository before this disposition is recorded. If a deep change conflicts with current foundation/architecture, stop and require my explicit approval before implementation. Prefer strengthening existing active projects over creating parallel systems. After project placement, use the project's current Opinionated Workspace defaults for runtime, deployment, integrations, verification, rollback, and cost constraints instead of reopening settled infrastructure choices or silently adding parallel infrastructure. For human-facing automation and discovery, optimize for visible relief: observe real work where appropriate, find friction before choosing technology, prove bounded value before monetization when safely possible, and never abandon substantial work at an unusable state; preserve state/evidence/changes/result/blocker/next action/handoff so work resumes without rediscovery. For value/ROI/prioritization work, decompose toward Work Atoms, distinguish Relief Atoms from mere recommendations, count only verified outcomes as Verified Relief Units, and consider Unlock Value plus Reuse Multiplier when comparing candidates.

This layer covers ordinary ChatGPT conversations, including mobile use.

### Layer 2 — Codex global instruction

Install the same rule into `$CODEX_HOME/AGENTS.md` (normally `%USERPROFILE%\.codex\AGENTS.md` on Windows).

A repository-specific `AGENTS.md` may add more constraints but must not weaken this global rule for Murat projects.

Use `scripts/install_global_mpe_policy.ps1` to install or update the managed block without replacing unrelated existing global Codex instructions.

### Layer 3 — Repository source of truth

The canonical detailed policies remain:

- `docs/NEW_IDEA_FILTER_POLICY.md`
- `docs/OPINIONATED_WORKSPACE_POLICY.md`
- `docs/HUMAN_VALUE_DELIVERY_PRINCIPLES.md`
- `docs/VALUE_UNIT_ECONOMICS.md`
- `docs/GLOBAL_MPE_ENFORCEMENT.md`

Project repositories should reference these policies from their own `AGENTS.md` or project instructions where practical.

Human-facing projects should additionally define how they implement, measure, or intentionally defer the following where applicable:

- real-work evidence rather than interview-only truth;
- friction-first intervention selection;
- visible relief / Proof of Relief;
- first-session completed value;
- graceful handoff and resumability;
- no-rediscovery continuation;
- trust-preserving observation and non-manipulative gamification;
- value-based, non-coercive monetization;
- relevant Work Atoms and Relief Atoms;
- criteria/evidence for Verified Relief Units;
- Unlock Value for bottleneck-breaking changes;
- Reuse Multiplier for reusable primitives.

### Layer 4 — GitHub enforcement

For code/repository work, an MPE disposition should be recorded before substantial implementation begins. The resolved workspace default and any deviation should also be visible in the task/PR/run evidence when material. Repository CI or PR templates may enforce the presence of that decision record where the project warrants hard enforcement.

For human-facing workflow changes, PR/run evidence should state the human friction being reduced, the completed or planned relief, and the terminal/handoff behavior if execution is interrupted.

For value-bearing automation changes, evidence should distinguish hypothesis/observed/implemented/verified state and avoid presenting unverified opportunities as completed VRUs.

GitHub enforcement is a backstop, not a replacement for the ChatGPT/Codex decision gate.

## Mandatory graceful-handoff invariant

A substantial workflow that stops because of quota, credentials, approval, unavailable integration, external dependency, budget, model/context boundary, or another blocker must preserve enough information to resume safely.

Minimum contract:

- STATE — what is completed;
- EVIDENCE — what was learned or verified;
- CHANGES — what changed;
- RESULT — usable value already delivered;
- BLOCKER — why execution stopped;
- NEXT ACTION — the smallest next action required;
- HANDOFF — sufficient context/artifacts to resume without repeating work.

Where code or files changed, preserve applicable diff/commit/artifact/test/rollback evidence according to project governance.

Canonical continuation rule: **No rediscovery required** when the needed context and evidence were already captured.

## Precedence and safety

This policy does not override higher-priority system, developer, security, legal, privacy, or safety instructions.

This policy does not introduce a daemon, scheduler, workflow engine, persistent runtime agent, autonomous memory service, adaptive router, autonomous installer, workspace runtime, or Router authority change.

Opinionated Workspace is a default-resolution policy, not vendor lock. Defaults remain replaceable when evidence justifies change and applicable risk/deep-change gates are satisfied.

Human-centered observation does not authorize covert employee surveillance, productivity scoring, collection of unnecessary sensitive content, deceptive gamification, or false claims that automation occurred when only a recommendation was generated.

Value-unit economics does not authorize fabricated monetary precision. Where financial conversion is uncertain, preserve multidimensional value measures and confidence instead of inventing exact ROI.

## Verification

Global enforcement is considered installed when:

1. ChatGPT Custom Instructions contain the global MPE rule.
2. `%USERPROFILE%\.codex\AGENTS.md` contains the managed MPE block on the user's Windows machine.
3. The canonical policies remain versioned in `Murkin1980/murat-project-engineer`.
4. New substantial project ideas receive an MPE disposition before implementation.
5. Substantial implementation uses the project's current workspace defaults or records an evidence-backed deviation.
6. Human-facing projects reference or implement `docs/HUMAN_VALUE_DELIVERY_PRINCIPLES.md` where applicable.
7. Value-bearing automation/prioritization work references or implements `docs/VALUE_UNIT_ECONOMICS.md` where applicable.
8. Interrupted substantial workflows preserve a resumable handoff rather than an unusable partial state.
