"""EXP-07 Strix retry guards: raw-evidence boundary, frozen baseline, status mapping.

These tests make the three PR #27 review findings enforceable instead of
aspirational:

1. raw penetration-test evidence must never be committed (sanitized artifacts only);
2. one target plus its baseline must be frozen before any Strix run;
3. execution outcomes map onto the existing canonical registry enum
   (``PASS``->``PASS``, ``WARNING``->``HOLD``, ``BLOCKED``->``HOLD``, ``FAIL``->``FAIL``)
   and the registry keeps the literal execution outcome in ``result_summary``.

Nothing here claims a scan happened: a ``NOT_RUN`` scan must keep every finding
count at zero and must not be represented as a value judgement about Strix.
"""
from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PILOT_DOC = ROOT / "docs" / "security" / "STRIX_PILOT.md"
ARTIFACT = ROOT / "evidence" / "exp-07" / "STRIX_RETRY_2026-09-28.json"
EVIDENCE_DIR = ROOT / "evidence" / "exp-07"
REGISTRY = ROOT / "experiments" / "EXPERIMENT_REGISTRY.json"
REGISTRY_SCHEMA = ROOT / "contracts" / "EXPERIMENT_REGISTRY.schema.json"
GITIGNORE = ROOT / ".gitignore"

FROZEN_TARGET_SHA = "2d6d60b240f8f4e2546cf451433c8f1ff0aad65a"
OUTCOME_TO_REGISTRY_STATUS = {"PASS": "PASS", "WARNING": "HOLD", "BLOCKED": "HOLD", "FAIL": "FAIL"}
EXECUTION_OUTCOMES = set(OUTCOME_TO_REGISTRY_STATUS)

REQUIRED_ARTIFACT_KEYS = {
    "artifact_id",
    "artifact_kind",
    "experiment_id",
    "generated_at",
    "target",
    "frozen_scope",
    "baseline",
    "strix",
    "execution_environment",
    "scan",
    "findings",
    "novelty_comparison",
    "actionable_findings_summary",
    "sanitization_statement",
    "execution_outcome",
    "registry_status",
    "recommendation",
    "next_action",
}


def artifact() -> dict:
    return json.loads(ARTIFACT.read_text(encoding="utf-8"))


def registry_exp07() -> dict:
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    matches = [e for e in registry["experiments"] if e["experiment_id"] == "EXP-07"]
    assert len(matches) == 1, "exactly one EXP-07 registry entry is expected"
    return matches[0]


class RawEvidenceBoundaryTests(unittest.TestCase):
    def test_pilot_doc_forbids_committing_raw_pentest_evidence(self):
        text = PILOT_DOC.read_text(encoding="utf-8")
        self.assertIn("RAW_STRIX_OUTPUT_NEVER_COMMITTED", text)
        for prohibited in (
            "raw Strix output",
            "exploit payloads",
            "exploitable endpoints",
            "source-code excerpts",
            "secrets, tokens, credentials, connection strings, configuration fragments",
            "sensitive vulnerability details",
        ):
            with self.subTest(prohibited=prohibited):
                self.assertIn(prohibited, text)
        self.assertIn("access-controlled temporary/local storage", text)

    def test_pilot_doc_lists_the_only_committable_sanitized_fields(self):
        text = PILOT_DOC.read_text(encoding="utf-8")
        for allowed in (
            "sanitized summary",
            "vulnerability class",
            "severity",
            "reproduction status",
            "remediation state",
            "already detected by existing tests",
            "sha256",
            "sanitization statement",
        ):
            with self.subTest(allowed=allowed):
                self.assertIn(allowed, text)

    def test_scope_no_longer_stores_the_raw_report_as_evidence(self):
        text = PILOT_DOC.read_text(encoding="utf-8")
        self.assertNotIn("Store raw report", text)
        self.assertIn("raw Strix output never enters Git", text)

    def test_gitignore_blocks_raw_capture_paths(self):
        ignore = GITIGNORE.read_text(encoding="utf-8")
        for pattern in ("strix_runs/", ".strix/", "raw-pentest/", "*.har", "*.pcap"):
            with self.subTest(pattern=pattern):
                self.assertIn(pattern, ignore)

    def test_no_raw_pentest_artifact_is_tracked(self):
        tracked = [
            path
            for path in ROOT.rglob("*")
            if path.is_file() and ".git" not in path.parts
        ]
        forbidden_suffixes = (".har", ".pcap")
        forbidden_dirs = {"strix_runs", "raw-pentest", ".strix"}
        for path in tracked:
            relative = path.relative_to(ROOT)
            with self.subTest(path=str(relative)):
                self.assertFalse(relative.as_posix().endswith(forbidden_suffixes))
                self.assertFalse(forbidden_dirs & set(relative.parts))

    def test_evidence_dir_holds_only_sanitized_artifacts(self):
        allowed = re.compile(r"^(README\.md|STRIX_RETRY_[0-9-]+\.json|STRIX_RUN_[A-Za-z0-9._-]+\.json)$")
        for path in sorted(EVIDENCE_DIR.iterdir()):
            with self.subTest(path=path.name):
                self.assertTrue(allowed.match(path.name), f"unsanctioned EXP-07 evidence file: {path.name}")

    def test_artifact_states_sanitization_and_holds_no_raw_output(self):
        data = artifact()
        statement = data["sanitization_statement"].lower()
        self.assertIn("sanitized", statement)
        self.assertIn("no raw strix output", statement)
        self.assertIn("exploit payload", statement)
        self.assertIsNone(data["scan"]["raw_output_location"])
        self.assertFalse(data["scan"]["raw_output_exists"])
        for check in data["baseline"]["checks"]:
            location = str(check.get("raw_log_location") or "")
            with self.subTest(check=check["check_id"]):
                # Raw logs stay in access-controlled local storage, never in the repo.
                self.assertFalse(location.startswith("/"))
                self.assertNotIn("github.com", location)
                self.assertFalse(location and (ROOT / location).exists())


class FrozenTargetAndBaselineTests(unittest.TestCase):
    def test_freeze_is_a_hard_gate_before_any_scan(self):
        text = PILOT_DOC.read_text(encoding="utf-8")
        self.assertIn("BASELINE_FREEZE_REQUIRED_BEFORE_SCAN", text)
        self.assertIn("STRIX_RUN_BEFORE_BASELINE_FREEZE = FORBIDDEN", text)
        self.assertIn("STRIX_WRITABLE_MOUNT_FORBIDDEN", text)
        for required in (
            "- repository;",
            "- branch;",
            "- exact commit SHA;",
            "- scan scope",
            "- excluded paths;",
            "- current test result",
            "- current build/typecheck result",
            "- existing static/security checks",
            "- current known security issues;",
            "- ordinary code-review baseline",
        ):
            with self.subTest(required=required):
                self.assertIn(required, text)
        self.assertIn("If no suitable bounded target exists, return `BLOCKED`", text)

    def test_target_and_baseline_are_frozen_at_one_sha(self):
        data = artifact()
        self.assertEqual(FROZEN_TARGET_SHA, data["target"]["commit_sha"])
        self.assertEqual("Murkin1980/mebeldocs-ai", data["target"]["repository"])
        self.assertTrue(data["frozen_scope"]["frozen_before_scan"])
        self.assertTrue(data["frozen_scope"]["one_target_only"])
        self.assertTrue(data["frozen_scope"]["one_bounded_scan_only"])
        self.assertFalse(data["frozen_scope"]["scope_expansion_allowed"])
        self.assertFalse(data["frozen_scope"]["production_destructive_testing_allowed"])
        self.assertFalse(data["frozen_scope"]["writable_working_tree_mount_allowed"])
        self.assertFalse(data["frozen_scope"]["autofix_allowed"])
        self.assertGreater(len(data["frozen_scope"]["scan_scope"]), 0)
        self.assertGreater(len(data["frozen_scope"]["excluded_paths"]), 0)
        self.assertIn(FROZEN_TARGET_SHA, PILOT_DOC.read_text(encoding="utf-8"))

    def test_baseline_records_executed_checks_and_review_comparison(self):
        baseline = artifact()["baseline"]
        self.assertEqual("PASS", baseline["status"])
        self.assertEqual(FROZEN_TARGET_SHA, baseline["frozen_against_commit_sha"])
        checks = {check["check_id"]: check for check in baseline["checks"]}
        for check_id in ("install", "unit_tests", "typecheck", "build"):
            with self.subTest(check=check_id):
                self.assertIn(check_id, checks)
                self.assertEqual("PASS", checks[check_id]["result"])
        self.assertIn("202 pass", checks["unit_tests"]["detail"])
        self.assertTrue(baseline["existing_static_security_checks"])
        self.assertGreater(len(baseline["known_security_issues"]), 0)
        self.assertGreater(len(baseline["ordinary_code_review_baseline"]["reviewed_paths"]), 0)
        self.assertGreater(len(baseline["ordinary_code_review_baseline"]["observations"]), 0)
        self.assertFalse(baseline["superseded_baseline"]["reuse_allowed"])

    def test_blocked_scan_is_never_simulated(self):
        data = artifact()
        scan = data["scan"]
        findings = data["findings"]
        if not scan["executed"]:
            self.assertEqual("NOT_RUN", scan["run_status"])
            self.assertFalse(scan["simulation_used"])
            self.assertFalse(scan["synthesized_results"])
            self.assertIsNone(scan["exit_code"])
            self.assertIsNone(scan["observed_cost_usd"])
            self.assertGreater(len(scan["blocking_prerequisites"]), 0)
            for prerequisite in scan["blocking_prerequisites"]:
                self.assertTrue(prerequisite["prerequisite"])
                self.assertTrue(prerequisite["observation"])
            for key in ("total", "confirmed", "false_positive", "inconclusive", "novel", "actionable"):
                with self.subTest(metric=key):
                    self.assertEqual(0, findings[key])
            self.assertEqual([], findings["items"])
            self.assertFalse(data["novelty_comparison"]["performed"])


class CanonicalStatusMappingTests(unittest.TestCase):
    def test_doc_maps_outcomes_onto_the_existing_enum_only(self):
        text = PILOT_DOC.read_text(encoding="utf-8")
        self.assertIn("EXECUTION_OUTCOME_IS_NOT_REGISTRY_STATUS", text)
        self.assertIn("No new registry status may be invented for EXP-07", text)
        for outcome, status in OUTCOME_TO_REGISTRY_STATUS.items():
            with self.subTest(outcome=outcome):
                self.assertIn(f"| `{outcome}` | `{status}` |", text)
        allowed = json.loads(REGISTRY_SCHEMA.read_text(encoding="utf-8"))
        allowed_statuses = allowed["properties"]["experiments"]["items"]["properties"]["status"]["enum"]
        self.assertEqual(
            {"IDEA", "PLANNED", "READY_TO_TEST", "RUNNING", "PASS", "FAIL", "HOLD", "ADOPTED"},
            set(allowed_statuses),
        )
        for status in OUTCOME_TO_REGISTRY_STATUS.values():
            self.assertIn(status, allowed_statuses)

    def test_artifact_outcome_and_registry_status_agree(self):
        data = artifact()
        self.assertIn(data["execution_outcome"], EXECUTION_OUTCOMES)
        self.assertEqual(
            OUTCOME_TO_REGISTRY_STATUS[data["execution_outcome"]],
            data["registry_status"],
        )
        self.assertEqual(OUTCOME_TO_REGISTRY_STATUS, data["status_mapping_applied"])

    def test_registry_entry_carries_the_mapped_status_and_literal_outcome(self):
        data = artifact()
        entry = registry_exp07()
        self.assertEqual(data["registry_status"], entry["status"])
        self.assertIn(f"execution_outcome: {data['execution_outcome']}", entry["result_summary"])
        self.assertIn("NOT_RUN", entry["result_summary"])
        self.assertIn(FROZEN_TARGET_SHA, entry["next_action"])
        self.assertIn(
            "https://github.com/Murkin1980/murat-project-engineer/blob/main/evidence/exp-07/STRIX_RETRY_2026-09-28.json",
            entry["evidence_links"],
        )
        self.assertIn(
            "https://github.com/Murkin1980/murat-project-engineer/pull/27",
            entry["pr_or_issue_links"],
        )

    def test_artifact_has_the_required_evidence_fields(self):
        data = artifact()
        missing = REQUIRED_ARTIFACT_KEYS - set(data)
        self.assertEqual(set(), missing)
        self.assertEqual("EXP-07", data["experiment_id"])
        self.assertEqual("sanitized_experiment_evidence", data["artifact_kind"])
        self.assertTrue(data["strix"]["source_repository"])
        self.assertTrue(data["strix"]["version_available"])
        self.assertIsNone(data["strix"]["version_used"])
        self.assertTrue(data["execution_environment"]["os"])
        self.assertFalse(data["execution_environment"]["docker_available"])
        self.assertFalse(data["execution_environment"]["llm_credentials_available"])
        self.assertTrue(data["recommendation"])
        self.assertTrue(data["next_action"])
        self.assertGreater(len(data["boundaries_respected"]), 0)


if __name__ == "__main__":
    unittest.main()
