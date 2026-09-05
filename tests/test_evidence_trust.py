"""EXP-002 Iteration 3 -> canonical MPE Evidence Trust Gate integration tests.

Proves the rule integrated into ``scripts/validate_package.py``:
  self-reported / unknown evidence PASS -> NOT PASS (fail-closed)
  trusted tool/platform evidence          -> may PASS when checks genuinely pass
  honest non-execution                  -> not verified-execution PASS
  existing valid trusted workflow        -> unchanged
  package validation still passes         -> no regression
"""
from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PKG_PATH = ROOT / "scripts" / "validate_package.py"

_spec = importlib.util.spec_from_file_location("validate_package", PKG_PATH)
validate_package = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(validate_package)

REQUIRED = list(validate_package.REQUIRED_EXECUTION_CHECKS)
TRUSTED = {"git_status", "secrets_scan", "compileall", "test_runner", "terminal_command", "ci_result"}


def self_reported() -> list[dict]:
    return [
        {"gate_id": "clean_diff_scope", "result": "PASS", "evidence_ref": "self_reported"},
        {"gate_id": "secrets_scan", "result": "PASS", "evidence_ref": "self_reported"},
        {"gate_id": "build", "result": "PASS", "evidence_ref": "self_reported"},
    ]


def unknown_source() -> list[dict]:
    return [{"gate_id": "build", "result": "PASS", "evidence_ref": "model_said_so"}]


def trusted_tool() -> list[dict]:
    return [
        {"gate_id": "clean_diff_scope", "result": "PASS", "evidence_ref": "git_status"},
        {"gate_id": "secrets_scan", "result": "PASS", "evidence_ref": "secrets_scan"},
        {"gate_id": "build", "result": "PASS", "evidence_ref": "compileall"},
    ]


def trusted_git_test_ci() -> list[dict]:
    return [
        {"gate_id": "clean_diff_scope", "result": "PASS", "evidence_ref": "git_diff"},
        {"gate_id": "secrets_scan", "result": "PASS", "evidence_ref": "ci_result"},
        {"gate_id": "build", "result": "PASS", "evidence_ref": "test_runner"},
    ]


def honest_no_execution() -> list[dict]:
    return []  # model understood the task but produced no gate results


class EvidenceTrustTests(unittest.TestCase):
    # 1. self-reported PASS -> NOT PASS
    def test_self_reported_not_pass(self):
        self.assertEqual(validate_package.derive_execution_outcome(self_reported()), "REWORK")
        self.assertTrue(validate_package.validate_gate_results(self_reported()))

    # 2. unknown evidence source -> NOT PASS (fail-closed)
    def test_unknown_source_not_pass(self):
        self.assertEqual(validate_package.classify_evidence_ref("model_said_so"), "UNKNOWN")
        self.assertEqual(validate_package.derive_execution_outcome(unknown_source()), "REWORK")
        self.assertTrue(validate_package.validate_gate_results(unknown_source()))

    # 3. trusted terminal/tool evidence -> PASS when all checks genuinely pass
    def test_trusted_tool_pass(self):
        self.assertEqual(validate_package.derive_execution_outcome(trusted_tool()), "PASS")
        self.assertEqual(validate_package.validate_gate_results(trusted_tool()), [])

    # 4. trusted git/test/CI equivalent -> PASS when valid
    def test_trusted_git_test_ci_pass(self):
        for g in trusted_git_test_ci():
            self.assertEqual(validate_package.classify_evidence_ref(g["evidence_ref"]), "TRUSTED")
        self.assertEqual(validate_package.derive_execution_outcome(trusted_git_test_ci()), "PASS")

    # 5. honest non-execution -> NOT verified-execution PASS
    def test_honest_non_execution_not_pass(self):
        self.assertEqual(validate_package.derive_execution_outcome(honest_no_execution()), "HUMAN_REQUIRED")
        self.assertNotEqual(validate_package.derive_execution_outcome(honest_no_execution()), "PASS")

    # 6. existing valid trusted workflow unchanged
    def test_existing_trusted_workflow_unchanged(self):
        self.assertEqual(validate_package.validate_gate_results(trusted_tool()), [])
        self.assertEqual(validate_package.derive_execution_outcome(trusted_tool()), "PASS")

    # 7. canonical package validation still passes (no regression / scope/approval/deep-change unchanged)
    def test_package_validation_unchanged(self):
        errors = validate_package.validate(ROOT)
        self.assertEqual(errors, [], f"package validation regressed: {errors}")


if __name__ == "__main__":
    unittest.main(verbosity=2)
