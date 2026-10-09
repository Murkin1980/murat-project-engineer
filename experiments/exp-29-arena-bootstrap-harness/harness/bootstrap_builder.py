#!/usr/bin/env python3
"""EXP-29 — deterministic Arena bootstrap builder (CP-02).

Derives a compact fresh-session launch packet (``ARENA_CONTEXT.json`` +
``ARENA_CONTEXT.md``) from canonical MPE Git sources only:

    canonical Git sources -> deterministic builder -> derived ARENA_CONTEXT packet

Properties (per ``ARENA_TASK.md`` CP-02):

- deterministic: identical inputs (sources + git refs) produce byte-identical
  output; no wall-clock, random, network, or LLM is used at build time;
- no persistent store, no daemon, no writes back into canonical sources — the
  only files written are the two derived artifacts named on the command line;
- every included item carries its canonical source path, and the packet records
  the SHA-256 of every source it was derived from;
- fail-closed verification: ``verify`` re-derives the packet from current
  sources and recomputes every digest. Any source change, digest mismatch,
  missing stop/deep-change rule, or invalid lesson scope makes the packet
  STALE or REJECTED and therefore a non-authoritative hint. The packet never
  overrides canonical files.

This module is experiment-scoped. It does not modify any production script,
contract, gate, governance document, or source of truth.

Usage:
    python3 experiments/exp-29-arena-bootstrap-harness/harness/bootstrap_builder.py \
        build --experiment EXP-27 --checkpoint CP-05 \
        --out-json ARENA_CONTEXT.json --out-md ARENA_CONTEXT.md
    python3 experiments/exp-29-arena-bootstrap-harness/harness/bootstrap_builder.py \
        verify --packet ARENA_CONTEXT.json
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

PACKET_VERSION = "exp-29-arena-context-v1"
AUTHORITY = "DERIVED_VIEW_NON_AUTHORITATIVE"
AUTHORITY_NOTE = (
    "Derived, non-authoritative launch brief assembled from canonical Git sources. "
    "Git remains the only source of truth: on any conflict the canonical files win; "
    "verify freshness before use and re-derive or discard this packet on any mismatch."
)
LESSON_SCOPES = ("GLOBAL", "PROJECT", "TASK", "NO_CHANGE")
GLOBAL_PROMOTION_MARKER = "PROMOTED_TO_GLOBAL"

CHECKPOINT_RE = re.compile(r"^#{2,3}\s+(CP-\d+)\b", flags=re.M)
LESSON_HEADING_RE = re.compile(r"^###\s+(R\d+)\s+—\s+(.+)$")

# Recognised boundary sections that carry task-local stop / deep-change rules. The
# titles are the headings canonical experiment files actually use (EXP-27 "Stop
# conditions"; EXP-22 "Boundaries", "Failure / stop criteria", "Guardrails").
# "Completion boundary" is deliberately excluded: it states the finish line, not a
# stop rule.
STOP_SECTION_TITLES = (
    "Stop conditions",
    "Scope stop rules",
    "Stop rules",
    "Deep-change stop conditions",
    "Failure / stop criteria",
    "Boundaries",
    "Guardrails",
)
ALLOWED_LEAD_RE = re.compile(r"^(allowed|permitted):?$", flags=re.IGNORECASE)
NOT_ALLOWED_LEAD_RE = re.compile(r"^not allowed:?$", flags=re.IGNORECASE)

# Lesson scope is this experiment's recorded, evidence-gated promotion decision
# (EXP-28 promotion rule: explicit evidence + known scope + minimal formulation +
# verification path + no governance conflict). It is NOT automatic learning: the
# lesson titles and texts are parsed from the canonical EXP-28 RESULTS.md below.
LESSON_SCOPE_DECISIONS = {
    "R1": (
        "PROJECT",
        "EXP-28 RESULTS.md R1 targets context-heavy MPE handoffs (one project line); "
        "EXP-28 records 'Two synthetic/fixed cases are too small to show generality', "
        "so R1 is not GLOBAL.",
    ),
    "R2": (
        "TASK",
        "EXP-28 RESULTS.md R2 heading records 'applied task-locally' — EXP-24 Phase 2 only.",
    ),
    "R3": (
        "NO_CHANGE",
        "EXP-28 RESULTS.md R3 heading records 'rejected' — observed, not promoted into "
        "the bootstrap.",
    ),
}

ROOT = Path(__file__).resolve().parents[3]


# --- small deterministic helpers (stdlib only; same pattern as EXP-27 run_state) ---

def sha256_file(path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def _trunc(text: str, limit: int) -> str:
    text = " ".join(str(text).split())
    return text if len(text) <= limit else text[: limit - 1].rstrip() + "…"


def _write_text(path, text: str) -> None:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(text, encoding="utf-8", newline="\n")


def _write_json(path, data: dict) -> None:
    _write_text(path, json.dumps(data, ensure_ascii=False, sort_keys=True, indent=1) + "\n")


def _git(root: Path, *args: str) -> str:
    try:
        completed = subprocess.run(
            ["git", "-C", str(root), *args], capture_output=True, text=True, timeout=15
        )
    except Exception:
        return "unknown"
    return completed.stdout.strip() if completed.returncode == 0 else "unknown"


# --- canonical-source parsers (deterministic, read-only) ----------------------

def _section(text: str, title_regex: str) -> list[str]:
    """Lines of the first ``## <title>`` section; ``###`` subsections included."""
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


def _bullets(section: list[str]) -> list[str]:
    return [line.strip()[2:].strip() for line in section if line.strip().startswith("- ")]


def _numbered(section: list[str]) -> list[str]:
    return [line.strip() for line in section if re.match(r"^\d+\.\s", line.strip())]


def _intro(section: list[str]) -> str:
    for line in section:
        if line.strip() and not line.strip().startswith("- "):
            return line.strip()
    return ""


def _parse_checkpoints(task_text: str) -> list[str]:
    seen, out = set(), []
    for match in CHECKPOINT_RE.finditer(task_text):
        if match.group(1) not in seen:
            seen.add(match.group(1))
            out.append(match.group(1))
    return out


def _parse_disposition(text: str) -> str:
    """Value of the first ``Decision:`` line in one canonical file ("" if none)."""
    for line in text.splitlines():
        if line.startswith("Decision:"):
            if "**" in line:
                return line.split("**")[1].strip()
            return line.split(":", 1)[1].strip()
    return ""


def _titled_sections(text: str, titles: tuple[str, ...]) -> list[tuple[str, list[str]]]:
    """Every ``## <title>`` section whose exact title is listed, in document order."""
    wanted = {title.lower() for title in titles}
    sections: list[tuple[str, list[str]]] = []
    current: tuple[str, list[str]] | None = None
    for line in text.splitlines():
        if line.startswith("## "):
            if current is not None:
                sections.append(current)
            title = line[3:].strip()
            current = (title, []) if title.lower() in wanted else None
        elif current is not None:
            current[1].append(line)
    if current is not None:
        sections.append(current)
    return sections


def _boundary_rules(section: list[str]) -> tuple[str, list[str]]:
    """(intro, rules) of one boundary section.

    An ``Allowed:`` list states permissions, not stop rules, so it never contributes.
    When a ``Not allowed:`` lead-in is present, only the bullets under it are rules.
    """
    for index, line in enumerate(section):
        if NOT_ALLOWED_LEAD_RE.match(line.strip()):
            rules: list[str] = []
            for follow in section[index + 1:]:
                stripped = follow.strip()
                if stripped.startswith("- "):
                    rules.append(stripped[2:].strip())
                elif stripped:
                    break
            return "Not allowed:", rules
    if any(ALLOWED_LEAD_RE.match(line.strip()) for line in section):
        return "", []
    return _intro(section), _bullets(section)


def _slug(title: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")


def _parse_stop_rules(
    task_text: str, readme_text: str
) -> tuple[list[str], str, list[tuple[str, str]]]:
    """Task-local stop/deep-change rules from every recognised boundary section.

    Union, not first-match: a boundary declared in several sections or in both files
    is never silently dropped. A section without parseable bullets contributes
    nothing, so a missing boundary still leaves the list empty (fail closed).
    Returns ``(rules, intro, [(file name, section anchor), ...])``.
    """
    rules: list[str] = []
    intros: list[str] = []
    sources: list[tuple[str, str]] = []
    for text, file_name in ((task_text, "ARENA_TASK.md"), (readme_text, "README.md")):
        for title, lines in _titled_sections(text, STOP_SECTION_TITLES):
            intro, bullets = _boundary_rules(lines)
            if not bullets:
                continue
            for rule in bullets:
                if rule not in rules:
                    rules.append(rule)
            if intro and intro not in intros:
                intros.append(intro)
            sources.append((file_name, _slug(title)))
    if rules:
        return rules, " / ".join(intros), sources
    fallback = [
        line.strip()
        for line in task_text.splitlines()
        if re.match(r"^STOP\b", line.strip())
    ]
    if fallback:
        return fallback, "", [("ARENA_TASK.md", "stop-lines")]
    return [], "", []


def _parse_lessons(results_text: str) -> list[dict]:
    section = _section(results_text, r"^##\s+Recommendations with the required evidence contract\s*$")
    lessons, current = [], None
    for line in section:
        stripped = line.strip()
        heading = LESSON_HEADING_RE.match(stripped)
        if heading:
            current = {"id": heading.group(1), "title": heading.group(2).strip(),
                       "minimal_change": "", "verification": ""}
            lessons.append(current)
            continue
        if current is None:
            continue
        if stripped.startswith("- **Minimal change:**"):
            current["minimal_change"] = stripped.split(":**", 1)[1].strip()
        elif stripped.startswith("- **Verification:**"):
            current["verification"] = stripped.split(":**", 1)[1].strip()
    return lessons


def _parse_components(results_text: str) -> list[dict]:
    section = _section(results_text, r"^##\s+Per-pattern disposition\s*$")
    rows = []
    for line in section:
        stripped = line.strip()
        if not stripped.startswith("|"):
            continue
        cells = [cell.strip() for cell in stripped.strip("|").split("|")]
        if len(cells) < 4 or cells[1] == "Pattern" or set(cells[0]) <= {"-", " "}:
            continue
        rows.append({"pattern": cells[1], "verdict": cells[2], "disposition": cells[3]})
    return rows


def _parse_traps(results_text: str) -> list[str]:
    return _bullets(_section(results_text, r"^##\s+Known limitations / blockers\s*$"))


def _parse_next_authorized_action(results_text: str) -> str:
    for line in _section(results_text, r"^##\s+Next authorized action\s*$"):
        if line.strip():
            return line.strip()
    return ""


def _parse_deep_change_gate(governance_text: str) -> dict:
    section = _section(governance_text, r"^##\s+6\.\s+Deep-change gate\s*$")
    return {"intro": _intro(section), "bullets": _bullets(section)}


def _parse_source_priority(governance_text: str) -> list[str]:
    return _numbered(_section(governance_text, r"^##\s+2\.\s+Source of truth\s*$"))


def _parse_handoff_fields(agents_text: str) -> list[str]:
    return _bullets(_section(agents_text, r"^##\s+Graceful handoff contract\s*$"))


# --- packet construction ------------------------------------------------------

def build_packet(
    root,
    experiment_id: str,
    checkpoint: str | None = None,
    *,
    git_branch: str | None = None,
    git_head: str | None = None,
    git_base: str | None = None,
) -> dict:
    """Derive the ARENA_CONTEXT packet for one experiment from canonical sources."""
    root = Path(root)
    registry_path = root / "experiments" / "EXPERIMENT_REGISTRY.json"
    registry = json.loads(registry_path.read_text(encoding="utf-8"))
    entry = next(e for e in registry["experiments"] if e["experiment_id"] == experiment_id)
    experiment_dir = root / entry["experiment_path"]

    task_path = experiment_dir / "ARENA_TASK.md"
    readme_path = experiment_dir / "README.md"
    results_path = experiment_dir / "RESULTS.md"
    status_path = root / "STATUS.md"
    agents_path = root / "AGENTS.md"
    governance_path = root / "docs" / "governance" / "SCOPE-CHANGE-CONTROL.md"
    lessons_path = root / "experiments" / "exp-28-agent-workflow-skills-retro" / "RESULTS.md"

    task_text = task_path.read_text(encoding="utf-8")
    readme_text = readme_path.read_text(encoding="utf-8") if readme_path.exists() else ""
    results_text = results_path.read_text(encoding="utf-8") if results_path.exists() else ""
    status_text = status_path.read_text(encoding="utf-8")
    agents_text = agents_path.read_text(encoding="utf-8")
    governance_text = governance_path.read_text(encoding="utf-8")
    lessons_text = lessons_path.read_text(encoding="utf-8")

    stop_rules, stop_intro, stop_sources = _parse_stop_rules(task_text, readme_text)
    stop_rules_source = " + ".join(
        f"{entry['experiment_path']}/{name}#{anchor}" for name, anchor in stop_sources
    ) or "none (no recognised boundary section)"
    # The checkpoint chain and disposition may be declared in either canonical file.
    checkpoints = _parse_checkpoints(task_text + "\n" + readme_text)
    if checkpoint is None and checkpoints:
        checkpoint = checkpoints[-1]
    disposition_sources = []
    for path, text in ((task_path, task_text), (readme_path, readme_text)):
        value = _parse_disposition(text)
        if value:
            disposition_sources.append({"path": str(path.relative_to(root)), "value": value})

    sources = [
        (registry_path, "registry"),
        (task_path, "task_instructions"),
        (readme_path, "task_readme"),
        (results_path, "experiment_results"),
        (status_path, "project_status"),
        (agents_path, "agents_rules"),
        (governance_path, "governance"),
        (lessons_path, "accepted_lessons"),
    ]
    source_refs = [
        {"path": str(path.relative_to(root)), "sha256": sha256_file(path), "role": role}
        for path, role in sources
        if path.exists()
    ]
    by_role = {ref["role"]: ref for ref in source_refs}

    lessons = []
    for parsed in _parse_lessons(lessons_text):
        scope, basis = LESSON_SCOPE_DECISIONS.get(parsed["id"], ("NO_CHANGE", "not promoted"))
        lessons.append({
            "id": parsed["id"],
            "title": parsed["title"],
            "scope": scope,
            "scope_basis": basis,
            "minimal_change": _trunc(parsed["minimal_change"], 200),
            "verification": _trunc(parsed["verification"], 200),
            "source": {"path": str(lessons_path.relative_to(root)), "anchor": parsed["id"]},
        })

    components = [
        {
            "pattern": row["pattern"],
            "verdict": row["verdict"],
            "disposition": row["disposition"],
            "source": {"path": str(results_path.relative_to(root)), "anchor": "per-pattern-disposition"},
        }
        for row in _parse_components(results_text)
    ]

    traps = [
        {
            "trap": trap,
            "source": {"path": str(results_path.relative_to(root)), "anchor": "known-limitations"},
        }
        for trap in _parse_traps(results_text)
    ]

    packet = {
        "packet_version": PACKET_VERSION,
        "authority": AUTHORITY,
        "authority_note": AUTHORITY_NOTE,
        "generated_against": {
            "git_branch": git_branch if git_branch is not None else _git(root, "rev-parse", "--abbrev-ref", "HEAD"),
            "git_head": git_head if git_head is not None else _git(root, "rev-parse", "HEAD"),
            "git_base": git_base if git_base is not None else _git_base(root),
        },
        "now": {
            "project": entry.get("owning_project", ""),
            "parent_goal": entry.get("why", ""),
            "experiment_id": entry["experiment_id"],
            "experiment_name": entry.get("name", ""),
            "experiment_path": entry["experiment_path"],
            "checkpoints": checkpoints,
            "disposition": disposition_sources[0]["value"] if disposition_sources else "",
            "disposition_sources": disposition_sources,
            "task": f"{experiment_id}/{checkpoint}" if checkpoint else experiment_id,
            "checkpoint": checkpoint or "",
            "registry_status": entry.get("status", ""),
            "registry_updated_at": entry.get("updated_at", ""),
            "nearest_action": entry.get("next_action", ""),
            "source": {"path": by_role["registry"]["path"]},
        },
        "rules": {
            "stop_rules_intro": stop_intro,
            "stop_rules": stop_rules,
            "stop_rules_source": stop_rules_source,
            "deep_change_gate": {
                **_parse_deep_change_gate(governance_text),
                "pointer": "docs/governance/SCOPE-CHANGE-CONTROL.md",
            },
            "source_of_truth_priority": _parse_source_priority(governance_text),
            "handoff_contract_fields": _parse_handoff_fields(agents_text),
            "sources": {
                "stop_rules": stop_rules_source,
                "deep_change_gate": "docs/governance/SCOPE-CHANGE-CONTROL.md",
                "source_of_truth_priority": "docs/governance/SCOPE-CHANGE-CONTROL.md",
                "handoff_contract": "AGENTS.md",
            },
        },
        "known_lessons": lessons,
        "reusable_components": components,
        "known_traps": traps,
        "resume": {
            "status": entry.get("status", ""),
            "result_summary": _trunc(entry.get("result_summary", ""), 300),
            "next_action": entry.get("next_action", ""),
            "next_authorized_action": _parse_next_authorized_action(results_text),
            "evidence": {
                "path": str(results_path.relative_to(root)) if results_path.exists() else "",
                "note": "full result record in the canonical experiment RESULTS.md",
            },
            "source": {"path": by_role["registry"]["path"]},
        },
        "source_refs": source_refs,
        "verification": {
            "command": (
                "python3 experiments/exp-29-arena-bootstrap-harness/harness/bootstrap_builder.py "
                "verify --packet <ARENA_CONTEXT.json> --root <repo-root>"
            ),
            "freshness_rule": (
                "FRESH only when every source_refs sha256 matches the current file AND the "
                "packet equals a deterministic rebuild from current sources; otherwise the "
                "packet is STALE or REJECTED and must be treated as a non-authoritative hint."
            ),
            "safety_invariants": [
                "authority disclaimer present (DERIVED_VIEW_NON_AUTHORITATIVE)",
                "at least one task stop/deep-change rule present",
                "deep-change gate bullets present",
                "lesson scopes limited to GLOBAL/PROJECT/TASK/NO_CHANGE; GLOBAL requires a "
                "PROMOTED_TO_GLOBAL marker in the canonical lesson source (no current source has one)",
            ],
        },
    }
    return packet


def _git_base(root: Path) -> str:
    for candidate in ("origin/main", "main"):
        base = _git(root, "merge-base", "HEAD", candidate)
        if base and base != "unknown":
            return base
    return "unknown"


# --- human-readable rendering -------------------------------------------------

def render_markdown(packet: dict) -> str:
    now, rules = packet["now"], packet["rules"]
    # Section labels describe the sources this packet was actually derived from
    # (by role), never a fixture's hardcoded experiment.
    by_role = {ref["role"]: ref["path"] for ref in packet["source_refs"]}
    results_source = by_role.get("experiment_results")
    lessons_source = by_role.get("accepted_lessons", "accepted lessons source")
    results_label = (
        f"from {results_source}" if results_source else "no experiment RESULTS.md present"
    )
    lines = [
        f"# ARENA_CONTEXT — derived launch brief ({packet['packet_version']})",
        "",
        f"> **{packet['authority']}**: {packet['authority_note']}",
        "",
        f"Verify freshness before use: `{packet['verification']['command']}`. "
        "Any source digest mismatch ⇒ STALE; missing stop rule or invalid lesson scope ⇒ REJECTED.",
        "",
        "## NOW",
        "",
        f"- Project: {now['project']}",
        f"- Goal: {now['parent_goal']}",
        f"- Task: {now['task']} (checkpoint {now['checkpoint'] or 'n/a'})",
        f"- Experiment: {now['experiment_id']} — {now['experiment_name']} (`{now['experiment_path']}`)",
        f"- Checkpoint chain: {' → '.join(now['checkpoints']) if now['checkpoints'] else 'n/a'}",
        f"- Disposition: {now['disposition'] or 'n/a'}",
        f"- Registry status: {now['registry_status']} (updated {now['registry_updated_at']})",
        f"- Nearest action: {now['nearest_action']}",
        "- Generated against (informational): "
        f"branch `{packet['generated_against']['git_branch']}`, "
        f"head `{packet['generated_against']['git_head']}`, "
        f"base `{packet['generated_against']['git_base']}`",
        "",
        "## RULES (mandatory)",
        "",
        f"Stop rules ({rules['stop_rules_source']}):",
    ]
    if rules["stop_rules_intro"]:
        lines.append(f"  > {rules['stop_rules_intro']}")
    lines += [f"- {rule}" for rule in rules["stop_rules"]] or ["- (none parsed)"]
    lines += [
        "",
        f"Deep-change gate ({rules['deep_change_gate']['pointer']} §6):",
    ]
    if rules["deep_change_gate"]["intro"]:
        lines.append(f"  > {rules['deep_change_gate']['intro']}")
    lines += [f"- {bullet}" for bullet in rules["deep_change_gate"]["bullets"]]
    lines += [
        "",
        "Source-of-truth priority (docs/governance/SCOPE-CHANGE-CONTROL.md §2):",
    ]
    lines += [f"{item}" for item in rules["source_of_truth_priority"]]
    lines += [
        "",
        "Graceful handoff minimum (AGENTS.md): " + ", ".join(rules["handoff_contract_fields"]),
        "",
        f"## KNOWN LESSONS (evidence-gated, from {lessons_source})",
        "",
    ]
    for lesson in packet["known_lessons"]:
        lines += [
            f"- **{lesson['id']} [{lesson['scope']}]** {lesson['title']}",
            f"  - change: {lesson['minimal_change']}",
            f"  - verify: {lesson['verification']}",
            f"  - source: `{lesson['source']['path']}#{lesson['source']['anchor']}` — {lesson['scope_basis']}",
        ]
    lines += [
        "",
        f"## REUSABLE COMPONENTS ({results_label})",
        "",
    ]
    for component in packet["reusable_components"]:
        lines.append(
            f"- {component['pattern']} — {component['verdict']} → {component['disposition']} "
            f"(`{component['source']['path']}`)"
        )
    if not packet["reusable_components"]:
        lines.append("- (none parsed)")
    lines += ["", f"## KNOWN TRAPS (verified limitations, {results_label})", ""]
    for trap in packet["known_traps"]:
        lines.append(f"- {trap['trap']} (`{trap['source']['path']}`)")
    if not packet["known_traps"]:
        lines.append("- (none parsed)")
    resume = packet["resume"]
    lines += [
        "",
        "## RESUME",
        "",
        f"- Status: {resume['status']}",
        f"- Result summary: {resume['result_summary']}",
        f"- Next action: {resume['next_action']}",
        f"- Next authorized action: {resume['next_authorized_action'] or '(none recorded)'}",
        f"- Evidence: `{resume['evidence']['path']}` ({resume['evidence']['note']})",
        "",
        "## PROVENANCE (canonical sources + digests)",
        "",
        "| Path | SHA-256 | Role |",
        "|---|---|---|",
    ]
    for ref in packet["source_refs"]:
        lines.append(f"| `{ref['path']}` | `{ref['sha256']}` | {ref['role']} |")
    lines += [
        "",
        "## FRESHNESS",
        "",
        f"- Rule: {packet['verification']['freshness_rule']}",
        f"- Safety invariants: {'; '.join(packet['verification']['safety_invariants'])}",
        "",
    ]
    return "\n".join(lines)


# --- fail-closed verification -------------------------------------------------

_MISSING = object()


def _diff(packet_value, canonical_value, path: str, diffs: list) -> None:
    if isinstance(packet_value, dict) and isinstance(canonical_value, dict):
        for key in sorted(set(packet_value) | set(canonical_value)):
            if not path and key == "generated_against":
                continue  # informational git refs are excluded from the freshness gate
            _diff(packet_value.get(key, _MISSING), canonical_value.get(key, _MISSING),
                  f"{path}.{key}" if path else key, diffs)
    elif isinstance(packet_value, list) and isinstance(canonical_value, list):
        if len(packet_value) != len(canonical_value):
            diffs.append({"field": path, "packet": f"<list of {len(packet_value)}>",
                          "canonical": f"<list of {len(canonical_value)}>"})
        else:
            for index, (left, right) in enumerate(zip(packet_value, canonical_value)):
                _diff(left, right, f"{path}[{index}]", diffs)
    elif packet_value is not _MISSING and canonical_value is not _MISSING and packet_value != canonical_value:
        diffs.append({"field": path, "packet": _trunc(packet_value, 120),
                      "canonical": _trunc(canonical_value, 120)})
    elif packet_value is _MISSING or canonical_value is _MISSING:
        diffs.append({"field": path, "packet": "<missing>" if packet_value is _MISSING else _trunc(packet_value, 120),
                      "canonical": "<missing>" if canonical_value is _MISSING else _trunc(canonical_value, 120)})


def _safety_violations(packet: dict, root: Path) -> list[str]:
    violations = []
    if packet.get("authority") != AUTHORITY or not packet.get("authority_note"):
        violations.append("missing_authority_disclaimer")
    rules = packet.get("rules", {})
    if not rules.get("stop_rules"):
        violations.append("missing_stop_rules")
    declared = {item.get("value") for item in packet.get("now", {}).get("disposition_sources", [])}
    if len(declared) > 1:
        violations.append("ambiguous_disposition")
    if not (rules.get("deep_change_gate") or {}).get("bullets"):
        violations.append("missing_deep_change_gate")
    for lesson in packet.get("known_lessons", []):
        scope = lesson.get("scope")
        if scope not in LESSON_SCOPES:
            violations.append(f"invalid_lesson_scope:{lesson.get('id')}")
        elif scope == "GLOBAL":
            source = root / str(lesson.get("source", {}).get("path", ""))
            text = source.read_text(encoding="utf-8") if source.exists() else ""
            if GLOBAL_PROMOTION_MARKER not in text:
                violations.append(
                    f"lesson_promoted_to_global_without_canonical_marker:{lesson.get('id')}"
                )
    return violations


def _digest_issues(packet: dict, root: Path) -> list[str]:
    issues = []
    for ref in packet.get("source_refs", []):
        path = root / ref["path"]
        if not path.exists():
            issues.append(f"source_missing:{ref['path']}")
        elif sha256_file(path) != ref["sha256"]:
            issues.append(f"source_digest_mismatch:{ref['path']}")
    return issues


def verify_packet(packet: dict, root) -> dict:
    """Fail-closed freshness/safety verification of a packet against canonical sources.

    Returns status FRESH (consistent with current canonical sources; still only a
    non-authoritative launch brief), STALE (a source changed, a digest mismatches,
    or the packet no longer equals a rebuild — degrade to a non-authoritative hint),
    or REJECTED (a safety invariant is violated — refuse the packet).
    """
    root = Path(root)
    safety = _safety_violations(packet, root)
    digests = _digest_issues(packet, root)
    diffs: list = []
    rebuild_error = ""
    try:
        expected = build_packet(
            root,
            packet["now"]["experiment_id"],
            packet["now"].get("checkpoint") or None,
            git_branch=packet["generated_against"]["git_branch"],
            git_head=packet["generated_against"]["git_head"],
            git_base=packet["generated_against"]["git_base"],
        )
        _diff(packet, expected, "", diffs)
        diffs = diffs[:10]
    except Exception as exc:  # fail closed on any rebuild problem
        rebuild_error = f"{type(exc).__name__}: {exc}"
        diffs = [{"field": "<rebuild>", "packet": "", "canonical": rebuild_error}]

    if safety:
        status = "REJECTED"
    elif digests or diffs:
        status = "STALE"
    else:
        status = "FRESH"

    if status == "FRESH":
        disposition = (
            "Consistent with current canonical sources. Usable as a non-authoritative "
            "launch brief; canonical Git sources remain authoritative on any conflict."
        )
    elif status == "STALE":
        disposition = (
            "Degrade to a non-authoritative hint: do not act on stale fields. Re-derive "
            "the packet from canonical sources or discard it; canonical files always win."
        )
    else:
        disposition = (
            "Refuse the packet: a safety invariant is violated (authority disclaimer, "
            "stop/deep-change rules, lesson scope, or a disposition that canonical files "
            "declare inconsistently). Re-derive from canonical sources."
        )

    return {
        "status": status,
        "consistent_with_canonical_sources": status == "FRESH",
        "disposition": disposition,
        "reasons": safety + digests + ([f"content_differs_from_rebuild:{d['field']}" for d in diffs] if diffs else []),
        "field_diffs": diffs,
        "checks": {
            "authority_disclaimer": "missing_authority_disclaimer" not in safety,
            "stop_rules_present": "missing_stop_rules" not in safety,
            "deep_change_gate_present": "missing_deep_change_gate" not in safety,
            "lesson_scopes_valid": not any(v.startswith(("invalid_lesson_scope", "lesson_promoted")) for v in safety),
            "disposition_unambiguous": "ambiguous_disposition" not in safety,
            "source_digests_match": not digests,
            "matches_rebuild": not diffs,
        },
    }


# --- CLI ----------------------------------------------------------------------

def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="EXP-29 deterministic Arena bootstrap builder")
    sub = parser.add_subparsers(dest="command", required=True)

    build = sub.add_parser("build", help="derive ARENA_CONTEXT.json/.md from canonical sources")
    build.add_argument("--experiment", required=True)
    build.add_argument("--checkpoint")
    build.add_argument("--root", default=str(ROOT))
    build.add_argument("--out-json", required=True)
    build.add_argument("--out-md", required=True)
    build.add_argument("--git-branch")
    build.add_argument("--git-head")
    build.add_argument("--git-base")

    verify = sub.add_parser("verify", help="fail-closed freshness/safety verification")
    verify.add_argument("--packet", required=True)
    verify.add_argument("--root", default=str(ROOT))
    verify.add_argument("--json", action="store_true", help="print the full result as JSON")

    args = parser.parse_args(argv)
    root = Path(args.root).resolve()

    if args.command == "build":
        packet = build_packet(
            root, args.experiment, args.checkpoint,
            git_branch=args.git_branch, git_head=args.git_head, git_base=args.git_base,
        )
        _write_json(args.out_json, packet)
        _write_text(args.out_md, render_markdown(packet))
        print(json.dumps({
            "built": packet["now"]["task"],
            "out_json": str(Path(args.out_json)),
            "out_md": str(Path(args.out_md)),
            "json_bytes": Path(args.out_json).stat().st_size,
            "md_bytes": Path(args.out_md).stat().st_size,
            "source_refs": len(packet["source_refs"]),
        }, sort_keys=True))
        return 0

    packet = json.loads(Path(args.packet).read_text(encoding="utf-8"))
    result = verify_packet(packet, root)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, sort_keys=True, indent=1))
    else:
        print(f"packet: {args.packet}")
        print(f"status: {result['status']}")
        print(f"disposition: {result['disposition']}")
        for reason in result["reasons"]:
            print(f"reason: {reason}")
    return {"FRESH": 0, "STALE": 2, "REJECTED": 3}[result["status"]]


if __name__ == "__main__":
    sys.exit(main())
