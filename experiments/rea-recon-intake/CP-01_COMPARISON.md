# EXP-33 / CP-01 — existing-method comparison

## Consumer and question

The only consumer is the existing `experiments/privetmaket-backend-recon` CP-02. Its current result is PARTIAL because it produced public DOM diagnostics but could not obtain a CDP/DevTools Network trace.

## Comparison

| Method | Current evidence | Gap for PrivetMaket | REA incremental potential | Result |
|---|---|---|---|---|
| Existing public DOM/route evidence | Product pages, route surface, WebGL/DOM diagnostics; no login or mutating requests | No browser Network/HAR facts | None required for this evidence class | KEEP_EXISTING |
| Manual DevTools/HAR in an authorized browser | Would provide the missing network manifest if a browser is available | No browser/CDP in this environment | REA documents browser-capture tools and evidence output | CANDIDATE, unproven |
| REA static JS/app analysis | Upstream documents JavaScript/Electron analysis | No downloaded or owner-supplied app bundle/artifact | Could inspect a local permitted artifact; not a replacement for live browser network observation | NOT APPLICABLE to current target |
| REA setup/MCP integration | Upstream supports Codex registration | Adds MCP/configuration surface | Exceeds this experiment's no-install/no-configuration boundary | REJECT FOR THIS RUN |

## Decision

REA is not a duplicate of the existing documentation/DOM path: it may help only if it can produce a lawful, redacted browser capture in an approved environment. But it cannot be credited with measurable value here because no package execution or capture occurred.

**CP-01 result: PARTIAL.** Keep the existing PrivetMaket evidence; do not adopt REA or add it to MPE tooling.
