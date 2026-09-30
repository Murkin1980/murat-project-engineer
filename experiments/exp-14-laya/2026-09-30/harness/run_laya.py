"""EXP-14 Sequence B — Laya zero-shot over the frozen dataset.

Run:  python3 harness/run_laya.py --arm B_laya_zero_shot_root \
          [--checkpoint root|typed-decisions] [--passes 3] [--device cpu]

ZERO-SHOT means: the frozen case input only, plus the closed decision contract.
No dataset example, no oracle value, no label, no few-shot demonstration, no
calibration and no fine-tuning is supplied to the model. The category
*definitions* are supplied as Laya typed-question criteria because the Laya API
requires typed options (`choice` needs a `criteria` map, `noul` is a yes/no
probability); they are quoted from the repository's own rule documents so the
model sees the same rule text a coordinator uses.

All four fields are answered in ONE forward pass, which is the candidate's
claimed operating mode (non-autoregressive System 1). Nothing here repairs a bad
answer: an out-of-vocabulary, missing or failed output is recorded verbatim,
flagged `invalid_output`, and replaced by SAFE_ESCALATION_DECISION exactly as
the frozen contract requires.

Cost: Laya is open-weight and runs locally, so there is no provider invoice.
`model_cost_usd` is therefore an OBSERVED 0.0 and token counts come from the
SDK's own `usage` block; no price is invented for local compute.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import sys
import time
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
RUN_DIR = HERE.parent
REPO_ROOT = RUN_DIR.parents[2]
sys.path.insert(0, str(HERE))

from exp14_common import (  # noqa: E402
    CHECKPOINT,
    DATASET_ID,
    DECISION_FIELDS,
    EXPERIMENT_ID,
    NOUL_THRESHOLD,
    RISK_TIERS,
    ROUTE_PROFILES,
    SAFE_ESCALATION_DECISION,
    is_valid_decision,
    render_state,
)

LAYA_SDK_PIN = "laya==0.3.22"
HF_REPO = "convaiinnovations/laya"
PINNED_REVISIONS = {
    # laya/revisions.py PINNED_REVISIONS, read from the installed SDK, not guessed
    "root": "55cf4c4ebb4ebe31b2550e8bdf3bd21b99753851",
    "typed-decisions": "1a793eb568e6718f15941d08f85432581df534e3",
}

# ---------------------------------------------------------------------------
# Frozen typed-question encoding of the four-field decision contract.
# Criteria text is quoted from:
#   skills/murat-project-engineer/references/risk-and-routing.md
#   skills/murat-project-engineer/references/route-profiles.md
#   playbooks/{fast,verified,deep-change}.md
#   docs/OPERATING_MODEL.md (authority boundaries, cost-aware execution)
# ---------------------------------------------------------------------------
QUESTIONS: dict[str, dict[str, Any]] = {
    "risk_tier": {
        "type": "choice",
        "instructions": (
            "Given the MPE task packet in `task_packet`, which single risk tier must the "
            "coordinator assign?"
        ),
        "criteria": {
            "FAST": "narrow, reversible, low-impact work; one expert, deterministic checks, report",
            "VERIFIED": "meaningful change, unfamiliar component, or semantic risk; architect then coder, "
                        "deterministic gates, independent reviewer when acceptance is not fully deterministic",
            "DEEP-CHANGE": "affects MASTER, core architecture, Router authority, credentials/security, "
                           "persistent agents, plugin boundaries, memory governance, or central runtime",
        },
    },
    "requires_human_gate": {
        "type": "noul",
        "instructions": (
            "Given the MPE task packet in `task_packet`, does this task require an explicit human "
            "approval gate before it may be implemented?"
        ),
        "criteria": {
            "true": "a human must approve first: deep change, destructive or irreversible effect, production "
                    "change, security or permissions change, sensitive data write, or maximum architectural "
                    "or data sensitivity",
            "false": "no human approval gate is required; deterministic gates are sufficient",
        },
    },
    "route_profile": {
        "type": "choice",
        "instructions": (
            "Given the MPE task packet in `task_packet`, which coordinator route profile should the "
            "dominant work of this task use?"
        ),
        "criteria": {
            "default": "normal coordination and low-risk work",
            "cheap-research": "extraction, classification, deduplication, read-only research",
            "coding": "implementation and tests",
            "strong-review": "architecture, security, semantic judgment",
        },
    },
    "escalate_to_system_two": {
        "type": "noul",
        "instructions": (
            "Given the MPE task packet in `task_packet`, must this decision be escalated to the "
            "deliberative System Two path (a general-purpose reasoning model plus human gate where "
            "required) instead of being closed by the fast System One layer?"
        ),
        "criteria": {
            "true": "escalate: deep change, required human gate, material unknowns, missing acceptance "
                    "criteria, unknown rollback, no repository scope, or high architectural, security or "
                    "data-sensitivity judgment",
            "false": "System One may close this decision: routine, fully specified, reversible, low impact",
        },
    },
}

WARMUP_STATE = json.dumps(
    {"task_packet": {"summary": "warmup", "work_kind": "coordination", "signals": []}},
    sort_keys=True, ensure_ascii=False)


def decode_answers(answers: dict[str, Any]) -> tuple[dict[str, Any] | None, str | None, dict[str, Any]]:
    """Turn a Laya answer block into the four-field decision.

    Returns (parsed_or_None, failure_reason_or_None, telemetry). Nothing is
    coerced, defaulted or repaired: an out-of-vocabulary choice is a failure.
    """
    telemetry: dict[str, Any] = {}
    if not isinstance(answers, dict):
        return None, f"answers is not a dict: {type(answers).__name__}", telemetry

    parsed: dict[str, Any] = {}
    for field in DECISION_FIELDS:
        answer = answers.get(field)
        if not isinstance(answer, dict):
            return None, f"missing or malformed answer for {field!r}: {answer!r}", telemetry
        telemetry[field] = {
            "type": answer.get("type"),
            "confidence": answer.get("confidence"),
            "answer_confidence": answer.get("answer_confidence"),
            "act_probability": (answer.get("action") or {}).get("act_probability"),
            "probabilities": answer.get("probabilities"),
            "noul": answer.get("noul"),
            "choice": answer.get("choice"),
        }
        if field in ("risk_tier", "route_profile"):
            value = answer.get("choice")
            vocabulary = RISK_TIERS if field == "risk_tier" else ROUTE_PROFILES
            if not isinstance(value, str) or value not in vocabulary:
                return None, f"{field}: out-of-contract choice {value!r} (allowed: {list(vocabulary)})", telemetry
            parsed[field] = value
        else:
            probability = answer.get("noul")
            if not isinstance(probability, (int, float)):
                return None, f"{field}: noul probability missing or non-numeric: {probability!r}", telemetry
            parsed[field] = bool(float(probability) >= NOUL_THRESHOLD)

    if not is_valid_decision(parsed):
        return None, f"decoded decision failed contract validation: {parsed!r}", telemetry
    return parsed, None, telemetry


def host_snapshot() -> dict[str, Any]:
    info: dict[str, Any] = {
        "python": platform.python_version(),
        "platform": platform.platform(),
        "machine": platform.machine(),
        "cpu_count": os.cpu_count(),
    }
    meminfo = Path("/proc/meminfo")
    if meminfo.exists():
        for line in meminfo.read_text(encoding="utf-8").splitlines():
            key = line.split(":")[0]
            if key in ("MemTotal", "MemAvailable"):
                info[key + "_kB"] = int(line.split()[1])
    for module_name in ("torch", "transformers", "laya", "safetensors", "huggingface_hub", "numpy"):
        try:
            module_object = __import__(module_name)
            info[f"{module_name}_version"] = getattr(module_object, "__version__", None)
        except Exception as exc:  # noqa: BLE001
            info[f"{module_name}_version"] = f"UNAVAILABLE: {type(exc).__name__}"
    return info


def write_blocked(args: argparse.Namespace, dataset_sha: str, reason: str, error: str) -> int:
    payload = {
        "experiment_id": EXPERIMENT_ID,
        "checkpoint": CHECKPOINT,
        "sequence": "B_LAYA_ZERO_SHOT",
        "arm": args.arm,
        "status": "INFRASTRUCTURE_BLOCKED",
        "dataset_id": DATASET_ID,
        "dataset_sha256_expected": dataset_sha,
        "reason": reason,
        "error": error,
        "host": host_snapshot(),
        "results": [],
    }
    args.out_dir.mkdir(parents=True, exist_ok=True)
    out_path = args.out_dir / f"laya_{args.arm}.json"
    out_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"INFRASTRUCTURE_BLOCKED: {reason}\n{error[:1200]}\nwrote {out_path}")
    return 4


def main() -> int:
    parser = argparse.ArgumentParser(description="EXP-14 Sequence B Laya zero-shot")
    parser.add_argument("--arm", default="B_laya_zero_shot_root")
    parser.add_argument("--checkpoint", choices=sorted(PINNED_REVISIONS), default="root")
    parser.add_argument("--passes", type=int, default=3)
    parser.add_argument("--device", default="cpu")
    parser.add_argument("--dataset", type=Path, default=RUN_DIR / "frozen/dataset_v1.json")
    parser.add_argument("--out-dir", type=Path, default=RUN_DIR / "raw")
    args = parser.parse_args()
    args.dataset = args.dataset.resolve()
    args.out_dir = args.out_dir.resolve()

    raw_bytes = args.dataset.read_bytes()
    dataset = json.loads(raw_bytes.decode("utf-8"))
    dataset_sha = hashlib.sha256(raw_bytes).hexdigest()
    digest_file = args.dataset.parent / "DATASET_SHA256.txt"
    if digest_file.exists():
        recorded = next((line.split()[0] for line in digest_file.read_text(encoding="utf-8").splitlines()
                         if line.endswith("dataset_v1.json")), None)
        if recorded and recorded != dataset_sha:
            print(f"FATAL: frozen dataset digest changed (recorded {recorded} != actual {dataset_sha})",
                  file=sys.stderr)
            return 2
    assert dataset["dataset_id"] == DATASET_ID and dataset["frozen"] is True
    print(f"frozen dataset digest verified: {dataset_sha}")

    subfolder = None if args.checkpoint == "root" else args.checkpoint
    revision = PINNED_REVISIONS[args.checkpoint]

    try:
        import laya  # noqa: PLC0415
        load_started = time.perf_counter()
        agent = laya.load(HF_REPO, device=args.device, revision=revision, subfolder=subfolder)
        load_seconds = time.perf_counter() - load_started
    except Exception as exc:  # noqa: BLE001
        return write_blocked(
            args, dataset_sha,
            "the pinned Laya checkpoint could not be loaded on this host",
            f"{type(exc).__name__}: {exc}")

    try:
        import torch  # noqa: PLC0415
        device_repr = str(getattr(agent, "device", None))
        dtype_repr = str(getattr(agent, "dtype", None))
    except Exception:  # noqa: BLE001
        torch = None  # type: ignore[assignment]
        device_repr = str(getattr(agent, "device", None))
        dtype_repr = str(getattr(agent, "dtype", None))

    checkpoint_meta = {
        "sdk_pin": LAYA_SDK_PIN,
        "sdk_version_observed": getattr(laya, "__version__", None),
        "hf_repo": HF_REPO,
        "subfolder": subfolder,
        "requested_revision": revision,
        "resolved_revision": getattr(agent, "revision", None),
        "revision_matches_pin": getattr(agent, "revision", None) == revision,
        "device": device_repr,
        "dtype": dtype_repr,
        "max_len": (getattr(agent, "cfg", {}) or {}).get("max_len"),
        "head_max_len": (getattr(agent, "cfg", {}) or {}).get("head_max_len"),
        "model_dir": str(getattr(agent, "model_dir", None)),
        "load_seconds": round(load_seconds, 3),
        "questions_sha256": hashlib.sha256(
            json.dumps(QUESTIONS, sort_keys=True, ensure_ascii=False).encode("utf-8")).hexdigest(),
        "noul_threshold": NOUL_THRESHOLD,
        "zero_shot": True,
        "few_shot_examples_supplied": 0,
        "oracle_values_supplied": False,
        "calibration_applied": False,
        "fine_tuning_applied": args.checkpoint == "typed-decisions",
        "checkpoint_note": (
            "root = the pre-registered candidate convaiinnovations/laya (English, ModernBERT-large, 421M)"
            if args.checkpoint == "root" else
            "typed-decisions = the vendor checkpoint already fine-tuned on its own typed-decisions "
            "benchmark training split; run as a clearly separated SECONDARY reference arm (B2), never "
            "mixed into the primary zero-shot result"),
    }

    # Warmup: one untimed call so first-touch allocation/JIT is not charged to
    # case latency. Recorded, not hidden.
    warmup_started = time.perf_counter()
    try:
        agent.system_one(WARMUP_STATE, QUESTIONS)
        warmup = {"ok": True, "seconds": round(time.perf_counter() - warmup_started, 3)}
    except Exception as exc:  # noqa: BLE001
        warmup = {"ok": False, "error": f"{type(exc).__name__}: {exc}",
                  "seconds": round(time.perf_counter() - warmup_started, 3)}
    print(f"checkpoint loaded in {load_seconds:.1f}s; warmup: {warmup}")

    args.out_dir.mkdir(parents=True, exist_ok=True)
    pass_digests: list[str] = []
    decision_vectors: list[str] = []

    for pass_index in range(1, args.passes + 1):
        results: list[dict[str, Any]] = []
        for case in dataset["cases"]:
            case_input = case["input"]
            state = json.dumps({"task_packet": json.loads(render_state(case_input))},
                               sort_keys=True, ensure_ascii=False)
            started = time.perf_counter_ns()
            try:
                output = agent.system_one(state, QUESTIONS)
                elapsed_ms = (time.perf_counter_ns() - started) / 1_000_000.0
                answers = output.get("answers") if isinstance(output, dict) else None
                usage = output.get("usage") if isinstance(output, dict) else None
                parsed, failure_reason, telemetry = decode_answers(answers)
                invalid = parsed is None
                decision = dict(parsed) if parsed is not None else dict(SAFE_ESCALATION_DECISION)
                if invalid and failure_reason is None:
                    failure_reason = "decoded output failed contract validation"
            except Exception as exc:  # noqa: BLE001
                elapsed_ms = (time.perf_counter_ns() - started) / 1_000_000.0
                output = None
                answers = None
                usage = None
                telemetry = {}
                parsed = None
                invalid = True
                failure_reason = f"model call failed: {type(exc).__name__}: {exc}"[:2000]
                decision = dict(SAFE_ESCALATION_DECISION)

            results.append({
                "case_id": case["case_id"],
                "input_sha256": case["input_sha256"],
                "rendered_state": state,
                "rendered_state_sha256": hashlib.sha256(state.encode("utf-8")).hexdigest(),
                "raw_output": output,
                "answers": answers,
                "usage": usage,
                "parsed_output": parsed,
                "decision": decision,
                "decision_source": "model" if not invalid else "safe_escalation_substituted",
                "invalid_output": invalid,
                "failure_reason": failure_reason,
                "telemetry": telemetry,
                "escalated": bool(decision["escalate_to_system_two"]),
                "latency_ms": elapsed_ms,
                "model_calls": 1,
                "tokens": {
                    "input": int((usage or {}).get("input_tokens") or 0),
                    "output": int((usage or {}).get("output_tokens") or 0),
                },
                "state_truncated": bool((usage or {}).get("truncated")),
                "model_cost_usd": 0.0,
                "cost_basis": "observed_zero_open_weights_local_inference_no_provider_invoice",
            })

        latencies = sorted(result["latency_ms"] for result in results)
        count = len(latencies)
        payload = {
            "experiment_id": EXPERIMENT_ID,
            "checkpoint": CHECKPOINT,
            "sequence": "B_LAYA_ZERO_SHOT",
            "arm": args.arm,
            "pass_index": pass_index,
            "dataset_id": DATASET_ID,
            "dataset_sha256_expected": dataset_sha,
            "candidate": checkpoint_meta,
            "host": host_snapshot(),
            "warmup": warmup,
            "case_count": count,
            "latency_ms": {
                "min": round(latencies[0], 4),
                "median": round(latencies[count // 2] if count % 2
                                else (latencies[count // 2 - 1] + latencies[count // 2]) / 2, 4),
                "mean": round(sum(latencies) / count, 4),
                "p95": round(latencies[max(0, int(round(0.95 * count)) - 1)], 4),
                "max": round(latencies[-1], 4),
                "total": round(sum(latencies), 4),
            },
            "invalid_output_count": sum(1 for r in results if r["invalid_output"]),
            "state_truncated_count": sum(1 for r in results if r["state_truncated"]),
            "model_calls": sum(r["model_calls"] for r in results),
            "tokens": {
                "input": sum(r["tokens"]["input"] for r in results),
                "output": sum(r["tokens"]["output"] for r in results),
            },
            "model_cost_usd": 0.0,
            "results": results,
        }
        rendered = json.dumps(payload, ensure_ascii=False, indent=2) + "\n"
        out_path = args.out_dir / f"laya_{args.arm}_pass{pass_index}.json"
        out_path.write_text(rendered, encoding="utf-8")
        pass_digests.append(hashlib.sha256(rendered.encode("utf-8")).hexdigest())
        decision_vectors.append(json.dumps([[r["case_id"], r["decision"], r["invalid_output"]]
                                            for r in results], sort_keys=True))
        print(f"pass {pass_index}: {count} cases, invalid={payload['invalid_output_count']}, "
              f"median {payload['latency_ms']['median']} ms, "
              f"tokens_in={payload['tokens']['input']}, sha256 {pass_digests[-1][:16]}…")

    identical = len(set(decision_vectors)) == 1
    summary = {
        "sequence": "B_LAYA_ZERO_SHOT",
        "arm": args.arm,
        "dataset_id": DATASET_ID,
        "dataset_sha256": dataset_sha,
        "candidate": checkpoint_meta,
        "passes": args.passes,
        "pass_files": [f"raw/laya_{args.arm}_pass{i}.json" for i in range(1, args.passes + 1)],
        "pass_file_sha256": pass_digests,
        "decisions_identical_across_passes": identical,
        "reproducible": identical,
        "warmup": warmup,
        "status": "EXECUTED",
    }
    (args.out_dir / f"laya_{args.arm}_reproducibility.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"decisions identical across {args.passes} passes: {identical}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
