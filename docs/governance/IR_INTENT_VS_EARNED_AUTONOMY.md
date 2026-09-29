# MPE IR Intent vs Earned Autonomy — Governed-Entry Permission Contract

**Status:** production contract (OBS-01 fix)
**Scope:** the intent hop of `IR intent → Task Packet → governed entry → executable permission`
**Related finding:** `OBS-01` in `experiments/exp-002-machine-protocol/ARENA_EXECUTION_RECORD.json`
(`mpe_governance_observation`), reproduced and resolved in the OBS-01 bounded change.

## The one non-contradictory contract

| Hop | Source of truth | Input | Output | Authority | Kind |
|---|---|---|---|---|---|
| Frozen IR | `experiments/exp-002-machine-protocol/MPE_IR_FROZEN.json` + `mpe-ir.schema.json` (EXP-002: *"Task Packet remains the source of truth… MPE IR is NOT a replacement for the Task Packet, a new source of truth"*) | human request | `decision` / `autonomy` blocks | task author declares | **intent** |
| IR intent → Task Packet | `scripts/mpe_ir_mapping.derive_ir_intent`, `contracts/TRIAGE_INPUT.schema.json` | IR blocks | TRIAGE_INPUT derivable subset + tighten-only `requested_human_approval` | deterministic mapping, fail-closed | **request / constraint** |
| requested autonomy | `scripts/mpe_ir_mapping` | `autonomy.level`, `requires_human_approval`, `decision.*` | `requested_human_approval` (tighten-only) | never grants anything | **request** |
| earned autonomy | `scripts/earned_autonomy.py` (*"Autonomy is EARNED from verified execution history only… L4 is never auto-granted"*) | trusted history + owner-granted `current_level` | `recommended_level` L0–L4 (ceiling) | Evidence Trust Gate (`validate_package.derive_execution_outcome`) | **recommendation (ceiling)** |
| governed-entry decision | `scripts/dispatch_autonomy.py` (*"Earned autonomy is a ceiling, never a bypass. The final allowed action is the MOST RESTRICTIVE result of…"*) | triage + earned ceiling + approval + safety | `allowed_action`, `execution_allowed`, `human_gate_required` | MPE Core enforcement (deterministic `min` of ceilings) | **permission (derived)** |
| executor invocation | `scripts/task_acceptance.enforce_execution` (*"invoke the executor ONLY when the decision permits"*) | `allowed_action` + `approval_recorded` | executor call or none | MPE Core | **permission enforcement** |

## Interpretation rules (normative)

1. **IR intent is never permission.** The IR `autonomy` / `decision` blocks are an
   intent declaration. `derive_ir_intent` returns `authorization: None` and
   `semantics: intent_only_never_permission` by construction.
2. **`requires_human_approval: false` is not an execution authorization.** It means
   only "no additional human gate is requested by this declaration". It can never
   remove a gate that triage or governance already requires, and it never raises
   the earned ceiling.
3. **`autonomy.level` / `decision.risk_tier` use the FAST / VERIFIED / DEEP-CHANGE
   risk-tier vocabulary** (the triage vocabulary). They are NOT the L0–L4
   earned-autonomy ladder and never populate it. The L0–L4 ladder is owner-granted
   (`current_level`) and history-earned (`evaluate_autonomy`) only.
4. **Intent is tighten-only.** `requires_human_approval: true`,
   `decision.human_approval_required: true`, or DEEP-CHANGE intent
   (`requested_human_approval=True`) keeps the human gate mandatory even when the
   recomputed triage of the task content would not require one
   (`approval_required = triage_approval or deep_change or requested_human_approval`).
   The gate opens only via an explicitly recorded approval (`approval_recorded`).
5. **Executable permission is derived, never declared:**
   `allowed_action = min(earned ceiling, approval ceiling, hard safety ceiling)`.
   With an **empty trusted history** the earned ceiling is L0, so the decision is
   deterministically `OBSERVE / NOT_PERMITTED / executor_invoked=false` at every
   owner level — including L4 — until verified trusted history exists.

## OBS-01 disposition

- **Reproduced** with unchanged production code (`triage_engine.py --governed-run`
  on the Arena-derived Task Packet): identical results and dispatch evaluation ids
  (`EA-0aabcd40fc91668d` at L0, `EA-2efb5ea81734a181` at L4) as recorded in
  `ARENA_EXECUTION_EVIDENCE.json` EV-06 / EV-07.
- **Root cause:** contract interpretation gap at the intent hop — (a) the IR
  `autonomy` block was never mapped by production code (the Arena run dropped it
  manually), (b) "autonomy level" naming invites reading the IR's risk-tier token
  as an L0–L4 permission, (c) the tighten-only direction of
  `requires_human_approval: true` was unenforced and would have been silently lost.
- **The observed denial itself is CORRECT Earned Autonomy behavior** (candidate 3):
  intent must not self-elevate; empty trusted history ⇒ earned L0 ⇒ OBSERVE. The
  governed-entry enforcement was not wrong and is unchanged in precedence.
- **Fix class applied (priority 1+2):** mapping fix + contract interpretation fix
  (`scripts/mpe_ir_mapping.py`, this document). No enforcement-precedence change,
  no Earned Autonomy model change, no schema or gate-registry change.

## Why Earned Autonomy is not weakened

- The earned ceiling derivation (`evaluate_autonomy`, thresholds L1/L2/L3, L4
  owner-only) is untouched.
- Intent enters the decision only as `requested_human_approval`, which can
  **add** a gate (reduce privilege), never remove one.
- The precedence `min(earned, approval, safety)` is unchanged; the only new term
  sits inside the existing approval ceiling.
- Empty history remains L0; untrusted/self-reported evidence still cannot promote.

## Negative controls (tests)

`tests/test_ir_intent_governed_entry.py`:

- IR/Task Packet can never obtain more autonomy than governance allows (L4 owner
  level with empty history still denied; doctored DEEP-CHANGE intent still denied
  or gated).
- `requires_human_approval: false` never loosens an existing triage gate.
- Empty trusted history is explicit and deterministic (identical repeated runs).
- `requires_human_approval: true` preserves the mandatory human gate; it opens
  only with recorded approval.
- Self-reported / unknown PASS evidence never becomes trusted evidence and never
  raises the earned ceiling.
- Malformed IR intent sources fail closed (`IrIntentError`); non-boolean
  `requested_human_approval` fails closed in dispatch.

## Rollback

`git revert` of the OBS-01 fix commit(s) restores the previous behavior exactly.
No schema, gate registry, evidence, or experiment artifact is mutated by the fix;
the frozen IR and its schema are untouched.
