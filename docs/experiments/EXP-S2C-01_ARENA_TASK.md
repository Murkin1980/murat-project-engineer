# Arena Task — EXP-S2C-01 Screenshot-to-Code Visual Workflow

Status: OWNER-AUTHORIZED EXECUTION  
Primary disposition: **EXPERIMENT**  
Executor: **Arena single agent**  
Repository: `Murkin1980/murat-project-engineer`

## Objective

Test whether one Arena agent can reconstruct one real existing Murat UI screen from a frozen screenshot more efficiently and with better visual fidelity when it uses an explicit render→compare→targeted-edit loop.

The experiment must answer:

> Does a bounded screenshot-to-code feedback loop materially improve reconstruction fidelity or reduce rework versus a one-pass screenshot implementation, without requiring a new runtime/service?

This is a workflow experiment, not a product implementation.

## Reuse requirements

Before execution, apply:
- `docs/governance/SCOPE-CHANGE-CONTROL.md`
- `docs/REUSABLE_DERIVED_ARTIFACT_PATTERN.md`
- EXP-29 Arena bootstrap when required by `AGENTS.md`

Treat:
- reference screenshot = authoritative visual source;
- screen regions/components = stable work units;
- rendered screenshots = derived artifacts;
- correction requests = minimal-diff revisions.

Do not build a new screenshot-to-code platform.

## Fixture

Use exactly one existing real screen from:

`Murkin1980/salamat-projects-dashboard`

Preferred fixture:
**the main portfolio/dashboard screen at its normal desktop route**.

Reason:
- public and Arena-readable;
- real Murat project;
- visually structured;
- responsive;
- no production write needed;
- existing source remains available for post-run comparison only.

### Critical anti-cheating rule

Arena may use the target repository only to:
1. start the app if necessary to capture the frozen reference screenshot;
2. determine the minimum runtime needed to display the chosen route.

Before the baseline and candidate implementations are complete, do **not** read/copy the target screen's React/component/CSS/Tailwind implementation, layout values, DOM structure, design tokens, or component source.

If the app cannot be launched without reading implementation details, use the live deployed screen as the visual reference when reachable.

After both reconstruction arms are frozen, source inspection is allowed only for post-run migration/cleanup comparison and must be recorded.

## Freeze before implementation

Create under:

`experiments/exp-s2c-01/`

at minimum:
- `FIXTURE.md`
- `reference/desktop.png`
- `reference/mobile.png` if the same screen has a meaningful mobile state
- `BASELINE_INSTRUCTION.md`
- `CANDIDATE_INSTRUCTION.md`

Record:
- source project;
- route/URL class;
- capture viewport;
- capture timestamp;
- screenshot hashes;
- any dynamic content that must be ignored;
- excluded regions if unavoidable.

Once frozen, do not replace the screenshots during the run.

## Scope

Reconstruct only one screen.

Do not recreate the entire dashboard application.

Allowed target:
- local static HTML/CSS, React/Vite fixture, or the smallest existing experiment-local frontend that Arena can render;
- no backend;
- no auth;
- no production deploy;
- no write to `salamat-projects-dashboard`.

Prefer the smallest implementation that can faithfully reproduce the screenshot.

## Arm A — BASELINE

Goal: represent a normal one-pass Arena screenshot reconstruction.

Use only:
- frozen reference screenshot(s);
- frozen BASELINE_INSTRUCTION.

Arena gets **one implementation pass** plus only fixes required to make the page render.

No visual feedback loop.
No iterative screenshot comparison.
No pixel-diff-guided correction.
No source inspection.

Then freeze:
- baseline source;
- desktop render;
- mobile render where applicable;
- elapsed observable effort/time;
- implementation/edit cycles;
- any render-fix cycle count.

Do not polish Arm A after its screenshot is frozen.

## Arm B — CANDIDATE

Start from a clean separate implementation directory.

Do not copy Arm A source.

Use:
- same frozen reference screenshot(s);
- same output scope;
- CANDIDATE_INSTRUCTION;
- explicit visual feedback loop.

Required loop:

```text
reference screenshot
→ implementation
→ browser render
→ comparison
→ identify largest visual mismatch
→ targeted edit
→ rerender
→ repeat
```

Maximum:
**5 visual correction cycles** after the first usable render.

Each cycle must record:
- largest observed mismatch;
- files/regions changed;
- reason;
- before screenshot;
- after screenshot;
- whether the change improved, worsened, or did not affect fidelity.

Use the EXP-24 minimal-diff lesson:
change only the region responsible for the mismatch where practical.

## Visual comparison

Required:
1. desktop visual comparison;
2. mobile comparison if the reference screen has a meaningful mobile layout;
3. independent final visual review by Arena after the implementation is frozen.

Optional:
- deterministic pixel/perceptual metric if easily available in the sandbox.

Do not add a heavy CV stack merely to produce a score.

### Visual review dimensions

Score baseline and candidate independently from 0–5 for:
- overall layout;
- spacing;
- typography hierarchy;
- component proportions;
- borders/radius/shadows;
- icon/asset placement;
- desktop fidelity;
- mobile fidelity.

Also state the three largest remaining mismatches.

Do not use a single similarity number as the sole verdict.

## Screenshot-as-layout prohibition

Forbidden:
- rendering the reference screenshot itself as the page/background;
- slicing the screenshot into layout images;
- canvas/image-map tracing that merely reproduces pixels;
- positioning a full-page image under transparent controls.

Normal reuse of genuine visual assets is allowed only if separately extracted/available and recorded.

## Measurement

For both arms record:
- start/end time or best observable duration;
- number of implementation/edit cycles;
- number of manual/agent correction instructions;
- source LOC excluding lockfiles/vendor;
- desktop score;
- mobile score;
- remaining mismatch count;
- renderer/tool dependencies;
- observed cost/credits where available.

Primary comparison:
- visual fidelity;
- rework/correction burden;
- time/effort.

## PASS

PASS if the candidate satisfies either:

A. at least **30% lower reconstruction/rework effort** with no material fidelity loss,

or

B. roughly equal effort but materially better fidelity.

Additionally all must hold:
- candidate mobile is not worse than baseline;
- screenshot-as-layout cheating = NO;
- no new persistent service/runtime;
- result is reproducible from frozen screenshots/instructions;
- target production repository remains unchanged.

## REWORK

Use REWORK when the feedback loop is clearly useful but one bounded issue prevents PASS, for example:
- unreliable screenshot capture;
- comparison too subjective;
- asset extraction remains weak;
- cleanup/migration burden uncertain.

## HOLD

Use HOLD when:
- iterative loop costs as much as or more than its fidelity gain;
- output is not materially better;
- result requires a persistent new service/runtime;
- experiment cannot be reproduced.

## Post-run source comparison

Only after both arms are frozen, Arena may read the original target implementation.

Purpose:
- estimate migration/cleanup effort;
- identify whether the candidate accidentally reinvented expensive structures;
- note reusable patterns.

Do not retrofit either frozen arm after source inspection.

## Required evidence

Under `experiments/exp-s2c-01/` preserve:
- frozen fixture metadata;
- reference screenshots;
- baseline source + final screenshots;
- candidate source + first render + correction-cycle screenshots + final screenshots;
- cycle log;
- metrics.json;
- FINAL_REVIEW.md;
- RESULTS.md.

Keep binary evidence bounded. Prefer compressed PNG/JPEG where adequate.

## Required terminal report

```text
RESULT: PASS / REWORK / HOLD
SINGLE_AGENT: YES
FIXTURE:
REFERENCE VIEWPORTS:
BASELINE CYCLES:
CANDIDATE CYCLES:
BASELINE TIME:
CANDIDATE TIME:
BASELINE DESKTOP SCORE:
CANDIDATE DESKTOP SCORE:
BASELINE MOBILE SCORE:
CANDIDATE MOBILE SCORE:
EFFORT DELTA:
FIDELITY DELTA:
SCREENSHOT_AS_LAYOUT: NO
TARGET REPO CHANGES: NONE
DEEP_CHANGE: NO / STOP
RECOMMENDATION: REUSE_COMPONENT / HOLD / REJECT
NEXT ACTION:
```

## Stop boundaries

STOP and ask the owner before:
- modifying `salamat-projects-dashboard`;
- deploying anything;
- creating a persistent visual service;
- creating a new repository;
- adding a database/queue/auth/runtime platform;
- broadening from one screen to multiple screens;
- using paid external screenshot-to-code providers;
- changing MPE authority/governance.

## Merge boundary

Open one bounded PR against `murat-project-engineer/main`.

Do not merge automatically.

The experiment ends after the evidence and final recommendation are recorded.
