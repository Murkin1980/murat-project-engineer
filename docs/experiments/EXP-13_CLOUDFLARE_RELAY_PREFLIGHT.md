# EXP-13 — Cloudflare Relay Preflight

Status: OWNER-AUTHORIZED EXPERIMENT  
Primary disposition: **EXPERIMENT**  
Parent experiment: `EXP-13 — Low-cost evaluation harness`  
Repository: `Murkin1980/murat-project-engineer`

## Purpose

Test whether an existing Cloudflare deployment path can provide a secure, bounded relay between Arena and the frozen OpenCode Go routes without exposing the OpenCode Go credential to Arena or Git.

Target shape:

```text
Arena
→ temporary Cloudflare Worker relay
→ OpenCode Go
```

This is a preflight only. It does **not** authorize EXP-13 Pilot Batch 1.

## Why Cloudflare

Existing Murat repositories already contain working Cloudflare Worker deployment patterns:

1. `Murkin1980/grand-mebel-document-control`
   - real `wrangler.jsonc`
   - existing Cloudflare account id
   - established Worker deployment path
   - previous production deployment evidence

2. `Murkin1980/grand-mebel-accounting-cloudflare`
   - real `wrangler.toml`
   - direct `wrangler deploy`
   - D1/R2 bindings

3. `Murkin1980/minibase-cloudflare`
   - Cloudflare Worker architecture and Wrangler toolchain
   - example config only; use as reference, not preferred deployment authority

Do not modify these production repositories for this preflight.

They are evidence/reference for Cloudflare access and deployment conventions only.

## Mandatory startup

Read:

- `AGENTS.md`
- `docs/governance/SCOPE-CHANGE-CONTROL.md`
- `docs/experiments/EXP-13_LOW_COST_EVALUATION_HARNESS.md`
- `docs/experiments/EXP-13_OPENCODE_GO_PREFLIGHT.md`
- `docs/experiments/EXP-13_ARENA_SECRET_PREFLIGHT.md`

If required by `AGENTS.md`, generate and verify EXP-29 bootstrap as `FRESH`.

## PHASE 0 — Confirm actual Cloudflare access

Before writing relay code, determine whether the current execution environment has working Cloudflare/Wrangler authentication.

Inspect the deployment setup of:

- `Murkin1980/grand-mebel-document-control`
- `Murkin1980/grand-mebel-accounting-cloudflare`

Do not read or expose secret values.

Run only safe identity/config checks such as:

- `npx wrangler whoami`
- Wrangler account metadata that does not expose credentials
- dry-run deployment/build if useful

Record:

- authenticated: YES/NO;
- account id if Wrangler returns it;
- auth source type if observable (OAuth/local config/token env/etc.), never value;
- whether Worker deployment is permitted;
- whether secret management command is available;
- whether outbound fetch from Workers is available by platform design/config.

### PHASE 0 stop

If Cloudflare authentication is unavailable:

Return:

`CLOUDFLARE_AUTH_MISSING`

Do not create relay code or request OpenCode Go credentials.

## PHASE 1 — Create bounded relay fixture

Only if PHASE 0 proves authenticated deploy access.

Create the relay only under:

`experiments/exp-13/cloudflare-relay/`

Do not create a new repository.

Minimum fixture:

- `src/index.ts`
- `wrangler.jsonc` or `wrangler.toml`
- `package.json` only if necessary
- `README.md`
- minimal tests if practical

Use a unique temporary Worker name clearly tied to EXP-13, for example:

`mpe-exp13-opencode-relay`

Do not reuse or modify production Worker names.

## Relay contract

The Worker must be narrow.

Allowed:
- health endpoint with no provider call;
- one relay endpoint for the two frozen EXP-13 model routes only.

Frozen allowlist:

- `opencode-go/deepseek-v4-flash`
- `opencode-go/kimi-k2.7-code`

Reject:
- any other model;
- arbitrary upstream URL;
- arbitrary HTTP method;
- arbitrary headers forwarded from caller;
- any request that attempts to override upstream host.

The Worker must not become a general-purpose proxy.

## OpenCode Go provider discovery

Before hard-coding an upstream endpoint or credential field:

1. identify the authoritative OpenCode Go API endpoint and authentication scheme from official provider documentation or existing trusted configuration;
2. record the source in `README.md`;
3. if endpoint/auth shape cannot be established confidently, stop with:

`OPENCODE_PROVIDER_CONFIG_UNKNOWN`

Do not guess endpoint hostnames, auth header names, or credential fields.

## Credential boundary

The OpenCode Go credential must exist only as a Cloudflare Worker secret.

Expected pattern:

```text
wrangler secret put <SECRET_NAME>
```

Never:
- commit credential values;
- place credential in `wrangler.jsonc`;
- place credential in env files committed to Git;
- print credential;
- copy credential into evidence;
- expose credential to Arena after binding.

### OWNER INPUT GATE

When the relay code is ready and Cloudflare secret binding is the only missing step:

STOP and return:

`OWNER_SECRET_REQUIRED`

Report:
- exact Worker name;
- exact secret binding name;
- exact command/interface the owner/admin must use;
- no secret value.

Do not invent or request the secret in chat logs if a safer Cloudflare secret-entry path exists.

## Relay authentication from Arena

Because Arena has no generic secret injection, do not introduce a second long-lived bearer secret unless necessary.

For the first connectivity test, prefer one of these bounded approaches in order:

1. Cloudflare platform-native access mechanism already available to the Arena runtime;
2. a temporary single-purpose unguessable test URL/token generated and scoped only to this EXP-13 preflight, with strict call limits and immediate revocation after test;
3. if neither can be implemented safely, stop with `ARENA_TO_RELAY_AUTH_BLOCKED`.

Do not create an open public spend proxy.

The relay must have:
- strict model allowlist;
- strict request-size limit;
- maximum output-token limit;
- no streaming if not needed;
- a hard per-test request cap where practical;
- no arbitrary upstream pass-through.

## PHASE 2 — Deploy health-only relay

Before any OpenCode Go secret is installed:

Deploy the Worker with provider-calling path disabled/fail-closed.

Verify:
- deployment succeeds;
- health endpoint responds;
- Arena can reach the Worker endpoint.

If Arena cannot reach the Worker:

Return:

`ARENA_EGRESS_TO_WORKER_BLOCKED`

Do not proceed to provider credential setup.

## PHASE 3 — Owner installs OpenCode Go secret

Only after:
- Cloudflare auth PASS;
- Worker deployed;
- Arena → Worker health connectivity PASS;
- upstream endpoint/auth shape known.

Stop at the OWNER INPUT GATE and ask the owner/admin to install the OpenCode Go credential through Cloudflare secret management.

After the owner confirms installation, resume from this phase.

Do not store the secret anywhere else.

## PHASE 4 — Two tiny provider calls

After secret installation, execute exactly:

- one Route A call;
- one Route B call.

Prompt:

`Reply with exactly OK`

Maximum intended provider work: these two calls only.

Record:
- route/model requested;
- actual model/provider if returned;
- HTTP success/failure;
- latency;
- input/output/total token usage returned by provider;
- provider request id if available;
- observed cost if returned;
- relay request id;
- whether usage evidence is attributable to exactly one call.

Do not estimate missing usage.

## Usage evidence requirement

The relay should preserve enough sanitized metadata for EXP-13 usage evidence without storing prompts or secrets.

Preferred minimal metadata:
- timestamp;
- route/model;
- request id;
- response status;
- latency;
- input tokens;
- output tokens;
- total tokens;
- observed cost if supplied.

Do not log authorization headers.

If OpenCode Go responds but does not provide trustworthy token/usage information, return:

`CALLABLE_BUT_USAGE_BLOCKED`

## Success criteria

Return `READY_FOR_EXP13_VIA_CLOUDFLARE_RELAY` only when all are true:

1. Cloudflare authenticated deployment path exists.
2. Temporary Worker deployed without changing production Workers.
3. Arena can reach the Worker.
4. OpenCode Go credential is stored only as Cloudflare secret.
5. Relay can call both frozen routes.
6. Real token usage for both calls is observable and attributable.
7. No secret appears in Git/log/evidence.
8. Relay is not an arbitrary/open proxy.
9. Pilot Batch 1 has not started.

## Allowed terminal statuses

Return exactly one:

- `CLOUDFLARE_AUTH_MISSING`
- `OPENCODE_PROVIDER_CONFIG_UNKNOWN`
- `OWNER_SECRET_REQUIRED`
- `ARENA_EGRESS_TO_WORKER_BLOCKED`
- `ARENA_TO_RELAY_AUTH_BLOCKED`
- `PROVIDER_BLOCKED`
- `CALLABLE_BUT_USAGE_BLOCKED`
- `READY_FOR_EXP13_VIA_CLOUDFLARE_RELAY`

Do not invent another status.

## Evidence

Store under:

`evidence/exp-13/cloudflare-relay-preflight/`

Minimum:

- `README.md`
- `RESULT.json`
- `CLOUDFLARE_ACCESS.md`
- `ARENA_EGRESS.md`
- `PROVIDER_CONFIG.md`
- `SECURITY_BOUNDARY.md`

After provider calls, also:
- `ROUTE_A.md`
- `ROUTE_B.md`

Never store secrets.

## RESULT.json minimum

- result;
- cloudflare authenticated;
- cloudflare account id;
- worker name;
- worker deployed;
- Arena health reachability;
- relay auth mode;
- upstream hostname;
- credential secret binding name;
- credential installed: true/false;
- Route A callable;
- Route B callable;
- token usage available A/B;
- secrets stored in Git: false;
- Pilot Batch started: false;
- blocker;
- next action.

## Production boundaries

Do not modify:
- `grand-mebel-document-control`;
- `grand-mebel-accounting-cloudflare`;
- `minibase-cloudflare`;
- any existing production Worker;
- any D1/R2 production binding.

Do not reuse their production Worker names.

No database is needed for this preflight.

No queue is needed.

No persistent general proxy is authorized.

## Cleanup

If the relay is not adopted:
- document exact cleanup command;
- delete/revoke temporary Worker access material where practical;
- keep only sanitized evidence in Git.

If EXP-13 later adopts this transport, that is a separate owner decision and must update the frozen route/transport contract explicitly.

## Terminal report

```text
RESULT: <one allowed terminal status>
CLOUDFLARE AUTHENTICATED: YES/NO
CLOUDFLARE ACCOUNT:
WORKER NAME:
WORKER DEPLOYED: YES/NO
ARENA → WORKER HEALTH: PASS/FAIL/NOT_RUN
UPSTREAM CONFIG KNOWN: YES/NO
OPENCODE SECRET INSTALLED: YES/NO
ROUTE A CALLABLE: YES/NO/NOT_RUN
ROUTE B CALLABLE: YES/NO/NOT_RUN
ROUTE A TOKENS: OBSERVED/UNAVAILABLE/NOT_RUN
ROUTE B TOKENS: OBSERVED/UNAVAILABLE/NOT_RUN
SECRETS IN GIT: NO
PILOT BATCH STARTED: NO
PRODUCTION WORKERS MODIFIED: NO
BLOCKER:
NEXT ACTION:
```

## PR boundary

Open one bounded PR against `murat-project-engineer/main`.

Do not merge automatically.

If the run stops at `OWNER_SECRET_REQUIRED`, preserve the exact resumable state and wait for owner input.
