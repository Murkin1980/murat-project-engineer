# EXP-33 — REA reconnaissance

**Status:** PARTIAL  
**Decision:** EXPERIMENT  
**Disposition:** DO_NOT_ADOPT for the current environment  
**Date:** 2026-11-05  
**Upstream:** https://github.com/morluto/rea  
**Consumer:** existing PrivetMaket Recon CP-02  
**VRU:** 0

## Objective

Assess whether REA can lawfully and safely close the existing PrivetMaket CP-02 evidence gap: an anonymous, redacted browser-network capture that existing public DOM/route collection could not produce.

## Bounded execution

This run used no Arena, no REA installation, setup, MCP registration, browser launch, live-target request, deployment, merge, new EXP, or persistent infrastructure.

| Checkpoint | Result | Record |
|---|---|---|
| CP-00 — REA and environment audit | PASS (audit only) | [CP-00_AUDIT.md](CP-00_AUDIT.md) |
| CP-01 — existing-tool comparison | PARTIAL | [CP-01_COMPARISON.md](CP-01_COMPARISON.md) |
| CP-02 — isolated read-only test | BLOCKED | [CP-02_READ_ONLY_TEST.md](CP-02_READ_ONLY_TEST.md) |
| CP-03 — results and evidence | PARTIAL | [CP-03_RESULTS.md](CP-03_RESULTS.md) |

## Result

REA may offer a non-duplicate browser-capture capability in an approved environment. It did not run here: the package is absent, acquisition/setup was outside authority, and no browser executable is available. The permitted `npx --no-install rea-agents --help` probe exited 1 because `rea-agents@6.8.0` was missing.

No functional capture occurred; therefore this experiment does not claim PASS or adoption.

## Boundary

Do not use this result as authority to install REA, configure it for Codex, run it against PrivetMaket, collect protected data, bypass controls, or start a follow-on experiment. Any later work requires separate owner authorization, package-acquisition review, a controlled browser environment, and an explicitly permitted target.

## Next action

STOP at CP-03. Preserve the existing PrivetMaket recon and this evidence; no further action is authorized by this PR.
