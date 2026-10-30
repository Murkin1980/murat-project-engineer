# CP-09 Recovery — owner-approved schema addition

- Date: 2026-10-30 (UTC)
- Repository: `Murkin1980/murat-project-engineer`
- Branch: `arena/4d9540dc-murat-project-engineer`
- Requested starting HEAD: `43d846b939988aedcd90e39f7c9d843df3d22b23`
- Verified local starting state: local checkout initially pointed at `db4fff4d3258f57318f8eeb2e883ce29877940fb`, but the complete working-tree Git tree exactly matched the published recovery HEAD tree `0ab3f763fe37d4ff097c02026caf0e073daf7b4d`. The local branch was safely aligned to `43d846b939988aedcd90e39f7c9d843df3d22b23` with `git reset --soft`; no file content changed.
- Owner approval: explicit approval to add `PARTIAL` and `RETIRED` to `contracts/EXPERIMENT_REGISTRY.schema.json`.
- Result: **PASS / HOLD** — implementation and mandatory checks pass; no merge or deploy authority exercised.
- Final SHA: recorded in `DELIVERY.md` and the PR #115 integration comment after push.

## Applied change

Only the approved one-line enum addition was applied to the public contract:

```diff
-          "status": {"enum": ["IDEA", "PLANNED", "READY_TO_TEST", "RUNNING", "PASS", "FAIL", "HOLD", "ADOPTED"]},
+          "status": {"enum": ["IDEA", "PLANNED", "READY_TO_TEST", "RUNNING", "PASS", "PARTIAL", "FAIL", "HOLD", "RETIRED", "ADOPTED"]},
```

- `schema_version` remains `1.0.0`.
- No required key, pattern, additionalProperties rule, registry data, governance, bootstrap semantics, or dashboard producer code changed.
- No status collapse or data migration.
- Historical recovery evidence under `evidence/cp09/recovery-2026-10-19/` and `evidence/cp09/recovery-2026-10-30/` was preserved; this directory adds the approval-phase evidence.

## Downstream compatibility

| Consumer / surface | Result |
|---|---|
| `tests/test_contracts.py` registry identity/status contract | **PASS**, 12 tests OK |
| Canonical registry | 30 records; all statuses accepted; required/closed-field compatibility PASS |
| Registry status counts | PASS 15, HOLD 6, PLANNED 3, RETIRED 3, READY_TO_TEST 1, FAIL 1, PARTIAL 1 |
| `scripts/registry_to_reladraw.py` | No change required; existing deterministic ordering handles all observed statuses |
| Dashboard/Reladraw focused tests | **15 OK** |
| `npm run check` | **52/52 PASS** |
| EXP-29 committed `EXP-29/CP-09` packet | **FRESH**, 9/9 checks, `field_diffs: []` |
| EXP-23 recovery packet | **FRESH**, 9/9 checks, `field_diffs: []` |
| Closure recovery packet | **FRESH**, 9/9 checks, `field_diffs: []` |
| EXP-29 full proof harness | **PASS**; NC-01…NC-06 and NC-08A/B/C fail closed |
| EXP-14 historical `HASHES.txt` | Expected digest drift only: it freezes the pre-approval schema digest. No active test/CI consumer found; historical artifact preserved unchanged. |

Schema digest before approval-phase change: `4e74c3a2c5ca53215d7a8b281479cc66c228158fda8ce35b0eaaec05e0879650`.
Schema digest after approved enum addition: `5f35226492a66c55484fb30fd4ec643c9a57445ca3e2b6a56fb9244caecfa863`.

## Mandatory checks

| Command | Exit | Result | Evidence |
|---|---:|---|---|
| `python -m unittest discover -s tests -v` | 0 | **448 tests OK, 0 failures, 0 errors, 1 skip** | `full-unittest.log` |
| `python -m unittest tests.test_contracts -v` | 0 | **12 OK** | `contracts-unittest.log` |
| `python -m unittest tests.test_exp29_bootstrap -v` | 0 | **47 OK** | `exp29-unittest.log` |
| `python -m unittest tests.test_registry_to_reladraw tests.test_dashboard_registry_views -v` | 0 | **15 OK** | `dashboard-unittest.log` |
| `python scripts/validate_package.py .` | 0 | **PASS** | `validator.log` |
| `npm run check` | 0 | **52/52 PASS** | `dashboard-check.log` |
| `python experiments/exp-29-arena-bootstrap-harness/harness/exp29_proof.py all --workdir <absolute-workdir>` | 0 | **PASS** | `proof-harness.log`, `proof/` |
| `git diff --check` / cached check | 0 | clean | `DELIVERY.md` / PR comment |

The previous four full-suite failures were exactly the blocked enum subtests for `EXP-QOOPIA-MEMORY`, `EXP-UX-UI-SKILLS`, `EXP-16`, and `EXP-26`. They are cleared by the approved enum addition. No new regression was observed.

## PR #115 integration preparation

- The permitted recovery branch contains the prior recovery merge plus this approved schema commit.
- PR #115's historical head `3bf900b4ad92a79945b5020cd1c4c63f02e04555` is an ancestor of the recovery branch.
- This session does not push PR #115's head branch `arena/1d43d7c6-murat-project-engineer`; doing so would bypass the active branch permission boundary.
- PR #115 is updated by comment/body with the exact recovery SHA and integration instructions for an authorized maintainer.
- No merge into `main` and no deploy were performed.

## Remaining boundary

Technical implementation gates are green. PR #115 still requires an authorized maintainer to update its head to the published recovery SHA, and any merge/deploy still requires explicit owner authority. No additional deep change is authorized or performed.
