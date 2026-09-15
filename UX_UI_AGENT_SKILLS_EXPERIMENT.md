# UX/UI Agent Skills Experiment

## Decision

**EXPERIMENT**

This experiment evaluates whether `plugin87/ux-ui-agent-skills` should become a reusable UI/UX quality layer for Murat Project Engineer (MPE) projects.

Upstream:
- https://github.com/plugin87/ux-ui-agent-skills

Do **not** fork the upstream repository for this experiment.
Do **not** copy the complete upstream repository into MPE or product repositories.
Do **not** introduce a new standalone UX/UI service or repository.

The experiment is selective and read-mostly: use only the minimum useful skills/checks required to evaluate an existing screen.

---

## Why this experiment exists

Current MPE projects already use UI reviews, browser checks, responsive validation, and project-specific acceptance rules. The upstream kit adds a broader design-quality layer with objective checks for accessibility, responsive behavior, interaction states, token intent, visual consistency, and anti-slop/taste issues.

The purpose of this experiment is not to replace existing project gates. The purpose is to determine whether the upstream kit finds meaningful defects that our current checks miss.

If successful, the result should become a small reusable **MPE UI Quality Profile**, not a duplicated copy of the upstream project.

---

## Primary test project

Use:

`Murkin1980/ai-microtask-factory`

Preferred target:
- an existing real UI screen that already has known browser/acceptance coverage;
- preferably Acceptance UI, Plan UI, or another screen with existing mobile/browser evidence.

Do not build a synthetic showcase for the primary experiment.
The value must be proven on an existing production-oriented screen.

---

## Experiment question

> Does a selective subset of `ux-ui-agent-skills` produce actionable UI/UX findings that are not already caught by the existing `ai-microtask-factory` checks, without creating excessive false positives, workflow duplication, or repository bloat?

---

## Allowed upstream capabilities

Start with only the following areas:

1. design doctrine / design-quality rules;
2. accessibility / WCAG checks;
3. responsive and overflow checks;
4. target-size checks;
5. keyboard and focus behavior;
6. reduced-motion checks where applicable;
7. token-by-intent checks;
8. anti-slop / taste audit;
9. `/gate` workflow;
10. `/critique` workflow.

Optional only if directly relevant to the chosen screen:
- data-dashboard guidance;
- component-level design review.

---

## Explicitly out of scope

For this experiment, do not:

- import all 138 design systems;
- import the full component library;
- replace existing MPE design rules;
- replace Refero as the visual-direction reference;
- replace Uiverse as the concrete component reference library;
- redesign the tested screen just to satisfy the external kit;
- add unrelated UI features;
- add a new repository;
- fork `plugin87/ux-ui-agent-skills`;
- add production dependencies unless needed to run the experiment;
- make the new checks required CI gates before the experiment is accepted.

---

## Existing design-source roles

Keep the following responsibilities separate:

- **Refero** → visual direction, screen patterns, design-system references.
- **Uiverse** → concrete UI component inspiration/implementation references.
- **ux-ui-agent-skills** → UI/UX rules, objective checks, critique, and quality gates.

The experiment must not blur these responsibilities.

---

## Integration rule

Prefer one of these approaches, in order:

1. run the upstream kit externally or via its supported selective-install mechanism;
2. pin the upstream version used for the experiment;
3. store only MPE-specific configuration, notes, allowlists, exclusions, and results in MPE;
4. copy individual upstream files only if a technical limitation makes external use impossible and the copied files are minimal and license-compatible.

Do not vendor the entire upstream repository.

---

## Baseline before running external checks

Before using `ux-ui-agent-skills`, capture the current state of the chosen screen:

- current branch / commit SHA;
- existing relevant test/gate results;
- current responsive/mobile status;
- current known UI issues;
- current screenshots or other evidence already produced by the project, when available.

This baseline is required so the experiment can distinguish new findings from already-known findings.

---

## Experiment procedure

### Phase 1 — Baseline

Run the existing project-native checks only.
Record all findings.

### Phase 2 — Selective upstream evaluation

Apply only the allowed upstream capabilities listed in this document.
Do not modify the UI yet.

Collect all findings from:
- objective gates;
- accessibility checks;
- responsive/interaction checks;
- token-intent checks;
- anti-slop/taste audit;
- critique.

### Phase 3 — Deduplicate

Classify each upstream finding as one of:

- `NEW_VALID` — meaningful defect/risk not caught by current project checks;
- `ALREADY_COVERED` — already found or enforced by existing checks;
- `FALSE_POSITIVE` — not valid in project context;
- `LOW_VALUE` — technically valid but not worth adding to the project workflow;
- `CONFLICT` — contradicts an intentional product/design rule.

### Phase 4 — Minimal fixes

Only for `NEW_VALID` findings that are safe and local:
- prepare minimal fixes;
- do not expand product scope;
- do not change architecture;
- do not introduce a new design system.

If a finding requires a deep product or architecture change, stop and mark it `HUMAN_REQUIRED`.

### Phase 5 — Re-run

Run:
1. existing native project checks;
2. selected upstream checks;
3. relevant mobile/browser evidence.

Existing project checks must remain green.

---

## PASS criteria

The experiment is **PASS** only if all of the following are true:

1. At least **2 meaningful `NEW_VALID` findings** are discovered that were not already caught by the current project-native UI/browser checks.
2. At least one new finding materially improves one of:
   - usability;
   - accessibility;
   - responsive/mobile behavior;
   - interaction clarity;
   - visual hierarchy;
   - semantic intent of controls.
3. The false-positive rate is low enough that the tool remains useful in normal development.
4. Existing native gates remain green after any accepted fixes.
5. The experiment does not require vendoring the entire upstream repository.
6. The experiment does not create a parallel design system or duplicate existing MPE infrastructure.
7. The useful subset can be described as a small reusable MPE profile.

---

## FAIL criteria

The experiment is **FAIL** if any of the following dominates:

- findings mostly duplicate existing checks;
- findings are mostly subjective noise or false positives;
- setup/maintenance cost is disproportionate to value;
- the useful result requires copying most of the upstream repository;
- it conflicts with project-specific product rules;
- it encourages generic redesign instead of targeted quality control;
- it materially bloats CI or local workflows without enough additional signal.

---

## Expected successful output

If PASS, create a reusable profile conceptually equivalent to:

```text
MPE UI Quality Profile
├── doctrine
├── accessibility
├── responsive
├── interaction
├── token-intent
├── anti-slop/taste
├── gate
└── critique
```

The profile should define:
- pinned upstream version;
- enabled checks;
- disabled checks;
- MPE-specific exceptions;
- invocation instructions;
- evidence/report format;
- adoption rules for product repositories.

The profile should be reusable by projects such as:
- `ai-microtask-factory`;
- `salamat-projects-dashboard`;
- `business-discovery`;
- Tender Assistant;
- Grand Mebel Document Control;
- future MPE-managed UI projects.

Adoption into each project remains explicit and project-scoped.

---

## Promotion decision after experiment

Allowed terminal outcomes:

- `REUSE_COMPONENT` — preferred PASS outcome; create/define the MPE UI Quality Profile.
- `HOLD` — useful but not currently worth operationalizing.
- `REJECT` — insufficient value or excessive duplication/noise.

Do not create a new repository as a result of PASS unless a later New Idea Filter explicitly returns `NEW_REPOSITORY`.

---

## Evidence report

At completion, produce a report with:

1. target repository, branch, and SHA;
2. target screen;
3. upstream version/commit used;
4. exact upstream capabilities enabled;
5. baseline project-native checks;
6. upstream findings table;
7. classification of every finding;
8. accepted fixes, if any;
9. before/after evidence;
10. native gate results after changes;
11. false-positive count;
12. maintenance/setup observations;
13. final verdict: `PASS` or `FAIL`;
14. final MPE disposition: `REUSE_COMPONENT`, `HOLD`, or `REJECT`.

---

## Guardrails

- Existing project architecture remains authoritative.
- Project-specific `DESIGN.md`, product rules, and established acceptance contracts override generic upstream advice.
- No production rollout from this experiment alone.
- No automatic cross-repository propagation.
- No new required CI gate until PASS is reviewed.
- No secrets, credentials, or private project data may be sent to external services as part of this experiment.
- Keep changes minimal and reversible.

---

## Initial status

**Status:** READY_FOR_EXPERIMENT

**Initial disposition:** EXPERIMENT

**Primary target:** `Murkin1980/ai-microtask-factory`

**Upstream:** `plugin87/ux-ui-agent-skills`

**Fork required:** NO

**New repository required:** NO
