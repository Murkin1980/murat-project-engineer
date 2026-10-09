"""EXP-20 CP-03 proof P1 — crash-tolerant, idempotent, resumable event evidence.

Donor (read-only audit, MIT): OpenHands ``software-agent-sdk``
``openhands/sdk/conversation/event_store.py`` with ``conversation/persistence_const.py``
and ``io/local.py``:

* one durable record per event, named so the order/index is visible without parsing
  the payload (``event-{idx:05d}-{event_id}.json``);
* a length-marker sidecar (``.eventlog-len-{length}.marker``) that answers "did the log
  advance?" with a single ``exists()`` instead of a full rescan, advanced delete-first so
  an interrupted update leaves *no* marker and forces a recount;
* duplicate event-id rejection on append (``ValueError``), so a replay cannot invent a
  second copy of the same evidence;
* ``_scan_and_build_index`` resume, which refuses a non-contiguous index instead of
  silently renumbering.

Host contract (UNCHANGED): MPE ``scripts/runtime_coordination.py`` — one append-only JSONL
event log per run, explicit single-writer claim file, ``validate_event`` and
``summarize_events`` (see ``docs/architecture/RUNTIME_COORDINATION_PATTERNS.md`` and the
``event_log_valid`` gate in ``gates/registry.yaml``).

This module is experiment-scoped. It *calls* the production helpers and never modifies
them; it writes only inside the directory it is given. Nothing here is production code and
no MPE contract, schema, gate, or source of truth is changed by importing it.
"""
from __future__ import annotations

import hashlib
import json
import os
import time
from pathlib import Path

try:  # normal package import
    from scripts import runtime_coordination as rc
except Exception:  # standalone import (tests / worker process)
    import sys

    sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
    from scripts import runtime_coordination as rc  # type: ignore

# Closed integrity vocabulary. Deliberately small: it annotates the existing
# ``event_log_valid`` gate, it does not create a new gate or a new status model.
INTEGRITY_COMPLETE = "COMPLETE"
INTEGRITY_MARKER_UNVERIFIED = "MARKER_UNVERIFIED"
INTEGRITY_DAMAGED = "DAMAGED"
INTEGRITY_DUPLICATE_EVENTS = "DUPLICATE_EVENTS"

# Closed damage-kind vocabulary (one record per damaged line, never a silent drop).
DAMAGE_TORN_TAIL = "torn_tail"
DAMAGE_INTERIOR = "interior_damage"
DAMAGE_INVALID_EVENT = "invalid_event"
DAMAGE_DUPLICATE_ID = "duplicate_event_id"


class DuplicateEventConflict(rc.ContractError):
    """A different event was replayed under an event_id that is already durable."""


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _marker_path(log: Path, count: int) -> Path:
    """Donor naming rule, adapted to MPE's dotfile sidecar convention."""
    return log.with_name(f".{log.name}.len-{count}")


def _markers(log: Path) -> list[int]:
    found = []
    for candidate in sorted(log.parent.glob(f".{log.name}.len-*")):
        suffix = candidate.name.rsplit("-", 1)[-1]
        if suffix.isdigit():
            found.append(int(suffix))
    return found


def marker_count(log: Path) -> int | None:
    """Cheap, marker-only answer to "how long was this log when it was last closed?".

    ``None`` means "no marker" — the caller must recount. A marker is never proof that
    the log is undamaged; it only records the length its writer believed it had written.
    """
    counts = _markers(log)
    if not counts:
        return None
    return max(counts)


def advance_marker(log: Path, previous: int | None, current: int) -> None:
    """Delete-first marker update (donor rule): an interrupted update leaves no marker."""
    if previous is not None:
        stale = _marker_path(log, previous)
        if stale.exists():
            stale.unlink()
    for count in _markers(log):
        if count != current:
            _marker_path(log, count).unlink(missing_ok=True)
    target = _marker_path(log, current)
    fd = os.open(target, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    os.close(fd)


def known_event_ids(log: Path) -> set[str]:
    """Event ids already durable in ``log`` (damaged lines contribute nothing)."""
    if not log.exists():
        return set()
    return {event["event_id"] for event in recover(log)["events"]}


def append_durable(log: Path, event: dict, *, writer_id: str = "coordinator") -> dict:
    """Append one event through the *production* writer, then advance the marker.

    Idempotent by ``event_id`` (donor duplicate-id rejection):

    * an identical replay is refused without touching the log (``DUPLICATE_REPLAYED``);
    * a *different* event under an existing id raises ``DuplicateEventConflict`` and the
      log is left byte-identical;
    * a new id is written by ``scripts.runtime_coordination.append_event`` (validation,
      single-writer claim, fsync and append semantics stay the production authority).
    """
    event_id = event.get("event_id")
    if not isinstance(event_id, str) or not event_id:
        raise rc.ContractError("invalid event_id")

    before = log.read_bytes() if log.exists() else b""
    for line in before.decode("utf-8", errors="replace").splitlines():
        if not line.strip():
            continue
        try:
            existing = json.loads(line)
        except json.JSONDecodeError:
            continue  # a damaged line cannot own an id
        if isinstance(existing, dict) and existing.get("event_id") == event_id:
            if existing == event:
                return {
                    "status": "DUPLICATE_REPLAYED",
                    "event_id": event_id,
                    "count": marker_count(log),
                    "bytes_written": 0,
                }
            raise DuplicateEventConflict(f"event_id already durable with a different payload: {event_id}")

    previous = marker_count(log)
    started = time.perf_counter()
    rc.append_event(log, event, writer_id=writer_id)
    write_seconds = time.perf_counter() - started
    current = len(recover(log)["events"])
    started = time.perf_counter()
    advance_marker(log, previous, current)
    marker_seconds = time.perf_counter() - started
    return {
        "status": "APPENDED",
        "event_id": event_id,
        "count": current,
        "bytes_written": len(log.read_bytes()) - len(before),
        "write_seconds": write_seconds,
        "marker_seconds": marker_seconds,
    }


def recover(log: Path) -> dict:
    """Recover every *durable* event from a possibly damaged JSONL log.

    The strict production reader (``rc.read_events``) is all-or-nothing: one unparsable
    line raises ``ContractError`` and the whole run loses its evidence. This recovery
    keeps that strictness as the default and adds an explicit, reported alternative:
    every unusable line becomes a damage record with its line number and kind, and the
    remaining events are still validated by the production ``rc.validate_event``.

    Damage is never silently dropped and never silently accepted: the caller gets the
    recovered events *and* the reason each line was not usable.
    """
    if not log.exists():
        raise rc.ContractError(f"event log not found: {log.name}")

    text = log.read_bytes().decode("utf-8", errors="replace")
    raw_lines = text.split("\n")
    terminated = text.endswith("\n")
    if terminated and raw_lines and raw_lines[-1] == "":
        raw_lines = raw_lines[:-1]

    events: list[dict] = []
    damage: list[dict] = []
    seen: dict[str, int] = {}
    last_index = len(raw_lines)

    for number, raw in enumerate(raw_lines, 1):
        line = raw.strip()
        if not line:
            damage.append({"line": number, "kind": DAMAGE_INTERIOR, "reason": "empty line", "bytes": len(raw)})
            continue
        is_tail = number == last_index and not terminated
        try:
            candidate = json.loads(line)
        except json.JSONDecodeError as exc:
            damage.append(
                {
                    "line": number,
                    "kind": DAMAGE_TORN_TAIL if is_tail else DAMAGE_INTERIOR,
                    "reason": f"unparsable JSON ({type(exc).__name__})",
                    "bytes": len(raw),
                    "terminated": not is_tail,
                }
            )
            continue
        try:
            rc.validate_event(candidate)
        except rc.ContractError as exc:
            damage.append({"line": number, "kind": DAMAGE_INVALID_EVENT, "reason": str(exc), "bytes": len(raw)})
            continue
        event_id = candidate["event_id"]
        if event_id in seen:
            damage.append(
                {
                    "line": number,
                    "kind": DAMAGE_DUPLICATE_ID,
                    "reason": f"event_id already recovered at line {seen[event_id]}",
                    "bytes": len(raw),
                    "event_id": event_id,
                }
            )
            continue
        seen[event_id] = number
        events.append(candidate)

    kinds = {record["kind"] for record in damage}
    if DAMAGE_TORN_TAIL in kinds or DAMAGE_INTERIOR in kinds or DAMAGE_INVALID_EVENT in kinds:
        integrity = INTEGRITY_DAMAGED
    elif DAMAGE_DUPLICATE_ID in kinds:
        integrity = INTEGRITY_DUPLICATE_EVENTS
    elif marker_count(log) == len(events):
        integrity = INTEGRITY_COMPLETE
    else:
        integrity = INTEGRITY_MARKER_UNVERIFIED

    return {
        "log": log.name,
        "events": events,
        "damage": damage,
        "recovered_count": len(events),
        "damaged_count": len(damage),
        "line_count": len(raw_lines),
        "marker_count": marker_count(log),
        "integrity": integrity,
    }


def integrity_check(log: Path, known_count: int) -> dict:
    """Marker-only check: has the log advanced past ``known_count``?

    One ``glob``/``stat`` per candidate marker and **zero** payload parses — the donor's
    cheap-writer-check idea. It answers only "advanced / unchanged / unverifiable"; it
    never claims the log is undamaged (that needs ``recover``).
    """
    counted = marker_count(log)
    if counted is None:
        return {"verdict": "MARKER_ABSENT", "marker_count": None, "known_count": known_count, "parse_ops": 0}
    return {
        "verdict": "ADVANCED" if counted > known_count else "UNCHANGED",
        "marker_count": counted,
        "known_count": known_count,
        "parse_ops": 0,
    }


def resume_packet(log: Path) -> dict:
    """What a fresh executor needs to continue, derived only from the log on disk.

    ``summarize_events`` is the *production* function, called unchanged on the recovered
    events: the borrowed part is the recovery, not the summary contract.
    """
    recovered = recover(log)
    events = recovered["events"]
    summary = rc.summarize_events(events)
    lifecycle = [event["status"] for event in events if event["type"] in {"spawn", "resume", "block", "terminal"}]
    return {
        "log": log.name,
        "integrity": recovered["integrity"],
        "recovered_count": recovered["recovered_count"],
        "damaged_count": recovered["damaged_count"],
        "damage": recovered["damage"],
        "run_id": events[0]["run_id"] if events else None,
        "task_id": events[0]["task_id"] if events else None,
        "lifecycle": lifecycle,
        "summary": summary,
        "resumable": bool(events) and summary["outcome"] not in rc.TERMINAL_STATES,
        "next_action": (
            "continue from the last durable event; re-emit the damaged tail explicitly"
            if recovered["damage"]
            else ("run is terminal; no resume required" if summary["outcome"] in rc.TERMINAL_STATES else "continue")
        ),
    }


def truncate_tail(log: Path, keep_bytes: int) -> dict:
    """Deterministic crash simulation: cut the final durable line mid-write."""
    data = log.read_bytes()
    cut = max(0, len(data) - keep_bytes)
    log.write_bytes(data[:cut])
    return {"original_bytes": len(data), "kept_bytes": cut, "removed_bytes": len(data) - cut}
