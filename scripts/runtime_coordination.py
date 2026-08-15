"""Bounded runtime-evidence helpers. No daemon, scheduler, or state service."""
from __future__ import annotations

import json
import os
import re
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Iterable

MAILBOX_STATUSES = {"READY", "CLAIMED", "DELIVERED", "FAILED", "SUPERSEDED"}
EVENT_TYPES = {"spawn", "handoff", "gate", "terminal", "claim", "block", "resume"}
STATES = {"CREATED", "READY", "WORKING", "BLOCKED", "WAITING", "REVIEWING", "DONE", "FAILED", "CANCELLED"}
TERMINAL_STATES = {"DONE", "FAILED", "CANCELLED"}
TRANSITIONS = {
    "CREATED": {"READY"}, "READY": {"WORKING"},
    "WORKING": {"BLOCKED", "WAITING", "REVIEWING", "DONE", "FAILED", "CANCELLED"},
    "BLOCKED": {"WORKING", "CANCELLED", "FAILED"},
    "WAITING": {"WORKING", "CANCELLED"},
    "REVIEWING": {"DONE", "WORKING", "FAILED"},
    "DONE": set(), "FAILED": set(), "CANCELLED": set(),
}
ACTIVE_WRITER_STATES = {"READY", "WORKING", "BLOCKED", "WAITING", "REVIEWING"}
SAFE_MESSAGE_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_-]{0,127}$", re.ASCII)


class ContractError(ValueError):
    pass


def _require(data: dict, fields: set[str]) -> None:
    missing = fields - data.keys()
    if missing:
        raise ContractError(f"missing fields: {', '.join(sorted(missing))}")


def _require_datetime(value: object, field: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ContractError(f"invalid {field}")
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ContractError(f"invalid {field}") from exc
    if parsed.tzinfo is None:
        raise ContractError(f"invalid {field}: timezone required")


def _is_reparse_point(path: Path) -> bool:
    if path.is_symlink():
        return True
    is_junction = getattr(path, "is_junction", None)
    return bool(is_junction and is_junction())


def _require_plain_directory_path(path: Path) -> None:
    """Reject symlink/junction traversal before using a mailbox directory."""
    absolute = path.absolute()
    for candidate in (absolute, *absolute.parents):
        if candidate.exists() and _is_reparse_point(candidate):
            raise ContractError(f"mailbox path crosses a reparse point: {candidate}")


def _require_plain_file_path(path: Path) -> None:
    _require_plain_directory_path(path.parent)
    if path.exists() and _is_reparse_point(path):
        raise ContractError(f"file path is a reparse point: {path}")


def validate_envelope(data: dict) -> None:
    _require(data, {"schema_version", "message_id", "run_id", "task_id", "sender_role", "recipient_role", "handoff_ref", "created_at", "status"})
    if data["schema_version"] != "1.0" or data["status"] not in MAILBOX_STATUSES:
        raise ContractError("invalid mailbox version or status")
    if not isinstance(data["message_id"], str) or not SAFE_MESSAGE_ID.fullmatch(data["message_id"]):
        raise ContractError("invalid message_id: use 1-128 ASCII letters, digits, underscores, or hyphens")
    for field in ("message_id", "run_id", "task_id", "sender_role", "recipient_role", "handoff_ref"):
        if not isinstance(data[field], str) or not data[field].strip():
            raise ContractError(f"invalid {field}")
    _require_datetime(data["created_at"], "created_at")


def deliver_atomic(inbox: Path, envelope: dict) -> Path:
    """Validate, fsync, then atomically rename a new envelope into an inbox."""
    validate_envelope(envelope)
    _require_plain_directory_path(inbox)
    inbox.mkdir(parents=True, exist_ok=True)
    _require_plain_directory_path(inbox)
    target = inbox / f"{envelope['message_id']}.json"
    lock = inbox / f".{envelope['message_id']}.lock"
    try:
        lock_fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    except FileExistsError as exc:
        raise ContractError(f"duplicate or active message_id: {envelope['message_id']}") from exc
    os.close(lock_fd)
    fd = -1
    temp_name = ""
    try:
        if target.exists():
            raise ContractError(f"duplicate message_id: {envelope['message_id']}")
        fd, temp_name = tempfile.mkstemp(prefix=".mailbox-", suffix=".tmp", dir=inbox)
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as stream:
            fd = -1
            json.dump(envelope, stream, ensure_ascii=False, sort_keys=True)
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temp_name, target)
    except BaseException:
        if fd >= 0:
            os.close(fd)
        if temp_name:
            Path(temp_name).unlink(missing_ok=True)
        raise
    finally:
        lock.unlink(missing_ok=True)
    return target


def validate_event(event: dict) -> None:
    _require(event, {"schema_version", "event_id", "run_id", "timestamp", "type", "actor", "task_id", "status"})
    if event["schema_version"] != "1.0" or event["type"] not in EVENT_TYPES:
        raise ContractError("invalid event version or type")
    for field in ("event_id", "run_id", "actor", "task_id", "status"):
        if not isinstance(event[field], str) or not event[field].strip():
            raise ContractError(f"invalid {field}")
    _require_datetime(event["timestamp"], "timestamp")


def _claim_event_writer(path: Path, writer_id: str) -> None:
    if not SAFE_MESSAGE_ID.fullmatch(writer_id):
        raise ContractError("invalid writer_id")
    owner = path.with_name(f".{path.name}.writer")
    _require_plain_file_path(owner)
    try:
        fd = os.open(owner, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    except FileExistsError:
        current = owner.read_text(encoding="ascii").strip()
        if current != writer_id:
            raise ContractError(f"event log already owned by writer: {current}")
        return
    with os.fdopen(fd, "w", encoding="ascii", newline="\n") as stream:
        stream.write(writer_id + "\n")
        stream.flush()
        os.fsync(stream.fileno())


def append_event(path: Path, event: dict, *, writer_id: str = "coordinator") -> None:
    """Append one event under a persistent, explicit single-writer contract."""
    validate_event(event)
    path.parent.mkdir(parents=True, exist_ok=True)
    _require_plain_file_path(path)
    _claim_event_writer(path, writer_id)
    line = json.dumps(event, ensure_ascii=False, sort_keys=True) + "\n"
    fd = os.open(path, os.O_APPEND | os.O_CREAT | os.O_WRONLY, 0o600)
    try:
        os.write(fd, line.encode("utf-8"))
        os.fsync(fd)
    finally:
        os.close(fd)


def read_events(path: Path) -> list[dict]:
    events = []
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        try:
            event = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ContractError(f"invalid JSONL line {number}") from exc
        validate_event(event)
        events.append(event)
    return events


def summarize_events(events: Iterable[dict]) -> dict:
    """Return deterministic values that map into, but never replace, Run Report fields."""
    ordered = list(events)
    for event in ordered:
        validate_event(event)
    roles = sorted({e["actor"] for e in ordered if e["type"] == "spawn"})
    handoffs = [e.get("ref") for e in ordered if e["type"] == "handoff" and e.get("ref")]
    gates = [{"gate_id": e.get("ref"), "result": e["status"]} for e in ordered if e["type"] == "gate"]
    terminals = [e for e in ordered if e["type"] == "terminal"]
    return {
        "experts_invoked": roles,
        "handoff_refs": handoffs,
        "handoff_count": len(handoffs),
        "deterministic_gate_results": gates,
        "outcome": terminals[-1]["status"] if terminals else None,
        "event_count": len(ordered),
    }


def validate_transition(previous: str, current: str, *, new_invocation: bool = False) -> None:
    if previous not in STATES or current not in STATES:
        raise ContractError("invalid lifecycle state")
    if previous in TERMINAL_STATES and new_invocation and current == "CREATED":
        return
    if current not in TRANSITIONS[previous]:
        raise ContractError(f"invalid transition: {previous} -> {current}")


def find_worktree_collisions(states: Iterable[dict]) -> list[dict]:
    owners: dict[str, dict] = {}
    collisions = []
    for state in states:
        if state.get("state") not in STATES:
            raise ContractError("invalid lifecycle state")
        worktree = state.get("worktree")
        if not worktree or state["state"] not in ACTIVE_WRITER_STATES:
            continue
        path = str(Path(worktree["worktree_path"]).resolve()).casefold()
        if path in owners and owners[path].get("role") != state.get("role"):
            collisions.append({"worktree_path": worktree["worktree_path"], "roles": [owners[path]["role"], state["role"]]})
        else:
            owners[path] = state
    return collisions
