# Global Murat Project Engineer Enforcement

Status: ACTIVE / MANDATORY

## Purpose

Make the Murat Project Engineer New Idea Filter and Opinionated Workspace defaults the default decision gates across ChatGPT, Codex, and repository work instead of relying on one conversation or one repository context.

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

## Enforcement layers

### Layer 1 — ChatGPT global custom instruction

Use the following instruction in ChatGPT Custom Instructions:

> MURAT PROJECT ENGINEER GLOBAL RULE: Before implementing or recommending implementation of any new product, feature, service, agent, plugin, integration, automation, repository, or substantial technical idea for my projects, first apply the Murat Project Engineer New Idea Filter. Check overlap with active projects, extension/reuse/merge opportunities, duplication, measurable value, smallest validation experiment, portfolio priority, and deep-change risk. Return exactly one primary disposition: EXTEND_EXISTING, REUSE_COMPONENT, MERGE, EXPERIMENT, HOLD, NEW_REPOSITORY, or REJECT. Do not begin implementation or create a new repository before this disposition is recorded. If a deep change conflicts with current foundation/architecture, stop and require my explicit approval before implementation. Prefer strengthening existing active projects over creating parallel systems. After project placement, use the project's current Opinionated Workspace defaults for runtime, deployment, integrations, verification, rollback, and cost constraints instead of reopening settled infrastructure choices or silently adding parallel infrastructure.

This layer covers ordinary ChatGPT conversations, including mobile use.

### Layer 2 — Codex global instruction

Install the same rule into `$CODEX_HOME/AGENTS.md` (normally `%USERPROFILE%\.codex\AGENTS.md` on Windows).

A repository-specific `AGENTS.md` may add more constraints but must not weaken this global rule for Murat projects.

Use `scripts/install_global_mpe_policy.ps1` to install or update the managed block without replacing unrelated existing global Codex instructions.

### Layer 3 — Repository source of truth

The canonical detailed policies remain:

- `docs/NEW_IDEA_FILTER_POLICY.md`
- `docs/OPINIONATED_WORKSPACE_POLICY.md`
- `docs/GLOBAL_MPE_ENFORCEMENT.md`

Project repositories should reference these policies from their own `AGENTS.md` or project instructions where practical.

### Layer 4 — GitHub enforcement

For code/repository work, an MPE disposition should be recorded before substantial implementation begins. The resolved workspace default and any deviation should also be visible in the task/PR/run evidence when material. Repository CI or PR templates may enforce the presence of that decision record where the project warrants hard enforcement.

GitHub enforcement is a backstop, not a replacement for the ChatGPT/Codex decision gate.

## Precedence and safety

This policy does not override higher-priority system, developer, security, legal, or safety instructions.

This policy does not introduce a daemon, scheduler, workflow engine, persistent runtime agent, autonomous memory service, adaptive router, autonomous installer, workspace runtime, or Router authority change.

Opinionated Workspace is a default-resolution policy, not vendor lock. Defaults remain replaceable when evidence justifies change and applicable risk/deep-change gates are satisfied.

## Verification

Global enforcement is considered installed when:

1. ChatGPT Custom Instructions contain the global MPE rule.
2. `%USERPROFILE%\.codex\AGENTS.md` contains the managed MPE block on the user's Windows machine.
3. The canonical policies remain versioned in `Murkin1980/murat-project-engineer`.
4. New substantial project ideas receive an MPE disposition before implementation.
5. Substantial implementation uses the project's current workspace defaults or records an evidence-backed deviation.
