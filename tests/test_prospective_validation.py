import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from scripts.prospective_validation import evaluate, execute, validate_execution, validate_registration
from scripts.triage_engine import ContractError


ROOT = Path(__file__).resolve().parents[1]
REGISTRATION_PATH = ROOT / "evidence" / "exp-12" / "prospective" / "P-001_PRE_REGISTRATION.json"
EXECUTION_PATH = ROOT / "evidence" / "exp-12" / "prospective" / "P-001_EXECUTION.json"


class ProspectiveValidationTests(unittest.TestCase):
    def registration(self):
        return json.loads(REGISTRATION_PATH.read_text(encoding="utf-8"))

    def test_p001_is_valid_immutable_registration(self):
        validate_registration(self.registration())

    def test_registration_rejects_embedded_engine_result(self):
        value = self.registration()
        value["engine_output"] = {}
        with self.assertRaises(ContractError):
            validate_registration(value)

    def test_evaluation_preserves_hash_and_three_way_agreement(self):
        raw = REGISTRATION_PATH.read_bytes()
        execution_raw = EXECUTION_PATH.read_bytes()
        execution_value = json.loads(execution_raw.decode("utf-8"))
        result = evaluate(self.registration(), execution_value, {"risk_tier": "VERIFIED", "human_approval_required": False}, "registration.json", raw, "execution.json", execution_raw)
        self.assertEqual(64, len(result["registration_sha256"]))
        self.assertEqual(64, len(result["execution_sha256"]))
        self.assertTrue(result["human_engine_agreement"])
        self.assertTrue(result["engine_observed_agreement"])
        self.assertTrue(result["human_observed_agreement"])

    def test_cli_direct_execution(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "evaluation.json"
            completed = subprocess.run([
                sys.executable, str(ROOT / "scripts" / "prospective_validation.py"), str(REGISTRATION_PATH), "--execution", str(EXECUTION_PATH),
                "--observed-risk-tier", "VERIFIED", "--observed-human-approval", "false", "--output", str(output)
            ], cwd=ROOT, capture_output=True, text=True)
            self.assertEqual(0, completed.returncode, completed.stderr)
            self.assertEqual("EVALUATED", json.loads(output.read_text(encoding="utf-8"))["state"])

    def test_execution_generator_and_hash_mismatch_rejection(self):
        raw = REGISTRATION_PATH.read_bytes()
        execution_value = execute(self.registration(), "registration.json", raw)
        validate_execution(execution_value, self.registration(), raw)
        execution_value["registration_sha256"] = "0" * 64
        with self.assertRaises(ContractError):
            validate_execution(execution_value, self.registration(), raw)

    def test_execution_cli_direct_execution(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "execution.json"
            completed = subprocess.run([sys.executable, str(ROOT / "scripts" / "prospective_execution.py"), str(REGISTRATION_PATH), "--output", str(output)], cwd=ROOT, capture_output=True, text=True)
            self.assertEqual(0, completed.returncode, completed.stderr)
            self.assertEqual("EXECUTED", json.loads(output.read_text(encoding="utf-8"))["state"])


if __name__ == "__main__":
    unittest.main()
