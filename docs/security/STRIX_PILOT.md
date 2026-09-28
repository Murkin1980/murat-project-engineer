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
- Commit only the sanitized evidence artifact defined in `Evidence handling and raw-output boundary`; raw Strix output never enters Git.

### Evidence handling and raw-output boundary (mandatory)

`RAW_STRIX_OUTPUT_NEVER_COMMITTED`

Raw penetration-test evidence **must not** be committed to this repository. Prohibited in Git, in any branch, PR, issue, comment, log or artifact:

- raw Strix output: reports, console/TUI logs, `strix_runs/**` directories, agent transcripts, sandbox captures;
- exploit payloads and working proofs of concept;
- exploitable endpoints, routes, hosts, parameters, or step-by-step reproduction of an attack;
- source-code excerpts that show how to exploit a finding;
- secrets, tokens, credentials, connection strings, configuration fragments;
- sensitive vulnerability details that would help an attacker before remediation lands.

Raw evidence lives **only** in access-controlled temporary/local storage: the Strix sandbox output directory (`strix_runs/<run-name>`) on the operator machine, or an owner-controlled store outside Git. It is never pushed, never pasted into a PR, and is retained or deleted by owner decision. `.gitignore` blocks `strix_runs/` and raw capture patterns.

What **may** be committed — a sanitized artifact containing at most:

- sanitized summary of the run;
- vulnerability class (for example `broken access control`) without exploit steps;
- affected component/path, only as far as needed to act on it, without exploit details;
- severity;
- reproduction status (`reproduced` / `not_reproduced` / `not_attempted`);
- whether the finding was already detected by existing tests, linters/static analysis, security checks, existing issues, or ordinary code review;
- remediation state (`open` / `fixed` / `accepted_risk` / `false_positive`);
- evidence hash or reference to the raw artifact when the reference itself is safe (path + `sha256`, never content).

Every committed EXP-07 artifact carries an explicit sanitization statement. A finding that cannot be described safely is recorded as `withheld — see access-controlled raw evidence <sha256>` instead of being pasted into the repository. No secrets and no working exploit payloads in Git, without exception.

### Target and baseline freeze (mandatory before any Strix run)

`BASELINE_FREEZE_REQUIRED_BEFORE_SCAN`

Exactly one MPE-owned target per retry. Before Strix starts, the sanitized artifact must record:

- repository;
- branch;
- exact commit SHA;
- scan scope (the paths Strix may read and test);
- excluded paths;
- current test result (command, counts, exit status);
- current build/typecheck result, if applicable;
- existing static/security checks that already run on the target;
- current known security issues;
- ordinary code-review baseline (what was reviewed and what it already found).

Hard gate: `STRIX_RUN_BEFORE_BASELINE_FREEZE = FORBIDDEN`. If any item cannot be recorded truthfully for the chosen commit, the retry is `BLOCKED` — inherited or estimated values from another commit are not a baseline. If no suitable bounded target exists, return `BLOCKED`; do not scan an unsuitable target just to produce output.

Purpose: after the scan it must be provable whether Strix found anything that ordinary tests, review, and existing security checks did **not** already find.

Execution-authority boundary: `STRIX_WRITABLE_MOUNT_FORBIDDEN`. The documented Strix CLI mounts a local target directory **writable** (the agent can edit real files, `.git` excepted), so Strix must never be pointed at a live working tree. Scan a clean clone/checkout of the frozen SHA (or the repository URL), commit or stash first, keep `--scope-mode` explicit, set `--max-turns` and `--max-budget` before starting, and refuse Strix fix/autofix affordances. Strix receives no execution authority over MPE code, no CI gate, and no automatic remediation.

#### Frozen retry target — 2026-09-28

```yaml
repository: Murkin1980/mebeldocs-ai
branch: main
commit_sha: 2d6d60b240f8f4e2546cf451433c8f1ff0aad65a
target_kind: owner-controlled code target (no live or production URL in scope)
scan_scope:
  - apps/web/app
  - apps/web/lib
  - apps/web/components
  - apps/web/tests
excluded_paths:
  - docs/**
  - data/**
  - design/**
  - tools/**
  - repository-root *.md
  - apps/web/node_modules/**
  - apps/web/.next/**
  - apps/web/package-lock.json
  - apps/web/tsconfig.tsbuildinfo
scan_mode: quick
scope_mode: full
planned_command: strix -n --target <clean-clone-at-frozen-sha> --scan-mode quick --scope-mode full --max-turns 200 --max-budget 15
live_target_url: none (no production or staging dynamic testing in this retry)
```

Baseline recorded at the frozen SHA (executed 2026-09-28, Arena sandbox, Node v22.22.3 / npm 10.9.8, clean shallow clone):

```yaml
baseline_status: PASS
install: npm ci -> exit 0
tests: npm test -> 202 tests, 202 pass, 0 fail, 0 skipped, exit 0
typecheck: npm run lint (tsc --noEmit) -> exit 0
build: npm run build (next build) -> exit 0 (21 API routes plus pages)
existing_static_security_checks: npm test suite (auth-guard, esf-xml-parser, pdf, integration, domain, pilot) and tsc --noEmit only; the target repository has no CI workflow, no SAST/DAST, no dependency scanning and no secrets scanning
known_security_issues: pilot-mode hardcoded server context (no real authentication; every caller is one owner identity of one company) documented as a pilot limitation while SECURITY.md requires roles, 2FA and company isolation before production; some API routes return internal error messages to clients
ordinary_code_review_baseline: manual review of lib/auth/server-context.ts, app/api/esf/import/route.ts, app/api/pilot/route.ts, lib/esf/xml-parser.ts and lib/storage/local-repositories.ts found no child_process/eval/new Function/dangerouslySetInnerHTML, an enforced 10 MB XML input cap and 10k text truncation on ESF import, user-supplied filename stored as metadata only (not used to build filesystem paths), and companyId filtering in list operations
```

The 2026-08-14 baseline (`mebeldocs-ai@fad30491a851825018cbab6aa1fbae0c60857627`, 197 pass / 2 fail) belongs to the first attempt and **must not** be reused for novelty comparison in this retry.

### Acceptance

These are **execution outcomes** of one retry, not registry statuses. A successful Strix start is not by itself a `PASS`: `PASS` requires measured additional value.

`PASS`
: Strix actually ran and produced at least one confirmed, actionable finding that existing tests, linters/static analysis, security checks, existing issues and ordinary code review did not already surface — or convincing evidence of useful security coverage that justifies further use — with acceptable operational cost.

`WARNING`
: Strix ran but the result is mixed: many false positives, weak novelty, or real but insufficiently proven additional value.

`BLOCKED`
: Runtime/prerequisite/credential/network/environment failure, unsupported target, or external service failure prevents a valid scan, or evidence cannot be validated. Results are never synthesized to fill the gap.

`FAIL`
: Strix ran correctly but the experiment shows insufficient value: findings are invalid, fully duplicate existing checks, operational cost/complexity is disproportionate to the benefit, or reliability is unacceptable.

### Canonical status mapping (mandatory)

`EXECUTION_OUTCOME_IS_NOT_REGISTRY_STATUS`

The canonical registry (`contracts/EXPERIMENT_REGISTRY.schema.json`, enforced by `tests/test_contracts.py`) allows only `IDEA`, `PLANNED`, `READY_TO_TEST`, `RUNNING`, `PASS`, `FAIL`, `HOLD`, `ADOPTED`. **No new registry status may be invented for EXP-07** and the schema is not extended for this experiment. The execution outcome is mapped onto the existing enum:

| Execution outcome | Registry `status` |
| --- | --- |
| `PASS` | `PASS` |
| `WARNING` | `HOLD` |
| `BLOCKED` | `HOLD` |
| `FAIL` | `FAIL` |

`FAIL` is reserved for a confirmed experiment failure: Strix ran correctly and the evidence shows insufficient value. A blocked or mixed run is never recorded as `FAIL`.

The registry `result_summary` must additionally carry the literal execution-outcome token (`execution_outcome: PASS|WARNING|BLOCKED|FAIL`) and a reference to the sanitized evidence artifact, so registry status and execution outcome are never mixed or lost. `tests/test_exp07_strix_retry.py` guards this mapping against the committed artifact.

### Promotion gate

Even after `PASS`, do not promote Strix to a portfolio-wide security gate automatically. A separate decision is required before CI integration, auto-fix, recurring scanning, or use against production.

### Retry execution record — 2026-09-28

```text
EXECUTION_OUTCOME = BLOCKED
REGISTRY_STATUS   = HOLD
STRIX_RUN         = NOT_RUN
FINDINGS          = 0 (not run; this is not a "nothing found" result)
```

Phase 1 (review findings fixed) and Phase 2 (preparation validated) completed. Phase 3 could not start: the execution environment (Arena sandbox, Debian bookworm, Python 3.11.2, Node v22.22.3, unprivileged container) lacks the documented Strix prerequisites. Observed, not assumed:

| Missing prerequisite | Required by | Observation on 2026-09-28 |
| --- | --- | --- |
| Docker Engine with a running daemon | Strix sandbox; the first run pulls the sandbox image | `docker`, `podman`, `nerdctl`, `containerd`, `runc` all absent from PATH; `/var/run/docker.sock` absent; `CapEff: 0000000000000000`, so a daemon cannot be started even if installed |
| Strix CLI (`strix` / `strix-agent`) | the scan itself | no `strix` binary; PyPI `strix-agent` 1.6.2 requires Python `>=3.12` while the environment provides 3.11.2; `pip install --dry-run strix-agent` in a clean venv returned `No matching distribution found for strix-agent` |
| LLM credential (`STRIX_LLM` + `LLM_API_KEY`, or `strix auth login chatgpt`) | every Strix scan | no LLM provider key present in the environment (only GitHub tokens); interactive ChatGPT sign-in is not available in a headless sandbox |
| Strix Cloud fallback | external managed service | not authorized: it is a new external security service and uploads owner code, both requiring separate owner approval |

Strix source/version checked on 2026-09-28: `usestrix/strix` (Apache-2.0), PyPI `strix-agent` 1.6.2, CLI reference `docs.strix.ai/usage/cli` — `--scan-mode quick|standard|deep` (default `deep`), `-n/--non-interactive`, `--scope-mode auto|diff|full`, `--diff-base`, `--max-budget` (USD), `--max-turns` (default 500), exit codes `0` = no vulnerabilities in headless mode, `1` = fatal error (missing environment variables, Docker unavailable), `2` = vulnerabilities found.

No scan was simulated, no findings were synthesized, and no Strix output exists anywhere in this repository. Sanitized artifact: `evidence/exp-07/STRIX_RETRY_2026-09-28.json`.

### Next action

Exactly one step: in an owner-controlled Docker-enabled environment with an LLM API key, install Strix, then run one bounded quick scan of a clean clone of the frozen target `Murkin1980/mebeldocs-ai@2d6d60b240f8f4e2546cf451433c8f1ff0aad65a` using the frozen scope, exclusions, `--max-turns`/`--max-budget` limits and the baseline recorded above, and commit only the sanitized result artifact under this same `EXP-07` identity. The frozen baseline is valid for that SHA only; if another commit is scanned, re-freeze the target and baseline first.
