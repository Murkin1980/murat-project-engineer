"""MPE Earned Autonomy — pre-execution dispatch integration tests.

Proves ``scripts/dispatch_autonomy.dispatch_with_autonomy`` derives the maximum
allowed action deterministically from:
  - the canonical task triage (risk tier + approval)
  - the Earned Autonomy ceiling
  - hard safety gates (scope / security / secrets / production / stop / deep-change)

and that autonomy is a ceiling, never a bypass. Existing triage, Evidence Trust
Gate, Earned Autonomy thresholds, approval outcomes, and package validation are
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


class DispatchAutonomyTests(unittest.TestCase):
    # TEST 1: L0 + FAST -> OBSERVE
    def test_l0_fast_observe(self):
        r = dispatch.dispatch_with_autonomy(fast_task(), history=[], current_level="L0")
        self.assertEqual(r["allowed_action"], "OBSERVE")
        self.assertEqual(r["earned_recommended_level"], "L0")
        self.assertFalse(r["execution_allowed"])

    # TEST 2: L1 + FAST -> RECOMMEND
    def test_l1_fast_recommend(self):
        r = dispatch.dispatch_with_autonomy(fast_task(), history=[verified_pass()], current_level="L1")
        self.assertEqual(r["allowed_action"], "RECOMMEND")
        self.assertEqual(r["earned_recommended_level"], "L1")

    # TEST 3: L2 + FAST -> DRAFT (never execute)
    def test_l2_fast_draft(self):
        r = dispatch.dispatch_with_autonomy(fast_task(), history=[verified_pass() for _ in range(3)], current_level="L2")
        self.assertEqual(r["allowed_action"], "DRAFT")
        self.assertEqual(r["earned_recommended_level"], "L2")
        self.assertFalse(r["execution_allowed"])

    # TEST 4: L3 + FAST -> EXECUTE_WITH_APPROVAL, human gate required
    def test_l3_fast_execute_with_approval(self):
        r = dispatch.dispatch_with_autonomy(fast_task(), history=[verified_pass() for _ in range(5)], current_level="L3")
        self.assertEqual(r["allowed_action"], "EXECUTE_WITH_APPROVAL")
        self.assertTrue(r["human_gate_required"])
        self.assertTrue(r["execution_allowed"])

    # TEST 5: L4 + FAST + no approval/blockers -> EXECUTE
    def test_l4_fast_execute(self):
        r = dispatch.dispatch_with_autonomy(fast_task(), history=[verified_pass() for _ in range(5)], current_level="L4")
        self.assertEqual(r["allowed_action"], "EXECUTE")
        self.assertFalse(r["human_gate_required"])
        self.assertTrue(r["execution_allowed"])

    # TEST 6: L4 + task requires human approval -> NOT autonomous EXECUTE
    def test_l4_approval_not_autonomous_execute(self):
        r = dispatch.dispatch_with_autonomy(approval_task(), history=[verified_pass() for _ in range(5)], current_level="L4")
        self.assertNotEqual(r["allowed_action"], "EXECUTE")
        self.assertEqual(r["allowed_action"], "EXECUTE_WITH_APPROVAL")
        self.assertTrue(r["human_gate_required"])
        self.assertTrue(r["approval_required"])

    # TEST 7: L4 + DEEP-CHANGE -> human approval required, NOT autonomous EXECUTE
    def test_l4_deep_change_not_autonomous_execute(self):
        r = dispatch.dispatch_with_autonomy(deep_change_task(), history=[verified_pass() for _ in range(5)], current_level="L4")
        self.assertNotEqual(r["allowed_action"], "EXECUTE")
        self.assertEqual(r["allowed_action"], "EXECUTE_WITH_APPROVAL")
        self.assertTrue(r["human_gate_required"])
        self.assertEqual(r["task_risk_tier"], "DEEP-CHANGE")

    # TEST 8: L3 + DEEP-CHANGE -> human approval required
    def test_l3_deep_change_human_required(self):
        r = dispatch.dispatch_with_autonomy(deep_change_task(), history=[verified_pass() for _ in range(5)], current_level="L3")
        self.assertEqual(r["allowed_action"], "EXECUTE_WITH_APPROVAL")
        self.assertTrue(r["human_gate_required"])
        self.assertTrue(r["approval_required"])

    # TEST 9: scope violation + any level -> execution blocked/reduced
    def test_scope_violation_blocks(self):
        r = dispatch.dispatch_with_autonomy(
            fast_task(), history=[verified_pass() for _ in range(5)], current_level="L4", scope_violation=True
        )
        self.assertEqual(r["allowed_action"], "OBSERVE")
        self.assertFalse(r["execution_allowed"])
        self.assertIn("scope_violation", r["blocking_reasons"])

    # TEST 10: security violation + L4 -> execution blocked
    def test_security_violation_blocks(self):
        r = dispatch.dispatch_with_autonomy(
            fast_task(), history=[verified_pass() for _ in range(5)], current_level="L4", security_violation=True
        )
        self.assertEqual(r["allowed_action"], "OBSERVE")
        self.assertFalse(r["execution_allowed"])
        self.assertIn("security_violation", r["blocking_reasons"])

    # TEST 11: untrusted history cannot raise earned level -> lower action
    def test_untrusted_history_cannot_raise(self):
        r = dispatch.dispatch_with_autonomy(fast_task(), history=[untrusted_pass()], current_level="L4")
        self.assertEqual(r["earned_recommended_level"], "L0")
        self.assertEqual(r["allowed_action"], "OBSERVE")
        self.assertFalse(r["execution_allowed"])

    # TEST 12: unknown evidence cannot raise earned level
    def test_unknown_evidence_cannot_raise(self):
        r = dispatch.dispatch_with_autonomy(fast_task(), history=[unknown_pass()], current_level="L4")
        self.assertEqual(r["earned_recommended_level"], "L0")
        self.assertEqual(r["allowed_action"], "OBSERVE")

    # TEST 13: existing Evidence Trust Gate unchanged
    def test_evidence_trust_gate_unchanged(self):
        self.assertEqual(vp.classify_evidence_ref("self_reported"), "UNTRUSTED")
        self.assertEqual(vp.classify_evidence_ref("git_status"), "TRUSTED")
        self.assertEqual(vp.derive_execution_outcome(untrusted_pass()["deterministic_gate_results"]), "REWORK")

    # TEST 14: existing Earned Autonomy threshold behavior unchanged
    def test_earned_autonomy_thresholds_unchanged(self):
        self.assertEqual(earned.evaluate_autonomy([verified_pass()], "L0")["recommended_level"], "L1")
        self.assertEqual(earned.evaluate_autonomy([verified_pass() for _ in range(3)], "L0")["recommended_level"], "L2")
        self.assertEqual(earned.evaluate_autonomy([verified_pass() for _ in range(5)], "L0")["recommended_level"], "L3")
        self.assertEqual(earned.evaluate_autonomy([verified_pass() for _ in range(8)], "L0")["recommended_level"], "L3")
        self.assertEqual(earned.evaluate_autonomy([untrusted_pass()], "L0")["verified_pass_count"], 0)

    # TEST 15: existing triage / risk behavior unchanged
    def test_triage_risk_unchanged(self):
        self.assertEqual(triage.triage(fast_task())["recommended_risk_tier"], "FAST")
        self.assertFalse(triage.triage(fast_task())["human_approval_required"])
        self.assertEqual(triage.triage(deep_change_task())["recommended_risk_tier"], "DEEP-CHANGE")
        self.assertTrue(triage.triage(deep_change_task())["human_approval_required"])
        self.assertEqual(triage.triage(approval_task())["recommended_risk_tier"], "FAST")
        self.assertTrue(triage.triage(approval_task())["human_approval_required"])

    # TEST 16: existing package validation unchanged
    def test_package_validation_unchanged(self):
        errors = vp.validate(ROOT)
        self.assertEqual(errors, [], f"package validation regressed: {errors}")


# Additional gate coverage (not required but exercised for completeness).
class DispatchGateCoverageTests(unittest.TestCase):
    def test_secrets_restricted_blocks(self):
        r = dispatch.dispatch_with_autonomy(
            fast_task(), history=[verified_pass() for _ in range(5)], current_level="L4", secrets_restricted=True
        )
        self.assertEqual(r["allowed_action"], "OBSERVE")
        self.assertFalse(r["execution_allowed"])
        self.assertIn("secrets_restriction", r["blocking_reasons"])

    def test_production_restricted_blocks(self):
        r = dispatch.dispatch_with_autonomy(
            fast_task(), history=[verified_pass() for _ in range(5)], current_level="L4", production_restricted=True
        )
        self.assertEqual(r["allowed_action"], "OBSERVE")
        self.assertIn("production_restriction", r["blocking_reasons"])

    def test_stop_condition_blocks(self):
        r = dispatch.dispatch_with_autonomy(
            fast_task(), history=[verified_pass() for _ in range(5)], current_level="L4", stop_condition=True
        )
        self.assertEqual(r["allowed_action"], "OBSERVE")
        self.assertFalse(r["execution_allowed"])
        self.assertIn("stop_condition", r["blocking_reasons"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
