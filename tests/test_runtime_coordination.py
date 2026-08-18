import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from scripts.runtime_coordination import ContractError, append_event, deliver_atomic, find_worktree_collisions, read_events, summarize_events, validate_envelope, validate_event, validate_transition

STAMP = "2026-08-15T12:00:00+05:00"


def envelope(**changes):
    value = {"schema_version": "1.0", "message_id": "msg-1", "run_id": "RUN-11", "task_id": "task-1", "sender_role": "Researcher", "recipient_role": "Implementer", "handoff_ref": "handoffs/research.md", "created_at": STAMP, "status": "READY"}
    value.update(changes)
    return value


def event(event_id="evt-1", kind="spawn", actor="Researcher", status="READY", ref=None):
    return {"schema_version": "1.0", "event_id": event_id, "run_id": "RUN-11", "timestamp": STAMP, "type": kind, "actor": actor, "target": None, "task_id": "task-1", "ref": ref, "status": status}


def state(role, path, status="WORKING"):
    return {"run_id": "RUN-11", "role": role, "task_id": "task-1", "state": status, "worktree": {"worktree_path": path}}


class MailboxTests(unittest.TestCase):
    def test_valid_envelope(self): validate_envelope(envelope())
    def test_missing_sender_rejected(self):
        data = envelope(); del data["sender_role"]
        with self.assertRaises(ContractError): validate_envelope(data)
    def test_missing_recipient_rejected(self):
        data = envelope(); del data["recipient_role"]
        with self.assertRaises(ContractError): validate_envelope(data)
    def test_invalid_status_rejected(self):
        with self.assertRaises(ContractError): validate_envelope(envelope(status="UNKNOWN"))
    def test_invalid_timestamp_rejected(self):
        with self.assertRaises(ContractError): validate_envelope(envelope(created_at="yesterday"))
    def test_message_id_traversal_and_separators_rejected(self):
        for message_id in ("../escape", "..\\escape", "a/b", "a\\b", ".", "-leading", "x" * 129, "msg space"):
            with self.subTest(message_id=message_id):
                with self.assertRaises(ContractError): validate_envelope(envelope(message_id=message_id))
    def test_atomic_delivery_and_duplicate(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = deliver_atomic(Path(tmp), envelope())
            self.assertEqual(envelope(), json.loads(target.read_text(encoding="utf-8")))
            self.assertFalse(list(Path(tmp).glob("*.tmp")))
            self.assertFalse(list(Path(tmp).glob("*.lock")))
            with self.assertRaises(ContractError): deliver_atomic(Path(tmp), envelope())
    def test_cross_process_duplicate_delivery(self):
        with tempfile.TemporaryDirectory() as tmp:
            payload = json.dumps(envelope())
            code = (
                "import json,sys; from pathlib import Path; "
                "from scripts.runtime_coordination import ContractError,deliver_atomic; "
                "data=json.loads(sys.argv[2]); "
                "\ntry: deliver_atomic(Path(sys.argv[1]),data)\n"
                "except ContractError: raise SystemExit(2)\n"
            )
            args = [sys.executable, "-c", code, tmp, payload]
            first = subprocess.Popen(args, cwd=Path(__file__).resolve().parents[1])
            second = subprocess.Popen(args, cwd=Path(__file__).resolve().parents[1])
            codes = sorted([first.wait(), second.wait()])
            self.assertEqual([0, 2], codes)
            self.assertEqual(1, len(list(Path(tmp).glob("msg-1.json"))))
    def test_symlink_mailbox_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            real = root / "real"; real.mkdir()
            link = root / "linked"
            try:
                os.symlink(real, link, target_is_directory=True)
            except (OSError, NotImplementedError) as exc:
                self.skipTest(f"symlink creation unavailable: {exc}")
            with self.assertRaises(ContractError): deliver_atomic(link, envelope())
    def test_reparse_point_branch_rejected_without_os_symlink_privilege(self):
        with tempfile.TemporaryDirectory() as tmp:
            inbox = Path(tmp) / "inbox"
            with patch("scripts.runtime_coordination._is_reparse_point", side_effect=lambda path: path == inbox.absolute()):
                with self.assertRaises(ContractError): deliver_atomic(inbox, envelope())
    @unittest.skipUnless(os.name == "nt", "Windows junction test")
    def test_windows_junction_mailbox_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            real = root / "real"; real.mkdir()
            junction = root / "junction"
            created = subprocess.run(
                ["cmd.exe", "/c", "mklink", "/J", str(junction), str(real)],
                capture_output=True,
                text=True,
            )
            if created.returncode != 0:
                self.skipTest(f"junction creation unavailable: {created.stderr or created.stdout}")
            try:
                with self.assertRaises(ContractError): deliver_atomic(junction, envelope())
            finally:
                os.rmdir(junction)
    def test_partial_json_not_accepted(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "events.jsonl"; path.write_text('{"schema_version":', encoding="utf-8")
            with self.assertRaises(ContractError): read_events(path)


class EventTests(unittest.TestCase):
    def test_valid_core_events(self):
        for kind in ("spawn", "handoff", "gate", "terminal"): validate_event(event(kind=kind))
    def test_unknown_event_rejected(self):
        with self.assertRaises(ContractError): validate_event(event(kind="thought"))
        with self.assertRaises(ContractError): validate_event({**event(), "timestamp": "2026-08-15"})
    def test_append_order_preserved(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "events.jsonl"
            append_event(path, event("evt-1")); append_event(path, event("evt-2", "terminal", status="PASS"))
            self.assertEqual(["evt-1", "evt-2"], [item["event_id"] for item in read_events(path)])
    def test_event_log_enforces_single_writer(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "events.jsonl"
            append_event(path, event("evt-1"), writer_id="coordinator")
            with self.assertRaises(ContractError):
                append_event(path, event("evt-2"), writer_id="reviewer")
            append_event(path, event("evt-3"), writer_id="coordinator")
            self.assertEqual(["evt-1", "evt-3"], [item["event_id"] for item in read_events(path)])
    def test_cross_process_event_writer_claim(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = str(Path(tmp) / "events.jsonl")
            payload = json.dumps(event())
            code = (
                "import json,sys; from pathlib import Path; "
                "from scripts.runtime_coordination import ContractError,append_event; "
                "data=json.loads(sys.argv[2]); "
                "\ntry: append_event(Path(sys.argv[1]),data,writer_id=sys.argv[3])\n"
                "except ContractError: raise SystemExit(2)\n"
            )
            root = Path(__file__).resolve().parents[1]
            first = subprocess.Popen([sys.executable, "-c", code, path, payload, "writer-a"], cwd=root)
            second = subprocess.Popen([sys.executable, "-c", code, path, payload, "writer-b"], cwd=root)
            self.assertEqual([0, 2], sorted([first.wait(), second.wait()]))
            self.assertEqual(1, len(read_events(Path(path))))
    def test_symlink_event_log_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            real = root / "real.jsonl"; real.write_text("", encoding="utf-8")
            link = root / "events.jsonl"
            try:
                os.symlink(real, link)
            except (OSError, NotImplementedError) as exc:
                self.skipTest(f"symlink creation unavailable: {exc}")
            with self.assertRaises(ContractError): append_event(link, event())
    def test_summary_is_deterministic(self):
        items = [event("1", "spawn", "Reviewer"), event("2", "spawn", "Researcher"), event("3", "handoff", ref="h1"), event("4", "gate", status="PASS", ref="unit_tests"), event("5", "terminal", status="PASS")]
        self.assertEqual(summarize_events(items), summarize_events(items))
        self.assertEqual(["Researcher", "Reviewer"], summarize_events(items)["experts_invoked"])
        self.assertEqual("PASS", summarize_events(items)["outcome"])


class LifecycleTests(unittest.TestCase):
    def test_valid_transitions(self):
        for pair in (("CREATED", "READY"), ("READY", "WORKING"), ("WORKING", "REVIEWING"), ("REVIEWING", "DONE")): validate_transition(*pair)
    def test_invalid_state_rejected(self):
        with self.assertRaises(ContractError): validate_transition("UNKNOWN", "WORKING")
    def test_same_worktree_collision(self):
        self.assertEqual(1, len(find_worktree_collisions([state("Researcher", "C:/tmp/w"), state("Implementer", "C:/tmp/w")])))
    def test_different_worktrees_allowed(self):
        self.assertEqual([], find_worktree_collisions([state("Researcher", "C:/tmp/a"), state("Implementer", "C:/tmp/b")]))
    def test_terminal_cannot_return_to_working(self):
        with self.assertRaises(ContractError): validate_transition("DONE", "WORKING")
        validate_transition("DONE", "CREATED", new_invocation=True)


if __name__ == "__main__": unittest.main()
