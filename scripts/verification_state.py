from __future__ import annotations

import argparse
import fnmatch
import hashlib
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


class VerificationStateError(ValueError):
    pass


def _digest_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _git(root: Path, *args: str) -> bytes:
    completed = subprocess.run(
        ["git", "-C", str(root), *args],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if completed.returncode:
        detail = completed.stderr.decode("utf-8", errors="replace").strip()
        raise VerificationStateError(f"git {' '.join(args)} failed: {detail}")
    return completed.stdout


def _repo_root(root: Path) -> Path:
    resolved = root.resolve()
    top = Path(_git(resolved, "rev-parse", "--show-toplevel").decode().strip()).resolve()
    if top != resolved:
        raise VerificationStateError(f"root must be the Git repository root: {top}")
    return resolved


def _repo_relative(root: Path, path: Path | None) -> str | None:
    if path is None:
        return None
    try:
        return path.resolve().relative_to(root).as_posix()
    except ValueError:
        return None


def _parse_status(raw: bytes, excluded: set[str]) -> list[dict[str, str]]:
    tokens = raw.decode("utf-8", errors="surrogateescape").split("\0")
    entries: list[dict[str, str]] = []
    index = 0
    while index < len(tokens):
        token = tokens[index]
        index += 1
        if not token:
            continue
        if len(token) < 4:
            raise VerificationStateError(f"unexpected git status entry: {token!r}")
        status, path = token[:2], token[3:]
        paths = [path]
        if "R" in status or "C" in status:
            if index >= len(tokens) or not tokens[index]:
                raise VerificationStateError("rename/copy status is missing its source path")
            paths.append(tokens[index])
            index += 1
        for position, value in enumerate(paths):
            normalized = Path(value).as_posix()
            if normalized in excluded:
                continue
            entry_status = status if position == 0 else f"{status}:source"
            entries.append({"path": normalized, "status": entry_status})
    return sorted(entries, key=lambda item: (item["path"], item["status"]))


def _parse_committed_status(raw: bytes, excluded: set[str]) -> list[dict[str, str]]:
    tokens = raw.decode("utf-8", errors="surrogateescape").split("\0")
    entries: list[dict[str, str]] = []
    index = 0
    while index < len(tokens):
        status = tokens[index]
        index += 1
        if not status:
            continue
        path_count = 2 if status.startswith(("R", "C")) else 1
        if index + path_count > len(tokens):
            raise VerificationStateError("committed name-status entry is incomplete")
        paths = tokens[index:index + path_count]
        index += path_count
        for position, value in enumerate(paths):
            if not value:
                raise VerificationStateError("committed name-status path is empty")
            normalized = Path(value).as_posix()
            if normalized in excluded:
                continue
            role = ":source" if path_count == 2 and position == 0 else ""
            entries.append({"path": normalized, "status": f"committed:{status}{role}"})
    return sorted(entries, key=lambda item: (item["path"], item["status"]))


def _content_digest(root: Path, value: str) -> str | None:
    path = root / value
    if not path.is_file():
        return None
    return _digest_bytes(path.read_bytes())


def _snapshot(root: Path, base_ref: str, excluded: set[str]) -> dict:
    head_sha = _git(root, "rev-parse", "HEAD").decode().strip()
    base_sha = _git(root, "rev-parse", "--verify", f"{base_ref}^{{commit}}").decode().strip()
    pathspec = [".", *[f":(exclude){value}" for value in sorted(excluded)]]
    raw_committed_status = _git(
        root, "diff", "--name-status", "-z", "--find-renames", f"{base_sha}...{head_sha}", "--", *pathspec
    )
    raw_status = _git(root, "status", "--porcelain=v1", "-z", "--untracked-files=all")
    entries = sorted(
        [*_parse_committed_status(raw_committed_status, excluded), *_parse_status(raw_status, excluded)],
        key=lambda item: (item["path"], item["status"]),
    )
    paths = sorted({entry["path"] for entry in entries})
    committed = _git(
        root, "diff", "--binary", "--full-index", "--no-ext-diff", f"{base_sha}...{head_sha}", "--", *pathspec
    )
    staged = _git(root, "diff", "--cached", "--binary", "--full-index", "--no-ext-diff", "--", *pathspec)
    unstaged = _git(root, "diff", "--binary", "--full-index", "--no-ext-diff", "--", *pathspec)
    content = {value: _content_digest(root, value) for value in paths}
    payload = {
        "head_sha": head_sha,
        "base_ref": base_ref,
        "base_sha": base_sha,
        "entries": entries,
        "content": content,
        "committed_diff_sha256": _digest_bytes(committed),
        "staged_diff_sha256": _digest_bytes(staged),
        "unstaged_diff_sha256": _digest_bytes(unstaged),
    }
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    return {**payload, "fingerprint_sha256": _digest_bytes(canonical)}


def _checkpoint_digest(state: dict) -> str:
    immutable = {
        "schema_version": state.get("schema_version"),
        "captured_at": state.get("captured_at"),
        "excluded_paths": state.get("excluded_paths"),
        "git": state.get("git"),
        "task_packet": state.get("task_packet"),
    }
    canonical = json.dumps(immutable, sort_keys=True, separators=(",", ":")).encode()
    return _digest_bytes(canonical)


def _scope_patterns(task_packet: dict) -> list[str]:
    values = task_packet.get("target_files_or_components")
    if not isinstance(values, list) or not values or not all(isinstance(item, str) and item for item in values):
        raise VerificationStateError("task packet needs a non-empty target_files_or_components string list")
    return [Path(item).as_posix().rstrip("/") for item in values]


def _task_packet_binding(root: Path, path: Path) -> dict:
    resolved = path.resolve()
    raw = resolved.read_bytes()
    try:
        packet = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise VerificationStateError(f"invalid Task Packet JSON: {exc}") from exc
    scope = _scope_patterns(packet)
    relative = _repo_relative(root, resolved)
    identity = relative if relative is not None else resolved.as_posix()
    location = "repository" if relative is not None else "external"
    scope_raw = json.dumps(scope, separators=(",", ":")).encode()
    return {
        "location": location,
        "path": identity,
        "sha256": _digest_bytes(raw),
        "scope": scope,
        "scope_sha256": _digest_bytes(scope_raw),
    }


def _in_scope(path: str, patterns: list[str]) -> bool:
    return any(
        path == pattern
        or path.startswith(pattern + "/")
        or fnmatch.fnmatchcase(path, pattern)
        for pattern in patterns
    )


def capture(
    root: Path,
    files: list[str] | None = None,
    *,
    base_ref: str = "HEAD",
    excluded_paths: set[str] | None = None,
    task_packet_path: Path | None = None,
) -> dict:
    root = _repo_root(root)
    excluded = set(excluded_paths or set())
    snapshot = _snapshot(root, base_ref, excluded)
    changed_paths = {entry["path"] for entry in snapshot["entries"]}
    if files:
        declared = {Path(value).as_posix() for value in files}
        omitted = sorted(changed_paths - declared)
        if omitted:
            raise VerificationStateError("--file scope omits Git changes: " + ", ".join(omitted))
    if not changed_paths:
        raise VerificationStateError("Git change set is empty")
    binding = _task_packet_binding(root, task_packet_path) if task_packet_path else None
    state = {
        "schema_version": "2.0",
        "state": "VERIFIED",
        "captured_at": datetime.now(timezone.utc).isoformat(),
        "excluded_paths": sorted(excluded),
        "git": snapshot,
        "task_packet": binding,
    }
    return {**state, "checkpoint_sha256": _checkpoint_digest(state)}


def check(
    root: Path,
    state: dict,
    *,
    require_clean_scope: bool = False,
    task_packet_path: Path | None = None,
    allowed_excluded_paths: set[str] | None = None,
) -> dict:
    root = _repo_root(root)
    if state.get("schema_version") != "2.0" or state.get("state") not in {"VERIFIED", "UNVERIFIED"}:
        raise VerificationStateError("invalid verification state")
    expected = state.get("git")
    if not isinstance(expected, dict) or not expected.get("fingerprint_sha256"):
        raise VerificationStateError("verification state needs a Git snapshot")
    stored_excluded = state.get("excluded_paths", [])
    if not isinstance(stored_excluded, list) or not all(isinstance(item, str) for item in stored_excluded):
        raise VerificationStateError("invalid excluded_paths")
    allowed_excluded = set(allowed_excluded_paths or set())
    reasons: list[str] = []
    if set(stored_excluded) != allowed_excluded:
        reasons.append("stored exclusions differ from the CLI-computed state path")
    if state.get("checkpoint_sha256") != _checkpoint_digest(state):
        reasons.append("verification checkpoint integrity digest mismatch")
    actual = _snapshot(root, expected.get("base_ref", "HEAD"), allowed_excluded)
    if actual["head_sha"] != expected.get("head_sha"):
        reasons.append("HEAD changed")
    if actual["base_sha"] != expected.get("base_sha"):
        reasons.append("base SHA changed")
    if actual["entries"] != expected.get("entries"):
        reasons.append("Git changed-file list or status changed")
    if actual["fingerprint_sha256"] != expected.get("fingerprint_sha256"):
        reasons.append("Git diff or changed-file content changed")
    if require_clean_scope:
        expected_packet = state.get("task_packet")
        if not isinstance(expected_packet, dict):
            raise VerificationStateError("--require-clean-scope requires a Task Packet bound during capture")
        if task_packet_path is None:
            raise VerificationStateError("--require-clean-scope requires --task-packet")
        try:
            current_packet = _task_packet_binding(root, task_packet_path)
        except (OSError, VerificationStateError) as exc:
            current_packet = None
            reasons.append(f"bound Task Packet is unavailable or invalid: {exc}")
        if current_packet is not None:
            if (current_packet["location"], current_packet["path"]) != (
                expected_packet.get("location"), expected_packet.get("path")
            ):
                reasons.append("Task Packet path identity changed")
            if current_packet["sha256"] != expected_packet.get("sha256"):
                reasons.append("Task Packet bytes changed")
            if current_packet["scope_sha256"] != expected_packet.get("scope_sha256"):
                reasons.append("Task Packet scope changed")
        patterns = expected_packet.get("scope")
        if not isinstance(patterns, list) or not patterns:
            raise VerificationStateError("bound Task Packet has no frozen scope")
        outside = sorted({entry["path"] for entry in actual["entries"] if not _in_scope(entry["path"], patterns)})
        if outside:
            reasons.append("out-of-scope Git changes: " + ", ".join(outside))
    if reasons:
        return {**state, "state": "UNVERIFIED", "invalidation_reason": "; ".join(reasons)}
    return {key: value for key, value in state.items() if key != "invalidation_reason"}


def main() -> int:
    parser = argparse.ArgumentParser(description="Capture or check a Git-complete MPE verification state.")
    subparsers = parser.add_subparsers(dest="command", required=True)
    capture_parser = subparsers.add_parser("capture")
    capture_parser.add_argument("--root", default=".")
    capture_parser.add_argument("--state", required=True)
    capture_parser.add_argument("--base", default="HEAD")
    capture_parser.add_argument("--file", action="append", dest="files")
    capture_parser.add_argument("--task-packet", type=Path)
    check_parser = subparsers.add_parser("check")
    check_parser.add_argument("--root", default=".")
    check_parser.add_argument("--state", required=True)
    check_parser.add_argument("--require-clean-scope", action="store_true")
    check_parser.add_argument("--task-packet", type=Path)
    args = parser.parse_args()
    try:
        root = _repo_root(Path(args.root))
        state_path = Path(args.state).resolve()
        state_relative = _repo_relative(root, state_path)
        if args.command == "capture":
            state = capture(
                root,
                args.files,
                base_ref=args.base,
                excluded_paths={state_relative} if state_relative else set(),
                task_packet_path=args.task_packet,
            )
            state_path.parent.mkdir(parents=True, exist_ok=True)
            state_path.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
        else:
            state = check(
                root,
                json.loads(state_path.read_text(encoding="utf-8")),
                require_clean_scope=args.require_clean_scope,
                task_packet_path=args.task_packet,
                allowed_excluded_paths={state_relative} if state_relative else set(),
            )
            if state["state"] == "UNVERIFIED":
                state_path.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
        print(json.dumps(state, sort_keys=True))
        return 0 if state["state"] == "VERIFIED" else 3
    except (OSError, json.JSONDecodeError, VerificationStateError) as exc:
        print(f"VERIFICATION STATE FAILED: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
