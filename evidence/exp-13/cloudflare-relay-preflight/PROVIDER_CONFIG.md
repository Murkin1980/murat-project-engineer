# EXP-13 Cloudflare relay preflight — OpenCode Go provider configuration

Sanitized. No credentials involved. No provider endpoint was contacted.
Date: 2026-10-10 · Base: `main` @ `a9881f1`

## Result

**Upstream configuration NOT established.** The relay's upstream hostname and
authentication scheme are unknown from every source available to this run. Nothing
was guessed.

This file records the state at the PHASE 0 stop. It is *not* the terminal status of
the run — the run stopped earlier, at `CLOUDFLARE_AUTH_MISSING`, so
`OPENCODE_PROVIDER_CONFIG_UNKNOWN` was not returned as a result. It is recorded
here because it is a second, independent gate that would still have to be cleared
before any relay code could hard-code an upstream.

## What the repository does establish

Frozen route slugs, from `experiments/exp-13/routes.json` (`exp-13-routes-v1`,
frozen 2026-08-21) — these are model slugs, not endpoints:

| Route | Profile | Slug |
|---|---|---|
| A | `cheap-research` | `opencode-go/deepseek-v4-flash` |
| B | `coding` | `opencode-go/kimi-k2.7-code` |
| premium | `strong-review` | `gpt-5.6-sol` (out of scope for this preflight) |

`docs/experiments/EXP-13_LOW_COST_EVALUATION_HARNESS.md` references the same two
slugs and shows the adapter being invoked with `--provider opencode-go --model
opencode-go/deepseek-v4-flash`. That is a local telemetry-adapter interface, not a
network endpoint.

## What is absent

Searched this repository (excluding `node_modules`) for an authoritative endpoint or
auth scheme:

- Files mentioning `opencode-go` / `OpenCode Go`: contracts (`USAGE_RECORD.md`,
  `USAGE_RECORD.example.json`, `RUN_REPORT.example.json`, `COMPUTE_BUDGET.example.json`),
  EXP-12/EXP-13 instruction documents, and the existing EXP-13 preflight evidence.
  All of them carry the provider *slug* only.
- Regex for a candidate host (`opencode*.{com,dev,io,ai,net}`, `api.opencode`,
  `opencode.ai`) across `.md` / `.json` / `.sh` / `.py`: **zero matches.**

So the repository contains no base URL, no auth header name, and no credential field
name for OpenCode Go.

## Runtime configuration

Absent, consistent with the earlier EXP-13 preflight:

- `~/.codex/`, `~/.codex/config.toml`, `~/.codex/auth.json`,
  `~/.codex/codex-router/usage-events.jsonl` — absent.
- `~/.config/opencode/`, `~/.local/share/opencode/`, `~/.opencode/`,
  `~/.opencode-mobile/` — absent.
- `opencode` / `codex` binaries — not on `PATH`.

`.devcontainer/start-opencode.sh` starts a local `opencode serve` on port 4096 with
HTTP Basic Auth for a mobile client. That is a local mobile-server credential, not a
provider credential, and it does not define an OpenCode Go API endpoint or auth
scheme. It is not usable as the relay's upstream authority.

## Why no external documentation lookup resolved it

Establishing the endpoint from official provider documentation would have required
outbound web access outside the sandbox allowlist
(`github.com`, `codeload.github.com`, `api.github.com`, `registry.npmjs.org`,
`pypi.org`, `files.pythonhosted.org`). No provider documentation host is on it.
Rather than infer a hostname from the slug, the run stopped — the instruction is
explicit: "Do not guess endpoint hostnames, auth header names, or credential
fields."

## Proposed binding name (not created, not bound)

If and when a relay is authorized, the credential should exist only as a Cloudflare
Worker secret. The name used consistently in this evidence set is:

```text
OPENCODE_GO_API_KEY
```

This is a **proposal**, not an existing binding. No secret was created, bound, or
requested in this run.

## Gate before PHASE 1 relay code

Before any relay hard-codes an upstream, the owner must supply, from official
provider documentation or existing trusted configuration:

1. the authoritative base URL / hostname;
2. the authentication scheme and exact header name;
3. the exact request/response shape, including where token usage is returned
   (EXP-13 requires real, attributable usage — no estimates);
4. confirmation that both frozen slugs are valid model identifiers on that endpoint.

Until those four are recorded here with their source, upstream config stays
`UNKNOWN`.
