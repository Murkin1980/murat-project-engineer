# EXP-13 — OpenCode Go connectivity preflight (evidence)

Authoritative instruction: `docs/experiments/EXP-13_OPENCODE_GO_PREFLIGHT.md`
Date: 2026-10-10 · Base: `main` @ `8fe0955` · Branch: `arena/aa09db6a-murat-project-engineer`

## Result

```text
RESULT: CREDENTIALS_MISSING
ROUTE A CALLABLE: NO
ROUTE B CALLABLE: NO
ROUTE A TOKENS: UNAVAILABLE
ROUTE B TOKENS: UNAVAILABLE
ROUTE A ADAPTER: NOT_RUN
ROUTE B ADAPTER: NOT_RUN
OBSERVED COST: UNOBSERVED
SECRETS STORED: NO
PILOT BATCH STARTED: NO
REPOSITORY CHANGES: evidence/exp-13/opencode-go-preflight/ only
BLOCKER: No OpenCode Go provider credential/config in the Arena runtime; Codex Router usage-events source absent; opencode CLI not installed.
NEXT ACTION: Owner/Arena admin provisions the OpenCode Go credential via the secret store and confirms the Router usage source and egress path; then rerun the preflight. No synthetic usage.
```

## What was checked

1. **Sync:** local `main` and `origin/main` are both `8fe0955`, the same as this branch's base. Nothing to pull.
2. **Startup reading:** `AGENTS.md`, `docs/governance/SCOPE-CHANGE-CONTROL.md`, `docs/experiments/EXP-13_LOW_COST_EVALUATION_HARNESS.md`, `scripts/usage_from_router_log.py`, `experiments/exp-13/routes.json`.
3. **Credential/config presence (names and paths only, no values):**
   - No OpenCode Go provider credential found in the environment. Only `GH_TOKEN` and `GITHUB_TOKEN` are set, and both are GitHub tokens.
   - Absent: `~/.codex/`, `~/.codex/codex-router/`, `~/.codex/config.toml`, `~/.codex/auth.json`, `~/.config/opencode/`, `~/.local/share/opencode/`, `~/.opencode/`, `~/.opencode-mobile/`.
   - `opencode` / `codex` binaries not on PATH.
   - The repo's `.devcontainer/start-opencode.sh` starts an OpenCode *mobile server* with basic-auth credentials. That is not a provider credential, and its state is absent here.
4. **Live calls:** none. The preflight allows the two calls only when credentials or config are present, so Route A and Route B were not called. No retries were used.
5. **Adapter:** `scripts/usage_from_router_log.py` has 29 passing unit tests (`ADAPTER_CHECK.md`). Against the real Router events path it fails closed, writes no output, and produces no record. No usage record was generated for either route, and none was fabricated.

## Files

- `RESULT.json` — machine-readable result and checks.
- `ROUTE_A.md` / `ROUTE_B.md` — per-route record. Both routes are NOT_RUN.
- `ADAPTER_CHECK.md` — sanitized adapter test and fail-closed transcript.

## Boundaries

- Pilot Batch 1 not started. EXP-13 stays `READY_TO_TEST`, not `READY_FOR_EXP13`.
- No secrets, tokens or credential values stored or printed.
- No frozen routes, thresholds, dataset, pricing snapshot, pre-registration, Router authority or adapter code changed.
- No paid calls made. Nothing purchased or topped up.
