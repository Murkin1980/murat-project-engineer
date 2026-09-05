"""EXP Earned Autonomy — baseline evaluator tests.

Proves the minimal, deterministic evaluator in ``scripts/earned_autonomy.py``:
  - promotion depends ONLY on verified trusted outcomes
  - self-reported / unknown evidence cannot promote
  - REWORK / HUMAN_REQUIRED do not count
  - scope / deep-change / security violations block promotion and recommend downgrade
  - L4 is never auto-granted
  - existing Evidence Trust Gate, approval, and package validation are unchanged
"""
from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _load(name: str, rel: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / rel)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


earned = _load("earned_autonomy", "scripts/earned_autonomy.py")
validate_package = _load("validate_package", "scripts/validate_package.py")
exp13 = _load("exp13_checks", "scripts/exp13_checks.py")

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


def rework() -> dict:
    return {"outcome": "REWORK"}


def human_required() -> dict:
    return {"outcome": "HUMAN_REQUIRED"}


def scope_violation() -> dict:
    return {"outcome": "PASS", "scope_violation": True}


def deep_change_violation() -> dict:
    return {"outcome": "PASS", "deep_change_violation": True}


class EarnedAutonomyTests(unittest.TestCase):
    # TEST 1: 0 verified PASS -> L0 remains L0
    def test_zero_history_l0(self):
        r = earned.evaluate_autonomy([], current_level="L0")
        self.assertEqual(r["verified_pass_count"], 0)
        self.assertEqual(r["recommended_level"], "L0")
        self.assertFalse(r["promotion_eligible"])

    # TEST 2: 1 verified PASS -> eligible for L1
    def test_one_verified_l1(self):
        r = earned.evaluate_autonomy([verified_pass()], current_level="L0")
        self.assertEqual(r["verified_pass_count"], 1)
        self.assertEqual(r["recommended_level"], "L1")
        self.assertTrue(r["promotion_eligible"])

    # TEST 3: 3 verified PASS total -> eligible for L2
    def test_three_verified_l2(self):
        r = earned.evaluate_autonomy([verified_pass() for _ in range(3)], current_level="L0")
        self.assertEqual(r["verified_pass_count"], 3)
        self.assertEqual(r["recommended_level"], "L2")
        self.assertTrue(r["promotion_eligible"])

    # TEST 4: 5 verified PASS total -> eligible for L3
    def test_five_verified_l3(self):
        r = earned.evaluate_autonomy([verified_pass() for _ in range(5)], current_level="L0")
        self.assertEqual(r["verified_pass_count"], 5)
        self.assertEqual(r["recommended_level"], "L3")
        self.assertTrue(r["promotion_eligible"])

    # TEST 5: 5+ verified PASS -> NOT auto-promoted to L4
    def test_never_auto_l4(self):
        r = earned.evaluate_autonomy([verified_pass() for _ in range(8)], current_level="L0")
        self.assertEqual(r["verified_pass_count"], 8)
        self.assertEqual(r["recommended_level"], "L3")
        self.assertNotEqual(r["recommended_level"], "L4")

    # TEST 6: self-reported / untrusted PASS does not count
    def test_untrusted_pass_does_not_count(self):
        r = earned.evaluate_autonomy([untrusted_pass()], current_level="L0")
        self.assertEqual(r["verified_pass_count"], 0)
        self.assertEqual(r["recommended_level"], "L0")
        self.assertFalse(r["promotion_eligible"])

    # TEST 7: REWORK does not count
    def test_rework_does_not_count(self):
        r = earned.evaluate_autonomy([rework(), verified_pass()], current_level="L0")
        self.assertEqual(r["verified_pass_count"], 1)
        self.assertNotIn("rework", r["blocking_events"])

    # TEST 8: HUMAN_REQUIRED does not count
    def test_human_required_does_not_count(self):
        r = earned.evaluate_autonomy([human_required(), verified_pass()], current_level="L0")
        self.assertEqual(r["verified_pass_count"], 1)
        self.assertNotIn("human", r["blocking_events"])

    # TEST 9: scope violation -> promotion blocked / downgrade recommendation
    def test_scope_violation_blocks(self):
        r = earned.evaluate_autonomy([verified_pass(), scope_violation()], current_level="L2")
        self.assertIn("scope_violation", r["blocking_events"])
        self.assertEqual(r["recommended_level"], "L1")
        self.assertFalse(r["promotion_eligible"])

    # TEST 10: deep-change violation -> promotion blocked / downgrade recommendation
    def test_deep_change_violation_blocks(self):
        r = earned.evaluate_autonomy([verified_pass(), deep_change_violation()], current_level="L3")
        self.assertIn("deep_change_violation", r["blocking_events"])
        self.assertEqual(r["recommended_level"], "L2")
        self.assertFalse(r["promotion_eligible"])

    # TEST 11: trusted PASS plus one invalid event -> invalid event does not contribute
    def test_invalid_event_does_not_contribute(self):
        r = earned.evaluate_autonomy([verified_pass(), rework()], current_level="L0")
        self.assertEqual(r["verified_pass_count"], 1)
        self.assertEqual(r["recommended_level"], "L1")
        self.assertTrue(r["promotion_eligible"])

    # TEST 12: existing Evidence Trust Gate behavior unchanged
    def test_evidence_trust_gate_unchanged(self):
        self.assertEqual(validate_package.classify_evidence_ref("self_reported"), "UNTRUSTED")
        self.assertEqual(validate_package.classify_evidence_ref("git_status"), "TRUSTED")
        self.assertEqual(
            validate_package.derive_execution_outcome(untrusted_pass()["deterministic_gate_results"]),
            "REWORK",
        )

    # TEST 13: existing approval behavior unchanged
    def test_approval_behavior_unchanged(self):
        self.assertIn("HUMAN_REQUIRED", exp13.OUTCOMES)
        self.assertEqual(
            exp13.derive_outcome({"escalation": "HUMAN_REVIEW_REQUIRED"}, []),
            "HUMAN_REQUIRED",
        )

    # TEST 14: existing package validation unchanged
    def test_package_validation_unchanged(self):
        errors = validate_package.validate(ROOT)
        self.assertEqual(errors, [], f"package validation regressed: {errors}")


if __name__ == "__main__":
    unittest.main(verbosity=2)
