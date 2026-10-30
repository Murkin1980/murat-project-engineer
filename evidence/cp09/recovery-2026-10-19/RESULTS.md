# CP-09 — Test Baseline Recovery: root-cause repair run

Date: 2026-10-19 UTC
Repository: `Murkin1980/murat-project-engineer`
Branch: `arena/1d43d7c6-murat-project-engineer` (Arena session branch — name is fixed by Arena
session tracking and is not freely choosable; instruction `docs/checkpoints/CP-09-RECOVERY-ARENA-INSTRUCTION.md`,
PR #114, explicitly permits the active Arena session branch)
Base: `3969b88ff2ad6220fcb1a8c5b3d8d8854e230bec` (current `origin/main`, includes PR #112 evidence)
Disposition: **PASS (implementation) / PR HOLD — do not merge without owner review**

## 0. Governance read (in order)

1. `docs/governance/SCOPE-CHANGE-CONTROL.md`
2. `AGENTS.md`
3. `docs/NEW_IDEA_FILTER_POLICY.md`, `docs/GLOBAL_MPE_ENFORCEMENT.md`, `docs/OPINIONATED_WORKSPACE_POLICY.md`
4. `evidence/cp09/RESULTS.md` + `evidence/cp09/baseline-unittest-94eeed9.log` (Phase 0–2 record, main)
5. `experiments/exp-29-arena-bootstrap-harness/README.md`, `RESULTS.md`, builder, workers, tests
6. Registry contract, `scripts/registry_to_reladraw.py` producers, dashboard/Reladraw tests,
   EXP-23 canonical artifacts

Open-PR search at start: no other CP-09 / test-recovery PR; PR #114 (instruction) and other open PRs
are independent. No duplicate work found.

## 1. Bootstrap safety (EXP-29) — PACKET BLOCKER RECORDED, canonical Git used

Documented invocation (`bootstrap_builder.py build --experiment … --checkpoint …`) was used; no
arguments guessed. Results:

| Attempt | Identity | verify | Consumed? |
|---|---|---|---|
| `--experiment EXP-29 --checkpoint CP-09` | `EXP-29/CP-09` | **REJECTED** `unsupported_active_checkpoint:CP-09` (EXP-29's chain is CP-01…CP-08; this task's CP-09 lives in `docs/checkpoints/`, which is not a builder source role) | **No** — REJECTED is not authority |
| `--experiment EXP-24 --checkpoint CP-09` | `EXP-24/CP-09` (HyperFrames "Programmatic assembly") | FRESH | **No** — wrong task identity; FRESH-but-wrong-identity is not authority |
| `--experiment EXP-23 --checkpoint CP-03` (before fix) | `EXP-23/CP-03` | **REJECTED** `ambiguous_disposition` | No — this is defect 3b, evidence kept |

A CP-09-identity packet **cannot be generated under the existing schema**. Per instruction §1 this
blocker is recorded and execution proceeded directly from canonical Git. Bootstrap semantics were
**not** changed to make the task start. Evidence: `cp09-packet-attempt.json/.md`, `exp23-before.json`.

## 2. Fresh baseline (re-verified on current main `3969b88`)

- `python -m unittest discover -s tests -v` → exit 1; **Ran 440 tests — FAILED (failures=27, skipped=1)**
  (= 412 pass / 27 fail / 0 errors / 1 skip — the `440/412/27/0/1` baseline of `evidence/cp09/RESULTS.md` remains valid).
- `python -m unittest tests.test_exp29_bootstrap -v` → 42 passed.
- `python scripts/validate_package.py .` → PASS (4 experts, 3 teams, 5 playbooks, contracts, 20 gates).
- Same 27 failures in 3 groups as inventoried in Phase 1 (4 registry-status + 21 dashboard-views + 2 reladraw-freshness).

## 3. Root-cause → change matrix

| # | Failing tests (before) | Root cause (normative evidence) | Fix (smallest supported) | Files |
|---|---|---|---|---|
| 3a | `test_contracts.py` registry identity/status subtests ×4 (`RETIRED` ×3, `PARTIAL` ×1) | **Contract enum lagged canonical data.** `RETIRED` was set by owner commit `6c65a76` (2026-10-01) with distinct do-not-run semantics; `PARTIAL` by EXP-26 record (PR #51); `experiments/EXPERIMENT_INVENTORY_2026-10-16.md` counts both as registered statuses; EXP-12 evidence records dashboard PR #32 accepting "canonical `PARTIAL` status acceptance/display"; EXP-29 `RESULTS.md` (CP-07) already named this "a pre-existing, separately-owned contract gap". Data correct; `contracts/EXPERIMENT_REGISTRY.schema.json` enum outdated. | Add exactly `PARTIAL` and `RETIRED` to the status enum. No data collapse (RETIRED ≠ HOLD, PARTIAL ≠ PASS — distinctions preserved), no test change, no blanket widening (no free strings; IDEA/RUNNING/ADOPTED untouched) | `contracts/EXPERIMENT_REGISTRY.schema.json` |
| 3b | EXP-23 bootstrap REJECTED `ambiguous_disposition` (CP-09 Phase 2 blocker) | **Parser conflated two lifecycle stages.** `docs/NEW_IDEA_FILTER_POLICY.md` defines the New Idea Filter "primary disposition" as the pre-implementation intake route (EXP-23: `EXPERIMENT`); the final lifecycle disposition is the header `Decision:` line plus registry/FINDINGS/final conclusion (**PASS / REUSE_COMPONENT**). Finalize commit `c31cf12` changed `Status: PLANNED→PASS`, `Decision: EXPERIMENT→REUSE_COMPONENT` and deliberately left the filter record untouched. The builder treated both stages as one field → false ambiguity. | Parser correction in `_parse_dispositions`: declarations inside a `## New Idea Filter` section are the initial route, not the disposition; every other declaration form is unchanged and still fails closed on true conflicting **final** values. 4 regression tests (2 positive + 2 negative). Packet schema `exp-29-arena-context-v1` unchanged; canonical files untouched | `experiments/exp-29-arena-bootstrap-harness/harness/bootstrap_builder.py`, `tests/test_exp29_bootstrap.py` |
| 3c | `test_dashboard_registry_views.py` ×21 (missing status assets ×3; stale text ×18) | **Two independent causes.** (i) Committed SVG views predate registry `updated_at 2026-10-16` (no EXP-23/EXP-24/EXP-S2C-01 cards, stale next-step text) — stale generated views, not a renderer defect; (ii) `dashboard/public/index.html` never exposed the FAIL/PARTIAL/RETIRED mobile views — those 3 statuses entered the registry after the CP-04 integration and the HTML was not extended | Regenerate all established derived artifacts per the documented `dashboard/README.md` ritual; extend the `#registry` mobile section with the 3 missing `<details>` blocks following the exact CP-04 pattern (PASS→…→HOLD→PARTIAL→FAIL→RETIRED) | `dashboard/public/index.html`, cp02 + dashboard SVG/reladraw copies |
| 3d | `test_registry_to_reladraw.py` ×2 (diagram + mobile freshness) | **Stale generated `.reladraw`** (header `updated_at 2026-10-10` vs registry `2026-10-16`; registry content drifted after EXP-23 finalize / EXP-24 reopen) | Regenerate via the documented producer (deterministic: no wall-clock; only source-derived date is registry `updated_at`; stable STATUS_ORDER/project ordering) | cp02 `*.reladraw` |
| 3c+ | 3 width regressions surfaced **during** regeneration (`status-ready_to_test.svg` 590px > 390px) | **Renderer limitation + long token data.** EXP-13's `next_action` legitimately references `docs/experiments/EXP-13_CLOUDFLARE_RELAY_PREFLIGHT.md` (53-char whitespace-free run). Pinned `reladraw@0.13.0` `wrap` folds only at word boundaries (its SYNTAX.md; no word-break option; tool stays external/pinned). Width contract (≤390px @ 14px) and text-tracking contract (exact `RELADRAW.short(next_action, 70)` in rendered text) both held by tests | Deterministic display rule in the shared `short()` transform: whitespace-free runs longer than 26 chars break at fixed 26-char chunk boundaries with ordinary spaces. Tests compute expected text via the same `RELADRAW.short()`, so text-tracking stays exact and reassembles across wrap points; every line ≤26 chars keeps the ≤390px contract (26-char lines render ≤355px) | `scripts/registry_to_reladraw.py` (then regenerated outputs) |

No test was deleted, weakened, or replaced; no architecture/source-of-truth change; the registry
data itself was not modified.

## 4. EXP-23 lifecycle semantics (resolved on documented semantics)

- **Initial route (immutable history):** `## New Idea Filter` → `Primary disposition: **EXPERIMENT**`
  — the pre-implementation intake decision per `docs/NEW_IDEA_FILTER_POLICY.md`.
- **Final decision (canonical):** `Status: PASS`, `Decision: REUSE_COMPONENT` — registry entry,
  `FINDINGS.md`, README conclusion; finalize commit `c31cf12` (owner, 2026-10-10) moved
  `Decision: EXPERIMENT` → `Decision: REUSE_COMPONENT` and left the filter record in place.
- **Semantics applied:** these are distinct lifecycle stages, not conflicting final dispositions.
  The bootstrap parser now resolves EXP-23's packet disposition to **REUSE_COMPONENT** (verified
  `FRESH`, all checks true — `exp23-after.json` / `exp23-after-verify.json`), while a true
  final-vs-final conflict still yields REJECTED `ambiguous_disposition` (negative regression test),
  and a filter-only declaration still yields REJECTED `missing_disposition` (fail-closed).
- Canonical files were **not** edited: both lifecycle stages remain visible in EXP-23's README.

## 5. Generated artifacts and exact producer commands

All derived artifacts were regenerated with the documented producers (no hand edits to generated
files):

```bash
CP02=experiments/exp-19-shirman-trend-intake/cp02
python scripts/registry_to_reladraw.py --out "$CP02/portfolio.reladraw" --mobile-dir "$CP02/mobile"
npx --yes reladraw@0.13.0 "$CP02/portfolio.reladraw" -o "$CP02/portfolio.svg"
cp "$CP02/portfolio.svg" dashboard/public/registry/portfolio.svg
for src in "$CP02"/mobile/status-*.reladraw; do
  npx --yes reladraw@0.13.0 "$src" -o "${src%.reladraw}.svg"
  cp "${src%.reladraw}.svg" "dashboard/public/registry/mobile/$(basename "${src%.reladraw}").svg"
done
```

Artifact list: `cp02/portfolio.reladraw|svg`, `cp02/mobile/status-{pass,ready_to_test,planned,hold,partial,fail,retired}.reladraw|svg`,
and byte-identical deployment copies under `dashboard/public/registry/`. `index.html` (hand-maintained
static snapshot) gained only the 3 missing status view blocks. The `*-390px.png` previews in cp02
remain the older illustrations — not covered by any acceptance contract, deliberately not churned.
The committed EXP-29 `ARENA_CONTEXT.json/.md` are byte-identical and still verify `FRESH` (the
parser correction does not affect EXP-29's declarations).

## 6. Verification after fixes (commands + exact results)

| Command | Result |
|---|---|
| `python -m unittest discover -s tests -v` | **exit 0 — Ran 444 tests, OK (skipped=1)** (440 baseline + 4 new regression tests; 0 failures, 0 errors) |
| `python -m unittest tests.test_exp29_bootstrap -v` | **exit 0 — Ran 46 tests, OK** (42 baseline + 4 new; log `unittest-exp29-after.log`) |
| `python scripts/validate_package.py .` | **exit 0 — VALIDATION PASSED** (4 experts, 3 teams, 5 playbooks, contracts, 20 gates) |
| `git diff --check` | **exit 0** — no whitespace errors |
| `npm run check` | **exit 0 — ALL CHECKS PASSED: 52/52** (config 5/5, build 1/1, preview 1/1, route 5/5, asset 8/8, parity 8/8, views 7/7, mobile-390 9/9, content 8/8) |

Raw after-logs: `unittest-full-after.log`, `unittest-exp29-after.log` (no sandbox paths, no secrets).
Baseline counts vs current: 440→444 total is the legitimate addition of 4 disposition-lifecycle
regression tests; the 1 skip is the pre-existing platform-specific skip.

## 7. Security / scope / deep-change statement

- No secrets, credentials, or sandbox paths in the diff or evidence (scanned).
- Scope: exactly the four authorized CP-09 sections; no feature work, no new infra/repo/dependency,
  no deployment, no merge.
- Deep-change assessment: (a) the enum addition is explicitly authorized contract reconciliation
  (instruction 3a) — additive, evidenced by owner commits and merged evidence, no migration;
  (b) the parser correction is explicitly authorized (instruction 3b: "minimal representation/parser
  correction") because the semantic contract already distinguishes the two lifecycle stages —
  bootstrap packet schema and source-of-truth hierarchy unchanged; fail-closed preserved for true
  final conflicts; (c) no fundamental contract was weakened. No `BLOCKED_DEEP_CHANGE` raised.

## 8. Remaining blockers / notes

1. **Bootstrap CP-09-identity blocker (non-blocking, recorded):** no packet can match this task's
   CP-09 identity under the existing schema (see §1). Not worked around; bootstrap semantics
   untouched. Owner may later decide whether `docs/checkpoints/` tasks need a bootstrap identity.
2. The EXP-29 committed packet's disposition semantics are unchanged (`REUSE_COMPONENT`); if the
   owner wants the initial filter route carried inside packets as its own field, that is a packet
   schema change requiring explicit approval (not done).
3. Cosmetic, unchanged: no dedicated Reladraw style colors for FAIL/PARTIAL/RETIRED (they use the
   default planned gray); cp02 `*-390px.png` previews are stale illustrations.
4. Merge/deploy authority stays with the owner; PR is opened as **HOLD / do not merge** per the
   instruction's delivery gate.

## 9. Handoff

- STATE: all four CP-09 repair sections implemented and verified on `arena/1d43d7c6-murat-project-engineer`.
- EVIDENCE: this directory — before/after packets (`exp23-before.json`, `exp23-after.json` +
  `exp23-after-verify.json`), bootstrap blocker attempt (`cp09-packet-attempt.json/.md`), raw after
  logs.
- CHANGES: see matrix §3; 4 root-cause commits.
- RESULT: **PASS (implementation) / PR HOLD**.
- BLOCKER: none inside scope; the bootstrap identity gap is recorded (§8.1).
- NEXT ACTION: owner reviews PR; decide on the bootstrap identity question (§8.1) and merge at
  owner discretion. No deploy.
- HANDOFF: PR body carries the same matrix; `evidence/cp09/RESULTS.md` (Phase 0–2) remains the
  baseline record and was not rewritten.
