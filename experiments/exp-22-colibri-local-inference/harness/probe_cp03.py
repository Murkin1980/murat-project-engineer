#!/usr/bin/env python3
"""EXP-22 CP-03 isolated provider-compatibility probe (stdlib only).

Probes the live `coli serve` HTTP surface and records status codes, latency,
and truncated response bodies: OpenAI model listing, OpenAI chat completions,
Anthropic messages, System One decision, and one malformed decision request.
"""
import json
import time
import urllib.request
import urllib.error
from pathlib import Path

BASE = "http://127.0.0.1:8000"


def call(method, path, body=None, timeout=60):
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(BASE + path, data=data, method=method,
                                 headers={"Content-Type": "application/json"})
    start = time.perf_counter()
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read().decode(errors="replace")
            status = resp.status
    except urllib.error.HTTPError as exc:
        raw = exc.read().decode(errors="replace")
        status = exc.code
    latency_ms = round((time.perf_counter() - start) * 1000.0, 1)
    try:
        parsed = json.loads(raw)
        shape = sorted(parsed.keys()) if isinstance(parsed, dict) else type(parsed).__name__
    except json.JSONDecodeError:
        parsed, shape = None, "non-json"
    return {"method": method, "path": path, "http_status": status,
            "latency_ms": latency_ms, "top_level_shape": shape,
            "body_truncated": raw[:600]}


def main():
    probes = []
    probes.append({"name": "openai_list_models", **call("GET", "/v1/models")})
    probes.append({"name": "openai_chat_completions", **call("POST", "/v1/chat/completions", {
        "model": "laya", "messages": [{"role": "user", "content": "hi"}], "max_tokens": 5})})
    probes.append({"name": "anthropic_messages", **call("POST", "/v1/messages", {
        "model": "laya", "max_tokens": 5,
        "messages": [{"role": "user", "content": "hi"}]})})
    probes.append({"name": "systemone_decision", **call("POST", "/v1/systemone", {
        "model": "jev-latest",
        "state": "Unit tests pass; integration suite flakes one run in five.",
        "questions": {"status": {"type": "choice",
                                 "instructions": "What is the delivery status?",
                                 "criteria": {"READY": "ok", "WARNING": "risk", "BLOCKED": "stuck"}}}})})
    probes.append({"name": "systemone_malformed_type", **call("POST", "/v1/systemone", {
        "model": "jev-latest", "state": "x",
        "questions": {"q": {"type": "essay", "instructions": "write prose"}}})})
    out = Path("experiments/exp-22-colibri-local-inference/evidence/cp03-results.json")
    out.write_text(json.dumps({"probes": probes}, indent=1) + "\n")
    for p in probes:
        print("%s %s -> %d (%s ms) keys=%s" % (
            p["method"], p["path"], p["http_status"], p["latency_ms"], p["top_level_shape"]))
        print("  " + p["body_truncated"][:300].replace("\n", " "))
    print("wrote", out)


if __name__ == "__main__":
    main()
