# EXP-29 — Arena Bootstrap Harness

Status: **PLANNED**
Primary disposition: **REUSE_COMPONENT**

## Purpose

Test whether a fresh Arena session can recover the minimum useful working context for a task from canonical MPE repository sources without relying on chat history, a memory database, a vector store, or a second source of truth.

The concept is intentionally "memory without memory": Arena starts fresh, while MPE assembles a short derived startup packet from Git-backed evidence.

## Reused evidence

- EXP-27 showed that a derived context packet can preserve task genealogy while sharply reducing rediscovery input.
- EXP-28 showed that lessons should be promoted only from evidence and that task-local fixes are preferable to new global policy for isolated incidents.
- Existing MPE graceful-handoff rules already require resumable state and "resume without rediscovery" where evidence exists.

## Hypothesis

A deterministic bootstrap packet assembled from existing canonical files can reduce rediscovery, context bytes, and tool calls before first useful work without creating an independent memory authority.

## Boundaries

This experiment must not create:

- a memory service;
- a vector database;
- a daemon or scheduler;
- automatic memory promotion;
- a persistent agent runtime;
- a second canonical source of truth;
- Router authority changes;
- global AGENTS.md rule growth merely to feed the packet.

Generated bootstrap artifacts are derived views only and must carry source references/digests.

## Executed checkpoints

See `ARENA_TASK.md` and `RESULTS.md`.

- **CP-01** — existing capability map (`CAPABILITY_MAP.md`): every need covered by
  KEEP_EXISTING / REUSE / EXTEND; duplicates (memory store, lesson index,
  automatic promotion) rejected; no `DEEP_CHANGE_REQUIRED`.
- **CP-02** — deterministic bootstrap builder (`harness/bootstrap_builder.py`):
  derives `ARENA_CONTEXT.json` / `ARENA_CONTEXT.md` from canonical Git sources
  with sha256 provenance and a fail-closed `verify` (FRESH / STALE / REJECTED).
- **CP-03** — fresh-session A/B comparison on the frozen fixture EXP-27:
  Arm A 5 files / 84,900 B / 7 tool ops vs Arm B 1 file / 12,782 B / 1 tool op
  (84.94% fewer context bytes; identical answers). *Byte figures superseded by
  CP-06: the EXP-27 packet was regenerated (AGENTS.md digest refresh, additive
  `disposition_sources`); current values are in RESULTS.md, CP-06.*
- **CP-04** — six stale/unsafe negative controls, all fail-closed
  (4 STALE, 2 REJECTED); canonical sources digest-identical before/after.
- **CP-05** — PASS / REUSE_COMPONENT; PR opened, not merged.
- **CP-06** — first real-use repair (H-1 stop-rule boundary sections, H-2
  source-true markdown labels, H-3 README-declared checkpoint chain and
  disposition, with ambiguous disposition refused): EXP-22/CP-01 now verifies
  FRESH (was REJECTED); six negative controls still fail closed; regression
  tests in `tests/test_exp29_bootstrap.py`. Not merged. See RESULTS.md, CP-06.

EXP-20 (Dify/OpenHands component extraction) was complete before this
experiment started, satisfying the queue condition.
