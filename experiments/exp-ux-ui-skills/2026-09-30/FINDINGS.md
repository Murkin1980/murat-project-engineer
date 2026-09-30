# FINDINGS — EXP-UX-UI-SKILLS / 2026-09-30

## 1. Findings ledger (experiment scope)

The experiment scope is the registered fixture `Murkin1980/ai-microtask-factory`. No screen, no source, and no
artifact from that project could be obtained (`BASELINE.md` §2), therefore **no experiment finding exists in either
direction** — there is no measured "no defects found" signal, and there is no measured defect list.

| ID | Location / screen | Observed violation | Native check that detects it | UX/UI skill that detects it | Reproduction evidence | Severity / category | False-positive status | New vs baseline |
|---|---|---|---|---|---|---|---|---|
| — | — | *None recorded* | NOT_APPLICABLE | NOT_APPLICABLE | `evidence/01_target_resolution.log` | — | — | **NOT_MEASURABLE** |

```
NATIVE_FINDINGS (fixture):  NOT_MEASURABLE
NEW_FINDINGS:               0 measured  (NOT_MEASURABLE — not a "clean screen" result)
ACTIONABLE_NEW_FINDINGS:    0 measured
FALSE_POSITIVES:            0 evaluated  (empty denominator — not a low false-positive rate)
```

**Explicit anti-misreading statement.** `NEW_FINDINGS: 0` here means *nothing was measured*, not *the UI was clean*
and not *the upstream skills found nothing*. No statement about the quality of the `ai-microtask-factory` UI can be
made from this run. Likewise `FALSE_POSITIVES: 0` is *not* evidence of a low false-positive rate, because no
upstream check ever executed.

## 2. The blocking condition

| Field | Value |
|---|---|
| Condition | Registered fixture `Murkin1980/ai-microtask-factory` is unavailable |
| Triggered stop condition | 1. "fixture `ai-microtask-factory` отсутствует"; 2. "невозможно отделить baseline findings от candidate findings" |
| Evidence | `evidence/01_target_resolution.log` — `gh repo view` unresolvable; API 404; web 404; `git ls-remote` "Repository not found"; owner's 37 public repos contain no `microtask` repository; sandbox GitHub App installation contains only `Murkin1980/murat-project-engineer` |
| Impact | Phases 1, 2, 3, 5 and PASS criteria 1/3/4 are unevaluatable |
| Classification | **Not a UI/UX defect and not a finding.** It is an experiment blocker, recorded separately so it cannot be counted toward any finding total |

## 3. Host-repository observations (OUT OF EXPERIMENT SCOPE — excluded from all counts)

Recorded for completeness and harness honesty. These were found by **MPE's own native checks**, on the MPE host
repository, at baseline commit `8f9e958900fc52e4354cd98a943374326446cd03`. They are **not** `NEW_VALID`, **not**
candidate findings, and must not be added to `NATIVE_FINDINGS` / `NEW_FINDINGS` above.

| ID | Location | Observed violation | Detected by | Severity | New? | Status |
|---|---|---|---|---|---|---|
| HOST-01 | `npm run check` suite | No violation — 43/43 checks pass, including `mobile-390 (6/6)` and served-bytes parity | MPE native check (pre-existing) | — | No | Green at baseline |
| HOST-02 | `experiments/exp-19-…/cp02/portfolio.reladraw` + `cp02/mobile/` | Committed Reladraw diagram and mobile views are stale relative to `EXPERIMENT_REGISTRY.json` (`updated_at 2026-09-30` vs artifacts generated 2026-09-29) | `tests/test_registry_to_reladraw.py::test_committed_diagram_is_fresh`, `::test_committed_mobile_views_are_fresh` | artifact freshness | No — pre-existing at baseline, reproduced in a clean clone | Open, **not fixed** (fixing is out of scope) |
| HOST-03 | `dashboard/public/registry/mobile/status-*.svg`, `dashboard/public/registry/portfolio.svg` | Rendered dashboard text does not track registry IDs/names/next actions — e.g. `'EXP-09' not found in 'HOLD (4) EXP-10 · … EXP-17 · …'`; 10 assertion failures across EXP-09 and EXP-18 | `tests/test_dashboard_registry_views.py::test_rendered_dashboard_text_tracks_registry_ids_names_and_next_steps` | rendered-content correctness | No — pre-existing at baseline, reproduced in a clean clone | Open, **not fixed** |
| HOST-04 | Host-repo test invocation artifact | 7 additional failures appear only when the checkout directory name differs from `package.json` `name` (`validate_package.py` compares `directory_slug(root)`) | `tests/test_contracts.py`, `tests/test_dispatch_autonomy.py` … | harness artifact | No | Documented, not a defect |

**Classification of HOST-02/HOST-03 under the contract's Phase 3 taxonomy: `ALREADY_COVERED`** — by construction,
because a native project check already detects them. They are retained here as a **negative control** demonstrating
that MPE's native checks do catch rendered-UI content-drift defects, i.e. the experiment's premise ("native checks
may miss UI defects") cannot be validated from these observations. `HOST-04` is neither a defect nor a finding.

## 4. Reproducibility of this run

| Artifact | Reproducible? | How |
|---|---|---|
| Fixture unavailability | YES | Re-run the eight probes in `evidence/01_target_resolution.log`; all return 404 / "Repository not found" |
| Upstream reachability + pinned SHA | YES | `gh api repos/plugin87/ux-ui-agent-skills/commits/2ffb677aa002b225c…dd` |
| Host-repo native check results | YES | `npm run check` (43/43) and `python3 -m unittest discover -s ./tests -t ./tests -p "test_*.py"` (343 tests, 12 pre-existing failures) at `8f9e958` |
| Any UX/UI experiment finding | **NO — none exists** | No upstream case was executed |

## 5. What would unblock this experiment

1. Grant this sandbox read access to `Murkin1980/ai-microtask-factory`, or make the repository public; **or**
2. Provide the target screen evidence (checkout, screenshots, existing gate results, known-issues list) into a
   location readable by MPE; **or**
3. Formally re-register a different target project through a new experiment contract (a scope change, explicitly
   outside this run).

Until one of these happens, EXP-UX-UI-SKILLS cannot produce `NEW_VALID` findings, and the main question
(*"does the upstream UX/UI skill evaluation discover actionable UI quality defects that the existing project checks
do not detect?"*) remains **unanswered** — not answered negatively.
