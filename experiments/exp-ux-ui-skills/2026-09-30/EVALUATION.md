# EVALUATION — EXP-UX-UI-SKILLS / 2026-09-30

## 1. Contract executability assessment

The registered contract (`UX_UI_AGENT_SKILLS_EXPERIMENT.md`) was checked clause by clause for whether it can be
executed at all without the target fixture.

| Contract clause | Requires | Executable now? |
|---|---|---|
| Phase 1 — Baseline: "Run the existing project-native checks only" | `ai-microtask-factory` checkout + its toolchain | **NO** — repository unobtainable |
| Phase 2 — Selective upstream evaluation against a real existing screen | the fixture's actual rendered screen | **NO** — no screen obtainable |
| Phase 3 — Deduplicate: classify each finding as `NEW_VALID` / `ALREADY_COVERED` / … | the Phase 1 baseline as the comparator | **NO** — no baseline exists to compare against |
| Phase 4 — Minimal fixes | accepted `NEW_VALID` findings + permission | N/A (and fixes are out of scope for this run by instruction) |
| Phase 5 — Re-run native + upstream + mobile evidence | fixture gates | **NO** |
| PASS criterion 1 — "≥2 `NEW_VALID` findings not already caught by current project-native UI/browser checks" | fixture native checks | **NO** — unevaluatable |
| PASS criterion 4 — "Existing native gates remain green after any accepted fixes" | fixture gates | **NO** — unevaluatable |
| PASS criterion 3 — false-positive rate usable in normal development | counted findings over a real screen | **NO** — zero denominator |
| Evidence report item 1 — "target repository, branch, and SHA" | fixture SHA | **NO** — NOT_OBTAINABLE |
| Evidence report item 5 — "baseline project-native checks" | fixture checks | **NO** |
| Evidence report item 9 — "before/after evidence" | fixture screenshots | **NO** |

**The registered contract cannot be executed on its registered target.** This is a stop condition independent of
the instruction list: *"зарегистрированный evaluation contract невозможно выполнить"*.

## 2. Upstream material availability — verified SEPARATELY and FOUND AVAILABLE

The stop condition "upstream material unavailable" does **not** apply. Raw transcript: `evidence/02_upstream_availability.log`.

| Check | Result |
|---|---|
| `plugin87/ux-ui-agent-skills` reachable | YES — `MIT`, default branch `main`, `pushed_at 2026-09-16T02:33:41Z`, size 9208 KB |
| MPE-pinned revision `2ffb677aa02b225c8a3da1b7f31d9ebb7c38f1dd` (v2.5.1) exists | YES — SHA confirmed via API |
| MPE already holds a committed selective adaptation | YES — `skills/ux-ui/UX_UI_AGENT_SKILL.md`, sha256 `7bdcf538…b5b0`, imported 2026-09-12, provenance recorded in its §20 |

It is important for the record that the **only** missing input is the fixture. The upstream knowledge layer and its
pinned provenance were already present in MPE before this run; nothing was cloned, forked, vendored, or installed
by this run.

## 3. Cases actually run

```
CASES_RUN: 0
```

- `ai-microtask-factory` screens inspected: **0** (none reachable)
- Upstream UX/UI checks executed against a fixture screen: **0**
- Accessibility / responsive / target-size / keyboard-focus / reduced-motion / token-intent / anti-slop cases executed: **0**
- Screens promoted, re-designed, or edited: **0**

**No upstream skill was applied to any `ai-microtask-factory` screen, because no such screen could be obtained.**
Running the upstream capability list against the MPE dashboard instead was deliberately rejected: it would be an
unregistered substitution of target, would answer a different question, and would produce findings that cannot be
classified as "new relative to `ai-microtask-factory` baseline".

## 4. Why the evaluation was stopped rather than approximated

1. **Substituting the target breaks the question.** The experiment asks whether upstream skills find defects *the
   existing `ai-microtask-factory` checks do not*. Without that project, the comparator does not exist.
2. **Constructing a synthetic fixture is expressly forbidden** by the contract ("Do not build a synthetic showcase
   for the primary experiment. The value must be proven on an existing production-oriented screen.").
3. **Baseline/candidate separation is impossible**, which is itself one of the run's explicit stop conditions.
4. **Any finding produced on a substitute screen would be unclassifiable** against the contract taxonomy
   (`NEW_VALID` requires "not caught by current project checks"; with no known-issues list, no such claim is provable).
5. **A fabricated or inferred baseline would be unsupported evidence.** No baseline, SHA, check result, or finding
   in this run is estimated, guessed, or reconstructed from unrelated repositories.

## 5. Compliance with run restrictions

| Restriction | Compliance |
|---|---|
| Do not change production code / UI / design | Respected — zero source files modified |
| Do not add CI gate | Respected — no workflow or gate file touched |
| Do not fork/vendor/install permanent dependency | Respected — upstream accessed only as read-only metadata (web API), no clone, no package install |
| Do not add a new runtime/service or permanent infrastructure | Respected — only offline static analysis of already-present evidence; no processes left running |
| Do not create a new experiment contract | Respected — `UX_UI_AGENT_SKILLS_EXPERIMENT.md` and `EXPERIMENT_REGISTRY.json` untouched |
| Do not run other experiments / Stage-2 / Stage-3 | Respected |
| Do not auto-fix discovered defects | Respected — the 12 pre-existing host-repo test failures were left unfixed |
| Evidence in `experiments/exp-ux-ui-skills/<run-date>/` | Done — this directory |
