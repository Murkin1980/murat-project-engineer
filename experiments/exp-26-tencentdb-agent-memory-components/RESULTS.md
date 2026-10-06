# EXP-26 — Results and component-level recommendation

- **Run date:** 2026-10-06 UTC
- **New Idea Filter disposition:** `REUSE_COMPONENT`
- **Experiment result:** **PARTIAL**
- **Adoption result:** **ADOPT_WITH_CHANGES**
- **Scope:** four frozen EXP-15 cases; no platform installation, new service, database, vector store, or production integration.

## Executive result

The current EXP-15 file-backed memory (A) already recalled every registered decision and constraint without reading canonical source documents at query time. The donor-inspired representations therefore did **not** improve recall correctness or reduce source-document reads. They did reduce the serialized context packet while retaining the tested facts and citations:

- **B — symbolic packet:** 51.1% fewer UTF-8 bytes and 76.9% fewer context lines than A.
- **C — layered scenario card:** 41.7% fewer bytes and 38.5% fewer lines than A for the frozen question, with provenance references included in the top layer.
- If C is expanded with full L1 item details, it needs one optional batched L1 lookup per case and grows to 164 lines / 8,082 bytes / about 2,021 heuristic tokens total, larger than A's 104 lines / 5,099 bytes / about 1,277 tokens.

The result is **PARTIAL**, not PASS: B is a deterministic serialization proxy because EXP-15 has no frozen raw session/tool-result logs; this does not verify TencentDB's actual long-log offload, summarization, or task-success effects. C's benefit is conditional on a task needing scenario bootstrap without all item metadata. Recall quality was already at ceiling in A.

## A/B/C measurements

All rows aggregate the same four tasks. Token figures are `ceil(UTF-8 bytes / 4)`, an approximate deterministic proxy, not a tokenizer measurement.

| Arm | Context lines | UTF-8 bytes | Approx. tokens | Decision recall | Constraint recall | False-positive items | Canonical doc/raw-log reads for query | Logical primary lookups | Required provenance drill-downs |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **A — current EXP-15 memory** | 104 | 5,099 | 1,277 | 4/4 | 4/4 | 0 | 0 | 4 | 0 |
| **B — symbolic short-term packet** | 24 | 2,492 | 625 | 4/4 | 4/4 | 0 | 0 | 4 | 0 |
| **C — layered progressive card** | 64 | 2,975 | 745 | 4/4 | 4/4 | 0 | 0 | 4 | 0 |

| Arm | Line reduction vs A | Byte reduction vs A | Provenance visible in initial context | Extra optional detail lookup |
|---|---:|---:|---|---:|
| A | 0% | 0% | Yes, full records | 0 |
| B | 76.9% | 51.1% | Yes, full refs attached to fact nodes | 0 |
| C | 38.5% | 41.7% | Yes, refs + L1 IDs in the L2 card | 4 total (one per case, only for extra L1 metadata) |

Per case, A used 26 lines (1,229–1,338 bytes), B used 6 lines (580–673 bytes), and C used 16 lines (699–792 bytes). C's optional full-detail view used 41 lines per case; its complete optional-detail total was 164 lines / 8,082 bytes / about 2,021 heuristic tokens.

### Reads, provenance, isolation, and writes

- **Retrieval source reads:** 0 canonical-document/raw-log reads in all arms for the fixed questions. The frozen EXP-15 memory fixture was loaded once; each query used its topic key. A and B made one logical recall lookup per case; C made one L2 scenario lookup per case. Shared evaluation—not recall—read **10 unique source files** to validate provenance paths and line-anchor ranges.
- **Decision/constraint recall:** 4/4 cases in every arm. A/B/C all preserve the frozen predicate oracle. No model was called; this is deterministic information-preservation testing, not an LLM answer-quality benchmark.
- **False positives:** 0 extra memory IDs across the four exact topic queries in each arm.
- **Provenance:** 16/16 cited file paths exist. Only **15/16 line anchors are in range**. The inherited invalid pointer is `MEM-MPE-006 → evidence/stage2/RUN-12_REPORT.json#L41`; that frozen JSON has 37 lines. Its second source (`docs/experiments/EXP-12_CLEARS_TRIAGE.md#L80`) exists. B and C preserve the original references, including the invalid one. The validator checks path/range only, not whether the cited line semantically proves the fact.
- **Isolation:** 0 cross-project leakage in the EXP-15 multi-project fixture for A, B, or C.
- **Write gate:** 3 deliberate unauthorized `NO_CHANGE` probes (one per arm), all rejected against temporary copies; 0 unauthorized mutations and 0 canonical fixture changes. Experiment output files were written only under EXP-26.
- **Complexity:** A uses the existing store; B is one transient serializer; C is a transient scoped topic index/card plus an optional L1 pointer resolver. 0 production files, dependencies, services, databases, vector stores, or persistent memory writes were added.

## Checkpoint and verification status

| Checkpoint/check | Result | Evidence |
|---|---|---|
| CP-01 architecture extraction | PASS — two bounded read-time patterns show plausible context savings without parallel runtime | [`UPSTREAM_AUDIT.md`](UPSTREAM_AUDIT.md), [`COMPONENT_MAP.md`](COMPONENT_MAP.md) |
| CP-02 frozen A/B/C comparison | PASS — four EXP-15 cases, same topic keys and IDs, all three arms executed | [`FIXED_CASES.md`](FIXED_CASES.md), [`evidence/comparison.json`](evidence/comparison.json) |
| CP-03 minimal harness | PASS — experiment-local Python standard-library harness; no service/dependency | `harness/compare_memory_components.py` |
| Python syntax | PASS — `python -m py_compile .../compare_memory_components.py` | command run 2026-10-06 |
| JSON syntax | PASS — registry and frozen JSON fixtures parse | `python -m json.tool` |
| Frozen input hashes | PASS — all four pinned EXP-15 inputs matched before execution | `evidence/comparison.json` |

The experiment terminal result remains **PARTIAL** because these checkpoint passes do not validate raw tool-log offload on this dataset and the frozen baseline has one out-of-range source anchor.

Full machine evidence and per-case context strings: [`evidence/comparison.json`](evidence/comparison.json). Human-readable runner output: [`evidence/comparison.log`](evidence/comparison.log). Reproduction and input pins: [`FIXED_CASES.md`](FIXED_CASES.md).

## Exact components to reuse

1. **Transient symbolic task packet:** preserve the full approved decision/constraint summaries, stable memory item IDs, and canonical source refs while omitting nonessential item metadata from the active context. Keep this a read-time projection; do not replace or update the underlying EXP-15 item.
2. **Read-only L2 scenario card:** scope by project/topic; include complete first-pass decision and constraint text plus compact L1 IDs and provenance references. Fetch full L1 details only when actually needed. Derive the card from canonical EXP-15 records; do not persist a parallel summary store.
3. **Reference/budget discipline:** every compressed or layered fact remains traceable to Git; use bounded context and explicit drill-down rather than broad loading. Add path/line-anchor validation before trusting refs.

Do **not** reuse/install the MemoryCore/Hub/Proxy/Knowledge platform, SQLite or vector backends, embedding/hybrid retrieval, background extraction, team-memory sharing, autonomous writes, or production routing. BM25/hybrid retrieval was not justified by this four-topic exact-match benchmark.

## Why PARTIAL / ADOPT_WITH_CHANGES

- The measured improvement is context serialization size, not more correct decisions, fewer canonical reads, less rediscovery, or verified real-world relief.
- The B arm does not have raw tool-output fixtures and therefore cannot prove actual upstream short-term log compaction.
- C saves context only when full item metadata can remain deferred; if it is needed, the L1 drill-down makes the total larger than A.
- The frozen baseline contains one invalid line anchor. Changing the fixture to conceal it would break the freeze; future use should validate/fix such citations through the normal approved memory-delta process.

`ADOPT_WITH_CHANGES` means retain the two narrow, read-only patterns as component-level candidates for future bounded use **only where the task has a large enough context set to justify them**. It does not authorize production integration or a persistent index. No Verified Relief Unit is claimed: no live or production-like workflow was changed or measured.
