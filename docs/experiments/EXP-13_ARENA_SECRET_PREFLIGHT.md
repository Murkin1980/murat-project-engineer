# EXP-13 — Arena Secret Injection Preflight

Status: OWNER-AUTHORIZED PREFLIGHT  
Primary disposition: **EXTEND_EXISTING**  
Experiment: `EXP-13 — Low-cost evaluation harness`  
Repository: `Murkin1980/murat-project-engineer`

## Purpose

Determine whether the Arena runtime has a supported secret-injection mechanism that can safely provide the OpenCode Go credential required by EXP-13.

This task does **not** authorize:
- any OpenCode Go live model call;
- any Pilot Batch 1 execution;
- any Cloudflare Worker;
- any new proxy/runtime/service;
- any repository-stored credential.

The only objective is to answer:

> Can the owner/admin inject an OpenCode Go credential into Arena securely at runtime, without committing it to Git or exposing it in logs?

## Startup

Read:
- `AGENTS.md`
- `docs/governance/SCOPE-CHANGE-CONTROL.md`
- `docs/experiments/EXP-13_LOW_COST_EVALUATION_HARNESS.md`
- `docs/experiments/EXP-13_OPENCODE_GO_PREFLIGHT.md`

Use EXP-29 bootstrap if required by `AGENTS.md`.

## Step 1 — Identify supported secret mechanisms

Inspect the Arena/runtime environment and determine whether any supported mechanism exists for owner/admin-provisioned secrets.

Examples that may exist:
- platform secret store;
- environment secret injection;
- workspace/repository secret binding;
- task/session secret binding;
- runtime-mounted secret file;
- provider credential configuration managed outside Git.

Do not assume any mechanism exists.

Do not print or expose secret values.

Report only:
- mechanism name/type;
- where it is configured by the owner/admin;
- whether it is available to this Arena runtime;
- whether it persists across sessions;
- whether it is scoped to repo / workspace / user / session;
- whether it can be read only at runtime rather than written into source files.

## Step 2 — Determine required credential shape

From the frozen EXP-13 route/provider configuration, determine the minimum credential form Arena would need for OpenCode Go.

Do not require or request the actual secret value.

Record:
- expected config key / environment variable / credential field name if the runtime or provider integration defines one;
- whether a base URL/provider config is also required;
- whether the OpenCode CLI is required, or direct provider/API access is sufficient.

Do not change frozen EXP-13 routes.

## Step 3 — Verify non-Git boundary

Prove that the identified mechanism, if any:
- does not require committing the key to Git;
- does not echo it in logs by default;
- does not write it into evidence files;
- can be revoked/rotated independently of repository history.

If this cannot be established, classify as unsupported.

## Step 4 — Egress dependency note

Do not make a live provider request.

Determine only whether successful secret injection would still depend on outbound network access to the OpenCode Go endpoint.

Report:
- expected outbound hostname if known from current provider configuration/docs already present in the repo/runtime;
- whether Arena's current allowlist appears to permit it;
- classify this as `KNOWN_OK`, `KNOWN_BLOCKED`, or `UNVERIFIED`.

Do not probe the provider endpoint in this task.

## Step 5 — classify exactly one result

Return exactly one:

### SECRET_INJECTION_READY

Use only when:
- a supported owner/admin secret mechanism exists;
- the OpenCode Go credential can be injected without Git;
- secret value need not be printed/logged;
- Arena can consume it at runtime;
- no architectural change is required.

### SECRET_MECHANISM_PRESENT_BUT_EGRESS_UNVERIFIED

Use when:
- secret injection is supported;
- but outbound access to the OpenCode Go endpoint is still not established.

### SECRET_MECHANISM_PRESENT_BUT_INCOMPATIBLE

Use when:
- a secret store exists;
- but it cannot supply the credential in a form Arena/OpenCode Go can consume without source changes or unsafe handling.

### NO_SUPPORTED_SECRET_MECHANISM

Use when:
- no owner/admin secret injection mechanism is available in this Arena runtime.

Do not invent a fifth status.

## Evidence

Create:

`evidence/exp-13/arena-secret-preflight/`

Minimum:
- `README.md`
- `RESULT.json`
- `SECRET_MECHANISM.md`
- `EGRESS_NOTE.md`

Never store:
- API keys;
- bearer tokens;
- secret values;
- copied credential files.

## RESULT.json minimum fields

- result;
- secret mechanism detected;
- mechanism type;
- scope;
- persistence;
- owner/admin configurable;
- Git required: true/false;
- runtime readable: true/false;
- logs expose secret by default: true/false/unknown;
- expected credential field/key name;
- base URL/provider config required: true/false/unknown;
- OpenCode CLI required: true/false/unknown;
- egress status;
- blocker;
- next action.

## Stop boundaries

Stop and ask for owner approval before:
- creating a Cloudflare Worker/proxy;
- changing provider routes;
- changing Arena runtime configuration outside the supported secret mechanism;
- storing credentials in Git;
- starting live OpenCode Go calls;
- starting EXP-13 Pilot Batch 1.

## Terminal report

```text
RESULT: SECRET_INJECTION_READY / SECRET_MECHANISM_PRESENT_BUT_EGRESS_UNVERIFIED / SECRET_MECHANISM_PRESENT_BUT_INCOMPATIBLE / NO_SUPPORTED_SECRET_MECHANISM
SECRET MECHANISM:
OWNER/ADMIN CONFIGURABLE: YES/NO
GIT REQUIRED: YES/NO
RUNTIME READABLE: YES/NO
EXPECTED CREDENTIAL FIELD:
BASE URL CONFIG REQUIRED:
OPENCODE CLI REQUIRED:
EGRESS STATUS: KNOWN_OK / KNOWN_BLOCKED / UNVERIFIED
SECRETS STORED: NO
LIVE PROVIDER CALLS: NO
PILOT BATCH STARTED: NO
BLOCKER:
NEXT ACTION:
```

## Merge boundary

Open one bounded PR against `murat-project-engineer/main`.

Do not merge automatically.

Stop after the result and evidence are recorded.
