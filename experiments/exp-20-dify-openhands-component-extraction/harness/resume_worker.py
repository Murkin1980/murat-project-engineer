#!/usr/bin/env python3
"""EXP-20 CP-03 proof P1 — fresh-process resume worker.

Started as an isolated interpreter with *only* the path of a (possibly damaged) MPE
event log. It has no chat context, no fixture, no other input, and must state the run
identity, the recovered evidence, the damage, and the next action — or fail loudly.

Usage:
    python3 resume_worker.py /path/to/run.events.jsonl
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

HARNESS_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(HARNESS_DIR))
sys.path.insert(0, str(HARNESS_DIR.parents[2]))

from durable_event_evidence import resume_packet  # noqa: E402


def main() -> int:
    if len(sys.argv) != 2:
        print(json.dumps({"error": "exactly one event-log path argument is required"}))
        return 2
    log = Path(sys.argv[1])
    if not log.is_file():
        print(json.dumps({"error": f"event log not found: {log.name}"}))
        return 2
    packet = resume_packet(log)
    packet["worker"] = "fresh_process"
    packet["read_from_chat"] = False
    print(json.dumps(packet, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
