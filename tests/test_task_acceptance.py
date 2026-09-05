"""MPE Earned Autonomy — task-acceptance integration tests.

Proves ``scripts/task_acceptance`` routes every accepted task through triage ->
earned autonomy -> dispatch_with_autonomy, FAILS CLOSED on any error, and ENFORCES
the decision so the executor can only run when genuinely permitted. Uses a fake
executor (no real provider). Existing dispatch / Earned Autonomy / Evidence Trust /
triage / approval behavior and package validation all remain unchanged.
"""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import dispatch_autonomy as dispatch  # noqa: E402
import earned_autonomy as earned  # noqa: E402
import exp13_checks as exp13  # noqa: E402
import task_acceptance as ta  # noqa: E402
import triage_engine as triage  # noqa: E402
import validate_package as vp  # noqa: E402
from unittest import mock  # noqa: E402

DEFAULT_GATES = [
    {"gate_id": "clean_diff_scope", "result": "PASS", "evidence_ref": "git_status"},
    {"gate_id": "secrets_scan", "result": "PASS", "evidence_ref": "secrets_scan"},
    {"gate_id": "build", "result": "PASS", "evidence_ref": "compileall"},
]


def verified_pass(gates=None) -> dict:
    return {"outcome": "PASS", "deterministic_gate_results": gates or DEFAULT_GATES}


def untrusted_pass() -> dict:
    return {
        "outcome": "PASS",
        "deterministic_gate_results": [
            {"gate_id": "clean_diff_scope", "result": "PASS", "evidence_ref": "self_reported"},
            {"gate_id": "secrets_scan", "result": "PASS", "evidence_ref": "self_reported"},
            {"gate_id": "build", "result": "PASS", "evidence_ref": "self_reported"},
        ],
    }


def unknown_pass() -> dict:
    return {
        "outcome": "PASS",
        "deterministic_gate_results": [
            {"gate_id": "clean_diff_scope", "result": "PASS", "evidence_ref": "unknown"},
            {"gate_id": "secrets_scan", "result": "PASS", "evidence_ref": "unknown"},
            {"gate_id": "build", "result": "PASS", "evidence_ref": "unknown"},
        ],
    }


def fast_task() -> dict:
    return {
        "task_id": "t-fast-1",
        "summary": "low risk fast task",
        "affected_repositories": ["repo-a"],
        "acceptance_criteria_present": True,
        "rollback_known": True,
        "ratings": {"complexity": 0, "risk": 0, "architectural_impact": 0, "data_sensitivity": 0, "unknowns": 0},
        "signals": [],
    }


def approval_task() -> dict:
    return {
        "task_id": "t-appr-1",
        "summary": "production change requiring approval",
        "affected_repositories": ["repo-a"],
        "acceptance_criteria_present": True,
        "rollback_known": True,
        "ratings": {"complexity": 1, "risk": 1, "architectural_impact": 1, "data_sensitivity": 0, "unknowns": 0},
        "signals": ["production_change"],
    }


def deep_change_task() -> dict:
    return {
        "task_id": "t-dc-1",
        "summary": "architecture redesign",
        "affected_repositories": ["repo-a"],
        "acceptance_criteria_present": True,
        "rollback_known": True,
        "ratings": {"complexity": 1, "risk": 1, "architectural_impact": 1, "data_sensitivity": 0, "unknowns": 1},
        "signals": ["architecture_redesign"],
    }


class FakeExecutor:
    def __init__(self):
        self.calls = 0

    def __call__(self, decision: dict) -> dict:
        self.calls += 1
        return {"ran": True, "task_id": decision.get("task_id")}


class TaskAcceptanceTests(unittest.TestCase):
    # TEST 1: L0 + FAST -> OBSERVE -> executor not invoked
    def test_l0_observe_executor_not_invoked(self):
        r = ta.accept_task(fast_task(), history=[], current_level="L0")
        self.assertEqual(r["allowed_action"], "OBSERVE")
        self.assertEqual(r["acceptance_state"], "ACCEPTED_OBSERVE")
        ex = FakeExecutor()
        ta.enforce_execution(r, ex)
        self.assertEqual(ex.calls, 0)

    # TEST 2: L1 + FAST -> RECOMMEND -> executor not invoked
    def test_l1_recommend_executor_not_invoked(self):
        r = ta.accept_task(fast_task(), history=[verified_pass()], current_level="L1")
        self.assertEqual(r["allowed_action"], "RECOMMEND")
        self.assertEqual(r["acceptance_state"], "ACCEPTED_RECOMMEND")
        ex = FakeExecutor()
        ta.enforce_execution(r, ex)
        self.assertEqual(ex.calls, 0)

    # TEST 3: L2 + FAST -> DRAFT -> final executor not invoked
    def test_l2_draft_final_executor_not_invoked(self):
        r = ta.accept_task(fast_task(), history=[verified_pass() for _ in range(3)], current_level="L2")
        self.assertEqual(r["allowed_action"], "DRAFT")
        self.assertEqual(r["acceptance_state"], "ACCEPTED_DRAFT")
        self.assertFalse(r["execution_allowed"])
        ex = FakeExecutor()
        ta.enforce_execution(r, ex)
        self.assertEqual(ex.calls, 0)

    # TEST 4: L3 + FAST -> EXECUTE_WITH_APPROVAL -> human gate -> not invoked before approval
    def test_l3_execute_with_approval_human_gate(self):
        r = ta.accept_task(fast_task(), history=[verified_pass() for _ in range(5)], current_level="L3")
        self.assertEqual(r["allowed_action"], "EXECUTE_WITH_APPROVAL")
        self.assertEqual(r["acceptance_state"], "HUMAN_REQUIRED")
        self.assertTrue(r["human_gate_required"])
        ex = FakeExecutor()
        ta.enforce_execution(r, ex)  # no approval recorded
        self.assertEqual(ex.calls, 0)

    # TEST 5: L3 + explicit approval -> execution may proceed
    def test_l3_with_approval_executes(self):
        r = ta.accept_task(fast_task(), history=[verified_pass() for _ in range(5)], current_level="L3")
        ex = FakeExecutor()
        result = ta.enforce_execution(r, ex, approval_recorded=True)
        self.assertEqual(ex.calls, 1)
        self.assertEqual(result["ran"], True)

    # TEST 6: L4 + FAST + all gates clear -> READY_TO_EXECUTE -> executor invoked
    def test_l4_fast_ready_to_execute(self):
        r = ta.accept_task(fast_task(), history=[verified_pass() for _ in range(5)], current_level="L4")
        self.assertEqual(r["allowed_action"], "EXECUTE")
        self.assertEqual(r["acceptance_state"], "READY_TO_EXECUTE")
        self.assertFalse(r["human_gate_required"])
        ex = FakeExecutor()
        ta.enforce_execution(r, ex)
        self.assertEqual(ex.calls, 1)

    # TEST 7: L4 + DEEP-CHANGE -> HUMAN_REQUIRED -> no autonomous execution
    def test_l4_deep_change_human_required(self):
        r = ta.accept_task(deep_change_task(), history=[verified_pass() for _ in range(5)], current_level="L4")
        self.assertEqual(r["acceptance_state"], "HUMAN_REQUIRED")
        self.assertEqual(r["task_risk_tier"], "DEEP-CHANGE")
        self.assertTrue(r["human_gate_required"])
        ex = FakeExecutor()
        ta.enforce_execution(r, ex)  # no approval recorded
        self.assertEqual(ex.calls, 0)

    # TEST 8: L4 + scope violation -> BLOCKED / safe state -> not invoked
    def test_l4_scope_violation_blocked(self):
        r = ta.accept_task(
            fast_task(), history=[verified_pass() for _ in range(5)], current_level="L4", scope_violation=True
        )
        self.assertIn("scope_violation", r["blocking_reasons"])
        self.assertEqual(r["acceptance_state"], "BLOCKED")
        self.assertFalse(r["execution_allowed"])
        ex = FakeExecutor()
        ta.enforce_execution(r, ex)
        self.assertEqual(ex.calls, 0)

    # TEST 9: L4 + security violation -> blocked -> not invoked
    def test_l4_security_violation_blocked(self):
        r = ta.accept_task(
            fast_task(), history=[verified_pass() for _ in range(5)], current_level="L4", security_violation=True
        )
        self.assertIn("security_violation", r["blocking_reasons"])
        self.assertEqual(r["acceptance_state"], "BLOCKED")
        ex = FakeExecutor()
        ta.enforce_execution(r, ex)
        self.assertEqual(ex.calls, 0)

    # TEST 10: untrusted history -> earned authority not increased -> not invoked above lower level
    def test_untrusted_history_no_authority_increase(self):
        r = ta.accept_task(fast_task(), history=[untrusted_pass()], current_level="L4")
        self.assertEqual(r["earned_recommended_level"], "L0")
        self.assertEqual(r["allowed_action"], "OBSERVE")
        ex = FakeExecutor()
        ta.enforce_execution(r, ex)
        self.assertEqual(ex.calls, 0)

    # TEST 11: unknown evidence history -> same fail-closed behavior
    def test_unknown_evidence_history_fail_closed(self):
        r = ta.accept_task(fast_task(), history=[unknown_pass()], current_level="L4")
        self.assertEqual(r["earned_recommended_level"], "L0")
        self.assertEqual(r["allowed_action"], "OBSERVE")
        ex = FakeExecutor()
        ta.enforce_execution(r, ex)
        self.assertEqual(ex.calls, 0)

    # TEST 12: missing/invalid autonomy level -> safe failure, no execution
    def test_invalid_autonomy_level_safe_failure(self):
        r = ta.accept_task(fast_task(), history=[verified_pass() for _ in range(5)], current_level="L9")
        self.assertEqual(r["acceptance_state"], "BLOCKED")
        self.assertEqual(r["allowed_action"], "OBSERVE")
        self.assertFalse(r["execution_allowed"])
        ex = FakeExecutor()
        ta.enforce_execution(r, ex)
        self.assertEqual(ex.calls, 0)

    # TEST 13: triage error -> safe failure, no execution
    def test_triage_error_safe_failure(self):
        r = ta.accept_task({}, current_level="L4")  # invalid task contract
        self.assertEqual(r["acceptance_state"], "BLOCKED")
        self.assertFalse(r["execution_allowed"])
        ex = FakeExecutor()
        ta.enforce_execution(r, ex)
        self.assertEqual(ex.calls, 0)

    # TEST 14: dispatch error -> safe failure, no execution
    def test_dispatch_error_safe_failure(self):
        with mock.patch.object(ta, "dispatch_with_autonomy", side_effect=RuntimeError("boom")):
            r = ta.accept_task(fast_task(), history=[verified_pass() for _ in range(5)], current_level="L4")
        self.assertEqual(r["acceptance_state"], "BLOCKED")
        self.assertEqual(r["allowed_action"], "OBSERVE")
        ex = FakeExecutor()
        ta.enforce_execution(r, ex)
        self.assertEqual(ex.calls, 0)

    # TEST 15: existing dispatch tests unchanged
    def test_dispatch_unchanged(self):
        self.assertEqual(
            dispatch.dispatch_with_autonomy(fast_task(), history=[verified_pass() for _ in range(5)], current_level="L4")["allowed_action"],
            "EXECUTE",
        )

    # TEST 16: existing Earned Autonomy tests unchanged
    def test_earned_autonomy_unchanged(self):
        self.assertEqual(earned.evaluate_autonomy([verified_pass() for _ in range(5)], "L0")["recommended_level"], "L3")

    # TEST 17: existing Evidence Trust tests unchanged
    def test_evidence_trust_unchanged(self):
        self.assertEqual(vp.classify_evidence_ref("self_reported"), "UNTRUSTED")
        self.assertEqual(vp.derive_execution_outcome(untrusted_pass()["deterministic_gate_results"]), "REWORK")

    # TEST 18: existing triage tests unchanged
    def test_triage_unchanged(self):
        self.assertEqual(triage.triage(fast_task())["recommended_risk_tier"], "FAST")

    # TEST 19: existing approval behavior unchanged
    def test_approval_unchanged(self):
        self.assertEqual(exp13.derive_outcome({"escalation": "HUMAN_REVIEW_REQUIRED"}, []), "HUMAN_REQUIRED")

    # TEST 20: existing package validation unchanged
    def test_package_validation_unchanged(self):
        errors = vp.validate(ROOT)
        self.assertEqual(errors, [], f"package validation regressed: {errors}")


# Explicit bypass test (brief section 16): executor_call_count invariants.
class ExecutorBypassTests(unittest.TestCase):
    def test_executor_call_count_bypass(self):
        # (current_level, history, kwargs) -> expected call count
        scenarios = [
            ("L0", [], {}, 0),
            ("L1", [verified_pass()], {}, 0),
            ("L2", [verified_pass() for _ in range(3)], {}, 0),
            ("L3", [verified_pass() for _ in range(5)], {}, 0),  # no approval
            ("L4", [verified_pass() for _ in range(5)], {"scope_violation": True}, 0),
            ("L3", [verified_pass() for _ in range(5)], {}, 1),  # approval recorded
            ("L4", [verified_pass() for _ in range(5)], {}, 1),
        ]
        for current_level, history, kwargs, expected in scenarios:
            r = ta.accept_task(fast_task(), history=history, current_level=current_level, **kwargs)
            ex = FakeExecutor()
            approval = current_level == "L3" and expected == 1
            ta.enforce_execution(r, ex, approval_recorded=approval)
            self.assertEqual(
                ex.calls, expected,
                f"level={current_level} history={len(history)} kwargs={kwargs} -> expected {expected}, got {ex.calls}",
            )

    def test_fail_closed_never_invokes_executor(self):
        for bad in (dict(current_level="L9"), dict(task=None), dict(history="not-a-list")):
            kwargs = {"current_level": bad.get("current_level", "L4")}
            if "task" in bad:
                task = bad["task"]
            else:
                task = fast_task()
            if "history" in bad:
                kwargs["history"] = bad["history"]
            r = ta.accept_task(task, **kwargs)
            self.assertEqual(r["acceptance_state"], "BLOCKED")
            ex = FakeExecutor()
            ta.enforce_execution(r, ex)
            self.assertEqual(ex.calls, 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
