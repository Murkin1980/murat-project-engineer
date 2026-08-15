# Munder reuse decision

Primary disposition before execution: **EXPERIMENT**.

Terminal pilot decision: **REUSE_PATTERN**.

## Reuse now (design patterns only)

1. Typed, atomic filesystem mailbox envelopes mapped to MPE's existing `HANDOFF` fields.
2. A minimal append-only event vocabulary (`spawn`, `handoff`, `gate`, `terminal`) that compiles into existing Run Reports rather than becoming a second source of truth.
3. Explicit ephemeral lifecycle/worktree metadata for parallel runs, owned by Codex rather than a new GOD service.

## Do not adopt

- Munder GOD as orchestrator.
- Autonomous Codex bypass mode.
- Semantic shared memory as authoritative context.
- Scheduled missions, heartbeats, persistent agents, or workflow-engine state.
- Direct Munder dependency in MPE until the Windows Codex startup issue is fixed and a three-role smoke test passes.

## Portfolio decision

No new repository and no deep architectural change are justified. Any implementation of the three reuse patterns should be proposed separately through the New Idea Filter as a small extension to existing MPE contracts/evidence, with measurable reductions in handoff ambiguity or collision rate.

