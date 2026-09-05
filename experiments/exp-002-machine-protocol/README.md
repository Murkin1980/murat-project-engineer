# EXP-002 — Machine Protocol Experiment

**Primary decision:** `EXTEND_EXISTING`

**Experiment status:** `CLOSED`
**Overall verdict:** `PASS`

## Research question

Can MPE Core use a deterministic canonical machine representation between the Task
Packet/Core and external executors **without changing the fundamental architecture**?

## Architecture under test

```
Human Request
  -> MPE Core / Task Packet
    -> MPE IR
      -> Executor Adapter
        -> External Model / Tool / Agent
```

## Clarification of roles

- **Task Packet remains the source of truth.** It is the canonical contract for what
  a task is, its constraints, and its required evidence.
- **MPE IR is a canonical executor representation / machine interface.** It is the
  deterministic, schema-validatable form an executor consumes.
- **MPE IR is NOT:**
  - a replacement for the Task Packet
  - a new source of truth
  - hidden-state communication
  - a binary protocol
  - a model-specific prompt language

The same IR can be understood by different external models/providers without changing
core MPE contracts, and execution PASS depends on trusted evidence provenance — not on
executor identity.

## Iteration history

### Iteration 1 — Canonical representation proof-of-concept
**Outcome:** `PASS`
**Key result:** The existing Task Packet could be deterministically encoded into MPE IR
and processed without changing core contracts. The encoder reuses the existing
deterministic triage engine and gate registry; the IR is an additional adapter-layer
representation only.

### Iteration 2 — Cross-model / cross-provider semantic portability
**Models/providers tested:**
- A) Alibaba Cloud Model Studio — `qwen3.7-plus`
- B) Hugging Face / Nscale — `Qwen/Qwen2.5-Coder-7B-Instruct`

**Result:** Both models correctly interpreted the same frozen MPE IR.

**Conclusion:** `CROSS_MODEL_SEMANTIC_PORTABILITY_SUPPORTED`

**But:** `CROSS_EXECUTOR_EXECUTION_PORTABILITY_INCONCLUSIVE` — because the external
models had no real repository/tool execution capability. Full execution portability is
**not** claimed.

### Important model-behavior finding (Iteration 2)

- **Alibaba `qwen3.7-plus`:**
  - understood the task correctly
  - had no repository/tool execution
  - nevertheless **claimed**: file creation, git diff, secrets scan PASS, build PASS,
    exit code 0, execution success
  - **Classification:** `SELF_REPORTED_EXECUTION_CLAIM` / `UNVERIFIED`

- **Hugging Face `Qwen/Qwen2.5-Coder-7B-Instruct`:**
  - understood the task correctly
  - acknowledged lack of external-system access
  - did **not** falsely claim execution
  - proposed an implementation framework only
  - **Classification:** `UNDERSTOOD_BUT_NOT_EXECUTED`

No credentials, access tokens, or raw provider responses are reproduced here.

### Iteration 3 — Capability-Aware Evidence Gate
**Verdict:** `STRONG_PASS`
**Research conclusion:** `EVIDENCE_TRUST_BOUNDARY_SUPPORTED`

| Case | Description | Validated outcome |
|------|-------------|-------------------|
| A | fabricated self-reported execution evidence | `REWORK` (never PASS) |
| B | honest capability limitation | `HUMAN_REQUIRED` (not PASS, not falsely executed) |
| C | trusted local tool evidence | `PASS` |
| D | unknown / untrusted evidence source | fail-closed `REWORK` |

**Key result:** MPE can distinguish `UNDERSTOOD`, `EXECUTED CLAIM`, and
`VERIFIED EXECUTION` using **evidence provenance** rather than executor
self-identification.

## Final architectural conclusion

1. MPE IR is viable as a canonical executor-facing representation.
2. Task Packet remains the source of truth.
3. The same IR can be semantically understood across different external models/providers.
4. Model understanding does **not** prove execution.
5. Execution PASS must depend on trusted evidence provenance.
6. Executor identity / signature is **not** required for trust.
7. Evidence provenance **is** required for verified execution PASS.
8. No new orchestration layer, protocol service, backend, database, or LLM was required.

**Recommended concise principle:**

> *Executor identity is optional. Trusted evidence provenance is mandatory for verified PASS.*

## Link to production integration

The successful Iteration 3 rule was promoted into the main MPE validation flow:

- Production code: `scripts/validate_package.py`
  (`classify_evidence_ref`, `derive_execution_outcome`, `validate_gate_results`, and a
  non-breaking scan inside `validate()` that excludes the legacy `evidence/` directory)
- Regression tests: `tests/test_evidence_trust.py`

The experiment references that production code; it does **not** duplicate it.

## EXP-002 research outcomes

- `CANONICAL_MACHINE_INTERFACE_SUPPORTED`
- `CROSS_MODEL_SEMANTIC_PORTABILITY_SUPPORTED`
- `EVIDENCE_TRUST_BOUNDARY_SUPPORTED`
- Execution portability: `INCONCLUSIVE`

## Artifacts in this directory

- `MPE_IR_FROZEN.json` — the exact frozen IR used across the experiment
  (SHA-256 `cdafe73309960c555d8da1c84efbfc7b4c1e6ca22d3eeafeca5a226ba43fdbfd`,
  1148 bytes, protocol `mpe-ir` / version `0.1`)
- `mpe-ir.schema.json` — the minimal MPE IR JSON Schema (draft 2020-12)
- `README.md` — this document
- `EXP-002_RESULTS.md` — detailed results and conclusions
