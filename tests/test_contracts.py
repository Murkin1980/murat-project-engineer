import importlib.util
import json
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

    def test_stage2_experiment_records_have_canonical_required_fields(self):
        schema = json.loads((ROOT / "contracts" / "EXPERIMENT_RECORD.schema.json").read_text(encoding="utf-8"))
        required = set(schema["required"])
        for run in range(6, 13):
            path = ROOT / "evidence" / "stage2" / f"RUN-{run:02d}_EXPERIMENT_RECORD.json"
            with self.subTest(run=run):
                self.assertTrue(path.exists(), f"missing canonical record: {path}")
                record = json.loads(path.read_text(encoding="utf-8"))
                self.assertEqual(required, set(record), f"schema field mismatch: {path}")
                self.assertEqual(f"RUN-{run:02d}", record["run_id"])

    def test_triage_contracts_match_fixture_and_engine_output(self):
        input_schema = json.loads((ROOT / "contracts" / "TRIAGE_INPUT.schema.json").read_text(encoding="utf-8"))
        output_schema = json.loads((ROOT / "contracts" / "TRIAGE_OUTPUT.schema.json").read_text(encoding="utf-8"))
        dataset = json.loads((ROOT / "datasets" / "exp-12-backtest.json").read_text(encoding="utf-8"))
        triage_spec = importlib.util.spec_from_file_location("triage_engine", ROOT / "scripts" / "triage_engine.py")
        triage_module = importlib.util.module_from_spec(triage_spec)
        assert triage_spec.loader
        triage_spec.loader.exec_module(triage_module)
        self.assertGreaterEqual(len(dataset["cases"]), 20)
        for case in dataset["cases"]:
            self.assertEqual(set(input_schema["required"]), set(case["input"]))
            output = triage_module.triage(case["input"])
            self.assertEqual(set(output_schema["required"]), set(output))

    def test_prospective_contract_field_parity(self):
        registration_schema = json.loads((ROOT / "contracts" / "PROSPECTIVE_CASE.schema.json").read_text(encoding="utf-8"))
        execution_schema = json.loads((ROOT / "contracts" / "PROSPECTIVE_EXECUTION.schema.json").read_text(encoding="utf-8"))
        evaluation_schema = json.loads((ROOT / "contracts" / "PROSPECTIVE_EVALUATION.schema.json").read_text(encoding="utf-8"))
        for case in ("P-001", "P-002"):
            registration = json.loads((ROOT / "evidence" / "exp-12" / "prospective" / f"{case}_PRE_REGISTRATION.json").read_text(encoding="utf-8"))
            execution = json.loads((ROOT / "evidence" / "exp-12" / "prospective" / f"{case}_EXECUTION.json").read_text(encoding="utf-8"))
            evaluation = json.loads((ROOT / "evidence" / "exp-12" / "prospective" / f"{case}_EVALUATION.json").read_text(encoding="utf-8"))
            self.assertEqual(set(registration_schema["required"]), set(registration))
            self.assertEqual(set(execution_schema["required"]), set(execution))
            self.assertEqual(set(evaluation_schema["required"]), set(evaluation))


if __name__ == "__main__":
    unittest.main()
