# EXP-26 frozen comparison cases

**Freeze source:** EXP-15 run dated 2026-09-30. The fixtures below are used in place; EXP-15 files are not copied or edited.

| Input | SHA-256 |
|---|---|
| `experiments/exp-15-memory/2026-09-30/fixtures/benchmark_tasks.json` | `dcb0d2f920ba8d95e9a2dfd6641f6855c20a5aa586fb021c21ab8303a70951e1` |
| `experiments/exp-15-memory/2026-09-30/fixtures/canonical_memory.json` | `24b2a00bc9627ebda9cf92bb6b06a269e4f0857577d1d57185dbe09f8a6623df` |
| `experiments/exp-15-memory/2026-09-30/fixtures/cross_project_memory.json` | `9705d797f766558ecffb7a1a4038a4e1f4e649fed42daff8b91cda51716e543e` |
| `experiments/exp-15-memory/2026-09-30/harness/memory_layer.py` | `15266ce759223c43973c7a3cb1d2a5bad1e7e3615d98d1859df080f45eab3de7` |

The first digest is also recorded in EXP-15 `HASHES.txt` as `dcb0d2f920ba8d95e9a2dfd6641f6855c20a5aa586fb021c21ab8303a70951e1`; the table above is intended to preserve that exact fixture pin. The harness validates all four inputs against the digests in `HASHES.txt`/the script before running. If a digest does not match, it stops rather than silently comparing changed cases.

## Cases

The unchanged frozen set is:

1. `TASK-MPE-08` — BrowserAct scraping and automation boundaries (`MEM-MPE-001`, `MEM-MPE-002`).
2. `TASK-MPE-11` — Runtime coordination messaging architecture (`MEM-MPE-003`, `MEM-MPE-004`).
3. `TASK-MPE-12` — CLEARS triage operational reliance (`MEM-MPE-005`, `MEM-MPE-006`).
4. `TASK-MPE-18` — Pirate Face model distribution architecture (`MEM-MPE-007`, `MEM-MPE-008`).

EXP-15's frozen `topic` key and `expected_memory_ids` are used for all three arms. A small deterministic predicate list in the harness checks required decision/outcome and constraint phrases from the same EXP-15 oracle. No case labels, source records, or expected outcomes were changed.

## Arm interpretation

The owner instruction defines A as **current memory**. Therefore:

- **A:** current EXP-15 file-backed memory lookup and complete `MemoryItem` context. This is EXP-15's memory-enabled arm (original EXP-15 Mode B), not its original no-memory Mode A.
- **B:** the same A lookup, represented as a transient symbolic/Mermaid task packet. Full decision/constraint summaries, item IDs, and source references are preserved; no model-generated compaction is used.
- **C:** a transient, project-scoped L2 topic/scenario card containing full decision/constraint summaries and linked L1 IDs/source references. An optional L1 lookup loads full item metadata when those details are specifically needed.

The original EXP-15 no-memory measurements (17 document reads, 1,838 inspected lines across four cases) remain historical context only. They are not substituted for arm A or rerun here.

## Measurement accounting

- The injected context is the text produced for each arm, measured as lines and UTF-8 bytes. Approximate tokens are `ceil(UTF-8 bytes / 4)`, a repeatable heuristic, not a model tokenizer.
- Runtime recall source-document/raw-log reads are counted separately from fixture loading and evaluator verification. A, B, and C each perform zero canonical source-document/raw-log reads for the frozen query; the EXP-15 memory fixture is loaded once, then the four cases use logical lookups.
- The shared provenance validator reads ten unique repository files once to check citation paths and line-anchor ranges. Those validation reads are not charged as retrieval context to any arm. The validator checks path existence and line range only; it does not claim semantic verification of each cited line.
- C's optional full-item drill-down is reported separately from its initial scenario context so that the cost of obtaining full L1 details is not hidden.
- Scope, approval-gate, and fixture-integrity probes are read-only against the frozen source. The three deliberate unauthorized-write probes target temporary copies and must be rejected without changing their files.

## Reproduction

From the repository root:

```bash
python experiments/exp-26-tencentdb-agent-memory-components/harness/compare_memory_components.py
```

Machine-readable and human-readable outputs are written only under this EXP-26 directory.
