import hashlib
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
        for run in range(6, 14):
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
        for case in ("P-001", "P-002", "P-003", "P-004"):
            registration = json.loads((ROOT / "evidence" / "exp-12" / "prospective" / f"{case}_PRE_REGISTRATION.json").read_text(encoding="utf-8"))
            execution = json.loads((ROOT / "evidence" / "exp-12" / "prospective" / f"{case}_EXECUTION.json").read_text(encoding="utf-8"))
            evaluation = json.loads((ROOT / "evidence" / "exp-12" / "prospective" / f"{case}_EVALUATION.json").read_text(encoding="utf-8"))
            self.assertEqual(set(registration_schema["required"]), set(registration))
            self.assertEqual(set(execution_schema["required"]), set(execution))
            self.assertEqual(set(evaluation_schema["required"]), set(evaluation))

    def test_exp002_frozen_ir_matches_schema(self):
        # GAP-1: executable binding between the frozen EXP-002 IR and its
        # schema. Read-only regression test: fails if the frozen bytes,
        # protocol/version consts, or schema parity drift.
        ir_path = ROOT / "experiments" / "exp-002-machine-protocol" / "MPE_IR_FROZEN.json"
        schema_path = ROOT / "experiments" / "exp-002-machine-protocol" / "mpe-ir.schema.json"
        self.assertTrue(ir_path.exists(), f"missing frozen IR: {ir_path}")
        self.assertTrue(schema_path.exists(), f"missing IR schema: {schema_path}")
        raw = ir_path.read_bytes()
        self.assertEqual(
            "cdafe73309960c555d8da1c84efbfc7b4c1e6ca22d3eeafeca5a226ba43fdbfd",
            hashlib.sha256(raw).hexdigest(),
            "frozen IR bytes drifted (SHA-256 mismatch)",
        )
        self.assertEqual(1148, len(raw), "frozen IR byte size drifted")
        record = json.loads(raw.decode("utf-8"))
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        self.assert_frozen_ir_conformance(record, schema)

    def assert_frozen_ir_conformance(self, record, schema):
        # Top-level contract parity: required keys present, nothing unexpected.
        self.assertEqual(set(schema["required"]), set(record), "frozen IR top-level parity mismatch")
        # Protocol/version self-identification must equal the schema consts.
        self.assertEqual(schema["properties"]["protocol"]["const"], record["protocol"])
        self.assertEqual(schema["properties"]["version"]["const"], record["version"])
        # Every closed nested object: required keys present, unexpected rejected.
        # (No subTest wrapper here: failures must raise so negative-proof
        # assertRaises blocks observe them; the field name is in the message.)
        for key, subschema in schema["properties"].items():
            if not isinstance(subschema, dict) or subschema.get("type") != "object":
                continue
            self.assertFalse(
                subschema.get("additionalProperties", True),
                f"schema object {key!r} must stay closed",
            )
            self.assertEqual(
                set(subschema.get("required", [])),
                set(record[key]),
                f"frozen IR nested parity mismatch: {key}",
            )

    def test_exp002_frozen_ir_conformance_rejects_drift(self):
        # Negative proof (in-memory mutations only; committed files untouched):
        # each drift shape must fail the conformance check.
        schema = json.loads(
            (ROOT / "experiments" / "exp-002-machine-protocol" / "mpe-ir.schema.json").read_text(encoding="utf-8")
        )
        record = json.loads(
            (ROOT / "experiments" / "exp-002-machine-protocol" / "MPE_IR_FROZEN.json").read_text(encoding="utf-8")
        )

        def mutated(**overrides):
            clone = json.loads(json.dumps(record))
            clone.update(overrides)
            return clone

        with self.subTest(drift="wrong protocol"):
            with self.assertRaises(AssertionError):
                self.assert_frozen_ir_conformance(mutated(protocol="other-ir"), schema)
        with self.subTest(drift="wrong version"):
            with self.assertRaises(AssertionError):
                self.assert_frozen_ir_conformance(mutated(version="9.9"), schema)
        with self.subTest(drift="extra top-level field"):
            with self.assertRaises(AssertionError):
                self.assert_frozen_ir_conformance(mutated(unknown_field="x"), schema)
        with self.subTest(drift="missing required field"):
            clone = json.loads(json.dumps(record))
            del clone["objective"]
            with self.assertRaises(AssertionError):
                self.assert_frozen_ir_conformance(clone, schema)
        with self.subTest(drift="extra nested field"):
            clone = json.loads(json.dumps(record))
            clone["task"]["unexpected"] = "x"
            with self.assertRaises(AssertionError):
                self.assert_frozen_ir_conformance(clone, schema)


if __name__ == "__main__":
    unittest.main()
