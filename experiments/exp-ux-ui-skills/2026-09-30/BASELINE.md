# BASELINE — EXP-UX-UI-SKILLS / 2026-09-30

## 1. Registered baseline requirements (from the contract)

`UX_UI_AGENT_SKILLS_EXPERIMENT.md` fixes the baseline object and its required content:

- **Primary test project:** `Murkin1980/ai-microtask-factory` (§"Primary test project").
- **Preferred target:** an existing real UI screen that already has known browser/acceptance coverage —
  preferably Acceptance UI, Plan UI, or another screen with existing mobile/browser evidence.
- **Explicitly forbidden:** building a synthetic showcase for the primary experiment.
- **Required baseline before external checks** (§"Baseline before running external checks"):
  current branch/commit SHA; existing relevant test/gate results; current responsive/mobile status;
  current known UI issues; current screenshots or other project evidence.
- **Required baseline purpose:** to distinguish new findings from already-known findings (§Phase 3).

The experiment registry entry (`experiments/EXPERIMENT_REGISTRY.json`, `EXP-UX-UI-SKILLS`) confirms the same target
and states the next action as: *"Capture the ai-microtask-factory baseline and run the selective upstream evaluation."*

**Conclusion:** the baseline object of this experiment is the `ai-microtask-factory` screen, not the MPE repository.
MPE is the harness/evidence host only.

## 2. Baseline capture attempt — target fixture

All attempts were made 2026-09-30 UTC. Full raw transcript: `evidence/01_target_resolution.log`.

| # | Probe | Result |
|---|---|---|
| 1 | `gh repo view Murkin1980/ai-microtask-factory` | `GraphQL: Could not resolve to a Repository` |
| 2 | `GET https://api.github.com/repos/Murkin1980/ai-microtask-factory` (unauthenticated) | **HTTP 404** |
| 3 | `GET https://github.com/Murkin1980/ai-microtask-factory` (web UI, following redirects) | **HTTP 404** |
| 4 | `git ls-remote https://github.com/Murkin1980/ai-microtask-factory` | `remote: Repository not found.` |
| 5 | Owner public repository enumeration (`users/Murkin1980/repos?per_page=100&type=all`) | 37 repositories; **no `microtask` repository of any name** |
| 6 | GitHub-wide repository search `microtask-factory` | 1 unrelated result (`microtask-factory/microtask-factory.github.io`); no `Murkin1980` match |
| 7 | Repositories reachable by this sandbox's GitHub App installation | **1 — `Murkin1980/murat-project-engineer` only** |
| 8 | Variant probes (`ai-microtask-factory-mpe`, `microtask-factory`, `microtask-factory-ai`) | all **HTTP 404** |

**Interpretation.** The fixture is not readable by this run through any available channel. A private repository
would also return 404 to an unauthorised caller, and the sandbox credential cannot enumerate the owner's private
repositories; therefore the fixture's private existence can be neither confirmed nor used. In either case the
fixture is **unobtainable for this run**, which is the operative fact.

### Baseline values that could not be captured

| Required baseline field | Status | Reason |
|---|---|---|
| Fixture branch / commit SHA | **NOT_OBTAINABLE** | No read access to the repository |
| Fixture native checks (test/gate results) | **NOT_CAPTURED** | Requires repository checkout |
| Fixture UI/UX findings already known | **NOT_CAPTURED** | Requires repository, issues, or project docs |
| Fixture responsive/mobile status | **NOT_CAPTURED** | Requires served or rendered screen |
| Fixture screenshots / existing browser evidence | **NOT_CAPTURED** | Requires repository artifacts |
| Fixture build / typecheck / lint state | **NOT_CAPTURED** | Requires repository checkout and toolchain |
| Target screen identity (Acceptance UI vs Plan UI) | **UNDETERMINED** | Screen inventory is inside the unavailable repository |

**No substitute was used.** Selecting a different repository (e.g. `Murkin1980/salamat-projects-dashboard`) would
change the registered target of a pre-registered experiment, would require a new experiment contract, and would
make the PASS criterion "at least 2 NEW_VALID findings not caught by the existing `ai-microtask-factory` checks"
literally unevaluatable. Under the run instructions ("не расширять scope", "не создавать новые experiment contracts")
this was not done.

## 3. Host-repository harness baseline (context only — **not** the experiment baseline)

MPE is where evidence is stored, so its own state was captured to document the harness honestly.
**These figures are not the EXP-UX-UI-SKILLS baseline and were not used to classify any finding.**

- Host repository: `Murkin1980/murat-project-engineer`
- Baseline commit SHA: `8f9e958900fc52e4354cd98a943374326446cd03`
  (`EXP-09: close non-reproducible experiment`, branch `arena/01a0f375-murat-project-engineer`, parent `main`)
- Working tree at capture: clean apart from this run's new untracked evidence directory
- Runtime captured: Node v22.22.3, Python 3.11.2 (full transcript: `evidence/03_mpe_host_native_checks.log`)

### Native check A — dashboard deploy check

```
$ npm run check
PASS  config (5/5)   PASS  build (1/1)     PASS  preview (1/1)
PASS  route (5/5)    PASS  asset (5/5)     PASS  parity (5/5)
PASS  views (7/7)    PASS  mobile-390 (6/6) PASS content (8/8)
ALL CHECKS PASSED: 43/43
```

This suite already enforces a 390px-class mobile readable-size contract and served-bytes parity with
`dashboard/public/`. It is a pre-existing MPE capability, not something introduced by this experiment.

### Native check B — Python unit suite

```
$ python3 -m unittest discover -s ./tests -t ./tests -p "test_*.py"
Ran 343 tests in 0.544s
FAILED (failures=12, skipped=1)
```

The 12 failures are **pre-existing at `8f9e958`**. Proof: the same command in a fresh clone of the same SHA,
checked out in a clean directory with the canonical name, reproduces exactly 12 failures (transcript in
`evidence/03_mpe_host_native_checks.log`, CHECK C). None of them can be attributed to this run, which only added
untracked evidence files.

Failing set (all are artifact-freshness / content-drift assertions, all UI-facing):

| Count | Test | Module |
|---|---|---|
| 1 | `test_committed_diagram_is_fresh` | `tests/test_registry_to_reladraw.py` |
| 1 | `test_committed_mobile_views_are_fresh` | `tests/test_registry_to_reladraw.py` |
| 10 | `test_rendered_dashboard_text_tracks_registry_ids_names_and_next_steps` | `tests/test_dashboard_registry_views.py` |

Concrete example (reproducible):

```
FAIL: ... (experiment='EXP-09', field='experiment_id', view='status-hold.svg')
AssertionError: 'EXP-09' not found in 'HOLD (4) EXP-10 · ... EXP-COMPUTE-BUDGET · ... EXP-STAGE3-SYNTHETIC · ... EXP-17 · ...'
```

The registry (`experiments/EXPERIMENT_REGISTRY.json`, `updated_at: 2026-09-30`) now lists EXP-09 as `HOLD`, but the
committed dashboard/mobile/diagram artifacts still reflect the 2026-09-29 registry state.

**Control observation.** Cloning the same SHA into a differently-named directory (`/tmp/mpe-pristine`) produces
19 failures instead of 12; the extra 7 (`test_package_contracts`, 6× `test_package_validation_unchanged`) are
false alarms caused by `scripts/validate_package.py` comparing `package.json` `name` against `directory_slug(root)`.
This is a checkout-path artifact, not a defect signal, and not an experiment finding.

### How this context is used

These host-repo failures are **detected by MPE's own native checks**. Under the contract's Phase 3 taxonomy they
would classify as `ALREADY_COVERED` by construction. They are therefore recorded here as a **negative control**:
MPE native checks demonstrably do catch rendered-UI content-drift defects. They must not be counted as
experiment findings, `NEW_VALID` results, or evidence for PASS. They were not fixed (no fixes were permitted).
