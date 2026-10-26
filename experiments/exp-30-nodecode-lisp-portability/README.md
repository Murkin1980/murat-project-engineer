# EXP-30 — Nodecode Lisp Cells and Portable LLM Artifacts

- **MPE decision:** EXPERIMENT
- **Status:** PLANNED / QUEUED
- **Owner:** Murat Project Engineer
- **Date:** 2026-10-25
- **Scope:** research-only, no integration or deployment.
- **Related:** EXP-002 Machine Protocol (MPE IR), existing Arena isolation and reusable skills.

## Research hypotheses

1. Nodecode can define, test, persist and reuse a small Common Lisp Cell across isolated sessions, with provenance and reproducible rollback.
2. Reuse offers measurable savings over the same tasks performed with existing Arena agents, without increasing error or privilege risk.
3. S-expressions may be useful as an optional executable **view** or DSL for agents, but should **not** replace the canonical Task Packet, schema-validated MPE IR (JSON), or verified evidence records without independent cross-model proofs.

## Checkpoints
- **CP-01 — Verification:** identify the canonical active Nodecode source, version, licensing, installation path, threat model, Cells Hub publication boundaries and maintenance signal. Note any discrepancy between legacy Rust and current Lisp documentation. STOP if source is not reviewable.
- **CP-02 — Isolated evaluation:** use disposable sandbox with no secrets, credentials, host FS, live network or merge rights. Benchmark 3 repeated tasks against current Arena flow. Record actual run traces, tests, wall clock, tokens/cost, persistence/rollback, dangerous-operation denials. Never auto-promote generated code.
- **CP-03 — Portable artifact:** encode one frozen EXP-002-like task in JSON MPE IR and S-expressions, run cross-model semantic interpretation and validation, measure parse ambiguity, deterministic round-trip, token cost and evidence provenance. Keep JSON authoritative throughout.
- **CP-04 — Review:** propose REUSE_COMPONENT / HOLD / REJECT recommendation based on results and new MPE filter review; independent owner approval required for any changes to runtimes or deep-change governance.

## Acceptance
- 100% core regression tests and no unauthorized writes, privileges, network or infrastructure access.
- Trusted tool-generated evidence; model self-report is not execution proof.
- Repeated tasks: target >=20% lower time or cost compared with controlled baseline, with equal or better correctness; an exploratory target, not a claimed result.
- No change to MPE Constitution, AGENTS.md, Task Packet source of truth, existing machine interface or production infrastructure.
- Record verifiable sources, exact refs and limitations.

**STOP:** Do not run CP-02/03 without the normal Arena task authorization. No auto merge, deploy, dependency installation, or publication to Cells Hub.
