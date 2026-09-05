"""MPE Earned Autonomy — task-acceptance boundary.

Thin, deterministic acceptance helper that sits at the task-acceptance boundary and
routes every accepted task through the canonical pipeline BEFORE execution:

    accepted_task + trusted_history + current_level + safety context
      -> triage()                 (scripts.triage_engine)
      -> evaluate_autonomy()      (scripts.earned_autonomy)
      -> dispatch_with_autonomy() (scripts.dispatch_autonomy)
      -> acceptance decision + acceptance_state

Design contract (from the integration brief):
- Earned autonomy is a *ceiling*, never a bypass.
- FAIL-CLOSED: any contract / triage / dispatch / history error yields a BLOCKED /
  HUMAN_REQUIRED decision with ``allowed_action = OBSERVE`` and NEVER invokes
  execution. It never falls back to autonomous execution.
- No real executor is contained here. The execution path enforces the decision by
  calling ``enforce_execution`` with an injected executor (a callable). There is a
  single enforcement point; no alternate path bypasses the dispatch decision.
- No new orchestration subsystem, storage, database, or backend. No Result Contract /
  Task Packet / MPE IR change. Reuses triage_engine, earned_autonomy, dispatch_autonomy.

Suggested acceptance_state vocabulary (compatible with existing BLOCKED / REVIEWING /
READY lifecycle concepts):
    OBSERVE              -> ACCEPTED_OBSERVE
    RECOMMEND            -> ACCEPTED_RECOMMEND
    DRAFT                -> ACCEPTED_DRAFT
    EXECUTE_WITH_APPROVAL-> HUMAN_REQUIRED
    EXECUTE              -> READY_TO_EXECUTE
Fail-closed / error     -> BLOCKED
"""
from __future__ import annotations

from typing import Any, Callable, Optional

try:  # normal package / module import
    from scripts.dispatch_autonomy import dispatch_with_autonomy
except Exception:  # when loaded standalone via importlib (e.g. tests)
    from dispatch_autonomy import dispatch_with_autonomy  # type: ignore

DEFAULT_LEVEL = "L0"

ACCEPTED_STATES = {
    "OBSERVE": "ACCEPTED_OBSERVE",
    "RECOMMEND": "ACCEPTED_RECOMMEND",
    "DRAFT": "ACCEPTED_DRAFT",
    "EXECUTE_WITH_APPROVAL": "HUMAN_REQUIRED",
    "EXECUTE": "READY_TO_EXECUTE",
}


def accept_task(
    task: dict[str, Any],
    history: Optional[list[dict[str, Any]]] = None,
    current_level: str = DEFAULT_LEVEL,
    *,
    scope_violation: bool = False,
    security_violation: bool = False,
    secrets_restricted: bool = False,
    production_restricted: bool = False,
    stop_condition: bool = False,
    required_checks: Optional[tuple[str, ...]] = None,
) -> dict[str, Any]:
    """Resolve the deterministic acceptance decision for one task (fail-closed).

    The execution path must then OBEY this decision via ``enforce_execution``.
    On any error the function returns a safe BLOCKED decision and never executes.
    """
    task_id = task.get("task_id") if isinstance(task, dict) else None
    try:
        decision = dispatch_with_autonomy(
            task,
            history,
            current_level,
            scope_violation=scope_violation,
            security_violation=security_violation,
            secrets_restricted=secrets_restricted,
            production_restricted=production_restricted,
            stop_condition=stop_condition,
            required_checks=required_checks,
        )
    except Exception as exc:  # fail-closed: never fall back to autonomous execution
        return {
            "task_id": task_id,
            "task_risk_tier": None,
            "current_autonomy_level": current_level,
            "earned_recommended_level": None,
            "allowed_action": "OBSERVE",
            "execution_allowed": False,
            "human_gate_required": True,
            "blocking_reasons": ["acceptance_error"],
            "dispatch_evaluation_id": None,
            "acceptance_state": "BLOCKED",
            "reason": f"fail-closed: {type(exc).__name__}: {exc}",
            "executor_invoked": False,
        }

    allowed = decision["allowed_action"]
    # A hard safety block reduces the action to OBSERVE, but the task is not
    # "accepted to observe" — it is BLOCKED.
    hard_block_reasons = {
        "scope_violation",
        "security_violation",
        "secrets_restriction",
        "production_restriction",
        "stop_condition",
    }
    if allowed == "OBSERVE" and (set(decision.get("blocking_reasons", [])) & hard_block_reasons):
        acceptance_state = "BLOCKED"
    else:
        acceptance_state = ACCEPTED_STATES.get(allowed, "BLOCKED")
    decision.update(
        {
            "task_id": task_id,
            "dispatch_evaluation_id": decision.get("evaluation_id"),
            "acceptance_state": acceptance_state,
            "executor_invoked": False,
        }
    )
    return decision


def enforce_execution(
    acceptance_result: dict[str, Any],
    executor: Callable[[dict[str, Any]], Any],
    approval_recorded: bool = False,
) -> Optional[Any]:
    """Single enforcement point: invoke the executor ONLY when the decision permits.

    Returns the executor result when permitted; otherwise returns ``None`` and the
    executor is never called. The executor is a small injected callable (never a real
    external provider). There is no alternate code path that bypasses this check.
    """
    allowed = acceptance_result.get("allowed_action")
    if allowed == "EXECUTE":
        return executor(acceptance_result)
    if allowed == "EXECUTE_WITH_APPROVAL" and approval_recorded:
        return executor(acceptance_result)
    return None
