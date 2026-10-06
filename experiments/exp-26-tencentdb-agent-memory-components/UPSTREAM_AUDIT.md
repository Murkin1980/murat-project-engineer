# EXP-26 upstream audit — TencentCloud/TencentDB-Agent-Memory

**Audit date:** 2026-10-06 UTC

**Purpose:** inspect candidate donor mechanisms only. No clone, package install, runtime, service, or data migration was performed. No upstream source code was copied.

## Pin and release status

- Repository default branch at audit: `feat/server_team`.
- Audited source snapshot: commit [`8b86874a2daea49e3ff0fb53d699203146c5c77d`](https://github.com/TencentCloud/TencentDB-Agent-Memory/tree/8b86874a2daea49e3ff0fb53d699203146c5c77d), the branch head reported by `git ls-remote` on 2026-10-06.
- Latest non-prerelease release reported by GitHub: `v2.0.1`, commit [`a5dcbe6e9fee0d1d1e32d935326f1d3bcf927fdb`](https://github.com/TencentCloud/TencentDB-Agent-Memory/releases/tag/v2.0.1). The repository also exposes the prerelease `v2.0.2-beta.3` at `5017e2bb927c65bd8302af2d984b04db46303f1b`; the code audit is pinned to the default-branch commit above, not that tag.
- The pinned [`LICENSE`](https://github.com/TencentCloud/TencentDB-Agent-Memory/blob/8b86874a2daea49e3ff0fb53d699203146c5c77d/LICENSE) text explicitly grants the project under MIT (copyright 2026 Tencent). GitHub's repository API returned `NOASSERTION` for its license metadata, so the text file is the evidence for the MIT statement. No code is copied into MPE by this experiment.

## Candidate mechanism 1 — symbolic short-term compaction

The pinned [`MemoryCore README`](https://github.com/TencentCloud/TencentDB-Agent-Memory/blob/8b86874a2daea49e3ff0fb53d/MemoryCore/README.md) and offload implementation describe an in-session context-offload path, distinct from long-term cross-session memory:

- [`OffloadEntry`](https://github.com/TencentCloud/TencentDB-Agent-Memory/blob/8b86874a2daea49e3ff0fb53d/MemoryCore/src/offload/types.ts) associates a tool-call ID with a concise result summary, a `result_ref` to the full result, an optional Mermaid `node_id`, timestamp, and replaceability score.
- [`l2-mermaid.ts`](https://github.com/TencentCloud/TencentDB-Agent-Memory/blob/8b86874a2daea49e3ff0fb53d/MemoryCore/src/offload/pipelines/l2-mermaid.ts) assigns and maintains node mappings for the task canvas.
- [`compaction-handler.ts`](https://github.com/TencentCloud/TencentDB-Agent-Memory/blob/8b86874a2daea49e3ff0fb53d/MemoryCore/src/offload_server/compact/compaction-handler.ts) applies recorded compaction state and selects fast-path, mild, aggressive, or emergency handling from context pressure.
- [`compressor.ts`](https://github.com/TencentCloud/TencentDB-Agent-Memory/blob/8b86874a2daea49e3ff0fb53d/MemoryCore/src/offload_server/compact/compressor.ts) uses score-gated summary replacement and pressure-based deletion; the upstream implementation uses a tokenizer for its own budget.
- [`mmd-injector.ts`](https://github.com/TencentCloud/TencentDB-Agent-Memory/blob/8b86874a2daea49e3ff0fb53d/MemoryCore/src/offload_server/compact/mmd-injector.ts) injects/deduplicates active and historical Mermaid summaries and associates history with node IDs.

**Potential donor:** the structural rule “keep a small task-state view, preserve stable IDs and references to the original evidence, and load full results only when needed.” The upstream compression thresholds, host hooks, LLM-generated summaries, token-calibration machinery, and write/state lifecycle are not adopted.

**Fit limitation:** none of the frozen EXP-15 cases contains a raw long-running session or tool-result transcript. EXP-26 can compare compact representations of the existing memory records, but cannot establish that this upstream mechanism reduces raw-log tokens or improves task success. B is therefore explicitly a deterministic representation proxy, not an upstream compactor benchmark.

## Candidate mechanism 2 — layered progressive-disclosure recall

The pinned [root README technical overview](https://github.com/TencentCloud/TencentDB-Agent-Memory/blob/8b86874a2daea49e3ff0fb53d699203146c5c77d/README.md#technical-implementation) defines a four-layer hierarchy:

- **L0 Conversation:** raw source and exact wording;
- **L1 Atom:** actionable facts, constraints, preferences, and events;
- **L2 Scenario:** project/scenario context for task bootstrap;
- **L3 Core/Persona:** stable user/team profile.

Retrieval normally bootstraps from higher-level context, then searches lower-level detail using keyword, embedding, or hybrid/BM25+RRF paths within item/character/time budgets. [`auto-recall.ts`](https://github.com/TencentCloud/TencentDB-Agent-Memory/blob/8b86874a2daea49e3ff0fb53d699203146c5c77d/MemoryCore/src/core/hooks/auto-recall.ts) shows L1 search alongside L3 profile and L2 scene navigation. [`scene-navigation.ts`](https://github.com/TencentCloud/TencentDB-Agent-Memory/blob/8b86874a2daea49e3ff0fb53d699203146c5c77d/MemoryCore/src/core/scene/scene-navigation.ts) renders summaries and paths intended for on-demand reads.

**Potential donor:** one project-scoped scenario capsule (L2) with explicit links to existing fact records (L1) and canonical files (L0); load full fact metadata only when requested. The EXP-26 C arm models just this narrow read path. It does not add personas, a memory extraction pipeline, semantic search, or another source of truth.

## Runtime, storage, and isolation assumptions

The pinned [`MemoryCore README`](https://github.com/TencentCloud/TencentDB-Agent-Memory/blob/8b86874a2daea49e3ff0fb53d699203146c5c77d/MemoryCore/README.md#runtime) documents a Node.js `>=22.16.0` HTTP Gateway (default `127.0.0.1:8420`), SQLite plus local files, and in-process pipeline state. Extraction/aggregation uses an OpenAI-compatible LLM API; BM25 is available without an embedding service. The full Agent Memory product additionally includes Gateway/Hub/Proxy/Knowledge capabilities and deploy tooling. These are platform/runtime assumptions, not components required for this local experiment.

The upstream team memory model uses Team/User/Agent identity and asset visibility/ACLs; the recommended v3 data plane requires `team_id`, `agent_id`, and `user_id`. That is a distinct access-control model. EXP-15 already scopes memory by project and has a frozen cross-project isolation fixture, so the experiment preserves that boundary instead of importing a new team/agent authority layer.

## Audit conclusion

**Donor-only.** The potentially reusable elements are:

1. a compact, symbolic task-context view that retains item IDs and evidence references; and
2. a scoped L2 scenario index/card that links to L1 records and defers nonessential detail.

They are useful only as bounded read-time projections over the existing Git-backed EXP-15 memory. Do not install TencentDB Agent Memory as a platform, copy its service stack, add a database/vector store, enable autonomous capture, or alter production routing/source-of-truth.
