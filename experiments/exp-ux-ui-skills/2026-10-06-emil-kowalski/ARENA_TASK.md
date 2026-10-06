# Arena task — Emil Kowalski UI skills reuse run

Decision: **REUSE_COMPONENT**

Target: `Murkin1980/salamat-projects-dashboard`  
Deployment: `https://projects.salamat-mebel.kz/`  
Upstream skills: `emilkowalski/skills@e8a175de22ae1e49370fc144c1f3bb9aeedf988d`

## Mission

Run a bounded UI-quality evaluation of the current Salamat Projects Dashboard using Emil Kowalski's skills, with emphasis on `break-ui` and `mobile-native`.

Do not implement fixes in the first pass.

## Mandatory first reads in target repo

Before analysis or coding, read:

1. `docs/governance/SCOPE-CHANGE-CONTROL.md`
2. `FOUNDATION.md`
3. `ARCHITECTURE.md`
4. `TRIAGE_RULES.md`
5. `CHECKPOINTS.md`
6. `PROJECT_STATUS.md`
7. `ROADMAP.md`
8. `AGENTS.md`

If any instruction conflicts with this task, follow source-of-truth priority and report the conflict.

## Phase A — baseline

1. Record target commit SHA.
2. Run native checks:
   - `npm test`
   - `npm run build`
   - any existing responsive/UI checks documented in the repo.
3. Record known failures before using external skills.
4. Capture the current main screens, at minimum:
   - Portfolio
   - Triage
   - Nodes
   - Experiments
5. Record desktop and narrow-mobile observations separately.

Do not change code.

## Phase B — break-ui

Use the upstream `break-ui` rules against a development-only fixture/data mode.

Stress at minimum:

- long Russian full name;
- long Kazakh full name;
- long project/repository name;
- long status explanation;
- long next-action text;
- URL/email-like unbroken strings;
- missing optional data;
- empty list;
- one item;
- hundreds/thousands of items where the existing architecture permits;
- large numeric counts.

Check:

- clipping;
- horizontal overflow;
- inaccessible buttons;
- collapsed controls;
- unreadable truncation;
- broken card/table heights;
- avatar/icon shrink;
- lost status meaning;
- empty-state quality;
- list performance symptoms.

If creating a stress-data switch is necessary, keep it strictly development-only and isolated. Do not merge it into production behavior as part of this run.

## Phase C — mobile-native

Audit at narrow mobile width and, where the environment permits, on a real phone/device session.

Check:

- sticky hover states after tap;
- tap target size;
- tap highlight/feedback;
- input zoom behavior;
- safe-area handling;
- bottom controls vs system gestures;
- 100vh/dynamic viewport behavior;
- on-screen keyboard effects;
- scroll locking;
- drawers/sheets;
- touch latency;
- accidental double actions;
- orientation changes where meaningful;
- browser zoom up to 200%.

Never disable user zoom.

If real-device verification is unavailable, mark those checks `UNVERIFIED_REAL_DEVICE`; do not claim PASS from desktop emulation alone.

## Phase D — design/motion review

Use `emil-design-eng` for a bounded review of defects already surfaced.

Use `review-animations` only if the current dashboard has meaningful animation. Do not add motion merely to exercise the skill.

Use `prototype` only when one confirmed issue has at least two materially different valid solutions. Prototype must remain isolated.

Use `pick-ui-library` only when a confirmed issue is caused by an unnecessary hand-built component.

## Finding classification

Every finding must be tagged as exactly one:

- `ALREADY_COVERED` — native project check already catches it.
- `NEW_BROWSER_CONFIRMED` — new and reproduced in browser.
- `CODE_SUSPICION` — inferred from code but not reproduced.
- `UNVERIFIED_REAL_DEVICE` — needs physical-device verification.
- `FALSE_POSITIVE` — skill recommendation is not applicable.
- `DESIGN_CHOICE` — valid product/design tradeoff, not a defect.

For each finding record:

- screen/component;
- input/state that triggered it;
- viewport;
- reproduction steps;
- screenshot or evidence path;
- severity;
- native check coverage;
- proposed minimal fix;
- whether the fix changes semantics or only presentation.

## Required Russian/Kazakh fixture examples

Use realistic non-sensitive synthetic examples. Include strings at least as long as:

- `Мухамеджанов Нурмухамед Абдурахманович`
- `Құрылыс және өндірістік автоматтандыру жобаларының басқару орталығы`
- `Экспериментальная интеграция локального inference-провайдера с маршрутизацией задач и проверкой ограниченных решений`

Do not use real customer PII.

## Stop conditions

STOP and report if:

- a deep-change is required;
- the target source-of-truth must be changed;
- the evaluation requires production data;
- an upstream skill asks to weaken accessibility;
- fixes require a new framework/design system;
- target deployment would be required just to continue diagnosis.

## Deliverables

Write the run evidence under:

`experiments/exp-ux-ui-skills/2026-10-06-emil-kowalski/`

End `FINDINGS.md` with:

```
RESULT: PASS | PARTIAL | FAIL
NEW_BROWSER_CONFIRMED: <count>
ALREADY_COVERED: <count>
CODE_SUSPICION: <count>
UNVERIFIED_REAL_DEVICE: <count>
FALSE_POSITIVE: <count>
TOP_3_FIXES:
1. ...
2. ...
3. ...
RECOMMENDATION: ADOPT_GATE | USE_ON_DEMAND | HOLD | REJECT
DEEP_CHANGE: YES | NO
```

Do not edit the dashboard in this run. If useful defects are confirmed, propose a separate minimal patch for approval.
