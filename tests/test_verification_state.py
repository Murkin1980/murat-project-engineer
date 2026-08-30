import json
import subprocess
import tempfile
import unittest
from pathlib import Path

from scripts.verification_state import VerificationStateError, capture, check


class VerificationStateTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.git("init", "-b", "main")
        self.git("config", "user.email", "mpe-tests@example.invalid")
        self.git("config", "user.name", "MPE Tests")
        (self.root / "candidate.txt").write_text("first", encoding="utf-8")
        (self.root / "second.txt").write_text("initial", encoding="utf-8")
        self.git("add", ".")
        self.git("commit", "-m", "initial")

    def tearDown(self):
        self.temp.cleanup()

    def git(self, *args):
        return subprocess.run(
            ["git", "-C", str(self.root), *args],
            check=True,
            capture_output=True,
            text=True,
        )

    def captured_change(self):
        (self.root / "candidate.txt").write_text("verified change", encoding="utf-8")
        return capture(self.root)

    def test_unchanged_git_change_set_remains_verified(self):
        state = self.captured_change()
        self.assertEqual("VERIFIED", check(self.root, state)["state"])
        self.assertEqual("2.0", state["schema_version"])
        self.assertIn("fingerprint_sha256", state["git"])

    def test_changed_registered_file_becomes_unverified(self):
        state = self.captured_change()
        (self.root / "candidate.txt").write_text("second mutation", encoding="utf-8")
        result = check(self.root, state)
        self.assertEqual("UNVERIFIED", result["state"])
        self.assertIn("content changed", result["invalidation_reason"])

    def test_new_untracked_file_after_capture_becomes_unverified(self):
        state = self.captured_change()
        (self.root / "new.txt").write_text("new", encoding="utf-8")
        result = check(self.root, state)
        self.assertEqual("UNVERIFIED", result["state"])
        self.assertIn("changed-file list", result["invalidation_reason"])

    def test_second_unregistered_file_change_becomes_unverified(self):
        (self.root / "candidate.txt").write_text("verified change", encoding="utf-8")
        state = capture(self.root, ["candidate.txt"])
        (self.root / "second.txt").write_text("not declared manually", encoding="utf-8")
        result = check(self.root, state)
        self.assertEqual("UNVERIFIED", result["state"])

    def test_manual_file_scope_cannot_omit_git_change(self):
        (self.root / "candidate.txt").write_text("changed", encoding="utf-8")
        (self.root / "second.txt").write_text("changed", encoding="utf-8")
        with self.assertRaisesRegex(VerificationStateError, "omits Git changes"):
            capture(self.root, ["candidate.txt"])

    def test_deleted_file_is_fingerprinted(self):
        (self.root / "candidate.txt").unlink()
        state = capture(self.root)
        self.assertIsNone(state["git"]["content"]["candidate.txt"])
        self.assertEqual("VERIFIED", check(self.root, state)["state"])

    def test_staged_to_unstaged_transition_becomes_unverified(self):
        (self.root / "candidate.txt").write_text("staged", encoding="utf-8")
        self.git("add", "candidate.txt")
        state = capture(self.root)
        (self.root / "candidate.txt").write_text("unstaged too", encoding="utf-8")
        result = check(self.root, state)
        self.assertEqual("UNVERIFIED", result["state"])

    def test_head_change_becomes_unverified(self):
        state = self.captured_change()
        self.git("add", "candidate.txt")
        self.git("commit", "-m", "move head")
        result = check(self.root, state)
        self.assertEqual("UNVERIFIED", result["state"])
        self.assertIn("HEAD changed", result["invalidation_reason"])

    def test_clean_worktree_captures_committed_diff_from_base(self):
        base_sha = self.git("rev-parse", "HEAD").stdout.strip()
        (self.root / "candidate.txt").write_text("committed change", encoding="utf-8")
        self.git("add", "candidate.txt")
        self.git("commit", "-m", "candidate change")
        state = capture(self.root, base_ref=base_sha)
        self.assertEqual("VERIFIED", check(self.root, state)["state"])
        self.assertIn(
            {"path": "candidate.txt", "status": "committed:M"},
            state["git"]["entries"],
        )
        self.assertNotEqual(
            "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
            state["git"]["committed_diff_sha256"],
        )

    def test_tampered_excluded_paths_cannot_hide_new_file(self):
        state = self.captured_change()
        state["excluded_paths"] = ["outside.txt"]
        (self.root / "outside.txt").write_text("hidden attempt", encoding="utf-8")
        result = check(self.root, state, allowed_excluded_paths=set())
        self.assertEqual("UNVERIFIED", result["state"])
        self.assertIn("stored exclusions differ", result["invalidation_reason"])
        self.assertIn("integrity digest mismatch", result["invalidation_reason"])

    def test_tampered_snapshot_fields_fail_integrity_check(self):
        state = self.captured_change()
        state["git"]["content"]["candidate.txt"] = "0" * 64
        result = check(self.root, state)
        self.assertEqual("UNVERIFIED", result["state"])
        self.assertIn("integrity digest mismatch", result["invalidation_reason"])

    def test_clean_scope_gate_rejects_outside_task_packet(self):
        state = self.captured_change()
        result = check(
            self.root,
            state,
            require_clean_scope=True,
            task_packet={"target_files_or_components": ["docs/"]},
        )
        self.assertEqual("UNVERIFIED", result["state"])
        self.assertIn("out-of-scope", result["invalidation_reason"])

    def test_clean_scope_gate_accepts_file_and_directory_patterns(self):
        state = self.captured_change()
        result = check(
            self.root,
            state,
            require_clean_scope=True,
            task_packet={"target_files_or_components": ["candidate.txt", "docs/"]},
        )
        self.assertEqual("VERIFIED", result["state"])

    def test_state_is_json_serializable(self):
        state = self.captured_change()
        self.assertEqual("VERIFIED", json.loads(json.dumps(state))["state"])

    def test_cli_final_diff_gate_is_executable(self):
        (self.root / "candidate.txt").write_text("verified change", encoding="utf-8")
        packet = self.root / "task-packet.json"
        packet.write_text(
            json.dumps({"target_files_or_components": ["candidate.txt", "task-packet.json"]}),
            encoding="utf-8",
        )
        state_path = self.root.parent / f"{self.root.name}-verification-state.json"
        script = Path(__file__).parents[1] / "scripts" / "verification_state.py"
        try:
            captured = subprocess.run(
                ["python", str(script), "capture", "--root", str(self.root), "--state", str(state_path)],
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(0, captured.returncode, captured.stderr)
            checked = subprocess.run(
                [
                    "python",
                    str(script),
                    "check",
                    "--root",
                    str(self.root),
                    "--state",
                    str(state_path),
                    "--require-clean-scope",
                    "--task-packet",
                    str(packet),
                ],
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(0, checked.returncode, checked.stderr)
            (self.root / "outside.txt").write_text("outside", encoding="utf-8")
            invalid = subprocess.run(
                [
                    "python",
                    str(script),
                    "check",
                    "--root",
                    str(self.root),
                    "--state",
                    str(state_path),
                    "--require-clean-scope",
                    "--task-packet",
                    str(packet),
                ],
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(3, invalid.returncode)
            self.assertIn("UNVERIFIED", invalid.stdout)
        finally:
            state_path.unlink(missing_ok=True)


if __name__ == "__main__":
    unittest.main()
