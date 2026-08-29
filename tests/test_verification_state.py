import json
import tempfile
import unittest
from pathlib import Path

from scripts.verification_state import VerificationStateError, capture, check


class VerificationStateTests(unittest.TestCase):
    def test_unchanged_file_remains_verified(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "candidate.txt").write_text("first", encoding="utf-8")
            state = capture(root, ["candidate.txt"])
            self.assertEqual("VERIFIED", check(root, state)["state"])

    def test_changed_file_becomes_unverified(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            candidate = root / "candidate.txt"
            candidate.write_text("first", encoding="utf-8")
            state = capture(root, ["candidate.txt"])
            candidate.write_text("second", encoding="utf-8")
            result = check(root, state)
            self.assertEqual("UNVERIFIED", result["state"])
            self.assertIn("candidate.txt", result["invalidation_reason"])

    def test_missing_or_outside_file_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            with self.assertRaises(VerificationStateError):
                capture(root, ["missing.txt"])
            outside = Path(tmp).parent / "outside.txt"
            outside.write_text("outside", encoding="utf-8")
            with self.assertRaises(VerificationStateError):
                capture(root, ["../outside.txt"])

    def test_state_is_json_serializable(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "candidate.txt").write_text("first", encoding="utf-8")
            self.assertEqual("VERIFIED", json.loads(json.dumps(capture(root, ["candidate.txt"])))["state"])
