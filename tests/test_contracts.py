import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("validate_package", ROOT / "scripts" / "validate_package.py")
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
SPEC.loader.exec_module(MODULE)


class PackageContractTests(unittest.TestCase):
    def test_package_contracts(self):
        self.assertEqual([], MODULE.validate(ROOT))

    def test_reviewer_is_independent(self):
        text = (ROOT / "experts" / "reviewer.md").read_text(encoding="utf-8")
        self.assertIn("must not edit the candidate", text)

    def test_deep_change_stops(self):
        text = (ROOT / "playbooks" / "deep-change.md").read_text(encoding="utf-8")
        self.assertIn("DEEP_CHANGE_REQUIRES_USER_APPROVAL", text)
        self.assertIn("HUMAN_REQUIRED", text)

    def test_gate_detection_and_human_approval_are_separate(self):
        text = (ROOT / "gates" / "registry.yaml").read_text(encoding="utf-8")
        self.assertIn("gate_id: deep_change_check\n    type: deterministic", text)
        self.assertIn("separate explicit human approval", text)

    def test_explicit_routes_and_experiment_template(self):
        routes = (ROOT / "skills" / "murat-project-engineer" / "references" / "route-profiles.md").read_text(encoding="utf-8")
        self.assertIn("opencode-go/deepseek-v4-flash", routes)
        self.assertIn("opencode-go/kimi-k2.7-code", routes)
        self.assertTrue((ROOT / "contracts" / "EXPERIMENT_RECORD.md").exists())


if __name__ == "__main__":
    unittest.main()
