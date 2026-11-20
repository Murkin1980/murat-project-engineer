# Secret mechanism assessment

## Disposition

`NO_SUPPORTED_SECRET_MECHANISM` for owner/admin-provisioned OpenCode Go credentials in the current Arena runtime.

This is scoped to the runtime and interfaces exposed to this task. It does not make a claim about a different Arena deployment or an owner/admin console that is not exposed here.

## Mechanisms checked

| Candidate | Observation in this runtime | Assessment |
|---|---|---|
| Arena/platform secret store | No secret-store interface or owner/admin secret configuration was exposed to this task. | Not available to this runtime. |
| Environment secret injection | A variable-name-only scan found `GH_TOKEN` and `GITHUB_TOKEN`; no OpenCode, Codex Router, or general provider credential variable name was present. These are GitHub integration credentials, not an arbitrary OpenCode Go binding. | No supported owner/admin injection path for this credential was found. No values were read or printed. |
| Workspace/repository/session binding | No such binding or configuration surface was exposed by the current task/runtime tools. | Not available to this runtime. |
| Runtime-mounted secret | `/run/secrets`, `/var/run/secrets`, `/mnt/secrets`, and `/etc/secrets` were absent. `/run/credentials` had only empty systemd service directories; no credential files were present. | No usable OpenCode Go secret mount was found. Names/existence only; no file contents were read. |
| Provider/CLI configuration | The checked OpenCode/Codex paths (`~/.codex`, `~/.codex/codex-router`, `~/.codex/config.toml`, `~/.codex/auth.json`, `~/.config/opencode`, `~/.local/share/opencode`, `~/.opencode`, and `~/.opencode-mobile`) were absent. `opencode` was not on `PATH`. | No provider configuration or CLI credential source was available. |

The local `.devcontainer/start-opencode.sh` uses `OPENCODE_SERVER_PASSWORD` for HTTP Basic Auth to its optional OpenCode Mobile `opencode serve` process. That is not an OpenCode Go provider credential or an Arena secret binding; the script was not run.

## Frozen EXP-13 credential shape

- `experiments/exp-13/routes.json` freezes only model slugs: `opencode-go/deepseek-v4-flash` and `opencode-go/kimi-k2.7-code`.
- `skills/murat-project-engineer/references/route-profiles.md` describes these as Codex Router model routes. It does not define a credential field, environment-variable name, provider URL, or base URL.
- Therefore the only defensible minimum is a provider-authentication credential accepted by the existing `opencode-go` provider in the Router. The exact field/key and credential form are **not defined** by the checked canonical configuration; no key name is guessed.
- The frozen route path does not require the OpenCode CLI; it is expressed as Codex Router model slugs. Whether direct provider/API access alone would satisfy the existing route and usage-evidence path is **unknown**.
- Whether a base URL/provider configuration is required is **unknown** because the frozen configuration contains no endpoint/provider settings.

## Non-Git, logs, and revocation boundary

- No credential was committed, staged, or stored in the repository. No local `.env` or generated OpenCode Mobile connection file was present at the checked paths.
- Because no supported injection mechanism was found, a non-Git injection path is **not confirmed**. Do not interpret `GIT REQUIRED: NO` in `RESULT.json` as evidence that a safe alternate path exists; it records only that no secret was placed in Git.
- Default log masking, runtime-only readability, and revocation/rotation independent of repository history could not be tested. Their status is **unknown**, not assumed safe.
- Secret values do not appear in this evidence. Only sanitized mechanism names, environment variable names, and path-presence results are recorded.
