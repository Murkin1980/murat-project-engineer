# CP-09 recovery — PR #115 conflict recovery against current main

- Date: 2026-10-30 (UTC)
- Repository: `Murkin1980/murat-project-engineer`
- Decision: `EXTEND_EXISTING`
- Overall result: **PARTIAL / HOLD**
- Deep-change portion: **BLOCKED_DEEP_CHANGE / HUMAN_REQUIRED** (`EXPERIMENT_REGISTRY.schema.json` not applied)
- Current `main` / recovery base: `db4fff4d3258f57318f8eeb2e883ce29877940fb` (includes merged PR #122)
- PR #115 historical head integrated locally: `3bf900b4ad92a79945b5020cd1c4c63f02e04555`
- Recovery branch: `arena/4d9540dc-murat-project-engineer`
- Recovery merge commit: `8cb629706381c43e1299cd2f1fa1351f37c791bc` (published on the permitted recovery branch; PR #115 head not yet updated by an authorized maintainer).
- Merge into `main`: **NOT PERFORMED**
- Deploy: **NOT PERFORMED**

## STATE

The local recovery merge integrates PR #115 with current `main` while preserving the merged PR #122 canonical closure. The only content conflict was `dashboard/public/index.html`. It was resolved by keeping the current `main` document byte-for-byte and adding only the missing `PARTIAL`, `FAIL`, and `RETIRED` mobile-status blocks from PR #115.

The closed EXP-29 experiment was **not re-implemented or re-opened**. Its canonical task/results/registry/STATUS records and committed `EXP-29/CP-09` packet from PR #122 were preserved. EXP-29 was exercised only as a compatibility/regression gate.

## EVIDENCE

### Baseline on current main

Command: `python -m unittest discover -s tests -v`

- Exit: 1
- Ran: **441**
- Failures: **27**
- Errors: **0**
- Skipped: **1**
- Failure set: identical to `evidence/cp09/baseline-unittest-94eeed9.log`; no new baseline failure after PR #122.
- Log: `baseline-full-unittest.log` (repository-root paths normalized to `<repo>`; trailing whitespace stripped for `git diff --check`; test records/counts unchanged)

Other baseline gates:

| Command | Result | Log |
|---|---:|---|
| `python -m unittest tests.test_exp29_bootstrap -v` | 43 tests OK | `baseline-exp29-unittest.log` |
| `python scripts/validate_package.py .` | PASS | `baseline-validator.log` |
| `npm run check` | 43/43 PASS | `baseline-dashboard-check.log` |

### Final recovery gates

| Command | Exit | Result | Log |
|---|---:|---|---|
| `python -m unittest discover -s tests -v` | 1 | **448 tests, 4 failures, 0 errors, 1 skip** | `final-full-unittest.log` |
| `python -m unittest tests.test_exp29_bootstrap -v` | 0 | **47 tests OK** | `final-exp29-unittest.log` |
| `python -m unittest tests.test_registry_to_reladraw tests.test_dashboard_registry_views -v` | 0 | **15 tests OK** | `final-dashboard-unittest.log` |
| `python -m unittest tests.test_contracts -v` | 1 | 12 tests, 4 status-enum subtest failures | `final-contracts-unittest.log` |
| `python scripts/validate_package.py .` | 0 | PASS | `final-validator.log` |
| `npm run check` | 0 | **52/52 PASS** | `final-dashboard-check.log` |
| `python experiments/exp-29-arena-bootstrap-harness/harness/exp29_proof.py all --workdir <absolute-workdir>` | 0 | **PASS**; NC-01…NC-06 and NC-08A/B/C fail closed | `proof-harness.log`, `proof/` |
| `git diff --check` / `git diff --cached --check` | 0 | clean | recorded in PR recovery comment |

The four remaining full-suite failures are exactly the blocked public-contract enum subtests:

- `EXP-QOOPIA-MEMORY` — `RETIRED`
- `EXP-UX-UI-SKILLS` — `RETIRED`
- `EXP-16` — `RETIRED`
- `EXP-26` — `PARTIAL`

No dashboard/Reladraw failure remains. No EXP-29 test failure remains. The full-suite total evolved 441 → 448 because PR #115 adds 4 disposition-lifecycle regressions and this recovery adds 3 display/navigation regressions.

### EXP-29 / CP-09 compatibility

- Committed `EXP-29/CP-09` packet: **FRESH**, 9/9 checks, `field_diffs: []` (`committed-exp29-cp09-verify.json`).
- Full proof harness: **PASS**; canonical sources unchanged during the proof; only derived artifacts were written by the ritual and then restored to the PR #122 committed bytes.
- NC-01…NC-06: 4 `STALE`, 2 `REJECTED`, all pass.
- NC-08A/B: `REJECTED`, worker refused; NC-08C: `STALE`, resume-action drift named.
- EXP-23 after parser recovery: **FRESH**, 9/9 checks, disposition `REUSE_COMPONENT` from the final README declaration; initial New Idea Filter route `EXPERIMENT` preserved (`exp23-after.json`, `exp23-after-verify.json`).
- Repository-recovery bootstrap identity remains unsupported: `EXP-29/CP-09-RECOVERY` verifies `REJECTED unsupported_active_checkpoint:CP-09-RECOVERY` (`recovery-identity-verify.json`). The valid `EXP-29/CP-09` packet is the closed experiment's canonical-closure packet, not authority for repository recovery. Work proceeded from canonical Git/checkpoint files.

## CHANGES

1. **Conflict resolution** — `dashboard/public/index.html`: current main snapshot/navigation preserved; added only PARTIAL/FAIL/RETIRED status blocks. Machine-readable proof: `merge-resolution.json`.
2. **EXP-23 lifecycle parser** — retained PR #115's minimal `bootstrap_builder.py` correction and 4 positive/negative regressions, compatible with PR #122's `CURRENT_CHECKPOINT=CP-09` and 9-checkpoint chain.
3. **Renderer review fix** — replaced PR #115's ordinary-space token splitting with a content-true display path: `short()` preserves tokens; derived Reladraw layout uses marked visual breaks; the documented SVG post-pass joins marked lines into one copyable SVG text node without inserting spaces. Added regressions for long-token copyability, spaced-slash preservation, post-pass idempotence, navigation, and all status views.
4. **Generated views** — regenerated portfolio + 7 mobile status Reladraw/SVG artifacts from the current registry (`updated_at 2026-10-29`) and copied dashboard renders byte-for-byte.
5. **Schema** — **not changed**. Exact proposed diff and consequences: `DEEP_CHANGE_GATE.md`, `proposed-schema.diff`.
6. **Evidence** — this directory; historical PR #115 evidence under `recovery-2026-10-19/` retained.

## Regeneration commands

```bash
CP02=experiments/exp-19-shirman-trend-intake/cp02
python scripts/registry_to_reladraw.py --out "$CP02/portfolio.reladraw" --mobile-dir "$CP02/mobile"
for src in "$CP02/portfolio.reladraw" "$CP02"/mobile/status-*.reladraw; do
  npx --yes reladraw@0.13.0 "$src" -o "${src%.reladraw}.svg"
  python scripts/registry_to_reladraw.py --svg "${src%.reladraw}.svg"
done
cp "$CP02/portfolio.svg" dashboard/public/registry/portfolio.svg
cp "$CP02"/mobile/status-*.svg dashboard/public/registry/mobile/
npm run build
npm run check
```

## BLOCKER

1. **Deep-change Gate:** owner approval is required for the exact one-line public enum addition in `proposed-schema.diff`. Until approved, the four status-enum subtests remain red and full CP-09 PASS is forbidden.
2. **PR head update authority:** this Arena session may push only `arena/4d9540dc-murat-project-engineer`. It cannot push PR #115's historical head branch `arena/1d43d7c6-murat-project-engineer`. The recovery merge is published on the permitted branch and recorded in PR #115; an authorized maintainer must fast-forward/update the PR head to the recovery commit if the PR itself is to carry it.
3. **Merge/deploy:** not authorized and not performed. Full-suite gate is not green while the schema decision is pending.

## NEXT ACTION

Owner reviews `DEEP_CHANGE_GATE.md` and explicitly approves or rejects the exact schema diff. If approved, apply only that one-line change, rerun all gates, and update PR #115. If rejected, keep the schema unchanged and decide a separate semantic reconciliation; do not collapse statuses or weaken tests. An authorized maintainer updates PR #115's head to the recovery merge commit. No merge/deploy until all mandatory checks and owner authority are satisfied.

## HANDOFF

- STATE: conflict resolved; safe recovery implemented and verified; schema portion stopped.
- EVIDENCE: this directory and PR #115 recovery comment.
- CHANGES: merge of current main + PR #115 safe changes; schema excluded.
- RESULT: PARTIAL / HOLD; not full PASS.
- BLOCKER: schema Deep-change approval; PR-head branch push authority; full-suite red pending schema.
- NEXT ACTION: owner schema decision + authorized PR-head update.
- HANDOFF: resume from this file, `DEEP_CHANGE_GATE.md`, `merge-resolution.json`, and the final logs; no rediscovery of the closed EXP-29 checkpoint is required.
