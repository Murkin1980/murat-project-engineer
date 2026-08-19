# MPE Three-Color Triage Visual Model

Date: 2026-08-19
Status: ADOPTED AS UI / MENTAL MODEL
New Idea Filter decision: `EXTEND_EXISTING`

## Purpose

MPE uses a three-color visual triage model as a fast human-readable layer over the existing risk classifications. This is a presentation and decision-support convention, not a replacement for the underlying machine-readable triage logic or evidence.

## Mapping

- 🟢 **GREEN — FAST**
  - low-risk, bounded work;
  - small blast radius;
  - no deep-change signal;
  - normal deterministic checks are sufficient.

- 🟡 **YELLOW — VERIFIED**
  - non-trivial or medium-risk work;
  - requires explicit checks, evidence and/or review according to the selected playbook;
  - may involve multiple files, schema-sensitive changes, UI/business-logic changes or regression risk;
  - not automatically blocked for human approval unless another rule requires it.

- 🔴 **RED — DEEP-CHANGE / HUMAN_REQUIRED**
  - high-risk, architecture-impacting, destructive, security/permissions-sensitive, production-impacting or otherwise approval-gated work;
  - execution must stop at the relevant human gate when approval is required;
  - red must never be used as a purely cosmetic severity marker: it represents an enforceable control state when policy requires it.

## Design rule

Color is a secondary representation only. The canonical state remains the explicit machine-readable classification (`FAST`, `VERIFIED`, `DEEP-CHANGE`) plus `approval_required`, gate results, evidence and terminal state.

Do not infer or downgrade a task from color alone. Do not allow UI color to override contracts, evidence or policy.

## Dashboard usage

The triage color should be visible in:

- portfolio/project lists;
- run cards;
- run-level audit view;
- failed-gate / pending-approval views;
- history and comparison views where task risk is shown.

A user should be able to understand the broad attention level at a glance, then drill down into the underlying evidence, reason codes and approval state.

## Relationship to EXP-12 CLEARS

EXP-12 remains responsible for deterministic triage mechanics and prospective validation. This three-color model is only a human-facing projection of the resulting classification.

Suggested projection:

`FAST → GREEN`

`VERIFIED → YELLOW`

`DEEP-CHANGE → RED`

If `approval_required=true`, the UI should also expose an explicit approval/human-gate indicator rather than relying on red color alone.

## Accessibility requirement

Color must never be the only carrier of meaning. Every colored state must also include a textual label and, where practical, an icon/state code so the interface remains understandable for color-vision deficiencies and non-visual representations.

## Future validation

During RUN-19 (Run-Level Audit Dashboard), validate whether this visual model reduces time-to-understand run status without causing users to ignore the underlying evidence or detailed classification.
