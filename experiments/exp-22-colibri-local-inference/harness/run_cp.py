#!/usr/bin/env python3
"""EXP-22 CP-01/CP-02 isolated harness (stdlib only).

POSTs each frozen fixture item to a running `coli serve` POST /v1/systemone
endpoint, 3 repeats per item for a determinism check. Records client-measured
latency, validates the constrained-output schema (choice always within the
listed options), runs a deterministic keyword reference baseline, and samples
server RSS (parent + descendants) around the run.

Quality/accuracy vs the reference is recorded but is NON-INFORMATIVE when the
server runs random (tiny-fixture) weights: only latency, footprint,
determinism, schema-safety, and API behavior are measured.
"""
import argparse
import json
import sys
import time
import urllib.request
from pathlib import Path

CP01_KEYWORDS = {
    "BLOCKED": ["cannot", "blocked", "missing", "waiting on", "fail", "rejected",
                "unreachable", "required before", "no access", "deferred"],
    "WARNING": ["flak", "pending", "awaiting", "scheduled", "85", "headroom",
                "review", "risk", "degrad", "partial", "budget"],
    "READY": ["pass", "green", "documented", "installed", "frozen", "complete"],
}

CP02_KEYWORDS = {
    "coder": ["implement", "fix", "refactor", "retry logic", "code"],
    "researcher": ["survey", "compare", "assess", "engines"],
    "reviewer": ["review", "audit"],
    "architect": ["design", "choose", "decide", "approach", "seam", "polling", "webhook"],
}


def reference_cp01(state):
    text = state.lower().replace("0 failed", "passed")  # "0 failed" is a pass, not a failure
    for label in ("BLOCKED", "WARNING", "READY"):
        if any(k in text for k in CP01_KEYWORDS[label]):
            return label
    return "READY"


def reference_cp02(state):
    text = state.lower()
    best, best_hits = None, 0
    for label, keywords in CP02_KEYWORDS.items():
        hits = sum(1 for k in keywords if k in text)
        if hits > best_hits:
            best, best_hits = label, hits
    return best or "researcher"


REFERENCE = {"CP-01": reference_cp01, "CP-02": reference_cp02}


def post_systemone(base_url, state, questions, model="jev-latest", timeout=120):
    body = json.dumps({"model": model, "state": state,
                       "questions": questions}).encode()
    req = urllib.request.Request(base_url + "/v1/systemone", data=body,
                                 headers={"Content-Type": "application/json"},
                                 method="POST")
    start = time.perf_counter()
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read().decode()
            status = resp.status
    except urllib.error.HTTPError as exc:
        raw = exc.read().decode(errors="replace")
        status = exc.code
    latency_ms = (time.perf_counter() - start) * 1000.0
    return status, raw, latency_ms


def validate_reply(reply, qid, options):
    """Constrained-output schema check. Returns list of problems (empty = clean)."""
    problems = []
    try:
        answers = reply["answers"]
        ans = answers[qid]
    except (KeyError, TypeError):
        return ["missing answers/%s" % qid]
    choice = ans.get("choice")
    probs = ans.get("probabilities") or {}
    if choice not in options:
        problems.append("choice %r not in options %s" % (choice, options))
    if set(probs.keys()) != set(options):
        problems.append("probability keys %s != options %s"
                        % (sorted(probs.keys()), options))
    else:
        total = sum(probs.values())
        if abs(total - 1.0) > 0.02:
            problems.append("probabilities sum to %f" % total)
        if probs and max(probs, key=probs.get) != choice:
            problems.append("choice %r is not the argmax" % choice)
    if "confidence" not in ans:
        problems.append("missing confidence")
    if "usage" not in reply:
        problems.append("missing usage")
    return problems


def proc_rss_kb(pid):
    try:
        with open("/proc/%d/status" % pid) as fh:
            for line in fh:
                if line.startswith("VmRSS:"):
                    return int(line.split()[1])
    except OSError:
        return 0
    return 0


def proc_hwm_kb(pid):
    try:
        with open("/proc/%d/status" % pid) as fh:
            for line in fh:
                if line.startswith("VmHWM:"):
                    return int(line.split()[1])
    except OSError:
        return 0
    return 0


def descendants(root_pid):
    try:
        import os
        pids = [int(p) for p in os.listdir("/proc") if p.isdigit()]
    except OSError:
        return []
    children = {root_pid}
    changed = True
    ppid_of = {}
    for pid in pids:
        try:
            with open("/proc/%d/stat" % pid) as fh:
                parts = fh.read().rsplit(")", 1)[1].split()
                ppid_of[pid] = int(parts[1])
        except OSError:
            continue
    while changed:
        changed = False
        for pid, ppid in ppid_of.items():
            if ppid in children and pid not in children:
                children.add(pid)
                changed = True
    return sorted(children)


def server_footprint(server_pid):
    pids = descendants(server_pid)
    return {"pids": pids,
            "rss_kb_total": sum(proc_rss_kb(p) for p in pids),
            "hwm_kb_max": max([proc_hwm_kb(p) for p in pids] + [0])}


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--fixture", required=True)
    parser.add_argument("--base-url", default="http://127.0.0.1:8000")
    parser.add_argument("--repeats", type=int, default=3)
    parser.add_argument("--server-pid", type=int, default=0)
    parser.add_argument("--out", required=True)
    parser.add_argument("--model-id", default="jev-latest")
    args = parser.parse_args(argv)

    fixture = json.loads(Path(args.fixture).read_text())
    checkpoint = fixture["checkpoint"]
    qid = next(iter(fixture["question"]))
    options = list(fixture["question"][qid]["criteria"].keys())
    ref_fn = REFERENCE[checkpoint]

    # Reference baseline must reproduce every frozen expected label, else the
    # harness rubric (not Colibri) is wrong: fail loudly.
    ref_mismatch = [it["id"] for it in fixture["items"]
                    if ref_fn(it["state"]) != it["expected"]]
    if ref_mismatch:
        print("REFERENCE BASELINE MISMATCH on %s; fix rubric, not data"
              % ref_mismatch, file=sys.stderr)
        return 2

    footprint_before = (server_footprint(args.server_pid)
                        if args.server_pid else None)
    results = {"checkpoint": checkpoint,
               "question_id": qid,
               "options": options,
               "repeats": args.repeats,
               "items": []}
    for item in fixture["items"]:
        runs = []
        for _ in range(args.repeats):
            status, raw, latency_ms = post_systemone(
                args.base_url, item["state"], fixture["question"],
                model=args.model_id)
            try:
                reply = json.loads(raw)
            except json.JSONDecodeError:
                reply = {"_raw": raw[:500]}
            problems = (validate_reply(reply, qid, options)
                        if status == 200 else ["http_%d" % status])
            ans = (reply.get("answers", {}).get(qid, {})
                   if isinstance(reply, dict) else {})
            runs.append({
                "http_status": status,
                "latency_ms": round(latency_ms, 1),
                "choice": ans.get("choice"),
                "probabilities": ans.get("probabilities"),
                "confidence": ans.get("confidence"),
                "usage": reply.get("usage") if isinstance(reply, dict) else None,
                "model": reply.get("model") if isinstance(reply, dict) else None,
                "provider": reply.get("provider") if isinstance(reply, dict) else None,
                "schema_problems": problems,
            })
        first = runs[0]
        deterministic = all(r["choice"] == first["choice"]
                            and r["probabilities"] == first["probabilities"]
                            for r in runs)
        results["items"].append({
            "id": item["id"],
            "expected": item["expected"],
            "reference": ref_fn(item["state"]),
            "runs": runs,
            "deterministic": deterministic,
            "matches_expected": first["choice"] == item["expected"],
        })
    results["footprint_before"] = footprint_before
    results["footprint_after"] = (server_footprint(args.server_pid)
                                  if args.server_pid else None)

    n = len(results["items"])
    lat = [r["latency_ms"] for it in results["items"] for r in it["runs"]]
    results["summary"] = {
        "n_items": n,
        "n_requests": len(lat),
        "http_200": sum(1 for it in results["items"] for r in it["runs"]
                        if r["http_status"] == 200),
        "malformed_outputs": sum(1 for it in results["items"] for r in it["runs"]
                                 if r["schema_problems"]),
        "deterministic_items": sum(1 for it in results["items"] if it["deterministic"]),
        "matches_expected": sum(1 for it in results["items"] if it["matches_expected"]),
        "latency_ms": {"min": min(lat), "max": max(lat),
                       "mean": round(sum(lat) / len(lat), 1),
                       "sorted": sorted(lat)},
    }
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.out).write_text(json.dumps(results, indent=1) + "\n")
    print(json.dumps(results["summary"], indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
