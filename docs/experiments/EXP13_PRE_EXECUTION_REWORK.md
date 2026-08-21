# EXP-13 — pre-execution rework

Date: 2026-08-21
Status: ACTIVE
Parent: `docs/experiments/EXP-13_LOW_COST_EVALUATION_HARNESS.md`

## Why a pre-execution stage

The EXP-12 line validates *triage* (what tier/approval a task needs). EXP-13
moves the cheap deterministic checks to **before** execution so a task that
must not run autonomously is stopped before budget is spent, instead of being
discovered by a Reviewer after the fact.

## Pre-execution vs execution checks

- **Pre-execution (cheap):** `route_resolves`, `triage_expected_match`,
  `acceptance_present`, `human_review_due`. No usage telemetry is needed.
- **Execution:** `usage_valid`, `usage_consistent`, `retries_within_limit`,
  `defects_within_limit`, `cost_within_limit`. Only run when the pre-execution
  stage says the run may proceed.

## Escalation precedence

`HUMAN_REVIEW_REQUIRED` > `PREMIUM_REQUIRED` > `NONE`.

- A task with a human-approval signal (e.g. `production_change`, any
  deep-change signal) escalates to `HUMAN_REVIEW_REQUIRED` before execution on
  every route. T-008 exercises this path legally.
- The `PREMIUM_REQUIRED` class (`DEEP-CHANGE` on a non-premium route) is
  separately defined and tested at the `escalation_for` layer. The current
  triage engine always marks `DEEP-CHANGE` human-approval-required, so
  end-to-end the human escalation wins first; a deep change is never
  auto-executed on any route.

## Rework vs reconstruction

The pre-execution stage is the *product* of this experiment. The implementation
itself is a controlled reconstruction (see the reconstruction note in the
parent document); its frozen semantics — dataset v2, routes, thresholds,
pricing snapshot and acceptance criteria — are authoritative from this revision
forward and must only change through a versioned asset plus a documented
decision.
