import json
import tempfile
import unittest
from pathlib import Path

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
    def test_atomic_delivery_and_duplicate(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = deliver_atomic(Path(tmp), envelope())
            self.assertEqual(envelope(), json.loads(target.read_text(encoding="utf-8")))
            self.assertFalse(list(Path(tmp).glob("*.tmp")))
            self.assertFalse(list(Path(tmp).glob("*.lock")))
            with self.assertRaises(ContractError): deliver_atomic(Path(tmp), envelope())
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
