# Changelog

## Unreleased — Stage 2 (2026-08-13)

- Added EXP-12 CLEARS deterministic triage contracts, stateless prototype, 20-case retrospective dataset, tests and evidence.
- Recorded 20/20 retrospective fixture agreement with zero DEEP-CHANGE false negatives; prospective accuracy remains NOT_OBSERVABLE pending pre-registered validation.
- Applied Router-review safety rework: maximum architectural impact cannot fall below DEEP-CHANGE/human approval, and runtime input validation enforces the triage contract.

- Activated `docs/NEW_IDEA_FILTER_POLICY.md` as a mandatory portfolio gate for new products, features, services, agents, plugins, integrations, automations, repositories and substantial technical ideas.
- Added `docs/OPERATING_MODEL.md` to connect portfolio dispositions (`EXTEND_EXISTING`, `REUSE_COMPONENT`, `MERGE`, `EXPERIMENT`, `HOLD`, `NEW_REPOSITORY`, `REJECT`) with the existing FAST / VERIFIED / DEEP-CHANGE execution model.
- Recorded Run 06 as a FAST coordinator run for status/operating-model synchronization.
- Preserved Run 05 as historically BLOCKED pending real repository-local package validator and unit-test execution; no retroactive PASS was claimed.
- Continued Option A+ without introducing a daemon, scheduler, generic workflow engine, persistent runtime agents, adaptive routing, autonomous memory promotion, Router authority changes, Prime runtime, mandatory external context providers or Workspace UI.

## Unreleased — Stage 2A (2026-08-11)

- Added `contracts/RUN_REPORT.schema.json` and `contracts/RUN_REPORT.example.json` without replacing the Markdown Run Report contract.
- Added machine-readable Experiment Record schema/example beside the existing Markdown template.
- Added explicit nullability for historically unobservable baseline metrics so `unknown` is not encoded as a false zero.
- Added `context/CONTEXT_MAP.md` for progressive source-of-truth disclosure by task class and Expert role.
- Added `docs/CONTEXT_PROVIDERS.md` with replaceable Project, Repository, Documentation, Live Web and User context-provider categories.
- Kept Docsalot and Context.dev optional/documented only; no runtime dependency was introduced.
- Captured real-work evidence for Stage 2A Runs 01–05 using four historical baselines and one resumed coordinator run.
- Added `STAGE2A_FIRST5_REVIEW.md` with risk distribution, baseline/coordinator observations, recovery findings, evidence-format findings and `CONTINUE_20_RUNS` recommendation.
- Preserved Option A+ boundaries: no daemon, scheduler, workflow engine, persistent agents, adaptive routing, autonomous memory promotion, Router authority change, Prime runtime or Workspace UI.
- Current Run 05 remains BLOCKED pending repository-local package validator and unit-test execution in a local/Codex environment; no unverified PASS was recorded.

## 1.0.0 — 2026-08-10

- Added the coordinator skill, four Expert contracts and three temporary Team definitions.
- Added FAST, VERIFIED, DEEP-CHANGE and Software Feature Playbooks.
- Added 12 Review Gates, context manifest, typed handoff and Run Report.
- Added deterministic validation and an isolated sample run.
- Preserved Codex, Router, MASTER, credentials and persistent-agent boundaries.
