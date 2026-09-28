# Strix Pilot Evidence

Date: 2026-08-14
Target: `Murkin1980/mebeldocs-ai`
Baseline commit: `fad30491a851825018cbab6aa1fbae0c60857627` (`main`)
Decision: `HOLD`

## New Idea Filter

Primary disposition: `EXTEND_EXISTING`.

Strix is evaluated only as an optional Security Validation capability inside Murat Project Engineer. No new repository, runtime, Router authority, or portfolio-wide rollout is introduced.

## Baseline

```yaml
repository: Murkin1980/mebeldocs-ai
commit_sha: fad30491a851825018cbab6aa1fbae0c60857627
branch: main
working_tree_clean: true
runtime: Node.js / Next.js 16.2.10 / TypeScript
package_manager: npm
install_command: not_run_dependencies_already_present
test_command: npm test
tests_passed: 197
tests_failed: 2
lint: PASS (tsc --noEmit)
typecheck: PASS
build: PASS
existing_security_checks: auth/access tests, company isolation checks, XML size/format checks, public-contract leakage tests
existing_agent_rules: AGENTS.md
existing_review_process: repository rules plus Murat Project Engineer VERIFIED/security review
approximate_duration: not_measured
```

The two test failures were sandbox write denials (`EPERM`) while creating a PDF fixture and an idempotency-event fixture. They are not attributed to Strix or to application defects. The production build completed successfully.

## Execution gate

`docker --version` and `docker info` could not run because Docker is not installed or available on PATH.

```text
STRIX_EXECUTION = BLOCKED_DOCKER
```

Official CLI documentation was checked on 2026-08-14. It confirms scan modes `quick`, `standard`, and `deep`, Docker-unavailable exit behavior, headless exit codes, and optional spend/turn limits. No CLI was installed and no scan was run because the documented runtime prerequisite failed.

## Findings and value gate

```text
total_findings: 0
validated_findings: 0
false_positives: 0
meaningful_vulnerabilities: 0
previously_detected_by_tests: 0
previously_detected_by_codex_review: 0
novel_meaningful_findings: 0
fixed_findings: 0
successful_retests: 0
operational_complexity: HIGH (blocked prerequisite)
approximate_runtime: not_observable
approximate_model_cost_if_observable: not_observable
```

No vulnerability claim is made. The repository's static pilot authentication context was visible to normal Codex review and therefore could not become a novel Strix finding even in a later scan without additional evidence that it violates the explicitly documented pilot boundary.

## Terminal recommendation

```text
STRIX_DECISION: HOLD
```

Reason: evidence is insufficient because execution was blocked before scanning. A future retry may use a local Docker-enabled environment, `quick` mode first, an explicit spend limit, and the exact same commit or a newly recorded baseline. Do not run against production or real documents.


---

## Retry registration — 2026-09-26

Source project: https://github.com/usestrix/strix

### New Idea Filter

Primary disposition: `EXTEND_EXISTING`.

This is not a new experiment identity. It reopens `EXP-07` for a controlled Strix retry because the 2026-08-14 Strix phase was blocked before any scan ran. The historical evidence above remains authoritative for the first attempt.

### Purpose

Test whether current Strix can add meaningful, reproducible security findings beyond existing tests and normal Codex/Arena review for an existing MPE-owned service.

### MVP scope

- Use exactly one authorized, low-blast-radius MPE-owned target.
- Prefer repository + non-production/staging URL when both are available and explicitly authorized.
- Start with Strix `quick` mode.
- Require Docker-enabled execution outside the smartphone.
- Set an explicit spend/turn limit before execution.
- No automatic fixes.
- No CI/CD gate.
- No production-wide rollout.
- No new repository or parallel security platform.
- Store raw report, validated findings, false positives, runtime and observable model cost as evidence.

### Acceptance

`PASS`
: At least one meaningful, reproducible finding is discovered that existing project tests and ordinary review did not already surface, with acceptable operational cost.

`WARNING`
: Strix runs successfully but produces only already-known issues, low-value findings, or operational overhead that is not yet justified.

`BLOCKED`
: Runtime/prerequisite/credential/environment failure prevents a valid scan, or evidence cannot be validated.

### Promotion gate

Even after `PASS`, do not promote Strix to a portfolio-wide security gate automatically. A separate decision is required before CI integration, auto-fix, recurring scanning, or use against production.

### Next action

Run one bounded quick scan in a Docker-enabled environment and record the result under this same `EXP-07` identity.
