# CP-09 — Test Baseline Recovery: Phase 0–2 findings

Date: 2026-10-16 UTC
Repository: `Murkin1980/murat-project-engineer`
Baseline commit: `94eeed98962e5de7f54498390782cca72d67c774` (`origin/main`)
Session branch: `arena/1c6d4a4f-murat-project-engineer`
Disposition: **PARTIAL / HOLD** — baseline reproduced; no corrective changes applied because the failure evidence is broader than a single safely attributable patch and EXP-23's bootstrap representation rejects the existing distinction without clarifying its contract.

## Phase 0 — governance and baseline

- PRs #109, #110, #111 are `MERGED`; merge timestamps 13:26:28Z, 13:27:33Z, 13:52:38Z on 2026-10-16. `origin/main` is exactly the reported merge commit `94eeed9`.
- Read `AGENTS.md` and mandatory `docs/governance/SCOPE-CHANGE-CONTROL.md`.
- Open PR search showed no open CP-09 / test-baseline recovery PR. Other open PRs are independent work; no duplicate CP-09 found.
- README documents `python -m unittest discover -s tests -v` as the full Python suite. The requested non-verbose command is equivalent discovery but is not the documented exact command. `package.json` separately offers dashboard commands; they are not documented as the Python acceptance suite.
- The baseline was run from a clean checkout at `origin/main` (same SHA as HEAD) using both `python -m unittest discover -s tests` and the documented verbose command. Full raw verbose output is preserved in `baseline-unittest-94eeed9.log`.
- Before any fix: **440 total; 412 pass, 27 fail, 0 errors, 1 skipped**. The pass count is calculated as total minus failure records and skips; the raw unittest output reports `Ran 440 tests`, 27 failures and 1 skip.
- `python scripts/validate_package.py .`: PASS (4 experts, 3 teams, 5 playbooks, contracts and 20 gates).
- EXP-29 specialized command `python -m unittest tests.test_exp29_bootstrap -v`: **42 passed**.

## Phase 1 — failure inventory

The exact failure records and tracebacks are in the preserved baseline log. They resolve into three failure groups:

| Test IDs / files | Cause evidenced by run | Component | CP/experiment | Before PR #111? | Classification | Minimal safe action / regression risk |
|---|---|---|---|---|---|---|
| `test_canonical_experiment_registry_has_required_identity_and_status_fields` (4 subtests), `tests/test_contracts.py` | Registry statuses `RETIRED` (3 entries) and `PARTIAL` (EXP-26) are rejected by the test's fixed allowed-status set. | Registry contract test | Registry governance; unrelated to EXP-29 | Not established by this baseline; tests passed after #111 only prove current state. | `OUTDATED_EXPECTATION` is plausible, but requires checking canonical status contract before editing; currently `UNKNOWN`. | Determine authoritative status enum then reconcile narrowly. Risk: accidentally bless unsupported statuses.
| `test_dashboard_exposes_a_mobile_view_for_each_registry_status` (3 subtests), `test_rendered_dashboard_text_tracks_registry_ids_names_and_next_steps` (18 subtests), `tests/test_dashboard_registry_views.py` | Committed SVG/dashboard views are missing status assets and contain truncated/stale text versus the current registry; expected content includes next-action text and entries that the rendered views omit. | Dashboard generated views / renderer | Registry dashboard; unrelated to EXP-29 | Not established. | `STALE_FIXTURE` / `OUTDATED_EXPECTATION` / renderer defect remain unresolved; current evidence alone cannot distinguish. | Establish renderer source and generation contract before regenerating or changing expectations. Risk: presenting incomplete or inaccurate portfolio status.
| `test_committed_mobile_views_are_fresh`, `test_committed_diagram_is_fresh`, `tests/test_registry_to_reladraw.py` | Generated Reladraw outputs differ from current renderer output (including generated date 2026-10-10 versus current 2026-10-16 and registry-derived content). | Generated dashboard artifacts | Registry dashboard; unrelated to EXP-29 | Not established. | `STALE_FIXTURE` likely; producer/config drift not excluded. | Rebuild only after checking the established generated-artifact process and reviewing output delta. Risk: broad generated-artifact churn.

No failure in this inventory has yet been proven attributable to an implementation defect. Therefore none was patched or reclassified as a confirmed root cause.

## Phase 2 — EXP-23 disposition

- Canonical registry `experiments/EXPERIMENT_REGISTRY.json`, `experiments/exp-23-papermorph-interactive-artifact/FINDINGS.md`, and the final-result sections of that experiment's `README.md` agree on **PASS / REUSE_COMPONENT**. Evidence says reuse is limited to the narration/visual synchronization contract and quiz data model; Papermorph itself is not adopted and no production integration is authorized.
- The apparent competing value is in the README's New Idea Filter section: `Primary disposition: EXPERIMENT`. This describes the initial routing/filter decision, while the final experiment recommendation is `REUSE_COMPONENT`; it may be a lifecycle distinction rather than conflicting final outcomes.
- Bootstrap-start evidence records the queue override (EXP-22 is HOLD; owner explicitly instructed starting EXP-23) and says it is not a data conflict.
- EXP-29 `RESULTS.md` records that its bootstrap validator rejects the packet with `ambiguous_disposition`, specifically because the parser sees `Decision: REUSE_COMPONENT` and `Primary disposition: EXPERIMENT` and previously resolved it by document order. This is a validation/representation collision, not evidence that the experiment's canonical final decision is uncertain.
- Evidence-backed canonical final identity: **EXP-23 = PASS / REUSE_COMPONENT**. Canonical representations: registry, FINDINGS and final closure all agree.
- Normative sources by task governance: current explicit CP-09 instruction first; then approved experiment result and canonical registry. The exact semantic contract for the README's *initial* disposition versus *final* disposition is not recorded as machine-readable. Changing either the experiment disposition or EXP-29 parser semantics would exceed a safe reconciliation absent an explicit contract decision. **EXP-23 reconciliation: BLOCKED pending clarification of the initial-vs-final disposition field semantics.** No arbitrary edit made.
- Dependent representations identified: registry entry, inventory, status/dashboard generated from registry, EXP-23 README/FINDINGS, and EXP-29 bootstrap packet and validator. This CP-09 run did not modify any of them.

## Phase 3–5 status

No corrective patch, after-baseline suite, PR, or merge recommendation can honestly be claimed. The current branch name is fixed by Arena session tracking and is not the requested `arena/cp09-test-baseline-recovery`; work remains on the active session branch. No PR was opened. No merge was attempted.

Next safe actions require a clarified authoritative status enum and disposition-field semantics, plus source-to-generated-artifact reconciliation for the dashboard. Then apply the smallest proven repairs, regenerate only governed outputs, and rerun the full suite and all CP-08 regression gates. Until then, acceptance is **PARTIAL / BLOCKED**, not PASS.
