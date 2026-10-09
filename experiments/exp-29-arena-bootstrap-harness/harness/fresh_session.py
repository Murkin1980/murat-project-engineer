#!/usr/bin/env python3
"""EXP-29 — isolated fresh-session workers (CP-03 Arm A / Arm B).

Every command runs as a separate, isolated interpreter
(``python3 -I fresh_session.py <command>``) with a temporary working directory,
so the worker cannot see the parent orchestration process or the chat. That is
the point of the fresh-session comparison:

- ``rediscover`` (Arm A — normal rediscovery): the worker receives only the task
  pointer and normal repository access. It must rediscover the task genealogy,
  stop conditions and resume facts from canonical files, recording every read
  and directory listing as a trace entry.
- ``answer`` (Arm B — bootstrap): the worker receives the same task pointer plus
  the generated ``ARENA_CONTEXT.json`` packet and answers from the packet alone
  (exactly one file read). It fail-closed refuses packets that lack the authority
  disclaimer, stop rules, deep-change gate, or that claim a GLOBAL lesson scope.

Both arms emit the same answer schema so the proof can compare them. The worker
uses its own independent parsers (stdlib only); it does not import the builder.
It performs no writes anywhere.

Usage (normally driven by ``exp29_proof.py``):
    python3 -I fresh_session.py rediscover --root R --experiment EXP-27 --checkpoint CP-05 --out O
    python3 -I fresh_session.py answer --packet P --out O
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

AUTHORITY = "DERIVED_VIEW_NON_AUTHORITATIVE"
LESSON_SCOPES = ("GLOBAL", "PROJECT", "TASK", "NO_CHANGE")

# Questions answered by both arms, in dependency order. The genealogy block
# (first five) defines the "first useful task action".
QUESTIONS = (
    "q_project",
    "q_parent_goal",
    "q_experiment_path",
    "q_checkpoints",
    "q_disposition",
    "q_stop_rules",
    "q_result_status",
    "q_next_action",
    "q_reusable_component",
    "q_known_trap",
    "q_next_authorized_action",
)
GENEALOGY_BLOCK = frozenset(QUESTIONS[:6])

CHECKPOINT_RE = re.compile(r"^#{2,3}\s+(CP-\d+)\b", flags=re.M)


class Tracer:
    """Records every read/list operation; the trace is the measurement."""

    def __init__(self):
        self.entries = []

    def _record(self, op, path, ok, size):
        self.entries.append({"op": op, "path": str(path), "ok": ok, "bytes": size})

    def read(self, path):
        path = Path(path)
        try:
            data = path.read_text(encoding="utf-8")
        except OSError:
            self._record("read", path, False, 0)
            raise
        self._record("read", path, True, len(data.encode("utf-8")))
        return data

    def listdir(self, path):
        path = Path(path)
        try:
            names = sorted(p.name for p in path.iterdir())
        except OSError:
            self._record("listdir", path, False, 0)
            raise
        self._record("listdir", path, True, 0)
        return names

    def totals(self):
        reads = [e for e in self.entries if e["op"] == "read" and e["ok"]]
        return {
            "files_read": len(reads),
            "bytes_read": sum(e["bytes"] for e in reads),
            "read_ops": len([e for e in self.entries if e["op"] == "read"]),
            "listdir_ops": len([e for e in self.entries if e["op"] == "listdir"]),
            "tool_ops": len(self.entries),
            "failed_ops": len([e for e in self.entries if not e["ok"]]),
        }

    def totals_at(self, count):
        sub = Tracer()
        sub.entries = self.entries[:count]
        return sub.totals()


# --- independent parsers (deliberately separate from the builder's) -----------

def _section(text, title_regex):
    lines = text.splitlines()
    start = None
    for index, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith("#") and re.match(title_regex, stripped):
            start = index
            break
    if start is None:
        return []
    out = []
    for line in lines[start + 1:]:
        if line.startswith("## "):
            break
        out.append(line)
    return out


def _bullets(section):
    return [line.strip()[2:].strip() for line in section if line.strip().startswith("- ")]


def _entry(registry, experiment_id):
    return next(e for e in registry["experiments"] if e["experiment_id"] == experiment_id)


def _answers_from_sources(tracer, root, experiment_id):
    """Arm A: rediscover every answer from canonical files, tracing the cost."""
    answers = {}
    cumulative = {}

    def snapshot():
        return tracer.totals()

    # 1. A careful fresh executor checks project status first (CONTEXT_MAP).
    tracer.read(root / "STATUS.md")

    # 2-3. Discover the experiment directory by listing, not by knowing the path.
    experiments = tracer.listdir(root / "experiments")
    prefix = experiment_id.lower()
    matches = [name for name in experiments if name.lower().startswith(prefix)]
    experiment_dir = root / "experiments" / matches[0]
    tracer.listdir(experiment_dir)

    # 4. README first (natural first stop for a task pointer).
    readme_text = tracer.read(experiment_dir / "README.md")

    # 5. Registry for identity, goal, status and next action.
    registry_text = tracer.read(root / "experiments" / "EXPERIMENT_REGISTRY.json")
    registry = json.loads(registry_text)
    entry = _entry(registry, experiment_id)

    # 6. ARENA_TASK for checkpoints and disposition.
    task_text = tracer.read(experiment_dir / "ARENA_TASK.md")

    # 7. RESULTS for reusable components, traps and the next authorized action.
    results_text = tracer.read(experiment_dir / "RESULTS.md")

    answers["q_project"] = entry["owning_project"]
    answers["q_parent_goal"] = entry["why"]
    answers["q_experiment_path"] = entry["experiment_path"]
    checkpoints, seen = [], set()
    for match in CHECKPOINT_RE.finditer(task_text):
        if match.group(1) not in seen:
            seen.add(match.group(1))
            checkpoints.append(match.group(1))
    answers["q_checkpoints"] = checkpoints
    disposition = ""
    for line in task_text.splitlines():
        if line.startswith("Decision:"):
            disposition = line.split("**")[1] if "**" in line else line.split(":", 1)[1].strip()
            break
    answers["q_disposition"] = disposition
    stop_rules = _bullets(_section(readme_text, r"^##\s+(Stop conditions|Scope stop rules)\s*$"))
    if not stop_rules:
        stop_rules = _bullets(_section(task_text, r"^##\s+(Stop conditions|Scope stop rules)\s*$"))
    answers["q_stop_rules"] = stop_rules
    answers["q_result_status"] = entry["status"]
    answers["q_next_action"] = entry["next_action"]

    component_rows = []
    for line in _section(results_text, r"^##\s+Per-pattern disposition\s*$"):
        stripped = line.strip()
        if not stripped.startswith("|"):
            continue
        cells = [cell.strip() for cell in stripped.strip("|").split("|")]
        if len(cells) >= 4 and cells[1] != "Pattern" and not set(cells[0]) <= {"-", " "}:
            component_rows.append(cells)
    first = component_rows[0]
    answers["q_reusable_component"] = f"{first[1]} — {first[3]}"
    traps = _bullets(_section(results_text, r"^##\s+Known limitations / blockers\s*$"))
    answers["q_known_trap"] = traps[0] if traps else ""
    next_action_lines = [line.strip() for line in _section(results_text, r"^##\s+Next authorized action\s*$") if line.strip()]
    answers["q_next_authorized_action"] = next_action_lines[0] if next_action_lines else ""

    # cumulative cost at the moment the genealogy block became answerable
    # (after the ARENA_TASK read, which is entry index 5: STATUS, 2x listdir,
    # README, registry, ARENA_TASK).
    cumulative["at_genealogy_complete"] = tracer.totals_at(6)
    cumulative["at_all_answers"] = snapshot()
    return answers, cumulative


def _packet_selfcheck(packet):
    """Fail-closed: refuse packets that are missing safety structure."""
    problems = []
    if packet.get("authority") != AUTHORITY:
        problems.append("missing_authority_disclaimer")
    if not (packet.get("rules", {}).get("stop_rules")):
        problems.append("missing_stop_rules")
    if not (packet.get("rules", {}).get("deep_change_gate", {}).get("bullets")):
        problems.append("missing_deep_change_gate")
    declared = {item.get("value") for item in packet.get("now", {}).get("disposition_sources", [])}
    if len(declared) > 1:
        problems.append("ambiguous_disposition")
    for lesson in packet.get("known_lessons", []):
        if lesson.get("scope") not in LESSON_SCOPES:
            problems.append(f"invalid_lesson_scope:{lesson.get('id')}")
        elif lesson.get("scope") == "GLOBAL":
            # A fresh session never accepts GLOBAL promotion without the canonical
            # marker; the builder's verify is the only place that can check it.
            problems.append(f"lesson_promoted_to_global:{lesson.get('id')}")
    return problems


def _answers_from_packet(packet):
    """Arm B: answer from the packet alone."""
    now, rules, resume = packet["now"], packet["rules"], packet["resume"]
    first_component = packet["reusable_components"][0]
    first_trap = packet["known_traps"][0]
    return {
        "q_project": now["project"],
        "q_parent_goal": now["parent_goal"],
        "q_experiment_path": now["experiment_path"],
        "q_checkpoints": now["checkpoints"],
        "q_disposition": now["disposition"],
        "q_stop_rules": rules["stop_rules"],
        "q_result_status": resume["status"],
        "q_next_action": resume["next_action"],
        "q_reusable_component": f"{first_component['pattern']} — {first_component['disposition']}",
        "q_known_trap": first_trap["trap"],
        "q_next_authorized_action": resume["next_authorized_action"],
    }


def _write_json(path, data):
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(data, ensure_ascii=False, sort_keys=True, indent=1) + "\n",
                      encoding="utf-8")


def main(argv=None):
    parser = argparse.ArgumentParser(description="EXP-29 isolated fresh-session worker")
    sub = parser.add_subparsers(dest="command", required=True)
    rediscover = sub.add_parser("rediscover", help="Arm A: normal rediscovery from canonical files")
    rediscover.add_argument("--root", required=True)
    rediscover.add_argument("--experiment", required=True)
    rediscover.add_argument("--checkpoint")
    rediscover.add_argument("--out", required=True)
    answer = sub.add_parser("answer", help="Arm B: answer from the bootstrap packet")
    answer.add_argument("--packet", required=True)
    answer.add_argument("--out", required=True)
    args = parser.parse_args(argv)

    if args.command == "rediscover":
        root = Path(args.root).resolve()
        tracer = Tracer()
        answers, cumulative = _answers_from_sources(tracer, root, args.experiment)
        result = {
            "arm": "A_rediscovery",
            "experiment": args.experiment,
            "checkpoint": args.checkpoint or "",
            "packet_used": False,
            "read_from_chat": False,
            "answers": answers,
            "trace": tracer.entries,
            "totals": tracer.totals(),
            "cost": cumulative,
        }
    else:
        packet_path = Path(args.packet).resolve()
        tracer = Tracer()
        packet_text = tracer.read(packet_path)
        packet = json.loads(packet_text)
        problems = _packet_selfcheck(packet)
        if problems:
            result = {
                "arm": "B_bootstrap",
                "packet": str(packet_path),
                "packet_used": True,
                "read_from_chat": False,
                "refused": True,
                "refusal_reasons": problems,
                "answers": {},
                "trace": tracer.entries,
                "totals": tracer.totals(),
            }
        else:
            result = {
                "arm": "B_bootstrap",
                "packet": str(packet_path),
                "packet_used": True,
                "read_from_chat": False,
                "refused": False,
                "answers": _answers_from_packet(packet),
                "trace": tracer.entries,
                "totals": tracer.totals(),
                "cost": {
                    "at_genealogy_complete": tracer.totals_at(1),
                    "at_all_answers": tracer.totals(),
                },
            }
    _write_json(args.out, result)
    print(json.dumps({k: result[k] for k in ("arm", "refused") if k in result}, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
