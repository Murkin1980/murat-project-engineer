"""MPE Earned Autonomy — minimal, deterministic evaluator.

Builds directly on the existing Evidence Trust Gate invariant
(``scripts/validate_package.derive_execution_outcome``): a run counts as a
*verified* PASS only when its final outcome is PASS **and** its required evidence is
trusted **and** no scope/approval/deep-change/security violation occurred.

Design constraints (from the integration brief):
- Autonomy is EARNED from verified execution history only.
- It must NOT increase from model identity, provider, signature, self-report,
  unverified evidence, prose, or attempt count.
- L4 is never auto-granted (owner approval only).
- DEEP-CHANGE always requires human approval regardless of level.
- Stateless: history in -> autonomy recommendation out. No database / state storage.

Levels (existing agreed model, not invented here):
    L0 OBSERVE
    L1 RECOMMEND
    L2 DRAFT
    L3 EXECUTE_WITH_APPROVAL
    L4 EXECUTE   (owner-controlled; never auto)
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import os
from typing import Any

try:  # normal package / module import
    from scripts.validate_package import (
        classify_evidence_ref,
        derive_execution_outcome,
        REQUIRED_EXECUTION_CHECKS,
    )
except Exception:  # when loaded standalone via importlib (e.g. tests)
    _here = os.path.dirname(__file__)
    _spec = importlib.util.spec_from_file_location(
        "validate_package", os.path.join(_here, "validate_package.py")
    )
    _vp = importlib.util.module_from_spec(_spec)
    _spec.loader.exec_module(_vp)
    classify_evidence_ref = _vp.classify_evidence_ref
    derive_execution_outcome = _vp.derive_execution_outcome
    REQUIRED_EXECUTION_CHECKS = _vp.REQUIRED_EXECUTION_CHECKS

AUTONOMY_LEVELS = ("L0", "L1", "L2", "L3", "L4")
LEVEL_ACTION = {
    "L0": "observe",
    "L1": "recommend",
    "L2": "draft",
    "L3": "execute_with_approval",
    "L4": "execute",
}
# Conservative baseline thresholds (total verified PASS count -> reachable level).
# L1 = 1, L2 = 3, L3 = 5; L4 is owner-controlled and never auto-granted.
L1_THRESHOLD = 1
L2_THRESHOLD = 3
L3_THRESHOLD = 5

_BLOCKING_FIELDS = (
    "scope_violation",
    "approval_violation",
    "deep_change_violation",
    "security_violation",
)


def _is_verified_pass(run: dict[str, Any], required_checks: tuple[str, ...]) -> bool:
    """A run is a VERIFIED PASS only if it satisfies the existing Evidence Trust Gate.

    Reuses ``derive_execution_outcome`` (single source of truth) — no second
    evidence-trust subsystem.
    """
    if run.get("outcome") != "PASS":
        return False
    if any(run.get(field) for field in _BLOCKING_FIELDS):
        return False
    gates = run.get("deterministic_gate_results")
    if gates:
        return derive_execution_outcome(gates, required_checks) == "PASS"
    # No gate detail: trust the already-validated outcome (which reflects evidence trust).
    return True


def _level_for_count(verified_pass_count: int) -> str:
    if verified_pass_count >= L3_THRESHOLD:
        return "L3"  # hard cap: never auto-promote to L4
    if verified_pass_count >= L2_THRESHOLD:
        return "L2"
    if verified_pass_count >= L1_THRESHOLD:
        return "L1"
    return "L0"


def _downgrade(level: str) -> str:
    idx = AUTONOMY_LEVELS.index(level)
    return AUTONOMY_LEVELS[max(0, idx - 1)]


def evaluate_autonomy(
    history: list[dict[str, Any]],
    current_level: str = "L0",
    required_checks: tuple[str, ...] | None = None,
) -> dict[str, Any]:
    """Deterministically derive an autonomy recommendation from verified run history.

    Returns: evaluation_id, current_level, verified_pass_count, blocking_events,
    recommended_level, promotion_eligible, reason, next_allowed_action.
    """
    if current_level not in AUTONOMY_LEVELS:
        raise ValueError(f"unknown current_level: {current_level!r}")
    required_checks = required_checks or REQUIRED_EXECUTION_CHECKS

    verified_pass_count = sum(
        1 for run in history if _is_verified_pass(run, required_checks)
    )
    blocking_events = sorted(
        {field for run in history for field in _BLOCKING_FIELDS if run.get(field)}
    )

    if blocking_events:
        # Scope / approval / deep-change / security violations block promotion and
        # recommend a one-level downgrade (never below L0).
        recommended_level = _downgrade(current_level)
    else:
        recommended_level = _level_for_count(verified_pass_count)

    promotion_eligible = (not blocking_events) and (
        AUTONOMY_LEVELS.index(recommended_level) > AUTONOMY_LEVELS.index(current_level)
    )

    if blocking_events:
        reason = (
            f"{verified_pass_count} verified PASS; blocking_events={blocking_events}; "
            f"recommend downgrade to {recommended_level}"
        )
    elif recommended_level == "L3" and verified_pass_count >= L3_THRESHOLD:
        reason = (
            f"{verified_pass_count} verified PASS; eligible for L3; "
            f"L4 requires explicit owner approval (never auto-granted)"
        )
    else:
        reason = (
            f"{verified_pass_count} verified PASS; "
            f"eligible level by count = {recommended_level}"
        )

    payload = json.dumps(
        {"current_level": current_level, "history": history},
        sort_keys=True,
        default=str,
    )
    evaluation_id = "EA-" + hashlib.sha256(payload.encode("utf-8")).hexdigest()[:16]

    return {
        "evaluation_id": evaluation_id,
        "current_level": current_level,
        "verified_pass_count": verified_pass_count,
        "blocking_events": blocking_events,
        "recommended_level": recommended_level,
        "promotion_eligible": promotion_eligible,
        "reason": reason,
        "next_allowed_action": LEVEL_ACTION[recommended_level],
    }
