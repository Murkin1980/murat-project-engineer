# EXP-13 — Cloudflare relay preflight (evidence)

Authoritative instruction: `docs/experiments/EXP-13_CLOUDFLARE_RELAY_PREFLIGHT.md`
Date: 2026-10-10 · Base: `main` @ `a9881f1` · Branch: `arena/a244d1b4-murat-project-engineer`

## Result

```text
RESULT: CLOUDFLARE_AUTH_MISSING
CLOUDFLARE AUTHENTICATED: NO
CLOUDFLARE ACCOUNT: UNKNOWN (not returned; not observable from any accessible source)
WORKER NAME: mpe-exp13-opencode-relay (planned, NOT created)
WORKER DEPLOYED: NO
ARENA → WORKER HEALTH: NOT_RUN
UPSTREAM CONFIG KNOWN: NO
OPENCODE SECRET INSTALLED: NO
ROUTE A CALLABLE: NOT_RUN
ROUTE B CALLABLE: NOT_RUN
ROUTE A TOKENS: NOT_RUN
ROUTE B TOKENS: NOT_RUN
SECRETS IN GIT: NO
PILOT BATCH STARTED: NO
PRODUCTION WORKERS MODIFIED: NO
BLOCKER: No Cloudflare/Wrangler authentication in this runtime, and outbound HTTPS to
         api.cloudflare.com and *.workers.dev is blocked by the sandbox allowlist.
NEXT ACTION: Owner confirms Cloudflare auth in an authenticated environment (or grants
             this runtime a scoped token AND adds api.cloudflare.com + *.workers.dev to
             the egress allowlist), then re-run from PHASE 0.
```

The run stopped at the instruction's **PHASE 0 stop**. That stop is explicit: when
Cloudflare authentication is unavailable, return `CLOUDFLARE_AUTH_MISSING` and
**do not create relay code or request OpenCode Go credentials**. Both were honoured.

## Why PHASE 0 failed — three independent findings

1. **No authentication.** `npx --yes wrangler@4.143.0 whoami` returned
   `You are not authenticated. Please run 'wrangler login'.` No account id, no auth
   source. Note its exit code was 0 — the stdout line, not the exit code, is the
   signal. Details: `CLOUDFLARE_ACCESS.md`.

2. **No credential available to inject.** The complete environment variable name list
   contains no `CLOUDFLARE_API_TOKEN`, no `CLOUDFLARE_ACCOUNT_ID`, and no `CF_*` /
   `WRANGLER_*` name. Only `GH_TOKEN` and `GITHUB_TOKEN` (GitHub, not Cloudflare).
   There is no local Wrangler OAuth store either: `~/.config/.wrangler` holds only
   `logs/` and `metrics.json`, no `config/default.toml`. Both repositories named as
   the deployment-pattern authority (`grand-mebel-document-control`,
   `grand-mebel-accounting-cloudflare`) return **HTTP 403
   `Resource not accessible by integration`** to this runtime, so their real
   `wrangler.jsonc` / `wrangler.toml` and account id could not be inspected. The one
   readable reference repo (`minibase-cloudflare`) contains only
   `REPLACE_WITH_*` placeholders and no `account_id`.

3. **No egress even if a token existed.** DNS resolves but HTTPS connect fails
   (`curl` code `000`) for both `api.cloudflare.com` and
   `murat-project-engineer.muriktl.workers.dev`, while the control probe to
   `registry.npmjs.org` returns `200`. So `wrangler deploy` could not run from here,
   and PHASE 2's "verify Arena can reach the Worker" could never pass. Details:
   `ARENA_EGRESS.md`.

Finding 3 is separate from finding 1. Clearing authentication alone would **not**
complete this preflight inside Arena.

## What was checked

- Sync: local branch and `origin/main` are both `a9881f1`; `git merge origin/main`
  reported `Already up to date.`
- Mandatory reading: `AGENTS.md`, `docs/governance/SCOPE-CHANGE-CONTROL.md`,
  `docs/experiments/EXP-13_LOW_COST_EVALUATION_HARNESS.md`,
  `docs/experiments/EXP-13_OPENCODE_GO_PREFLIGHT.md`,
  `docs/experiments/EXP-13_ARENA_SECRET_PREFLIGHT.md`.
- `npx --yes wrangler@4.143.0 --version` → `4.143.0`; `whoami` → unauthenticated.
- Local Wrangler config store inspected by **path names only**.
- `wrangler secret put --help` → subcommand exists in the installed CLI, but is not
  usable here (no auth, no egress).
- `npx --yes wrangler@4.143.0 deploy --dry-run` on the repository root config →
  succeeded offline (`Read 11 files from the assets directory … /dist`,
  `No bindings found.`, `--dry-run: exiting now.`, exit 0). The toolchain is healthy;
  only auth and egress are missing.
- Egress probes to three hosts, one request each, no credentials.
- Repository searched for an OpenCode Go endpoint / auth scheme: **none present.**
  Details: `PROVIDER_CONFIG.md`.

## Live calls and spend

None. No Cloudflare deployment, no OpenCode Go call, no purchase, no top-up. Route A
and Route B are `NOT_RUN`; no token usage was observed and none was estimated.

## Files

- `RESULT.json` — machine-readable result and every check.
- `CLOUDFLARE_ACCESS.md` — PHASE 0 identity/credential transcript (sanitized).
- `ARENA_EGRESS.md` — egress probes and per-phase consequences.
- `PROVIDER_CONFIG.md` — what is and is not known about the OpenCode Go upstream.
- `SECURITY_BOUNDARY.md` — secret handling, diff scope, production boundaries, and
  the relay security contract that a future run must enforce.

## Boundaries preserved

- No relay code created; `experiments/exp-13/cloudflare-relay/` does not exist.
- No production Worker, D1 or R2 binding touched; no production repository modified.
- No secret created, bound, requested, or stored. Nothing sensitive in Git.
- EXP-13 Pilot Batch 1 not started; frozen routes, thresholds, dataset, pricing
  snapshot, pre-registration and adapter code unchanged.
- Terminal status is one of the eight allowed values; no new status was invented.

## Resumable state

Everything needed to resume is in this directory. The exact next checks are:

```bash
# In an authenticated environment (owner's machine, or CI with the token set):
npx --yes wrangler@4.143.0 whoami          # must print an account id
npx --yes wrangler@4.143.0 secret --help   # secret path usable once authenticated
```

Only after `whoami` prints an account **and** `api.cloudflare.com` plus
`*.workers.dev` are reachable should PHASE 1 (create the fixture under
`experiments/exp-13/cloudflare-relay/`, Worker name `mpe-exp13-opencode-relay`)
begin. The `OPENCODE_GO_API_KEY` binding name in `PROVIDER_CONFIG.md` is a proposal,
not an existing binding.
