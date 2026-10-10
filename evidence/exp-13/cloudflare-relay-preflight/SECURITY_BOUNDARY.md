# EXP-13 Cloudflare relay preflight — security boundary

Date: 2026-10-10 · Base: `main` @ `a9881f1` · Branch: `arena/a244d1b4-murat-project-engineer`

## Secret handling in this run

| Rule | Status |
|---|---|
| No credential value read, printed, logged, or stored | **Confirmed** |
| No secret created or bound in Cloudflare | **Confirmed** — none exists; auth is missing |
| No credential committed to Git | **Confirmed** — see diff scope below |
| No credential in `wrangler.jsonc` or any env file | **Confirmed** — no config file was created or edited |
| No credential copied into evidence | **Confirmed** — evidence contains only command names, redacted names, HTTP codes, and exit codes |
| OpenCode Go credential requested | **NO** — the instruction forbids requesting it at a PHASE 0 stop |

Environment inspection recorded **variable names only** (`env | cut -d= -f1`, and
`grep … | sed -E 's/=.*/=<REDACTED>/'`). No value was ever emitted. The transcript in
`CLOUDFLARE_ACCESS.md` §2 is the complete name list.

## Diff scope of this run

Additions only, all under one evidence directory:

```text
evidence/exp-13/cloudflare-relay-preflight/
├── README.md
├── RESULT.json
├── CLOUDFLARE_ACCESS.md
├── ARENA_EGRESS.md
├── PROVIDER_CONFIG.md
└── SECURITY_BOUNDARY.md
```

No source code, no `wrangler.jsonc`, no `package.json`, no workflow file, no frozen
EXP-13 artifact (`routes.json`, `thresholds.json`, `pricing_snapshot.json`,
`tasks_v2.json`, `PILOT_BATCH1_PRE_REGISTRATION.json`) was modified.

No files were created under `experiments/exp-13/cloudflare-relay/`. The instruction's
PHASE 0 stop explicitly forbids creating relay code when Cloudflare authentication is
unavailable, so the relay fixture does not exist. There is nothing to clean up in
Cloudflare, because nothing was deployed.

## Production boundaries

| Boundary | Status |
|---|---|
| `grand-mebel-document-control` modified | **NO** — HTTP 403; not even readable, let alone changed |
| `grand-mebel-accounting-cloudflare` modified | **NO** — HTTP 403; not even readable, let alone changed |
| `minibase-cloudflare` modified | **NO** — read-only shallow clone into `/tmp` (outside the repository) |
| Any existing production Worker modified | **NO** — no `wrangler deploy` ran; only `deploy --dry-run`, which exits before any upload |
| Production Worker names reused | **NO** |
| Any D1/R2 production binding touched | **NO** — none declared, none referenced |
| Database / queue created | **NO** |
| Persistent or general-purpose proxy created | **NO** |

The one Wrangler invocation against real config was
`npx wrangler@4.143.0 deploy --dry-run`, which ended with `--dry-run: exiting now.`
and uploaded nothing. The repository's root `wrangler.jsonc` (`murat-project-engineer`
static dashboard) was not edited.

## Relay security contract — still to be enforced later

Recorded so the boundary is not lost when the preflight is eventually resumed. A
future relay must, at minimum:

- accept **POST only** on one relay endpoint, plus a health endpoint that makes no
  provider call;
- allow **only** `opencode-go/deepseek-v4-flash` and `opencode-go/kimi-k2.7-code`;
  reject every other model with 4xx;
- reject arbitrary upstream URLs, caller-supplied upstream hosts, and caller-supplied
  header forwarding; it must never become a general-purpose proxy;
- enforce a strict request-size limit and a maximum output-token limit;
- not stream unless required;
- apply a hard per-test request cap;
- fail closed when the `OPENCODE_GO_API_KEY` binding is absent (503, no provider
  call) — this is what makes the health-only PHASE 2 deploy safe before the owner
  installs the secret;
- log only sanitized metadata (timestamp, route/model, relay request id, status,
  latency, input/output/total tokens, observed cost if supplied) and **never**
  authorization headers, prompts, or secret values;
- be authenticated from the caller side by a bounded mechanism — never an open
  public spend proxy.

## Relay authentication from Arena — open question

Not determined in this run. Arena has no generic secret injection available here
(the only token-bearing environment variables are GitHub tokens), and no
Cloudflare-native access mechanism was observable. Per the instruction's ordering,
the first choice would be a Cloudflare platform-native mechanism, then a temporary
single-purpose unguessable test URL scoped to this preflight with strict call limits
and immediate revocation. If neither can be implemented safely the correct status is
`ARENA_TO_RELAY_AUTH_BLOCKED`. That gate is downstream of the current stop and was
not reached.

## Cleanup

Nothing to clean up. No Worker, no secret, no binding, no deployment exists. If a
future run creates the Worker, the documented cleanup is:

```bash
npx --yes wrangler@4.143.0 delete mpe-exp13-opencode-relay
npx --yes wrangler@4.143.0 secret delete OPENCODE_GO_API_KEY --name mpe-exp13-opencode-relay
```

Both require authentication that this runtime does not have.
