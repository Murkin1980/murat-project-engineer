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

## Planned execution

See `ARENA_TASK.md`.

Execution is intentionally queued **after the currently active EXP-20 Dify/OpenHands component-extraction experiment**. No EXP-29 implementation is authorized before the owner starts it.
