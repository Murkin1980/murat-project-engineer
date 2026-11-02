import importlib.util
import os
import unittest
from unittest.mock import patch
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("race_guard", ROOT / "scripts" / "check_experiment_registration.py")
guard = importlib.util.module_from_spec(spec)
spec.loader.exec_module(guard)


def entry(identifier, name, why="bounded hypothesis", status="PLANNED"):
    return {
        "experiment_id": identifier, "name": name, "owning_project": "MPE", "status": status,
        "why": why, "date_added": "2026-11-02", "next_action": "review",
        "result_summary": "planned", "repo": "Murkin1980/murat-project-engineer",
        "experiment_path": "docs/example.md", "evidence_links": [], "pr_or_issue_links": [],
        "updated_at": "2026-11-02",
    }


class RegistrationRaceGuardTests(unittest.TestCase):
    def test_duplicate_id_or_title_is_rejected(self):
        with self.assertRaises(SystemExit):
            guard.records({"experiments": [entry("EXP-47", "One"), entry("EXP-47", "Two")]}, "test")
        with self.assertRaises(SystemExit):
            guard.records({"experiments": [entry("EXP-47", "One"), entry("EXP-48", " one ")]}, "test")

    def test_exp_34_and_identical_existing_experiment_are_rejected(self):
        canonical = [entry("EXP-46", "Existing", "same hypothesis")]
        with self.assertRaises(SystemExit):
            guard.validate_new_identities({"EXP-34": entry("EXP-34", "New")}, canonical)
        with self.assertRaises(SystemExit):
            guard.validate_new_identities({"EXP-47": entry("EXP-47", "Existing", "other")}, canonical)
        with self.assertRaises(SystemExit):
            guard.validate_new_identities({"EXP-47": entry("EXP-47", "New", "same hypothesis")}, canonical)

    def test_fifo_serializes_parallel_claims_and_allows_next_id_after_merge(self):
        canonical = [entry("EXP-46", "Existing")]
        with self.assertRaises(SystemExit):
            guard.assert_fifo({"EXP-48": entry("EXP-48", "Later")}, canonical, [{"number": 200, "created_at": "2026-11-02T00:00:00Z"}])
        guard.assert_fifo({"EXP-47": entry("EXP-47", "First")}, canonical, [])
        guard.assert_fifo({"EXP-48": entry("EXP-48", "Second")}, canonical + [entry("EXP-47", "First")], [])

    def test_status_change_adds_no_registration_claim(self):
        canonical = [entry("EXP-46", "Existing", status="PLANNED")]
        proposal = [entry("EXP-46", "Existing", status="PASS")]
        self.assertEqual({}, guard.added_identity(proposal, canonical))

    def test_non_numeric_new_id_and_missing_contract_fail_closed(self):
        with self.assertRaises(SystemExit):
            guard.validate_new_identities({"EXP-NAMED": entry("EXP-NAMED", "New")}, [])
        with self.assertRaises(SystemExit):
            guard.records({"experiments": [{"experiment_id": "EXP-47"}]}, "test")

    def test_missing_github_evidence_and_changed_main_fail_closed(self):
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaises(SystemExit):
                guard.api("/repos/example/example")
        with self.assertRaises(SystemExit):
            guard.assert_current_main("129", "old-main", "new-main")


if __name__ == "__main__":
    unittest.main()
