"""MPE IR intent -> governed-entry mapping (OBS-01 contract fix).

Deterministic, fail-closed mapping for the intent hop of the production chain:

    IR intent -> derived Task Packet -> governed entry -> executable permission

Contract (source of truth: ``experiments/exp-002-machine-protocol/README.md``,
``scripts/dispatch_autonomy.py``, ``scripts/earned_autonomy.py``):

- The MPE IR is a canonical executor-facing representation. The **Task Packet
  remains the source of truth**; the IR is never a permission document.
- The IR ``autonomy`` / ``decision`` blocks are an **intent declaration** plus,
  at most, a **tighten-only constraint**:
    * ``requires_human_approval`` / ``human_approval_required: true``  -> the
      human gate stays mandatory (it can be passed only via an explicitly
      recorded approval).
    * ``requires_human_approval: false`` means "no additional human gate is
      requested by this declaration". It NEVER means "execution is authorized".
    * ``autonomy.level`` / ``decision.risk_tier`` use the FAST / VERIFIED /
      DEEP-CHANGE risk-tier vocabulary (the triage vocabulary). They are NOT
      the L0-L4 earned-autonomy ladder and can never populate it. DEEP-CHANGE
      intent requests human approval (existing policy: DEEP-CHANGE always
      requires human approval).
- Executable permission is derived exclusively by the governed entry as the
  MOST RESTRICTIVE of the earned-autonomy ceiling, the approval ceiling and the
  hard safety ceiling. The earned level comes only from trusted history.
- Therefore an IR intent can only ever TIGHTEN the decision (add a human gate);
  it can never loosen a gate nor raise an earned level.

TRIAGE_INPUT parity: the IR v0.1 can only supply the derivable Task Packet
subset (``task_id``, ``summary``, ``affected_repositories``,
``acceptance_criteria_present``). ``rollback_known``, ``ratings`` and
``signals`` are not representable in the IR and stay with the Task Packet
author (``task_packet_fields_not_in_ir``). The TRIAGE_INPUT schema is closed
and is not changed by this module.

No policy is invented here: every rule above is quoted from the existing
contracts; this module only makes the previously manual hop explicit.
"""
from __future__ import annotations

from typing import Any

IR_PROTOCOL = "mpe-ir"
IR_VERSION = "0.1"

# IR risk-tier vocabulary (mpe-ir.schema.json ``decision.risk_tier`` /
# ``autonomy.level`` enums == the triage risk-tier vocabulary).
RISK_TIERS = ("FAST", "VERIFIED", "DEEP-CHANGE")
_TIER_RESTRICTIVENESS = {tier: rank for rank, tier in enumerate(RISK_TIERS)}  # DEEP-CHANGE most restrictive

INTENT_SEMANTICS = "intent_only_never_permission"

_DERIVABLE_TASK_FIELDS = (
    "task_id",
    "summary",
    "affected_repositories",
    "acceptance_criteria_present",
)
_NOT_IN_IR_FIELDS = ("rollback_known", "ratings", "signals")


class IrIntentError(ValueError):
    """Raised fail-closed on any malformed IR intent source."""


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise IrIntentError(message)


def derive_ir_intent(ir: Any) -> dict[str, Any]:
    """Map the IR intent block to tighten-only governed-entry inputs.

    Returns a deterministic dict:

    - ``semantics``: always ``intent_only_never_permission``
    - ``authorization``: always ``None`` — intent never carries permission
    - ``ir_task_id`` / ``ir_objective``: identity for audit
    - ``requested_risk_tier``: most restrictive of ``decision.risk_tier`` and
      ``autonomy.level`` (risk-tier vocabulary; never an L0-L4 token)
    - ``requested_human_approval``: tighten-only flag — True when any intent
      source requests a human gate (``autonomy.requires_human_approval``,
      ``decision.human_approval_required``, or DEEP-CHANGE intent)
    - ``task_packet_fields``: the TRIAGE_INPUT subset derivable from the IR
    - ``task_packet_fields_not_in_ir``: fixed tuple naming the TRIAGE_INPUT
      fields that must come from the Task Packet author

    Fail-closed: any shape / type / vocabulary violation raises
    ``IrIntentError`` (a ``ValueError``); no partial intent is produced.
    """
    _require(isinstance(ir, dict), "IR intent source must be an object")
    _require(ir.get("protocol") == IR_PROTOCOL, "unexpected IR protocol")
    _require(ir.get("version") == IR_VERSION, "unexpected IR version")

    task = ir.get("task")
    decision = ir.get("decision")
    autonomy = ir.get("autonomy")
    scope = ir.get("scope")
    _require(isinstance(task, dict), "IR task block must be an object")
    _require(isinstance(decision, dict), "IR decision block must be an object")
    _require(isinstance(autonomy, dict), "IR autonomy block must be an object")
    _require(isinstance(scope, dict), "IR scope block must be an object")

    task_id = task.get("task_id")
    summary = task.get("summary")
    objective = ir.get("objective")
    _require(isinstance(task_id, str) and task_id, "IR task.task_id must be a non-empty string")
    _require(isinstance(summary, str) and summary, "IR task.summary must be a non-empty string")
    _require(isinstance(objective, str) and objective, "IR objective must be a non-empty string")

    decision_tier = decision.get("risk_tier")
    autonomy_level = autonomy.get("level")
    _require(decision_tier in RISK_TIERS, "IR decision.risk_tier must use the FAST/VERIFIED/DEEP-CHANGE vocabulary")
    _require(autonomy_level in RISK_TIERS, "IR autonomy.level must use the FAST/VERIFIED/DEEP-CHANGE vocabulary")

    decision_approval = decision.get("human_approval_required")
    autonomy_approval = autonomy.get("requires_human_approval")
    _require(isinstance(decision_approval, bool), "IR decision.human_approval_required must be a boolean")
    _require(isinstance(autonomy_approval, bool), "IR autonomy.requires_human_approval must be a boolean")

    repos = scope.get("affected_repositories")
    _require(
        isinstance(repos, list) and bool(repos) and all(isinstance(r, str) and r for r in repos),
        "IR scope.affected_repositories must contain non-empty strings",
    )

    acceptance_criteria = ir.get("acceptance_criteria")
    _require(
        isinstance(acceptance_criteria, list) and all(isinstance(c, str) and c for c in acceptance_criteria),
        "IR acceptance_criteria must contain non-empty strings",
    )

    # Most restrictive intent tier wins (DEEP-CHANGE > VERIFIED > FAST).
    requested_risk_tier = max(decision_tier, autonomy_level, key=_TIER_RESTRICTIVENESS.__getitem__)
    # Tighten-only: any approval request in the intent (incl. DEEP-CHANGE,
    # which always requires human approval) keeps the human gate mandatory.
    requested_human_approval = bool(
        autonomy_approval or decision_approval or requested_risk_tier == "DEEP-CHANGE"
    )

    return {
        "semantics": INTENT_SEMANTICS,
        "authorization": None,
        "ir_task_id": task_id,
        "ir_objective": objective,
        "requested_risk_tier": requested_risk_tier,
        "requested_human_approval": requested_human_approval,
        "task_packet_fields": {
            "task_id": task_id,
            "summary": summary,
            "affected_repositories": list(repos),
            "acceptance_criteria_present": bool(acceptance_criteria),
        },
        "task_packet_fields_not_in_ir": _NOT_IN_IR_FIELDS,
    }
