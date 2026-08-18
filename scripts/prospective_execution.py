from __future__ import annotations

import argparse
import json
from pathlib import Path

try:
    from scripts.prospective_validation import execute
except ModuleNotFoundError:
    from prospective_validation import execute


def main() -> int:
    parser = argparse.ArgumentParser(description="Create immutable EXP-12 EXECUTED evidence")
    parser.add_argument("registration", type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    raw = args.registration.read_bytes()
    registration = json.loads(raw.decode("utf-8"))
    result = execute(registration, args.registration.as_posix(), raw)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
