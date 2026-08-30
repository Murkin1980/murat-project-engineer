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


def _content_digest(root: Path, value: str) -> str | None:
    path = root / value
    if not path.is_file():
        return None
    return _digest_bytes(path.read_bytes())


def _snapshot(root: Path, base_ref: str, excluded: set[str]) -> dict:
    raw_status = _git(root, "status", "--porcelain=v1", "-z", "--untracked-files=all")
    entries = _parse_status(raw_status, excluded)
    paths = sorted({entry["path"] for entry in entries})
    head_sha = _git(root, "rev-parse", "HEAD").decode().strip()
    base_sha = _git(root, "rev-parse", "--verify", f"{base_ref}^{{commit}}").decode().strip()
    pathspec = [".", *[f":(exclude){value}" for value in sorted(excluded)]]
    staged = _git(root, "diff", "--cached", "--binary", "--full-index", "--no-ext-diff", "--", *pathspec)
    unstaged = _git(root, "diff", "--binary", "--full-index", "--no-ext-diff", "--", *pathspec)
    content = {value: _content_digest(root, value) for value in paths}
    payload = {
        "head_sha": head_sha,
        "base_ref": base_ref,
        "base_sha": base_sha,
        "entries": entries,
        "content": content,
        "staged_diff_sha256": _digest_bytes(staged),
        "unstaged_diff_sha256": _digest_bytes(unstaged),
    }
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    return {**payload, "fingerprint_sha256": _digest_bytes(canonical)}


def _scope_patterns(task_packet: dict) -> list[str]:
    values = task_packet.get("target_files_or_components")
    if not isinstance(values, list) or not values or not all(isinstance(item, str) and item for item in values):
        raise VerificationStateError("task packet needs a non-empty target_files_or_components string list")
    return [Path(item).as_posix().rstrip("/") for item in values]


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
    return {
        "schema_version": "2.0",
        "state": "VERIFIED",
        "captured_at": datetime.now(timezone.utc).isoformat(),
        "excluded_paths": sorted(excluded),
        "git": snapshot,
    }


def check(
    root: Path,
    state: dict,
    *,
    require_clean_scope: bool = False,
    task_packet: dict | None = None,
) -> dict:
    root = _repo_root(root)
    if state.get("schema_version") != "2.0" or state.get("state") not in {"VERIFIED", "UNVERIFIED"}:
        raise VerificationStateError("invalid verification state")
    expected = state.get("git")
    if not isinstance(expected, dict) or not expected.get("fingerprint_sha256"):
        raise VerificationStateError("verification state needs a Git snapshot")
    excluded = state.get("excluded_paths", [])
    if not isinstance(excluded, list) or not all(isinstance(item, str) for item in excluded):
        raise VerificationStateError("invalid excluded_paths")
    actual = _snapshot(root, expected.get("base_ref", "HEAD"), set(excluded))
    reasons: list[str] = []
    if actual["head_sha"] != expected.get("head_sha"):
        reasons.append("HEAD changed")
    if actual["base_sha"] != expected.get("base_sha"):
        reasons.append("base SHA changed")
    if actual["entries"] != expected.get("entries"):
        reasons.append("Git changed-file list or status changed")
    if actual["fingerprint_sha256"] != expected.get("fingerprint_sha256"):
        reasons.append("Git diff or changed-file content changed")
    if require_clean_scope:
        if task_packet is None:
            raise VerificationStateError("--require-clean-scope requires --task-packet")
        patterns = _scope_patterns(task_packet)
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
            state = capture(root, args.files, base_ref=args.base, excluded_paths={state_relative} if state_relative else set())
            state_path.parent.mkdir(parents=True, exist_ok=True)
            state_path.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
        else:
            packet = None
            if args.task_packet:
                packet = json.loads(args.task_packet.read_text(encoding="utf-8"))
            state = check(
                root,
                json.loads(state_path.read_text(encoding="utf-8")),
                require_clean_scope=args.require_clean_scope,
                task_packet=packet,
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
