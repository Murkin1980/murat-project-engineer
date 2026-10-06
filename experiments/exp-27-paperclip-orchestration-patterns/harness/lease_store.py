"""EXP-27 CP-03 — smallest deterministic, file-backed task-lease proof.

Experiment-scoped proof only. This is NOT a production component and adds no
daemon, service, database, queue, or scheduler.

Atomicity primitive: ``os.open(path, O_CREAT | O_EXCL)`` — the same exclusive
create/claim primitive already used by ``scripts/runtime_coordination.py``
(``deliver_atomic`` mailbox lock and the single-writer event-log contract). The
lease adds what that helper deliberately does not provide: durable owner identity,
a bounded expiry/reclaim path, and visible release/terminal records.

Layout for one task:
  <task>.lease.lock         atomic exclusivity anchor (created O_EXCL, removed on release)
  <task>.lease.json         durable record: generation, owner, expiry, history[]
  <task>.lease.reclaim.lock bounded, serialized expiry-reclaim marker

Observable statuses (never silent):
  LEASE_ACQUIRED, LEASE_ACQUIRED_RECLAIMED, LEASE_CONFLICT,
  LEASE_RELEASED, LEASE_RELEASE_DENIED
"""
from __future__ import annotations

import json
import os
import tempfile
import time
from pathlib import Path

LEASE_ACQUIRED = "LEASE_ACQUIRED"
LEASE_ACQUIRED_RECLAIMED = "LEASE_ACQUIRED_RECLAIMED"
LEASE_CONFLICT = "LEASE_CONFLICT"
LEASE_RELEASED = "LEASE_RELEASED"
LEASE_RELEASE_DENIED = "LEASE_RELEASE_DENIED"

READ_RETRIES = 20
READ_RETRY_SECONDS = 0.002


def _now(clock=None) -> float:
    return clock() if clock is not None else time.time()


def _iso(epoch: float) -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime(epoch)) + "Z"


def _atomic_write_json(path: Path, data: dict) -> None:
    fd, temp_name = tempfile.mkstemp(prefix=".lease-", suffix=".tmp", dir=str(path.parent))
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as stream:
            json.dump(data, stream, ensure_ascii=False, sort_keys=True, indent=1)
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temp_name, path)
    except BaseException:
        Path(temp_name).unlink(missing_ok=True)
        raise


def _read_json(path: Path):
    """Bounded read retry: a concurrent exclusive-create may be mid-write."""
    for _ in range(READ_RETRIES):
        if not path.exists():
            return None
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            time.sleep(READ_RETRY_SECONDS)
    raise ValueError(f"unreadable lease record: {path}")


def _active(record: dict, now: float) -> bool:
    return record.get("status") == "ACTIVE" and float(record["expires_at_epoch"]) > now


def _conflict(record, owner: str, now: float, reason: str = "LEASE_CONFLICT") -> dict:
    record = record or {}
    return {
        "status": LEASE_CONFLICT,
        "reason": reason,
        "owner": owner,
        "current_owner": record.get("owner"),
        "generation": record.get("generation"),
        "expires_at": record.get("expires_at"),
        "last_action": record.get("last_action"),
        "record_status": record.get("status"),
    }


def _new_record(owner: str, now: float, ttl_seconds: float, *, history: list, generation: int,
                last_action: str, reclaimed_from=None) -> dict:
    return {
        "record_version": "exp-27-lease-v1",
        "generation": generation,
        "status": "ACTIVE",
        "owner": owner,
        "acquired_at": _iso(now),
        "acquired_at_epoch": now,
        "expires_at": _iso(now + ttl_seconds),
        "expires_at_epoch": now + ttl_seconds,
        "ttl_seconds": ttl_seconds,
        "last_action": last_action,
        "reclaimed_from": reclaimed_from,
        "released_at": None,
        "release_reason": None,
        "history": history,
    }


def _terminalize(record: dict, now: float, reason: str) -> dict:
    return {
        "generation": record.get("generation"),
        "owner": record.get("owner"),
        "status": "SUPERSEDED",
        "reason": reason,
        "expired_at": _iso(now),
        "expires_at": record.get("expires_at"),
    }


def lease_paths(lease_dir) -> tuple[Path, Path, Path]:
    base = Path(lease_dir)
    return (base / "task.lease.lock", base / "task.lease.json", base / "task.lease.reclaim.lock")


def read_record(lease_dir):
    _, record_path, _ = lease_paths(lease_dir)
    return _read_json(record_path)


def acquire(lease_dir, owner: str, ttl_seconds: float, *, clock=None, last_action: str = "checkout") -> dict:
    """Acquire the task lease. Exactly one ACTIVE owner per task at any time."""
    lock_path, record_path, reclaim_path = lease_paths(lease_dir)
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    now = _now(clock)
    try:
        fd = os.open(lock_path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    except FileExistsError:
        # The exclusivity anchor exists. Another executor may be inside the small
        # window between creating the anchor and persisting its record, so wait a
        # bounded time for a readable record instead of taking the lease over.
        record = None
        for _ in range(READ_RETRIES):
            record = _read_json(record_path)
            if record is not None:
                break
            time.sleep(READ_RETRY_SECONDS)
        if record is None:
            return _conflict(None, owner, _now(clock), reason="LEASE_INITIALIZING")
        if _active(record, now):
            return _conflict(record, owner, now)
        # Expired or terminal: reclaim under a bounded, serialized marker.
        reclaim_now = _now(clock)
        try:
            rfd = os.open(reclaim_path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
        except FileExistsError:
            return _conflict(record, owner, reclaim_now, reason="LEASE_RECLAIM_IN_PROGRESS")
        try:
            record = _read_json(record_path)
            reclaim_now = _now(clock)
            if record is None or _active(record, reclaim_now):
                return _conflict(record, owner, reclaim_now,
                                 reason="LEASE_CONFLICT" if record else "LEASE_INITIALIZING")
            history = list(record.get("history", [])) if record else []
            if record:
                history.append(_terminalize(record, reclaim_now, "LEASE_EXPIRED"))
            new_record = _new_record(
                owner, reclaim_now, ttl_seconds,
                history=history,
                generation=(record.get("generation", 0) + 1) if record else 1,
                last_action=last_action,
                reclaimed_from=record.get("owner") if record else None,
            )
            _atomic_write_json(record_path, new_record)
            return {
                "status": LEASE_ACQUIRED_RECLAIMED,
                "reason": "LEASE_EXPIRED",
                "owner": owner,
                "reclaimed_from": new_record["reclaimed_from"],
                "generation": new_record["generation"],
                "expires_at": new_record["expires_at"],
                "record": new_record,
            }
        finally:
            reclaim_path.unlink(missing_ok=True)
    else:
        os.close(fd)
        previous = _read_json(record_path)
        history = list(previous.get("history", [])) if previous else []
        if previous:
            history.append(_terminalize(previous, now, f"LEASE_{previous.get('status', 'TERMINAL')}"))
        record = _new_record(
            owner, now, ttl_seconds,
            history=history,
            generation=(previous.get("generation", 0) + 1) if previous else 1,
            last_action=last_action,
            reclaimed_from=None,
        )
        if previous:
            record["previous_owner"] = previous.get("owner")
            record["previous_release_reason"] = previous.get("release_reason")
        _atomic_write_json(record_path, record)
        return {
            "status": LEASE_ACQUIRED,
            "owner": owner,
            "generation": record["generation"],
            "expires_at": record["expires_at"],
            "previous_owner": record.get("previous_owner"),
            "record": record,
        }


def release(lease_dir, owner: str, *, reason: str = "TERMINAL_DONE", clock=None) -> dict:
    """Release by the active owner only; the terminal record stays visible."""
    lock_path, record_path, _ = lease_paths(lease_dir)
    now = _now(clock)
    record = _read_json(record_path)
    if not record:
        return {"status": LEASE_RELEASED, "reason": "NO_LEASE_RECORD", "owner": owner}
    if record.get("status") != "ACTIVE" or not lock_path.exists():
        return {"status": LEASE_RELEASED, "reason": f"ALREADY_{record.get('status') or 'RELEASED'}",
                "owner": owner, "current_owner": record.get("owner")}
    if record.get("owner") != owner:
        return {"status": LEASE_RELEASE_DENIED, "reason": "LEASE_OWNED_BY_OTHER",
                "owner": owner, "current_owner": record.get("owner")}
    record.update({
        "status": "RELEASED",
        "released_at": _iso(now),
        "release_reason": reason,
        "released_by": owner,
        "last_action": "release",
    })
    _atomic_write_json(record_path, record)
    lock_path.unlink(missing_ok=True)
    return {"status": LEASE_RELEASED, "owner": owner, "reason": reason,
            "released_at": record["released_at"], "record": record}
