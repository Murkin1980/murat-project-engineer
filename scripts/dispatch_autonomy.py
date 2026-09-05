"""MPE Earned Autonomy — deterministic pre-execution dispatch.

Combines the canonical task decision (``scripts/triage_engine.triage``) with the
Earned Autonomy evaluator (``scripts/earned_autonomy.evaluate_autonomy``) to derive
the maximum allowed action BEFORE a task is executed.

Design contract (from the integration brief):

- Earned autonomy is a *ceiling*, never a bypass.
- The final allowed action is the MOST RESTRICTIVE result of:
    * earned autonomy level
    * task risk tier
    * approval requirements
    * scope / security / secrets / production / stop constraints
    * deep-change rules
- Hard safety gates OVERRIDE autonomy; autonomy can never relax them.
- DEEP-CHANGE always requires human approval.
- L4 is owner-controlled and never auto-granted: it is honored only when the
  executor has verifiably earned at least L3 and no earned-history violation
  exists. Untrusted / unknown evidence cannot raise the earned level.
- No new orchestration subsystem: this is a single deterministic composition
  function reusing existing MPE modules. No Result Contract / Task Packet / MPE IR
  change.

Allowed-action vocabulary (existing autonomy model):
    L0 -> OBSERVE
    L1 -> RECOMMEND
    L2 -> DRAFT
    L3 -> EXECUTE_WITH_APPROVAL
    L4 -> EXECUTE
"""
from __future__ import annotations

from typing import Any, Optional

try:  # normal package / module import
    from scripts.earned_autonomy import evaluate_autonomy
    from scripts.triage_engine import ContractError, triage
except Exception:  # when loaded standalone via importlib (e.g. tests)
    from earned_autonomy import evaluate_autonomy  # type: ignore
    from triage_engine import ContractError, triage  # type: ignore

AUTONOMY_LEVELS = ("L0", "L1", "L2", "L3", "L4")

LEVEL_TO_ACTION = {
    "L0": "OBSERVE",
    "L1": "RECOMMEND",
    "L2": "DRAFT",
    "L3": "EXECUTE_WITH_APPROVAL",
    "L4": "EXECUTE",
}

# privilege: higher == more authority. Lower is more restrictive.
ACTION_PRIVILEGE = {
    "OBSERVE": 0,
    "RECOMMEND": 1,
    "DRAFT": 2,
    "EXECUTE_WITH_APPROVAL": 3,
    "EXECUTE": 4,
}
PRIVILEGE_ACTION = {value: key for key, value in ACTION_PRIVILEGE.items()}


def _effective_earned_level(ea_result: dict[str, Any], current_level: str) -> str:
    """Resolve the earned ceiling, honoring owner-controlled L4 under constraints.

    ``evaluate_autonomy`` never auto-grants L4, so the only path to an EXECUTE
    ceiling is an explicit owner-set current level of L4 combined with a verifiedly
    earned L3 and zero earned-history violation signals. Untrusted / unknown
    evidence can never reach this path.
    """
    earned_level = ea_result["recommended_level"]
    earned_blocking = set(ea_result.get("blocking_events", []))
    if current_level == "L4" and earned_level == "L3" and not earned_blocking:
        return "L4"
    return earned_level


def dispatch_with_autonomy(
    task: dict[str, Any],
    history: Optional[list[dict[str, Any]]] = None,
    current_level: str = "L0",
    *,
    scope_violation: bool = False,
    security_violation: bool = False,
    secrets_restricted: bool = False,
    production_restricted: bool = False,
    stop_condition: bool = False,
    required_checks: Optional[tuple[str, ...]] = None,
) -> dict[str, Any]:
    """Deterministically derive the maximum allowed action for a task.

    Pipeline (fixed precedence):
        1. triage task                      -> risk tier, approval requirement
        2. evaluate earned autonomy         -> earned ceiling
        3. apply hard safety gates          -> block execution on scope/security/...
        4. apply approval requirements      -> cap at EXECUTE_WITH_APPROVAL
        5. cap action by earned autonomy    -> never exceed earned level
        6. derive allowed_action
        7. derive execution_allowed
        8. emit reason / blockers

    Returns the canonical dispatch result. No LLM chooses the precedence.
    """
    if current_level not in AUTONOMY_LEVELS:
        raise ValueError(f"unknown current_level: {current_level!r}")

    triage_output = triage(task)
    risk_tier = triage_output["recommended_risk_tier"]
    human_approval_required = bool(triage_output["human_approval_required"])
    human_reasons = list(triage_output.get("human_approval_reasons", []))

    ea_result = evaluate_autonomy(history or [], current_level, required_checks)
    earned_level = _effective_earned_level(ea_result, current_level)
    earned_blocking = set(ea_result.get("blocking_events", []))

    # 3. Hard safety gates that OVERRIDE autonomy and block execution.
    hard_blocks: list[str] = []
    if scope_violation:
        hard_blocks.append("scope_violation")
    if security_violation:
        hard_blocks.append("security_violation")
    if secrets_restricted:
        hard_blocks.append("secrets_restriction")
    if production_restricted:
        hard_blocks.append("production_restriction")
    if stop_condition:
        hard_blocks.append("stop_condition")

    # 4. Approval requirement: triage-mandated approval OR DEEP-CHANGE risk tier.
    deep_change = risk_tier == "DEEP-CHANGE"
    approval_required = human_approval_required or deep_change

    # Ceilings (privilege integers; lower == more restrictive).
    earned_ceiling = ACTION_PRIVILEGE[LEVEL_TO_ACTION[earned_level]]
    approval_ceiling = (
        ACTION_PRIVILEGE["EXECUTE_WITH_APPROVAL"] if approval_required else ACTION_PRIVILEGE["EXECUTE"]
    )
    safety_ceiling = ACTION_PRIVILEGE["OBSERVE"] if hard_blocks else ACTION_PRIVILEGE["EXECUTE"]

    # 5/6. Final action is the MOST RESTRICTIVE of all ceilings.
    final_privilege = min(earned_ceiling, approval_ceiling, safety_ceiling)
    allowed_action = PRIVILEGE_ACTION[final_privilege]

    # 7. Execution is permitted for execution-class actions (EXECUTE_WITH_APPROVAL
    #    or EXECUTE) when no hard safety gate blocks it. The human_gate_required
    #    flag disambiguates whether a human must approve first.
    execution_allowed = (final_privilege >= ACTION_PRIVILEGE["EXECUTE_WITH_APPROVAL"]) and not hard_blocks
    human_gate_required = approval_required or (earned_level == "L3")

    # 8. Blockers / reasons.
    blocking_reasons: set[str] = set(hard_blocks) | earned_blocking
    if approval_required:
        blocking_reasons |= set(human_reasons) | {"human_approval_required"}
    if deep_change:
        blocking_reasons.add("deep_change_approval_required")

    reason = (
        f"earned={earned_level} risk_tier={risk_tier} approval_required={approval_required} "
        f"hard_blocks={sorted(hard_blocks) or 'none'}; "
        f"allowed_action={allowed_action} execution_allowed={execution_allowed}"
    )

    return {
        "current_autonomy_level": current_level,
        "earned_recommended_level": ea_result["recommended_level"],
        "evaluation_id": ea_result.get("evaluation_id"),
        "verified_pass_count": ea_result["verified_pass_count"],
        "task_risk_tier": risk_tier,
        "approval_required": approval_required,
        "allowed_action": allowed_action,
        "execution_allowed": execution_allowed,
        "human_gate_required": human_gate_required,
        "blocking_reasons": sorted(blocking_reasons),
        "reason": reason,
    }
