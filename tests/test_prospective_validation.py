import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from scripts.prospective_validation import evaluate, validate_registration
from scripts.triage_engine import ContractError


ROOT = Path(__file__).resolve().parents[1]
REGISTRATION_PATH = ROOT / "evidence" / "exp-12" / "prospective" / "P-001_PRE_REGISTRATION.json"


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
        result = evaluate(self.registration(), {"risk_tier": "VERIFIED", "human_approval_required": False}, "evidence/p001.json", raw)
        self.assertEqual(64, len(result["registration_sha256"]))
        self.assertTrue(result["human_engine_agreement"])
        self.assertTrue(result["engine_observed_agreement"])
        self.assertTrue(result["human_observed_agreement"])

    def test_cli_direct_execution(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "evaluation.json"
            completed = subprocess.run([
                sys.executable, str(ROOT / "scripts" / "prospective_validation.py"), str(REGISTRATION_PATH),
                "--observed-risk-tier", "VERIFIED", "--observed-human-approval", "false", "--output", str(output)
            ], cwd=ROOT, capture_output=True, text=True)
            self.assertEqual(0, completed.returncode, completed.stderr)
            self.assertEqual("EVALUATED", json.loads(output.read_text(encoding="utf-8"))["state"])


if __name__ == "__main__":
    unittest.main()
