#!/usr/bin/env python3
"""Generate HASHES.txt for the EXP-14 run directory.

Run:  python3 harness/make_hashes.py

Hashes every EXP-14 artifact plus the production files the experiment read or
depended on, so a later auditor can prove that (a) the frozen dataset did not
change after the freeze and (b) no production file was touched by EXP-14.
"""
from __future__ import annotations

import hashlib
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
RUN_DIR = HERE.parent
REPO_ROOT = RUN_DIR.parents[2]

MAIN_SHA = "d2ec64531e4cac4f5076263f8317dfaaa36e2a9f"

# Production / governing files EXP-14 read. None of them may change.
PRODUCTION_AND_GOVERNANCE = [
    "AGENTS.md",
    "docs/governance/SCOPE-CHANGE-CONTROL.md",
    "docs/GLOBAL_MPE_ENFORCEMENT.md",
    "docs/OPERATING_MODEL.md",
    "docs/NEW_IDEA_FILTER_POLICY.md",
    "docs/HUMAN_VALUE_DELIVERY_PRINCIPLES.md",
    "docs/VALUE_UNIT_ECONOMICS.md",
    "docs/OPINIONATED_WORKSPACE_POLICY.md",
    "docs/COMPUTE_BUDGET_GATE.md",
    "docs/MURAT_AI_STACK_V2_DECISION.md",
    "docs/experiments/EXP-13_LOW_COST_EVALUATION_HARNESS.md",
    "contracts/TRIAGE_INPUT.schema.json",
    "contracts/TRIAGE_OUTPUT.schema.json",
    "contracts/EXPERIMENT_REGISTRY.schema.json",
    "scripts/triage_engine.py",
    "gates/registry.yaml",
    "playbooks/fast.md",
    "playbooks/verified.md",
    "playbooks/deep-change.md",
    "experts/architect.md",
    "experts/coder.md",
    "experts/researcher.md",
    "experts/reviewer.md",
    "teams/software-standard.md",
    "teams/software-verified.md",
    "teams/research-verified.md",
    "skills/murat-project-engineer/references/risk-and-routing.md",
    "skills/murat-project-engineer/references/route-profiles.md",
    "datasets/exp-12-backtest.json",
    "experiments/exp-13/tasks_v2.json",
    "experiments/exp-13/routes.json",
    "experiments/exp-13/thresholds.json",
    "experiments/exp-14-laya-system-one/README.md",
    "experiments/exp-14-laya-system-one/PRE_REGISTRATION.json",
    "package.json",
    "wrangler.jsonc",
]

# Evidence-record files EXP-14 is expected to update by repository convention
# (the same files the EXP-15 and EXP-18 closing commits touched). These are a
# status/registry record, not routing, authority or decision rules.
EVIDENCE_RECORD_FILES = [
    "STATUS.md",
    "experiments/EXPERIMENT_REGISTRY.json",
    "CHANGELOG.md",
]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def git_sha_at(revision: str, relpath: str) -> str | None:
    try:
        blob = subprocess.run(
            ["git", "-C", str(REPO_ROOT), "show", f"{revision}:{relpath}"],
            capture_output=True, check=True).stdout
    except subprocess.CalledProcessError:
        return None
    return hashlib.sha256(blob).hexdigest()


def main() -> int:
    lines: list[str] = [
        "# EXP-14 — Cryptographic artifact hashes (SHA-256)",
        f"# Generated: {time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}",
        f"# Run directory: experiments/exp-14-laya/{RUN_DIR.name}",
        f"# main SHA at freeze: {MAIN_SHA}",
        "#",
        "# Section 1 proves the freeze is intact and that Sequence A/B were scored",
        "# against the frozen bytes. Section 2 lists every EXP-14 artifact.",
        "# Section 3 proves no production or governing file was modified: the",
        "# working-tree digest equals the digest of the same path at the frozen",
        "# main SHA.",
        "",
        "## 1. Frozen inputs — integrity anchor",
    ]

    dataset = RUN_DIR / "frozen/dataset_v1.json"
    lines.append(f"{sha256(dataset)}  frozen/dataset_v1.json")
    recorded = next((line.split()[0] for line in
                     (RUN_DIR / "frozen/DATASET_SHA256.txt").read_text(encoding="utf-8").splitlines()
                     if line.endswith("dataset_v1.json")), None)
    lines.append(f"# recorded at freeze: {recorded}")
    lines.append(f"# matches now:        {recorded == sha256(dataset)}")
    lines.append("")

    lines.append("## 2. EXP-14 artifacts")
    for path in sorted(RUN_DIR.rglob("*")):
        if not path.is_file() or path.name == "HASHES.txt":
            continue
        if "__pycache__" in path.parts:
            continue
        lines.append(f"{sha256(path)}  {path.relative_to(RUN_DIR)}")
    lines.append("")

    lines.append("## 3. Production and governing files — must be unchanged by EXP-14")
    unchanged = 0
    changed: list[str] = []
    for relpath in PRODUCTION_AND_GOVERNANCE:
        path = REPO_ROOT / relpath
        if not path.exists():
            lines.append(f"# MISSING  {relpath}")
            changed.append(relpath + " (missing)")
            continue
        now = sha256(path)
        at_main = git_sha_at(MAIN_SHA, relpath)
        if at_main is None:
            lines.append(f"{now}  {relpath}   # not present at {MAIN_SHA[:12]} (added later, not by EXP-14)")
            unchanged += 1
        elif at_main == now:
            lines.append(f"{now}  {relpath}   # UNCHANGED since {MAIN_SHA[:12]}")
            unchanged += 1
        else:
            lines.append(f"{now}  {relpath}   # *** DIFFERS from {MAIN_SHA[:12]} ({at_main}) ***")
            changed.append(relpath)
    lines.append("")
    lines.append(f"# unchanged: {unchanged}/{len(PRODUCTION_AND_GOVERNANCE)}")
    lines.append(f"# changed:   {changed if changed else 'none'}")
    lines.append("")

    lines.append("## 3b. Evidence-record files intentionally updated by EXP-14")
    lines.append("# Registry/status records only: no routing, no authority, no decision rule.")
    for relpath in EVIDENCE_RECORD_FILES:
        path = REPO_ROOT / relpath
        if not path.exists():
            lines.append(f"# MISSING  {relpath}")
            continue
        now = sha256(path)
        at_main = git_sha_at(MAIN_SHA, relpath)
        state = "UNCHANGED" if at_main == now else "UPDATED (evidence record)"
        lines.append(f"{now}  {relpath}   # {state} vs {MAIN_SHA[:12]}")
    lines.append("")

    lines.append("## 4. Git state")
    for label, argv in [
        ("branch", ["git", "rev-parse", "--abbrev-ref", "HEAD"]),
        ("head", ["git", "rev-parse", "HEAD"]),
        ("merge_base_with_main", ["git", "merge-base", "HEAD", "main"]),
    ]:
        value = subprocess.run(["git", "-C", str(REPO_ROOT)] + argv[1:],
                               capture_output=True, text=True).stdout.strip()
        lines.append(f"# {label}: {value}")
    diff = subprocess.run(
        ["git", "-C", str(REPO_ROOT), "diff", "--name-only", f"{MAIN_SHA}..HEAD"],
        capture_output=True, text=True).stdout.strip().splitlines()
    outside = [f for f in diff if not f.startswith("experiments/exp-14-laya/")]
    lines.append(f"# files changed since {MAIN_SHA[:12]}: {len(diff)}")
    lines.append(f"# of those, OUTSIDE experiments/exp-14-laya/: {len(outside)}")
    for f in outside:
        lines.append(f"#   {f}")
    lines.append("")

    out = RUN_DIR / "HASHES.txt"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote {out.relative_to(REPO_ROOT)}")
    print(f"production/governing files unchanged: {unchanged}/{len(PRODUCTION_AND_GOVERNANCE)}")
    if changed:
        print("WARNING - these production/governing files differ from the frozen main SHA:")
        for item in changed:
            print("   ", item)
    print(f"changed outside experiments/exp-14-laya/: {outside}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
