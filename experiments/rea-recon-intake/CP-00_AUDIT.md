# EXP-33 / CP-00 — REA and environment audit

**Date:** 2026-11-05 UTC  
**Mode:** read-only; no REA installation, setup, configuration write, browser launch, target request, merge, or deploy.

## Upstream identity and scope

- Upstream read: `morluto/rea`, files `README.md`, `LICENSE`, `package.json`, and `docs/installation.md`.
- Package named by upstream: `rea-agents`; the package runner resolved the requested package name to `rea-agents@6.8.0`.
- License text present upstream: MIT.
- Upstream says REA supports browser/web investigation, but its documented setup registers an MCP server and can write agent configuration. That setup path is out of scope for this experiment.
- Upstream documents Node 22.x >=22.23.4, 24.x >=24.22.1, or 26.12.1+. Environment Node is `v24.22.1`, so the Node version gate alone is met.

## Environment facts

| Check | Observed result |
|---|---|
| `node --version` | `v24.22.1` |
| `npm --version` | `11.9.0` |
| `command -v rea` | no executable found |
| `command -v chromium`, `google-chrome`, `playwright` | no executable found |
| direct non-install package probe | package absent; see CP-02 |

The previous PrivetMaket CP-02 record states that this execution context lacked CDP DevTools/Chromium and could not collect a browser Network map. This audit independently finds no REA executable or browser executable in PATH.

## Security and scope result

REA itself is not assessed as unsafe. However, obtaining and executing it would require package acquisition, while installation/setup/configuration is explicitly outside this run. There is also no local authorized target artifact and no browser runtime for a web capture.

**CP-00 result: PASS (audit only).** This does not establish REA functional capability or eligibility for adoption.
