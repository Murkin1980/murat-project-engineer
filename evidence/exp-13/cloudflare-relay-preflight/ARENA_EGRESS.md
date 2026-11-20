# EXP-13 Cloudflare relay preflight — Arena egress check

Sanitized transcript. No credentials involved.
Date: 2026-10-10 · Base: `main` @ `a9881f1`

## Result

**`KNOWN_BLOCKED`.** This runtime cannot reach either the Cloudflare management API
or any `*.workers.dev` host. This blocks the preflight independently of
authentication: even with a valid token, `wrangler deploy` would fail here, and
Arena could never satisfy the PHASE 2 requirement "verify Arena can reach the
Worker endpoint".

## Probe

One probe per host, no credentials, 12 s connect timeout:

```bash
for h in api.cloudflare.com \
         murat-project-engineer.muriktl.workers.dev \
         registry.npmjs.org ; do
  getent hosts "$h"                                   # DNS
  curl -s -o /dev/null -w "%{http_code}" "https://$h/"  # TLS + HTTP
done
```

| Host | DNS | HTTPS result |
|---|---|---|
| `api.cloudflare.com` | OK (resolves) | `000` — connect failed |
| `murat-project-engineer.muriktl.workers.dev` | OK (resolves) | `000` — connect failed |
| `registry.npmjs.org` (control) | OK (resolves) | `200` |

Raw:

```text
api.cloudflare.com                             DNS=OK(2606:4700:300a::6813:c0b0) HTTPS=000 CONNECT=FAIL
murat-project-engineer.muriktl.workers.dev     DNS=OK(2606:4700:3031::6815:39e3) HTTPS=000 CONNECT=FAIL
registry.npmjs.org                             DNS=OK(2606:4700::6810:a22) HTTPS=200
```

Notes:

- `000` is curl's "no HTTP response received" code — a transport-level failure, not
  a 4xx/5xx from Cloudflare. It means the connection never completed.
- DNS resolution succeeding but the connection failing is the expected signature of
  an egress allowlist rather than a broken network.
- The `registry.npmjs.org` control returning `200` proves the probe method itself
  works, so the two failures are specific to those hosts.

## Sandbox outbound allowlist (observed)

`github.com`, `codeload.github.com`, `api.github.com`, `registry.npmjs.org`,
`pypi.org`, `files.pythonhosted.org`.

Neither `api.cloudflare.com` nor `*.workers.dev` is on it.

## Consequences for the instruction's phases

| Phase | Requirement | Status |
|---|---|---|
| PHASE 0 | `wrangler whoami` identity check | Ran. Result: not authenticated. |
| PHASE 1 | Create relay fixture | **Not attempted** — PHASE 0 stop. |
| PHASE 2 | Deploy health-only Worker | Impossible from here (management API unreachable). |
| PHASE 2 | "Arena can reach the Worker endpoint" | Impossible from here (`*.workers.dev` unreachable) → would be `ARENA_EGRESS_TO_WORKER_BLOCKED` even if auth existed. |
| PHASE 3 | Owner installs secret | Not reached. |
| PHASE 4 | Two tiny provider calls | Not reached. |

Two independent blockers exist. Clearing authentication alone is **not** sufficient
to complete this preflight inside Arena; the egress allowlist must also include
`api.cloudflare.com` (for deploy) and `*.workers.dev` (for health verification).

This also matches the earlier EXP-13 finding in
`evidence/exp-13/opencode-go-preflight/RESULT.json` (`egress_note`), which recorded
the same allowlist and that no OpenCode Go endpoint is on it.

## No probing of the provider

No OpenCode Go endpoint was resolved or contacted. See `PROVIDER_CONFIG.md`.
