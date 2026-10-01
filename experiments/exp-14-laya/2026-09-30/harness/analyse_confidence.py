"""EXP-14 — evaluation-stage analysis of the arm-B confidence signal.

Run:  python3 harness/analyse_confidence.py

This is EVALUATION, not calibration. It adopts no threshold, changes no decision
and re-scores nothing. Its only purpose is to answer, with evidence, the two
questions `CONTRACT.md` section 9 requires before stage C or stage D may be
considered:

  1. Is there a decision boundary worth improving? i.e. does the model's own
     confidence/act signal separate correct from incorrect answers well enough
     that a threshold could buy coverage without masking a safety failure?
  2. Is there real potential value that would justify fine-tuning?

Method:
  - per field, compare the SDK's `confidence` (normalized entropy for `choice`,
    max(p) for `noul`) and `answer_confidence` (the calibrated max(p)) between
    correct and incorrect predictions;
  - compute a threshold-free separation measure (Mann-Whitney AUC) so the answer
    does not depend on a chosen cut;
  - compute the majority-class and random baselines for `risk_tier` on THIS
    frozen dataset, so Laya's zero-shot accuracy can be read against chance;
  - compute, for every possible confidence cut, the best routine coverage that a
    "trust System One only above the cut, otherwise escalate" policy could reach
    on this frozen set — an oracle-of-the-threshold upper bound. It is an
    upper bound computed on the evaluation set itself, so it is optimistic by
    construction and is reported as such.
"""

from __future__ import annotations

import argparse
import itertools
import json
import sys
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
RUN_DIR = HERE.parent
sys.path.insert(0, str(HERE))

from exp14_common import DECISION_FIELDS, RISK_TIERS  # noqa: E402


def auc(scores_correct: list[float], scores_incorrect: list[float]) -> float | None:
    """Mann-Whitney U / (n1*n2): P(correct score > incorrect score), ties at 0.5."""
    if not scores_correct or not scores_incorrect:
        return None
    wins = 0.0
    for a, b in itertools.product(scores_correct, scores_incorrect):
        wins += 1.0 if a > b else 0.5 if a == b else 0.0
    return round(wins / (len(scores_correct) * len(scores_incorrect)), 4)


def analyse(metrics: dict[str, Any], dataset: dict[str, Any]) -> dict[str, Any]:
    by_id = {case["case_id"]: case for case in dataset["cases"]}
    raw_by_id = {case["case_id"]: case for case in metrics["cases"]}

    per_field: dict[str, Any] = {}
    for field in DECISION_FIELDS:
        correct_conf, incorrect_conf = [], []
        correct_ans, incorrect_ans = [], []
        correct_act, incorrect_act = [], []
        for case_id, scored in raw_by_id.items():
            telemetry = (scored.get("telemetry") or {}).get(field)
            if not telemetry:
                # the metrics file does not carry telemetry; fall back to the raw pass file
                continue
            hit = scored["field_match"][field]
            for key, bucket_c, bucket_i in (
                ("confidence", correct_conf, incorrect_conf),
                ("answer_confidence", correct_ans, incorrect_ans),
                ("act_probability", correct_act, incorrect_act),
            ):
                value = telemetry.get(key)
                if isinstance(value, (int, float)):
                    (bucket_c if hit else bucket_i).append(float(value))
        per_field[field] = {
            "n_correct": len(correct_conf),
            "n_incorrect": len(incorrect_conf),
            "confidence_mean_correct": round(sum(correct_conf) / len(correct_conf), 4) if correct_conf else None,
            "confidence_mean_incorrect": round(sum(incorrect_conf) / len(incorrect_conf), 4) if incorrect_conf else None,
            "answer_confidence_mean_correct": round(sum(correct_ans) / len(correct_ans), 4) if correct_ans else None,
            "answer_confidence_mean_incorrect": round(sum(incorrect_ans) / len(incorrect_ans), 4) if incorrect_ans else None,
            "auc_confidence": auc(correct_conf, incorrect_conf),
            "auc_answer_confidence": auc(correct_ans, incorrect_ans),
            "auc_act_probability": auc(correct_act, incorrect_act),
        }

    # ---- risk_tier against chance on THIS frozen dataset
    tiers = [by_id[c["case_id"]]["oracle_risk_tier"] for c in metrics["cases"]]
    counts = {tier: tiers.count(tier) for tier in RISK_TIERS}
    majority = max(counts.values()) / len(tiers)
    predicted = [c["scored_decision"]["risk_tier"] for c in metrics["cases"]]
    pred_counts = {tier: predicted.count(tier) for tier in RISK_TIERS}
    observed_accuracy = sum(1 for o, p in zip(tiers, predicted) if o == p) / len(tiers)
    chance = {
        "n": len(tiers),
        "oracle_distribution": counts,
        "laya_distribution": pred_counts,
        "majority_class_baseline": round(majority, 4),
        "random_uniform_baseline": round(1 / len(RISK_TIERS), 4),
        "laya_zero_shot_risk_tier_accuracy": round(observed_accuracy, 4),
        "beats_majority_class": observed_accuracy > majority,
        "beats_random_uniform": observed_accuracy > 1 / len(RISK_TIERS),
    }

    # ---- upper bound: best routine coverage achievable by ANY confidence cut
    # Policy shape: trust System One's FAST answer only when its risk_tier
    # confidence >= cut; otherwise escalate. Routine coverage counts routine
    # cases whose full four-field decision is exactly right AND trusted.
    routine = [c for c in metrics["cases"] if not by_id[c["case_id"]]["protected_decision"]]
    rows = []
    confidences = sorted({
        float(((c.get("telemetry") or {}).get("risk_tier") or {}).get("confidence") or 0.0)
        for c in metrics["cases"]})
    for cut in [0.0] + confidences:
        trusted_exact = 0
        for case in routine:
            telemetry = (case.get("telemetry") or {}).get("risk_tier") or {}
            confidence = float(telemetry.get("confidence") or 0.0)
            if confidence >= cut and case["exact_case_match"]:
                trusted_exact += 1
        # unsafe cost of the same cut: protected cases answered FAST without escalation
        unsafe = 0
        for case in metrics["cases"]:
            if not by_id[case["case_id"]]["protected_decision"]:
                continue
            telemetry = (case.get("telemetry") or {}).get("risk_tier") or {}
            confidence = float(telemetry.get("confidence") or 0.0)
            scored = case["scored_decision"]
            if confidence >= cut and scored["risk_tier"] == "FAST" and not scored["escalate_to_system_two"]:
                unsafe += 1
        rows.append({"confidence_cut": round(cut, 4), "routine_trusted_exact": trusted_exact,
                     "routine_coverage_upper_bound": round(trusted_exact / len(routine), 4) if routine else None,
                     "protected_false_negatives_at_cut": unsafe})
    best = max(rows, key=lambda row: (row["routine_trusted_exact"], -row["confidence_cut"])) if rows else None

    # ---- high-confidence wrong answers, and confidence at the safety failures
    high_confidence_wrong: dict[str, Any] = {}
    for field in DECISION_FIELDS:
        rows = []
        for case in metrics["cases"]:
            telemetry = (case.get("telemetry") or {}).get(field) or {}
            answer_confidence = telemetry.get("answer_confidence")
            if not isinstance(answer_confidence, (int, float)):
                continue
            rows.append({
                "case_id": case["case_id"],
                "answer_confidence": float(answer_confidence),
                "correct": bool(case["field_match"][field]),
                "oracle": case["oracle"][field],
                "predicted": case["scored_decision"][field],
            })
        wrong = [r for r in rows if not r["correct"]]
        high_confidence_wrong[field] = {
            "n": len(rows),
            "wrong": len(wrong),
            "wrong_with_answer_confidence_ge_0.90": sum(1 for r in wrong if r["answer_confidence"] >= 0.90),
            "wrong_with_answer_confidence_ge_0.80": sum(1 for r in wrong if r["answer_confidence"] >= 0.80),
            "wrong_with_answer_confidence_ge_0.70": sum(1 for r in wrong if r["answer_confidence"] >= 0.70),
            "max_answer_confidence_among_wrong": round(max((r["answer_confidence"] for r in wrong), default=0.0), 4),
            "examples": sorted(wrong, key=lambda r: -r["answer_confidence"])[:5],
        }

    protected_failure_confidence = []
    unsafe_fast_confidence = []
    for case in metrics["cases"]:
        telemetry = case.get("telemetry") or {}
        flat = {field: (telemetry.get(field) or {}).get("answer_confidence") for field in DECISION_FIELDS}
        if case["blocking_safety_failures"]:
            protected_failure_confidence.append({
                "case_id": case["case_id"],
                "blocking_safety_failures": case["blocking_safety_failures"],
                "materially_dangerous": by_id[case["case_id"]]["materially_dangerous"],
                "answer_confidence": flat,
                "mean_answer_confidence": round(
                    sum(v for v in flat.values() if isinstance(v, float)) / max(1, len(flat)), 4),
            })
        if case["scored_decision"]["risk_tier"] == "FAST" and by_id[case["case_id"]]["protected_decision"]:
            unsafe_fast_confidence.append({"case_id": case["case_id"], "answer_confidence": flat})

    return {
        "note": ("evaluation-stage analysis; no threshold adopted, no decision changed, nothing re-scored. "
                 "The coverage upper bound is computed on the evaluation set itself and is therefore "
                 "optimistic by construction."),
        "per_field_confidence_separation": per_field,
        "risk_tier_vs_chance": chance,
        "high_confidence_wrong_answers": high_confidence_wrong,
        "confidence_at_protected_failures": protected_failure_confidence,
        "confidence_at_unsafe_fast_decisions": unsafe_fast_confidence,
        "confidence_threshold_upper_bound": {
            "routine_cases": len(routine),
            "best_cut": best,
            "cuts_evaluated": len(rows),
            "interpretation": ("if no cut reaches a meaningful routine coverage, thresholding cannot create the "
                               "coverage EXP-14 criterion 3 requires, and stage C has nothing to improve"),
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="EXP-14 confidence-signal analysis")
    parser.add_argument("--metrics", type=Path, default=RUN_DIR / "raw/metrics_B_laya_zero_shot_root_pass1.json")
    parser.add_argument("--raw", type=Path, default=RUN_DIR / "raw/laya_B_laya_zero_shot_root_pass1.json")
    parser.add_argument("--dataset", type=Path, default=RUN_DIR / "frozen/dataset_v1.json")
    parser.add_argument("--out", type=Path, default=RUN_DIR / "raw/analysis_confidence_signal.json")
    args = parser.parse_args()

    metrics = json.loads(args.metrics.read_text(encoding="utf-8"))
    raw = json.loads(args.raw.read_text(encoding="utf-8"))
    dataset = json.loads(args.dataset.read_text(encoding="utf-8"))

    # metrics files do not carry the model telemetry; attach it from the raw pass file
    telemetry_by_id = {result["case_id"]: result.get("telemetry") for result in raw["results"]}
    for case in metrics["cases"]:
        case["telemetry"] = telemetry_by_id.get(case["case_id"])

    report = analyse(metrics, dataset)
    report["inputs"] = {
        "metrics_file": args.metrics.name,
        "raw_file": args.raw.name,
        "dataset_id": dataset["dataset_id"],
    }
    args.out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(json.dumps(report["risk_tier_vs_chance"], indent=1))
    print()
    for field, value in report["per_field_confidence_separation"].items():
        print(f"{field:<24} auc(conf)={value['auc_confidence']} auc(ans_conf)={value['auc_answer_confidence']} "
              f"auc(act)={value['auc_act_probability']} mean_conf correct={value['confidence_mean_correct']} "
              f"incorrect={value['confidence_mean_incorrect']}")
    print()
    print("best threshold cut:", json.dumps(report["confidence_threshold_upper_bound"]["best_cut"]))
    print()
    for field, value in report["high_confidence_wrong_answers"].items():
        print(f"{field:<24} wrong={value['wrong']}/{value['n']} "
              f"wrong@>=0.90={value['wrong_with_answer_confidence_ge_0.90']} "
              f"wrong@>=0.80={value['wrong_with_answer_confidence_ge_0.80']} "
              f"wrong@>=0.70={value['wrong_with_answer_confidence_ge_0.70']} "
              f"max_conf_among_wrong={value['max_answer_confidence_among_wrong']}")
    print()
    print("protected failures:", len(report["confidence_at_protected_failures"]))
    for row in report["confidence_at_protected_failures"]:
        print("  ", row["case_id"], row["blocking_safety_failures"], "mean_answer_confidence",
              row["mean_answer_confidence"], "dangerous", row["materially_dangerous"])
    print("unsafe FAST decisions:", len(report["confidence_at_unsafe_fast_decisions"]))
    print(f"wrote {args.out.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
