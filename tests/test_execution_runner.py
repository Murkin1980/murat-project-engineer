"""MPE Earned Autonomy — execution-runner wiring tests.

Proves ``scripts.execution_runner.run_task`` routes every mutating execution through
accept_task -> enforce_execution before the executor runs, fails closed on any
error, and never lets executor self-report become a trusted VERIFIED PASS. Uses a
fake/stub executor (no real provider). Existing task-acceptance / dispatch / Earned
Autonomy / Evidence Trust / triage / approval behavior and package validation remain
unchanged.
"""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import dispatch_autonomy as dispatch  # noqa: E402
import earned_autonomy as earned  # noqa: E402
import execution_runner as runner  # noqa: E402
import task_acceptance as ta  # noqa: E402
import triage_engine as triage  # noqa: E402
import validate_package as vp  # noqa: E402

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
        return {"status": "PASS", "task_id": decision.get("task_id")}


class RaisingExecutor:
    def __init__(self):
        self.calls = 0

    def __call__(self, decision: dict) -> dict:
        self.calls += 1
        raise RuntimeError("executor boom")


class ExecutionRunnerTests(unittest.TestCase):
    # TEST 1: runner + L0 -> executor calls = 0
    def test_l0_executor_not_called(self):
        ex = FakeExecutor()
        r = runner.run_task(fast_task(), ex, history=[], current_level="L0")
        self.assertEqual(ex.calls, 0)
        self.assertFalse(r["executor_invoked"])

    # TEST 2: runner + L1 -> executor calls = 0
    def test_l1_executor_not_called(self):
        ex = FakeExecutor()
        r = runner.run_task(fast_task(), ex, history=[verified_pass()], current_level="L1")
        self.assertEqual(ex.calls, 0)

    # TEST 3: runner + L2 -> executor calls = 0
    def test_l2_executor_not_called(self):
        ex = FakeExecutor()
        r = runner.run_task(fast_task(), ex, history=[verified_pass() for _ in range(3)], current_level="L2")
        self.assertEqual(ex.calls, 0)
        self.assertEqual(r["execution_status"], "NOT_PERMITTED")

    # TEST 4: runner + L3 without approval -> 0 + HUMAN_REQUIRED
    def test_l3_no_approval_human_required(self):
        ex = FakeExecutor()
        r = runner.run_task(fast_task(), ex, history=[verified_pass() for _ in range(5)], current_level="L3")
        self.assertEqual(ex.calls, 0)
        self.assertFalse(r["executor_invoked"])
        self.assertEqual(r["acceptance_state"], "HUMAN_REQUIRED")
        self.assertEqual(r["execution_status"], "HUMAN_REQUIRED")

    # TEST 5: runner + L3 with explicit approval -> 1
    def test_l3_with_approval_runs(self):
        ex = FakeExecutor()
        r = runner.run_task(fast_task(), ex, history=[verified_pass() for _ in range(5)], current_level="L3", approval_recorded=True)
        self.assertEqual(ex.calls, 1)
        self.assertTrue(r["executor_invoked"])
        self.assertEqual(r["execution_status"], "RAN")

    # TEST 6: runner + L4 FAST clear -> 1
    def test_l4_fast_runs(self):
        ex = FakeExecutor()
        r = runner.run_task(fast_task(), ex, history=[verified_pass() for _ in range(5)], current_level="L4")
        self.assertEqual(ex.calls, 1)
        self.assertTrue(r["executor_invoked"])

    # TEST 7: runner + L4 DEEP-CHANGE without approval -> 0
    def test_l4_deep_change_no_approval(self):
        ex = FakeExecutor()
        r = runner.run_task(deep_change_task(), ex, history=[verified_pass() for _ in range(5)], current_level="L4")
        self.assertEqual(ex.calls, 0)
        self.assertFalse(r["executor_invoked"])

    # TEST 8: runner + L4 DEEP-CHANGE with explicit approval -> 1 only after gate
    def test_l4_deep_change_with_approval_runs(self):
        ex = FakeExecutor()
        r = runner.run_task(deep_change_task(), ex, history=[verified_pass() for _ in range(5)], current_level="L4", approval_recorded=True)
        self.assertEqual(ex.calls, 1)
        self.assertTrue(r["executor_invoked"])

    # TEST 9: scope blocker -> 0
    def test_scope_blocker(self):
        ex = FakeExecutor()
        r = runner.run_task(fast_task(), ex, history=[verified_pass() for _ in range(5)], current_level="L4", scope_violation=True)
        self.assertEqual(ex.calls, 0)
        self.assertFalse(r["executor_invoked"])
        self.assertEqual(r["acceptance_state"], "BLOCKED")

    # TEST 10: security blocker -> 0
    def test_security_blocker(self):
        ex = FakeExecutor()
        r = runner.run_task(fast_task(), ex, history=[verified_pass() for _ in range(5)], current_level="L4", security_violation=True)
        self.assertEqual(ex.calls, 0)
        self.assertFalse(r["executor_invoked"])

    # TEST 11: secrets restriction -> 0
    def test_secrets_restriction(self):
        ex = FakeExecutor()
        r = runner.run_task(fast_task(), ex, history=[verified_pass() for _ in range(5)], current_level="L4", secrets_restricted=True)
        self.assertEqual(ex.calls, 0)
        self.assertFalse(r["executor_invoked"])

    # TEST 12: stop condition -> 0
    def test_stop_condition(self):
        ex = FakeExecutor()
        r = runner.run_task(fast_task(), ex, history=[verified_pass() for _ in range(5)], current_level="L4", stop_condition=True)
        self.assertEqual(ex.calls, 0)
        self.assertFalse(r["executor_invoked"])

    # TEST 13: untrusted history -> authority not raised -> 0
    def test_untrusted_history(self):
        ex = FakeExecutor()
        r = runner.run_task(fast_task(), ex, history=[untrusted_pass()], current_level="L4")
        self.assertEqual(ex.calls, 0)
        self.assertFalse(r["executor_invoked"])

    # TEST 14: invalid task -> fail closed -> 0
    def test_invalid_task_fail_closed(self):
        ex = FakeExecutor()
        r = runner.run_task({}, ex, current_level="L4")
        self.assertEqual(ex.calls, 0)
        self.assertFalse(r["executor_invoked"])
        self.assertEqual(r["acceptance_state"], "BLOCKED")

    # TEST 15: invalid autonomy level -> fail closed -> 0
    def test_invalid_level_fail_closed(self):
        ex = FakeExecutor()
        r = runner.run_task(fast_task(), ex, history=[verified_pass() for _ in range(5)], current_level="L9")
        self.assertEqual(ex.calls, 0)
        self.assertFalse(r["executor_invoked"])
        self.assertEqual(r["acceptance_state"], "BLOCKED")

    # TEST 16: executor raises exception -> ERROR, no fabricated PASS
    def test_executor_exception_error(self):
        ex = RaisingExecutor()
        r = runner.run_task(fast_task(), ex, history=[verified_pass() for _ in range(5)], current_level="L4")
        self.assertEqual(ex.calls, 1)  # executor was invoked, then errored
        self.assertEqual(r["execution_status"], "ERROR")
        self.assertNotEqual(r["execution_status"], "PASS")
        self.assertNotIn("verified_pass", str(r).lower())
        self.assertIn("error", r["execution_result"])

    # TEST 17: executor returns {"status":"PASS"} -> NOT a trusted VERIFIED PASS
    def test_executor_pass_not_verified(self):
        ex = FakeExecutor()
        r = runner.run_task(fast_task(), ex, history=[verified_pass() for _ in range(5)], current_level="L4")
        self.assertEqual(r["execution_status"], "RAN")
        self.assertEqual(r["execution_result"], {"status": "PASS", "task_id": "t-fast-1"})
        # The runner must never claim a trusted VERIFIED PASS from executor self-report.
        self.assertNotEqual(r["execution_status"], "VERIFIED_PASS")
        self.assertNotIn("verified_pass", r)
        self.assertNotIn("outcome", r)  # no synthesized outcome field

    # TEST 18: existing task-acceptance tests unchanged
    def test_task_acceptance_unchanged(self):
        r = ta.accept_task(fast_task(), history=[verified_pass() for _ in range(5)], current_level="L4")
        self.assertEqual(r["acceptance_state"], "READY_TO_EXECUTE")

    # TEST 19: existing dispatch tests unchanged
    def test_dispatch_unchanged(self):
        self.assertEqual(
            dispatch.dispatch_with_autonomy(fast_task(), history=[verified_pass() for _ in range(5)], current_level="L4")["allowed_action"],
            "EXECUTE",
        )

    # TEST 20: existing Earned Autonomy tests unchanged
    def test_earned_autonomy_unchanged(self):
        self.assertEqual(earned.evaluate_autonomy([verified_pass() for _ in range(5)], "L0")["recommended_level"], "L3")

    # TEST 21: existing Evidence Trust tests unchanged
    def test_evidence_trust_unchanged(self):
        self.assertEqual(vp.classify_evidence_ref("self_reported"), "UNTRUSTED")
        self.assertEqual(vp.derive_execution_outcome(untrusted_pass()["deterministic_gate_results"]), "REWORK")

    # TEST 22: existing package validation unchanged
    def test_package_validation_unchanged(self):
        errors = vp.validate(ROOT)
        self.assertEqual(errors, [], f"package validation regressed: {errors}")


# Explicit mutation-order test (brief section 13): executor never before acceptance/enforcement.
class CallOrderTests(unittest.TestCase):
    def test_executor_never_before_acceptance_enforcement(self):
        for level, hist, kwargs, expect_run in [
            ("L0", [], {}, False),
            ("L1", [verified_pass()], {}, False),
            ("L2", [verified_pass() for _ in range(3)], {}, False),
            ("L3", [verified_pass() for _ in range(5)], {}, False),
            ("L4", [verified_pass() for _ in range(5)], {"scope_violation": True}, False),
            ("L3", [verified_pass() for _ in range(5)], {}, True),  # approval recorded
            ("L4", [verified_pass() for _ in range(5)], {}, True),
        ]:
            ex = FakeExecutor()
            approval = level == "L3" and expect_run
            r = runner.run_task(fast_task(), ex, history=hist, current_level=level, approval_recorded=approval, **kwargs)
            events = r["events"]
            self.assertEqual(events[0], "acceptance")
            self.assertLess(events.index("acceptance"), events.index("enforcement"))
            if not expect_run:
                self.assertNotIn("executor", events)
            else:
                self.assertIn("executor", events)
                # executor always strictly after enforcement
                self.assertLess(events.index("enforcement"), events.index("executor"))
            self.assertEqual(ex.calls == 1, expect_run)


if __name__ == "__main__":
    unittest.main(verbosity=2)
