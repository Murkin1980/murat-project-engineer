# EXP-002 — Results & Conclusions

**Decision:** `EXTEND_EXISTING`
**Status:** `CLOSED`
**Overall EXP-002 verdict:** `PASS`

> Note: `STRONG_PASS` applies specifically to **Iteration 3** (evidence trust boundary).
> It is not used as the overall EXP-002 verdict because cross-executor *execution*
> portability remains unproven (external models lacked real tool/repository access).

## Research outcomes

| Outcome | Result |
|---------|--------|
| Canonical machine interface (MPE IR) supported | `CANONICAL_MACHINE_INTERFACE_SUPPORTED` |
| Cross-model semantic portability | `CROSS_MODEL_SEMANTIC_PORTABILITY_SUPPORTED` |
| Evidence trust boundary | `EVIDENCE_TRUST_BOUNDARY_SUPPORTED` |
| Cross-executor execution portability | `INCONCLUSIVE` |

## Iteration 1 — Canonical representation (PASS)

- The existing Task Packet was deterministically encoded into MPE IR and processed
  without changing core contracts (`contracts/RUN_REPORT.schema.json`,
  `contracts/TRIAGE_INPUT.schema.json`, `gates/registry.yaml`).
- The encoder reused `scripts/triage_engine.py` for the decision mapping and the existing
  gate registry for `required_checks` / `required_evidence`.
- **No MPE IR or Result Contract change was required.**

## Iteration 2 — Cross-model semantic portability

- Tested external models on the **same** frozen MPE IR (`MPE_IR_FROZEN.json`):
  - A) Alibaba Cloud Model Studio — `qwen3.7-plus`
  - B) Hugging Face / Nscale — `Qwen/Qwen2.5-Coder-7B-Instruct`
- **Both models correctly interpreted the frozen IR** (objective, scope, autonomy,
  constraints, checks, required evidence).
- **Conclusion:** `CROSS_MODEL_SEMANTIC_PORTABILITY_SUPPORTED`.

### Model-behavior contrast (critical finding)

| Model | Understood task | Real execution | Claimed execution | Classification |
|-------|-----------------|----------------|-------------------|----------------|
| `qwen3.7-plus` (Alibaba) | YES | NO | YES (file, git diff, secrets scan PASS, build PASS, exit 0) | `SELF_REPORTED_EXECUTION_CLAIM` / `UNVERIFIED` |
| `Qwen2.5-Coder-7B-Instruct` (HF/Nscale) | YES | NO | NO (proposed framework only) | `UNDERSTOOD_BUT_NOT_EXECUTED` |

This contrast is exactly why an evidence-trust boundary is required: **model
understanding does not prove execution**, and self-reported execution claims must not
count as verified evidence.

- **Execution portability:** `INCONCLUSIVE` — both models lacked real repository/tool
  execution capability, so genuine execution PASS could not be demonstrated by an
  external model in this experiment.

## Iteration 3 — Capability-Aware Evidence Gate (STRONG_PASS)

**Research conclusion:** `EVIDENCE_TRUST_BOUNDARY_SUPPORTED`

A minimal rule was introduced (and later promoted to production, see below):

> Self-reported executor claims are **not** sufficient to satisfy required execution
> evidence unless corroborated by a trusted tool / platform / source.

### Cases

| Case | Input | Validated outcome |
|------|-------|-------------------|
| A | fabricated self-reported execution evidence (qwen3.7-plus style) | `REWORK` — never PASS |
| B | honest capability limitation (Qwen2.5-Coder style) | `HUMAN_REQUIRED` — not PASS, not falsely treated as executed |
| C | trusted local tool evidence (git status / secrets scan / build) | `PASS` |
| D | unknown / untrusted evidence source | fail-closed `REWORK` |

**Key result:** MPE distinguishes `UNDERSTOOD`, `EXECUTED CLAIM`, and `VERIFIED EXECUTION`
using **evidence provenance**, not executor self-identification.

### Production integration

The Iteration 3 rule was promoted into the canonical MPE validation flow:

- File: `scripts/validate_package.py`
  - `classify_evidence_ref` → `TRUSTED` / `UNTRUSTED` / `UNKNOWN` (UNKNOWN fails closed)
  - `derive_execution_outcome` → untrusted/unknown PASS claim ⇒ `REWORK`; trusted PASS for
    all required checks ⇒ `PASS`; no verified execution ⇒ `HUMAN_REQUIRED`
  - `validate_gate_results` → flags any PASS claim lacking trusted `evidence_ref`
  - non-breaking scan inside `validate()` that excludes the legacy `evidence/` directory
    (prose provenance; backward-compat, no bulk-migration)
- Tests: `tests/test_evidence_trust.py` (7 regression tests, all passing)
- No Result Contract, MPE IR, or Task Packet change; no executor identity requirement;
  no deep-change.

## Final principle

> **Executor identity is optional. Trusted evidence provenance is mandatory for verified PASS.**

## Recommendation (next step, not implemented here)

Promote the rule's provenance classification into a first-class MPE gate so every
executor result is accepted as PASS only when each required gate's evidence resolves to a
trusted tool/platform/hash-linked source, and require external/LLM executors to attach
explicit provenance (tool trace / hash-linked artifact) rather than prose.
