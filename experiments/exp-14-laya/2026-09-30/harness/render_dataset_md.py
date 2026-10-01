"""Generate DATASET.md from the frozen dataset (no hand transcription)."""
from __future__ import annotations

import json
from pathlib import Path

RUN_DIR = Path(__file__).resolve().parent.parent
DATASET = json.loads((RUN_DIR / "frozen/dataset_v1.json").read_text(encoding="utf-8"))
DIGEST = (RUN_DIR / "frozen/DATASET_SHA256.txt").read_text(encoding="utf-8").strip().splitlines()

CASES = DATASET["cases"]
COMP = DATASET["composition"]

PROSE = f"""# EXP-14 — Frozen dataset (`{DATASET['dataset_id']}`)

Status: **FROZEN** — immutable for the rest of this experiment
Frozen at: `{DATASET['frozen_at_utc']}`
`main` SHA at freeze: `{DATASET['main_sha_at_freeze']}`
Builder: `harness/build_dataset.py` (deterministic; re-running reproduces the
exact bytes and therefore the exact digest)

```text
{chr(10).join(DIGEST)}
```

Any change to `frozen/dataset_v1.json` after this point invalidates the run.
`harness/run_laya.py` and `harness/evaluate.py` both re-verify this digest and
abort if it no longer matches; `raw/baseline_reproducibility.json` records the
digest the Sequence A evidence was produced against.

---

## 1. Composition

| Property | Value |
|---|---|
| cases | **{COMP['cases']}** (contract minimum: 30) |
| risk tiers | FAST {COMP['by_risk_tier']['FAST']} · VERIFIED {COMP['by_risk_tier']['VERIFIED']} · DEEP-CHANGE {COMP['by_risk_tier']['DEEP-CHANGE']} |
| route profiles | default {COMP['by_route_profile']['default']} · cheap-research {COMP['by_route_profile']['cheap-research']} · coding {COMP['by_route_profile']['coding']} · strong-review {COMP['by_route_profile']['strong-review']} |
| protected decisions | **{COMP['protected_cases']}** |
| materially dangerous if answered FAST | **{COMP['materially_dangerous_cases']}** (contract minimum: 5) |
| ambiguous / under-determined | **{COMP['ambiguous_cases']}** |
| oracle `escalate_to_system_two` true / false | {COMP['oracle_escalate_true']} / {COMP['oracle_escalate_false']} |
| cases whose `risk_tier` + `requires_human_gate` reproduce a label already frozen in the repository | **{COMP['provenance_cases_with_pre_existing_label']}** |

Every contract requirement is met: ≥30 labelled cases, several risk tiers,
ordinary FAST cases, VERIFIED cases, DEEP-CHANGE/escalation cases, ambiguous
cases, and ≥5 cases where a wrong FAST answer is materially dangerous.

## 2. Case input schema

Each `input` is the production `contracts/TRIAGE_INPUT.schema.json` object,
validated by `scripts/triage_engine.validate_task` (imported, never modified),
plus one EXP-14-local field:

| Field | Type | Source |
|---|---|---|
| `task_id`, `summary`, `affected_repositories`, `acceptance_criteria_present`, `rollback_known`, `ratings{{complexity,risk,architectural_impact,data_sensitivity,unknowns}}`, `signals` | per contract | `contracts/TRIAGE_INPUT.schema.json` |
| `work_kind` | `coordination` \\| `research` \\| `implementation` \\| `review` | **EXP-14 input extension** |

`work_kind` names the dominant work type of the case so that `route_profile` is
reproducible. It is deliberately orthogonal to `risk_tier` — a FAST case can be
`implementation`, a DEEP-CHANGE case can be `review`. It is handed **identically
to both arms**, it is not a new decision category, and it is not added to any
production contract or schema. Without it `route_profile` has no deterministic
input at all: `route-profiles.md` states that "definitions reference profiles,
while the coordinator resolves profiles at run time", and the repository contains
no machine-readable rule that distinguishes research from implementation work.

Two labeler annotations are recorded per case and are **oracle-side only** — they
are not part of the model input:

- `security_boundary` — the labeler's reading that the summary changes a
  credentials/security boundary (drives rule `O-T3`);
- `source_of_truth_change` — the summary destroys or rewrites frozen governance
  evidence (drives rule `O-T5`).

These exist because `risk-and-routing.md` and `playbooks/deep-change.md` key
DEEP-CHANGE on *what the request affects*, which is stated in natural language,
while `contracts/TRIAGE_INPUT.schema.json` has no field for it. Recording the
judgment explicitly makes the oracle auditable instead of implicit. Both arms see
the same `summary` text and are expected to reach the same conclusion from it.

## 3. Provenance

| Block | Cases | Source |
|---|---|---|
| P-001…P-012 | 12 | `experiments/exp-13/tasks_v2.json` (frozen EXP-13 dataset v2, labels pre-registered 2026-08-21) |
| P-013…P-025 | 13 | `datasets/exp-12-backtest.json` (retrospective labels from recorded Stage 2/2A runs and recorded MPE boundary cases) |
| N-001…N-018 | 18 | authored for EXP-14 from MPE rule text, because the two predecessor sets contain no destructive-operation, credential/security, sensitive-data-write or genuinely under-specified case |

For the 25 provenance cases the `input` object is copied **verbatim** from the
named artifact and the `risk_tier` / `requires_human_gate` labels are the labels
**already frozen in the repository before EXP-14 started**. Builder gate `G2`
requires the EXP-14 oracle rules to reproduce all {COMP['provenance_cases_with_pre_existing_label']} of
them before the dataset may be written; if any one disagreed the build aborted
and nothing was frozen. Result: **{COMP['provenance_cases_with_pre_existing_label']}/{COMP['provenance_cases_with_pre_existing_label']} reproduced**.

No label was created, edited or re-read after any model output was observed. The
builder ran to completion, wrote the digest, and Sequence A ran against that
digest before any Laya call was attempted.

## 4. Label policy (verbatim from the frozen artifact)

> {DATASET['label_policy']}

## 5. Candidate pin

```text
{json.dumps(DATASET['candidate_pin'], indent=2)}
```

The revision is the SDK's own reviewed pin (`laya/revisions.py
PINNED_REVISIONS`), read from the installed `laya==0.3.22` package rather than
guessed, so the checkpoint is supply-chain pinnable and `laya.load` can verify
digests against it.

---

## 6. Frozen case table

`P` = protected decision, `D` = materially dangerous if answered FAST,
`A` = ambiguous/under-determined. Rules are the ids defined in `ORACLE.md`.
"""


def table() -> str:
    lines = [
        "| case_id | summary | tier | gate | route | esc | flags | rules |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for case in CASES:
        flags = "".join([
            "P" if case["protected_decision"] else "·",
            "D" if case["materially_dangerous"] else "·",
            "A" if case["ambiguous"] else "·",
        ])
        rules = case["oracle_rules"]
        rule_text = "/".join([rules["risk_tier"], rules["requires_human_gate"],
                              rules["route_profile"], rules["escalate_to_system_two"]])
        summary = case["input"]["summary"].replace("|", "\\|")
        if len(summary) > 78:
            summary = summary[:75] + "…"
        lines.append(
            f"| `{case['case_id']}` | {summary} | {case['oracle_risk_tier']} | "
            f"{'Y' if case['oracle_requires_human_gate'] else 'n'} | "
            f"`{case['oracle_route_profile']}` | "
            f"{'Y' if case['oracle_escalate_to_system_two'] else 'n'} | `{flags}` | {rule_text} |")
    return "\n".join(lines)


def detail() -> str:
    out = ["", "---", "", "## 7. Per-case rationale and provenance", ""]
    for case in CASES:
        previous = case["provenance"]["pre_existing_frozen_label"]
        out.append(f"### `{case['case_id']}`")
        out.append("")
        out.append(f"- **summary** — {case['input']['summary']}")
        out.append(f"- **provenance** — `{case['provenance']['source']}`")
        if previous is not None:
            out.append(f"- **pre-existing frozen label** — `risk_tier={previous['risk_tier']}`, "
                       f"`human_approval_required={previous['human_approval_required']}` "
                       f"(reproduced by the EXP-14 oracle rules)")
        out.append(f"- **input** — repos={case['input']['affected_repositories']}, "
                   f"acceptance_criteria_present={case['input']['acceptance_criteria_present']}, "
                   f"rollback_known={case['input']['rollback_known']}, "
                   f"ratings={case['input']['ratings']}, signals={case['input']['signals']}, "
                   f"work_kind=`{case['input']['work_kind']}`")
        annotations = case["labeler_annotations"]
        active = [key for key, value in annotations.items() if value]
        if active:
            out.append(f"- **labeler annotations (oracle-side only)** — {', '.join(f'`{a}`' for a in active)}")
        out.append(f"- **oracle** — `risk_tier={case['oracle_risk_tier']}`, "
                   f"`requires_human_gate={case['oracle_requires_human_gate']}`, "
                   f"`route_profile={case['oracle_route_profile']}`, "
                   f"`escalate_to_system_two={case['oracle_escalate_to_system_two']}`")
        out.append(f"- **flags** — protected={case['protected_decision']}, "
                   f"materially_dangerous={case['materially_dangerous']}, ambiguous={case['ambiguous']}")
        out.append(f"- **rules fired** — {json.dumps(case['oracle_rules'])}")
        out.append(f"- **rationale** — {case['rationale']}")
        out.append(f"- **input sha256** — `{case['input_sha256']}`")
        out.append("")
    return "\n".join(out)


def main() -> int:
    text = PROSE + "\n" + table() + "\n" + detail()
    (RUN_DIR / "DATASET.md").write_text(text, encoding="utf-8")
    print(f"wrote DATASET.md ({len(text.splitlines())} lines, {len(CASES)} cases)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
