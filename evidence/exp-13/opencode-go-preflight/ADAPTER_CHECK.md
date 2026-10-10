# EXP-13 OpenCode Go preflight — adapter check (sanitized transcript)

Scope: verifies `scripts/usage_from_router_log.py` behaviour. No live provider telemetry exists in this run, so no `USAGE_RECORD` is produced for Route A or Route B.

## 1. Existing adapter unit tests (synthetic fixtures inside the test suite)

Command:

```text
python3 -m unittest tests.test_usage_from_router_log tests.test_usage_instrumentation
```

Output (sanitized):

```text
Ran 29 tests in 0.005s
OK
```

These tests use fixtures written into the test code. They prove the adapter's rules (window filter, mixed-traffic rejection, unmetered-request rejection, expected-call count, token-sum checks). They are **not** evidence of Route A or Route B usage and are not PREFLIGHT_ONLY records.

## 2. Fail-closed run against the real Router events path (no live telemetry)

Command (sanitized; `$HOME` is the sandbox home directory):

```text
python3 scripts/usage_from_router_log.py \
  --events "$HOME/.codex/codex-router/usage-events.jsonl" \
  --run-id EXP13-PREFLIGHT-A --provider opencode-go \
  --model opencode-go/deepseek-v4-flash \
  --start 2026-10-10T00:00:00Z --end 2026-10-10T23:59:00Z \
  --expected-calls 1 --output /tmp/preflight_A.json
```

Result: exit code 1, `RouterUsageImportError: Router usage events file not found`. No output file was written. The adapter failed closed. Observation: it surfaces as an uncaught traceback rather than a clean CLI error; not changed in this preflight (minimal-diff rule, not a blocker).

## 3. Not run

- Route A adapter run on live telemetry: NOT_RUN (no successful live call; no events file).
- Route B adapter run on live telemetry: NOT_RUN (same reason).
- No synthetic or estimated usage records were generated.
