from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path


class VerificationStateError(ValueError):
    pass


def _safe_file(root: Path, value: str) -> Path:
    path = (root / value).resolve()
    try:
        path.relative_to(root.resolve())
    except ValueError as exc:
        raise VerificationStateError(f"file escapes root: {value}") from exc
    if not path.is_file():
        raise VerificationStateError(f"file does not exist: {value}")
    return path


def _digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def capture(root: Path, files: list[str]) -> dict:
    if not files:
        raise VerificationStateError("at least one verified file is required")
    normalized = sorted(dict.fromkeys(files))
    return {
        "schema_version": "1.0",
        "state": "VERIFIED",
        "captured_at": datetime.now(timezone.utc).isoformat(),
        "files": {value: _digest(_safe_file(root, value)) for value in normalized},
    }


def check(root: Path, state: dict) -> dict:
    if state.get("schema_version") != "1.0" or state.get("state") not in {"VERIFIED", "UNVERIFIED"}:
        raise VerificationStateError("invalid verification state")
    files = state.get("files")
    if not isinstance(files, dict) or not files:
        raise VerificationStateError("verification state needs at least one file")
    changed = []
    for value, expected in files.items():
        try:
            actual = _digest(_safe_file(root, value))
        except VerificationStateError:
            changed.append(value)
            continue
        if actual != expected:
            changed.append(value)
    if changed:
        return {
            **state,
            "state": "UNVERIFIED",
            "invalidation_reason": "post-verification change: " + ", ".join(sorted(changed)),
        }
    return {key: value for key, value in state.items() if key != "invalidation_reason"}


def main() -> int:
    parser = argparse.ArgumentParser(description="Capture or check bounded MPE verification state.")
    subparsers = parser.add_subparsers(dest="command", required=True)
    capture_parser = subparsers.add_parser("capture")
    capture_parser.add_argument("--root", default=".")
    capture_parser.add_argument("--state", required=True)
    capture_parser.add_argument("--file", action="append", dest="files", required=True)
    check_parser = subparsers.add_parser("check")
    check_parser.add_argument("--root", default=".")
    check_parser.add_argument("--state", required=True)
    args = parser.parse_args()
    try:
        root = Path(args.root).resolve()
        state_path = Path(args.state).resolve()
        if args.command == "capture":
            state = capture(root, args.files)
            state_path.parent.mkdir(parents=True, exist_ok=True)
            state_path.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
        else:
            state = check(root, json.loads(state_path.read_text(encoding="utf-8")))
            state_path.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
        print(json.dumps(state, sort_keys=True))
        return 0 if state["state"] == "VERIFIED" else 3
    except (OSError, json.JSONDecodeError, VerificationStateError) as exc:
        print(f"VERIFICATION STATE FAILED: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
