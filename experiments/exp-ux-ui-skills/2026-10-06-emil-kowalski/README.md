# EXP-UX-UI-SKILLS — Emil Kowalski reuse run — 2026-10-06

Decision: **REUSE_COMPONENT**  
Run type: bounded reuse evaluation  
Host experiment: `EXP-UX-UI-SKILLS` (historical experiment remains RETIRED)  
Target project: `Murkin1980/salamat-projects-dashboard`  
Target deployment: `https://projects.salamat-mebel.kz/`

## Purpose

Reuse the existing UX/UI experiment harness to evaluate Emil Kowalski's current UI skills against an accessible real project.

This run does **not** reactivate the old inaccessible `ai-microtask-factory` fixture and does **not** create a new standalone experiment.

## Upstream pin

Repository: `emilkowalski/skills`  
Pinned revision: `e8a175de22ae1e49370fc144c1f3bb9aeedf988d`  
Pinned date: 2026-10-02  
Upstream commit message: `Add break ui skill`

At this pin, the repository exposes 14 skills:

- emil-design-eng
- animate
- animate-expo
- review-animations
- improve-animations
- find-animation-opportunities
- animation-vocabulary
- apple-design
- write-swift
- pick-ui-library
- prototype
- mobile-native
- break-ui
- ask-sonner

## Selected skill set for this run

Use only the skills relevant to the target:

1. **break-ui** — primary stress test.
2. **mobile-native** — primary mobile usability test.
3. **emil-design-eng** — secondary quality review.
4. **review-animations** — only if the target contains meaningful motion.
5. **prototype** — only if a concrete defect has two or more plausible fixes.
6. **pick-ui-library** — only if a defect is caused by a hand-rolled UI component and an existing library is clearly preferable.

Do not install or invoke unrelated skills just because they exist.

## Required stress data

The run must cover realistic Murat/Salamat data, not generic Latin demo data:

- long Russian and Kazakh names;
- long project names;
- long URLs and email-like strings;
- missing avatar/image;
- missing optional fields;
- empty lists;
- very large counts;
- many rows/cards;
- long status/reason/next-action text;
- narrow mobile width;
- zoom to 200%.

Any synthetic data switch must be development-only and must not enter production output.

## Evaluation order

```
native project checks
→ baseline screenshots/observations
→ break-ui
→ mobile-native
→ emil-design-eng
→ review-animations (if applicable)
→ findings
→ proposed fixes
```

## Core rule

**Find first, fix later.**

The first Arena pass must not modify production UI code. It should separate:

- defects already detected by native tests;
- new defects found by the Emil skills;
- code-only suspicions not confirmed in a browser;
- browser-confirmed defects;
- real-device-only checks that remain unverified.

## Success signal

This reuse run is valuable if it finds actionable defects that native project checks do not already detect, especially defects affecting:

- mobile use;
- overflow/truncation;
- inaccessible controls;
- empty/error states;
- touch behavior;
- zoom;
- long operational data.

## Guardrails

- No new repository.
- No new EXP ID.
- No production deployment.
- No automatic UI fixes in the first pass.
- No replacement of project design system.
- Respect `salamat-projects-dashboard/AGENTS.md` and its scope/change-control policy.
- Do not weaken zoom/accessibility to make screenshots pass.
- Do not treat a resized desktop browser as proof of real-device behavior.
- Any deep-change stops the run and requires Murat's explicit approval.

## Expected artifacts

Arena should produce under this dated run:

- `BASELINE.md`
- `FINDINGS.md`
- `EVALUATION.md`
- `evidence/`
- optional `PROPOSED_FIXES.md`

No target-project changes are required for the diagnostic pass.
