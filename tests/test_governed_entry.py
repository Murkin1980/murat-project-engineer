"""MPE — real entry point wiring tests.

The real Task Packet intake is ``scripts/triage_engine.py`` (the deterministic
triage CLI/module). This suite covers its opt-in governed-run mode
(``triage_engine.governed_run``), which routes a Task Packet through the
already-validated path:

    governed_run -> execution_runner.run_task -> accept_task
                 -> dispatch_with_autonomy -> evaluate_autonomy
                 -> enforce_execution -> [injected executor]

It proves the entry point can never call the executor below the permitted
action, fails closed on any error, and never turns an executor self-report into
a VERIFIED PASS. Existing execution-runner / task-acceptance / dispatch /
Earned Autonomy / Evidence Trust / package-validation behavior is unchanged.

A fake/stub executor is used throughout (no real provider).
"""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import execution_runner as runner  # noqa: E402
import task_acceptance as ta  # noqa: E402
import triage_engine as te  # noqa: E402
import validate_package as vp  # noqa: E402

DEFAULT_GATES = [
    {"gate_id": "clean_diff_scope", "result": "PASS", "evidence_ref": "git_status"},
    {"gate_id": "secrets_scan", "result": "PASS", "evidence_ref": "secrets_scan"},
    {"gate_id": "build", "result": "PASS", "evidence_ref": "compileall"},
]


def verified_pass(gates=None) -> dict:
    return {"outcome": "PASS", "deterministic_gate_results": gates or DEFAULT_GATES}


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
    """Counts calls; returns a plain self-reported PASS (never trusted)."""

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


class GovernedEntryTests(unittest.TestCase):
    # Defaults are conservative: empty history + L0.
    def test_defaults_are_conservative_l0_empty_history(self):
        ex = FakeExecutor()
        r = te.governed_run(fast_task(), ex)  # no level / history
        self.assertEqual(ex.calls, 0)
        self.assertFalse(r["executor_invoked"])
        self.assertEqual(r["acceptance_state"], "ACCEPTED_OBSERVE")

    # 1. L0 -> executor 0
    def test_l0_executor_not_called(self):
        ex = FakeExecutor()
        r = te.governed_run(fast_task(), ex, history=[], current_level="L0")
        self.assertEqual(ex.calls, 0)
        self.assertFalse(r["executor_invoked"])

    # 2. L1 -> executor 0
    def test_l1_executor_not_called(self):
        ex = FakeExecutor()
        r = te.governed_run(fast_task(), ex, history=[verified_pass()], current_level="L1")
        self.assertEqual(ex.calls, 0)

    # 3. L2 -> executor 0
    def test_l2_executor_not_called(self):
        ex = FakeExecutor()
        r = te.governed_run(fast_task(), ex, history=[verified_pass() for _ in range(3)], current_level="L2")
        self.assertEqual(ex.calls, 0)

    # 4. L3 without approval -> 0 + HUMAN_REQUIRED
    def test_l3_no_approval_human_required(self):
        ex = FakeExecutor()
        r = te.governed_run(fast_task(), ex, history=[verified_pass() for _ in range(5)], current_level="L3")
        self.assertEqual(ex.calls, 0)
        self.assertFalse(r["executor_invoked"])
        self.assertEqual(r["acceptance_state"], "HUMAN_REQUIRED")
        self.assertEqual(r["execution_status"], "HUMAN_REQUIRED")

    # 5. L3 with explicit approval -> 1
    def test_l3_approved_runs(self):
        ex = FakeExecutor()
        r = te.governed_run(
            fast_task(), ex, history=[verified_pass() for _ in range(5)],
            current_level="L3", approval_recorded=True,
        )
        self.assertEqual(ex.calls, 1)
        self.assertTrue(r["executor_invoked"])
        self.assertEqual(r["execution_status"], "RAN")

    # 6. L4 FAST clear -> 1
    def test_l4_fast_clear_runs(self):
        ex = FakeExecutor()
        r = te.governed_run(fast_task(), ex, history=[verified_pass() for _ in range(5)], current_level="L4")
        self.assertEqual(ex.calls, 1)
        self.assertTrue(r["executor_invoked"])

    # 7. L4 scope blocker -> 0
    def test_l4_scope_blocker_blocks(self):
        ex = FakeExecutor()
        r = te.governed_run(
            fast_task(), ex, history=[verified_pass() for _ in range(5)],
            current_level="L4", scope_violation=True,
        )
        self.assertEqual(ex.calls, 0)
        self.assertFalse(r["executor_invoked"])
        self.assertEqual(r["acceptance_state"], "BLOCKED")

    # 8. L4 security blocker -> 0
    def test_l4_security_blocker_blocks(self):
        ex = FakeExecutor()
        r = te.governed_run(
            fast_task(), ex, history=[verified_pass() for _ in range(5)],
            current_level="L4", security_violation=True,
        )
        self.assertEqual(ex.calls, 0)
        self.assertFalse(r["executor_invoked"])
        self.assertEqual(r["acceptance_state"], "BLOCKED")

    # 8b. remaining hard-safety blockers also block L4
    def test_l4_secrets_production_stop_blockers_block(self):
        for flag in ("secrets_restricted", "production_restricted", "stop_condition"):
            ex = FakeExecutor()
            r = te.governed_run(
                fast_task(), ex, history=[verified_pass() for _ in range(5)],
                current_level="L4", **{flag: True},
            )
            self.assertEqual(ex.calls, 0, flag)
            self.assertFalse(r["executor_invoked"], flag)
            self.assertEqual(r["acceptance_state"], "BLOCKED", flag)

    # 9. DEEP-CHANGE without approval -> 0
    def test_deep_change_no_approval_blocks(self):
        ex = FakeExecutor()
        r = te.governed_run(deep_change_task(), ex, history=[verified_pass() for _ in range(5)], current_level="L4")
        self.assertEqual(ex.calls, 0)
        self.assertFalse(r["executor_invoked"])
        self.assertEqual(r["acceptance_state"], "HUMAN_REQUIRED")

    # 9b. DEEP-CHANGE with explicit approval still gated, runs only after gate
    def test_deep_change_with_approval_runs_once(self):
        ex = FakeExecutor()
        r = te.governed_run(
            deep_change_task(), ex, history=[verified_pass() for _ in range(5)],
            current_level="L4", approval_recorded=True,
        )
        self.assertEqual(ex.calls, 1)
        self.assertTrue(r["executor_invoked"])

    # 10. invalid input -> fail closed, executor never called
    def test_invalid_input_fail_closed(self):
        for bad in ({}, None, "not-a-dict", []):
            ex = FakeExecutor()
            r = te.governed_run(bad, ex, current_level="L4")  # type: ignore[arg-type]
            self.assertEqual(ex.calls, 0, bad)
            self.assertFalse(r["executor_invoked"], bad)
            self.assertEqual(r["acceptance_state"], "BLOCKED", bad)

    def test_invalid_level_fail_closed(self):
        ex = FakeExecutor()
        r = te.governed_run(fast_task(), ex, history=[verified_pass() for _ in range(5)], current_level="L9")
        self.assertEqual(ex.calls, 0)
        self.assertFalse(r["executor_invoked"])
        self.assertEqual(r["acceptance_state"], "BLOCKED")

    # 11. executor raises -> ERROR, never a fabricated PASS
    def test_executor_error_is_error_not_pass(self):
        ex = RaisingExecutor()
        r = te.governed_run(fast_task(), ex, history=[verified_pass() for _ in range(5)], current_level="L4")
        self.assertEqual(ex.calls, 1)
        self.assertEqual(r["execution_status"], "ERROR")
        self.assertNotEqual(r["execution_status"], "PASS")
        self.assertIn("error", r["execution_result"])

    # 12. executor self-report {"status":"PASS"} -> NOT a VERIFIED PASS
    def test_executor_self_report_not_verified(self):
        ex = FakeExecutor()
        r = te.governed_run(fast_task(), ex, history=[verified_pass() for _ in range(5)], current_level="L4")
        self.assertEqual(r["execution_status"], "RAN")
        self.assertEqual(r["execution_result"]["status"], "PASS")  # raw output preserved
        self.assertNotEqual(r["execution_status"], "VERIFIED_PASS")
        self.assertNotIn("verified_pass", r)
        self.assertNotIn("outcome", r)  # no synthesized trusted outcome
        # trust is never inferred from executor identity
        r2 = te.governed_run(deep_change_task(), ex, current_level="L4")
        self.assertFalse(r2["executor_invoked"])

    # The entry point never calls the executor directly — it only delegates to run_task.
    def test_entry_delegates_to_runner_never_calls_executor_directly(self):
        import inspect

        source = inspect.getsource(te.governed_run)
        self.assertNotIn("executor(", source.replace("run_task(", ""))
        self.assertIn("run_task(", source)

    # The built-in CLI executor is non-mutating (provider-neutral probe).
    def test_default_cli_executor_is_non_mutating_probe(self):
        r = te.governed_run(fast_task(), history=[verified_pass() for _ in range(5)], current_level="L4")
        self.assertTrue(r["executor_invoked"])
        self.assertEqual(r["execution_result"]["status"], "PROBE_ONLY")
        self.assertFalse(r["execution_result"]["executed"])

    # Events preserve the fixed order: acceptance -> enforcement -> executor.
    def test_event_order_acceptance_before_enforcement_before_executor(self):
        ex = FakeExecutor()
        r = te.governed_run(
            fast_task(), ex, history=[verified_pass() for _ in range(5)],
            current_level="L3", approval_recorded=True,
        )
        events = r["events"]
        self.assertEqual(events[0], "acceptance")
        self.assertLess(events.index("acceptance"), events.index("enforcement"))
        self.assertLess(events.index("enforcement"), events.index("executor"))


class GovernedEntryCliTests(unittest.TestCase):
    """End-to-end via the real CLI (the actual entry point)."""

    def _run_cli(self, task, *extra, history=None):
        with tempfile.TemporaryDirectory() as tmp:
            task_path = Path(tmp) / "task.json"
            task_path.write_text(json.dumps(task), encoding="utf-8")
            cmd = [sys.executable, str(ROOT / "scripts" / "triage_engine.py"), str(task_path), *extra]
            if history is not None:
                hist_path = Path(tmp) / "history.json"
                hist_path.write_text(json.dumps(history), encoding="utf-8")
                cmd += ["--history-file", str(hist_path)]
            proc = subprocess.run(cmd, capture_output=True, text=True, cwd=str(ROOT))
            return proc

    def test_cli_default_triage_unchanged(self):
        proc = self._run_cli(fast_task())
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertEqual(json.loads(proc.stdout)["recommended_risk_tier"], "FAST")

    def test_cli_governed_run_default_l0_blocks(self):
        proc = self._run_cli(fast_task(), "--governed-run")
        self.assertEqual(proc.returncode, 0, proc.stderr)
        out = json.loads(proc.stdout)
        self.assertFalse(out["executor_invoked"])
        self.assertIn(out["execution_status"], {"NOT_PERMITTED", "BLOCKED"})

    def test_cli_governed_run_l4_clear_invokes_probe(self):
        hist = [verified_pass() for _ in range(5)]
        proc = self._run_cli(fast_task(), "--governed-run", "--level", "L4", history=hist)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        out = json.loads(proc.stdout)
        self.assertTrue(out["executor_invoked"])
        self.assertEqual(out["execution_result"]["status"], "PROBE_ONLY")

    def test_cli_governed_run_invalid_task_fails_closed(self):
        proc = self._run_cli({}, "--governed-run", "--level", "L4")
        self.assertEqual(proc.returncode, 0, proc.stderr)  # fail closed, not a crash
        out = json.loads(proc.stdout)
        self.assertFalse(out["executor_invoked"])
        self.assertEqual(out["acceptance_state"], "BLOCKED")

    def test_cli_backtest_and_governed_run_mutually_exclusive(self):
        proc = self._run_cli({"cases": []}, "--backtest", "--governed-run")
        self.assertNotEqual(proc.returncode, 0)


class ExistingModulesUnchangedTests(unittest.TestCase):
    # 13. execution runner unchanged
    def test_execution_runner_unchanged(self):
        ex = FakeExecutor()
        r = runner.run_task(fast_task(), ex, history=[verified_pass() for _ in range(5)], current_level="L4")
        self.assertTrue(r["executor_invoked"])

    # 14. task acceptance unchanged
    def test_task_acceptance_unchanged(self):
        r = ta.accept_task(fast_task(), history=[verified_pass() for _ in range(5)], current_level="L4")
        self.assertEqual(r["acceptance_state"], "READY_TO_EXECUTE")

    # 18. package validation unchanged
    def test_package_validation_unchanged(self):
        self.assertEqual(vp.validate(ROOT), [])


if __name__ == "__main__":
    unittest.main(verbosity=2)
