# Reusable UI Reconstruction Feedback Pattern

Status: ACTIVE / REUSE_COMPONENT  
Source evidence: EXP-S2C-01  
Validated: 2026-10-10

## Purpose

Provide a default bounded workflow for reconstructing or visually matching an existing UI from screenshots or rendered references without creating a separate screenshot-to-code platform.

This pattern is intended for Arena/Codex UI reconstruction and refinement tasks where the target is an existing visual reference.

## Default workflow

```text
frozen reference
→ initial implementation
→ render
→ compare
→ identify largest remaining mismatch
→ targeted minimal-diff correction
→ rerender
→ early stop on diminishing returns
```

## Default correction budget

Use:
- **1 initial render**
- **up to 3 targeted correction cycles**
- stop early when either:
  - desktop fidelity >= 4.6 AND mobile fidelity >= 4.6; or
  - the latest correction improves average fidelity by < 0.10.

Do not use 5 cycles by default.

## Evidence from EXP-S2C-01

Fixture: real Salamat Projects Dashboard screen at 1280×800 desktop and 390×844 mobile.

Baseline:
- ~5 minutes;
- desktop 4.11 / 5;
- mobile 4.20 / 5.

Original 5-cycle candidate:
- ~10 minutes;
- desktop 4.81 / 5;
- mobile 4.70 / 5.

Efficient-budget candidate:
- ~6 minutes;
- 2 targeted correction cycles;
- desktop 4.75 / 5;
- mobile 4.70 / 5;
- 91.4% of desktop fidelity gain retained;
- 100% of mobile fidelity gain retained;
- stopped before cycle 3.

## Required rules

1. Freeze the reference first. Record viewport/source and hash where practical.
2. Do not use screenshot-as-layout tricks.
3. After each comparison, fix the single largest mismatch with the smallest practical localized change.
4. Protect stabilized regions from unrelated edits.
5. Validate desktop and mobile when the UI is responsive.
6. Stop on diminishing returns; do not spend cycles on cosmetic differences once the gate is met.
7. Do not create a new persistent screenshot-to-code platform/service by default.
8. Treat reconstruction outputs as derived artifacts until the owning project explicitly adopts them.

## Applicability

Use for:
- screenshot-to-code reconstruction;
- visual parity work;
- recreation of a reference screen in an existing project;
- bounded UI migration with a known visual target;
- visual QA requiring local corrections.

Do not force it onto:
- greenfield UI without a visual reference;
- backend-only work;
- business logic changes;
- infrastructure tasks;
- product redesign where parity is not the goal.

## Relationship to the derived-artifact pattern

This specializes `docs/REUSABLE_DERIVED_ARTIFACT_PATTERN.md`.

For screenshot/UI work:
- frozen screenshot = authoritative visual source;
- regions/components = stable work units;
- renders = derived artifacts;
- targeted visual corrections = minimal-diff revisions.

## New Idea Filter preference

When this pattern fits, prefer **REUSE_COMPONENT** or **EXTEND_EXISTING** before proposing a new screenshot-to-code runtime/platform.
