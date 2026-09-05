"""MPE Earned Autonomy — canonical execution runner (bounded proof path).

The MPE core has no pre-existing production execution runner. The only ``execute()``
in ``scripts/`` is ``prospective_validation.execute()``, a frozen EXP-12 experiment
harness whose ``REGISTRATION_KEYS`` / ``EXECUTION_KEYS`` contract must not change.
Per the integration brief, ONE bounded runner is wired here as the canonical proof
path that enforces the task-acceptance boundary before any mutating executor call.

Pipeline (deterministic order):
    1. receive task
    2. receive trusted history
    3. receive current autonomy level
    4. receive safety context
    5. accept_task(...)            (scripts.task_acceptance)
    6. inspect acceptance decision
    7. enforce_execution(...)      (the single executor gate)
    8. invoke executor only if permitted
    9. collect execution result
   10. return combined acceptance + execution outcome

Invariants:
- No executor mutation occurs before step 7. There is NO code path that calls the
  executor directly; ``enforce_execution`` is the only gate.
- The executor is an injected, provider-neutral callable. No provider-specific code.
- Fail-closed: any acceptance / dispatch / safety / history / level error yields a
  BLOCKED result with ``executor_invoked = False``. An executor exception during a
  permitted call is recorded as ``execution_status = ERROR`` — never a fabricated PASS.
- Execution success is NOT trusted evidence: the runner stores the raw executor
  output as ``execution_result`` and never synthesizes a VERIFIED PASS outcome. The
  existing Evidence Trust Gate still governs any final PASS.

No new orchestration framework / subsystem. Reuses task_acceptance (accept_task,
enforce_execution), which in turn reuse triage_engine, earned_autonomy,
dispatch_autonomy, and validate_package.
"""
from __future__ import annotations

from typing import Any, Callable, Optional

try:  # normal package / module import
    from scripts.task_acceptance import accept_task, enforce_execution
except Exception:  # when loaded standalone via importlib (e.g. tests)
    from task_acceptance import accept_task, enforce_execution  # type: ignore


def run_task(
    task: dict[str, Any],
    executor: Callable[[dict[str, Any]], Any],
    history: Optional[list[dict[str, Any]]] = None,
    current_level: str = "L0",
    *,
    approval_recorded: bool = False,
    scope_violation: bool = False,
    security_violation: bool = False,
    secrets_restricted: bool = False,
    production_restricted: bool = False,
    stop_condition: bool = False,
    required_checks: Optional[tuple[str, ...]] = None,
) -> dict[str, Any]:
    """Run one task through the acceptance boundary and, if permitted, the executor.

    Returns a combined acceptance + execution outcome. The executor is invoked ONLY
    via ``enforce_execution``; it can never run below the permitted action or before
    the human gate. Fails closed on any error.
    """
    # 5. call accept_task (fail-closed inside task_acceptance)
    acceptance = accept_task(
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
    allowed = acceptance["allowed_action"]
    acceptance_state = acceptance["acceptance_state"]

    events: list[str] = ["acceptance"]
    execution_status = "NOT_RUN"
    execution_result: Any = None
    execution_invoked = False

    # 7/8. enforce_execution is the ONLY path to the executor.
    try:
        result = enforce_execution(acceptance, executor, approval_recorded=approval_recorded)
    except Exception as exc:
        # Executor raised during a permitted call: record ERROR, never fake PASS.
        events.append("enforcement")
        events.append("executor")
        return {
            "task_id": acceptance.get("task_id"),
            "acceptance_state": acceptance_state,
            "allowed_action": allowed,
            "executor_invoked": True,
            "approval_recorded": approval_recorded,
            "execution_status": "ERROR",
            "execution_result": {"error": f"{type(exc).__name__}: {exc}"},
            "blocking_reasons": acceptance.get("blocking_reasons", []),
            "reason": f"executor error: {exc}",
            "dispatch_evaluation_id": acceptance.get("dispatch_evaluation_id"),
            "task_risk_tier": acceptance.get("task_risk_tier"),
            "current_autonomy_level": acceptance.get("current_autonomy_level"),
            "earned_recommended_level": acceptance.get("earned_recommended_level"),
            "events": events,
        }

    events.append("enforcement")
    if result is None:
        # Executor not permitted for this decision / approval state.
        execution_invoked = False
        if acceptance_state == "BLOCKED":
            execution_status = "BLOCKED"
        elif allowed == "EXECUTE_WITH_APPROVAL" and not approval_recorded:
            execution_status = "HUMAN_REQUIRED"
        else:
            execution_status = "NOT_PERMITTED"
    else:
        # 8/9. Executor ran exactly once, only because the gate permitted it.
        events.append("executor")
        execution_invoked = True
        execution_status = "RAN"
        execution_result = result

    return {
        "task_id": acceptance.get("task_id"),
        "acceptance_state": acceptance_state,
        "allowed_action": allowed,
        "executor_invoked": execution_invoked,
        "approval_recorded": approval_recorded,
        "execution_status": execution_status,
        "execution_result": execution_result,
        "blocking_reasons": acceptance.get("blocking_reasons", []),
        "reason": acceptance.get("reason"),
        "dispatch_evaluation_id": acceptance.get("dispatch_evaluation_id"),
        "task_risk_tier": acceptance.get("task_risk_tier"),
        "current_autonomy_level": acceptance.get("current_autonomy_level"),
        "earned_recommended_level": acceptance.get("earned_recommended_level"),
        "events": events,
    }
