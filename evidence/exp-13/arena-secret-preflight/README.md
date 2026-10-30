# EXP-13 — Arena secret injection preflight

Authoritative instruction: `docs/experiments/EXP-13_ARENA_SECRET_PREFLIGHT.md`
Date: 2026-10-10 (UTC)
Repository: `Murkin1980/murat-project-engineer`
Branch: `arena/4020ab5a-murat-project-engineer`
Fetched `origin/main`: `d893002824943330079622e553a8aeaa37847632` (same as this branch's starting `HEAD`)

## Result

```text
RESULT: NO_SUPPORTED_SECRET_MECHANISM
SECRET MECHANISM: None exposed for owner/admin-provisioned OpenCode Go credentials in this Arena runtime. GitHub integration environment-variable names were present but are not a generic OpenCode Go secret binding.
OWNER/ADMIN CONFIGURABLE: NO (no supported arbitrary-secret control was exposed to this runtime)
GIT REQUIRED: NO (no secret was put in Git; this does not establish a working non-Git injection path)
RUNTIME READABLE: NO (no OpenCode Go credential was available to the runtime)
EXPECTED CREDENTIAL FIELD: Not defined by the frozen route/provider configuration or current runtime
BASE URL CONFIG REQUIRED: UNKNOWN
OPENCODE CLI REQUIRED: NO for the frozen Codex Router model-slug route; direct-provider/API sufficiency is unverified
EGRESS STATUS: UNVERIFIED
SECRETS STORED: NO
LIVE PROVIDER CALLS: NO
PILOT BATCH STARTED: NO
BLOCKER: No owner/admin-configurable secret store, arbitrary environment binding, workspace/repository/session binding, or usable mounted OpenCode Go secret was available in this runtime. The provider credential field and endpoint hostname are not defined in the frozen route configuration.
NEXT ACTION: Ask the Arena owner/admin to identify a supported non-Git secret binding and provide the authoritative provider credential field/endpoint configuration. Do not change routes, probe the provider, or start the pilot under this preflight.
```

## Evidence summary

- `SECRET_MECHANISM.md` records the runtime mechanism checks, credential-shape limits, and non-Git/logging conclusions. Environment variable **names only** were inspected; no secret values were read or recorded.
- `EGRESS_NOTE.md` records why endpoint egress remains `UNVERIFIED`. No endpoint was resolved or contacted.
- `RESULT.json` is the machine-readable result.

## Boundaries

- No API keys, bearer tokens, secret values, or credential files were read, printed, copied, or added to evidence.
- No live OpenCode Go/provider request or egress probe was made.
- Pilot Batch 1 was not started; no Cloudflare Worker was created.
- Frozen EXP-13 routes/configuration were not changed.
- The only repository changes for this preflight are the four sanitized evidence files in this directory.

## Bootstrap note

The EXP-29 bootstrap builder was tried with temporary outputs outside the repository. It stopped before producing a packet because the current EXP-13 registry entry points `experiment_path` at the harness Markdown file, while the builder expects an experiment directory containing `ARENA_TASK.md`. No bootstrap artifact, registry change, or harness change was made. The canonical task/startup sources were read directly; this tooling mismatch did not affect the runtime secret or egress observations.
