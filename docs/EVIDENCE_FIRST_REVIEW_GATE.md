# Evidence-First Review Gate Policy

**Status:** ACTIVE / MANDATORY  
**Date:** 2026-10-05  
**Canonical Rule:** **Agent claims are not evidence.**

---

## Core Principle

In Murat Project Engineer, an assertion made by an agent or executor—such as "tests passed", "file updated", "deployment succeeded", or "requirements satisfied"—holds zero evidential weight on its own. 

Self-reported or model-generated claims cannot clear a Review Gate. Every pass verdict requires independent, verifiable, and deterministic evidence captured from the actual execution environment.

If evidence is missing, unverified, or ambiguous, the state must remain **`UNKNOWN/UNVERIFIED`**, never converted into `PASS` or `SUCCESS`.

---

## Verification Requirements by Claim Type

| Claim | Unacceptable (Claim Only) | Required Verifiable Evidence |
|---|---|---|
| **"Tests passed"** | Agent prose: *"All unit tests executed and passed without errors."* | Captured command invocation, exit status code (`exit 0`), and test count summary (e.g. `Ran N tests in Xs ... OK`). |
| **"File updated"** | Agent prose: *"Updated the configuration file as requested."* | `git diff` output, `git status`, or read-back inspection verifying file content, path, and line modifications. |
| **"Deployment succeeded"** | Agent prose: *"Deployment to worker was successful."* | Captured deployment command output, deployment URL/version ID, plus live HTTP health-check / read-back response. |
| **"Requirement completed"** | Agent prose: *"All acceptance criteria have been fully implemented."* | Traceable matrix mapping each specific acceptance criterion to its verifying automated test, command trace, or inspection artifact. |

---

## Review Gate Enforcement Rules

1. **Fail-Closed on Unverified Claims:**
   - Any gate result claiming `PASS` backed by `self_reported`, `model_generated`, or `executor_prose` fails immediately.
   - For required execution checks (`clean_diff_scope`, `secrets_scan`, `build`), an untrusted claim forces an outcome of `REWORK`, never `PASS`.
2. **Missing Evidence is UNKNOWN/UNVERIFIED:**
   - Absence of evidence does not mean success.
   - If an automated check could not run or was skipped without an explicit authorized exception, its status must be recorded as `UNKNOWN/UNVERIFIED` or `NOT_OBSERVABLE`.
3. **Independent Reviewer Duty:**
   - The Reviewer role is an independent verifier. The Reviewer must directly inspect captured command outputs, diffs, and artifact integrity.
   - The Reviewer is strictly prohibited from relying on the Coder's or Architect's prose assertions.
4. **Trusted Evidence Sources:**
   - Only verifiable system artifacts are classified as `TRUSTED` evidence:
     - `git_status`, `git_diff`
     - `test_runner`, `compileall`, `terminal_command`
     - `secrets_scan`, `ci_result`
     - `platform_tool_trace`, `hash_linked_artifact`
5. **Human Gate on Ambiguity:**
   - When required evidence cannot be deterministically verified by an automated gate or independent reviewer, the run must halt at `HUMAN_REQUIRED`.
