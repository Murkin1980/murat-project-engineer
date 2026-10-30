# EXP-29 / CP-08 — independent final acceptance

Date: 2026-10-29
Verifier: independent Arena acceptance session (`arena/e51ab251-murat-project-engineer`), not the
CP-08 authoring session (`arena/dce03808-murat-project-engineer`).
Verified state: `main` @ `83c786b291c4c1dff9633434562a1bb457713cdf`, clean tree, session branch at
the same commit.

This record is **verification evidence only**. CP-08 was not re-implemented, nothing was merged,
deployed, or promoted, and no canonical source was modified by this acceptance run.

## Verdict

**PASS — CP-08 accepted.** No CP-08 defect was found; the delivered checkpoint satisfies every
CP-08 PASS criterion on current canonical `main`. The CP-08 PR is already **merged** by the owner,
so no merge action remains for CP-08 itself.

Experiment closure is **prepared but not executed** (section "Closure readiness"): it needs a
separate owner-authorized checkpoint because it must touch canonical registry/`STATUS.md` state and
the Reladraw/dashboard regeneration ritual, which CP-08 explicitly deferred and which currently
sits inside the pre-existing failing set owned by the CP-09 recovery work.

## Delivery identity (existing PR with the CP-08 results)

| Item | Value |
|---|---|
| PR | [#111 — EXP-29 CP-08: bootstrap state consistency recovery](https://github.com/Murkin1980/murat-project-engineer/pull/111) |
| Branch | `arena/dce03808-murat-project-engineer` → `main` |
| Head SHA | `23a0b1ba7f069c59edb1c1bb1a4b0c54bab433df` |
| Base SHA | `653abffad4ff07b6bb1476f2d65e3dbd35d70402` |
| Merge commit | `94eeed98962e5de7f54498390782cca72d67c774` (merged by `Murkin1980`, 2026-10-16T13:52:38Z) |
| Diff | 17 files, +1,343 / −279 |
| Ancestry | merge commit verified an ancestor of current `main` (`git merge-base --is-ancestor`) |
| Post-merge `main` changes | `dashboard/public/index.html`, `evidence/cp09/**` only — no EXP-29 file changed after the merge |

## Packet verification (`ARENA_CONTEXT.json` / `.md`)

| Check | Result |
|---|---|
| `bootstrap_builder.py verify --json` | `FRESH`, `consistent_with_canonical_sources: true`, `field_diffs: []` |
| Verifier checks | 9/9 true (authority, stop rules, deep-change gate, lesson scopes, disposition declared + unambiguous, active checkpoint declared, source digests, rebuild match) |
| Task / checkpoint | `EXP-29/CP-08`; chain `CP-01 → CP-02 → … → CP-08` (CP-01…CP-07 kept as history) |
| Disposition | `REUSE_COMPONENT`, from both canonical declarations (`ARENA_TASK.md`, `README.md`) |
| Resume action | `resume.next_authorized_action` = complete canonical paragraph (860 B, ends with `.`), not a truncated line |
| Provenance | 8 source refs, each with `sha256`, all matching current Git |
| Stop rules | 16 stop/deep-change rules present |
| Artifact size | 15,057 B JSON / 12,020 B MD |
| Markdown | `ARENA_CONTEXT.md` byte-identical to `render_markdown(committed packet)` |
| Rebuild identity | rebuild identical to the committed packet once `generated_against` (informational git refs, excluded from freshness by design) is ignored |
| Evidence reproducibility | a fresh `exp29_proof.py cp08` run reproduced `evidence/cp08.json` **byte-identically** (`diff` = 0 lines); the in-place ritual writes were reverted with `git checkout` afterwards |

## Tests run (independently reproduced, 2026-10-29)

| Gate | Command | Result |
|---|---|---|
| EXP-29 focused suite | `PYTHONHASHSEED=0 python3 -m unittest tests.test_exp29_bootstrap -v` | **42 tests — OK** |
| Full proof harness + negative controls | `python3 …/harness/exp29_proof.py all --workdir /tmp/exp29-accept-work` | exit 0, `EXP-29 proof result: PASS`; NC-01…NC-06 → 4 `STALE`, 2 `REJECTED`; CP-08 drift controls NC-08A/B/C fail closed |
| CP-08 evidence replay | `python3 …/harness/exp29_proof.py cp08` | exit 0, output identical to committed `evidence/cp08.json` |
| Full unittest suite, before | `git worktree` at `653abff` (CP-08 merge base), `PYTHONHASHSEED=0 python3 -m unittest discover -s tests` | 432 tests — **29 failures**, 1 skipped |
| Full unittest suite, after | same command on `main` @ `83c786b` | 440 tests — **27 failures**, 1 skipped |
| Failure delta | `comm` on the two failure sets | −2 (`test_committed_packet_is_fresh`, `test_committed_packet_matches_fresh_build`), **+0 regressions** |
| Package validator | `python3 scripts/validate_package.py .` | `VALIDATION PASSED` (4 experts, 3 teams, 5 playbooks, contracts, 20 gates) |
| Whitespace | `git diff --check` | clean |
| Secrets | token/key/password pattern scan over the PR #111 diff | 0 hits |
| Scope | file list of PR #111 | 17/17 files inside `experiments/exp-29-arena-bootstrap-harness/**` + `tests/test_exp29_bootstrap.py` |

CP-08 PASS criteria (from `ARENA_TASK.md`), re-checked independently:

| Criterion | Verdict |
|---|---|
| Committed packet `FRESH` and rebuild-identical | PASS |
| Names the current authorized task and checkpoint (`EXP-29/CP-08`) | PASS |
| Preserves `REUSE_COMPONENT` | PASS (both canonical declarations) |
| Resume action complete, current, authorized | PASS (canonical paragraph; see observation O-1) |
| CP-01…CP-07 kept as historical checkpoints | PASS (evidence untouched) |
| Fail-closed regression coverage for the drift | PASS (`Exp29StateConsistencyTests`, NC-08A/B/C) |
| No new failing full-suite test | PASS (29 → 27, 0 new) |

## Failure classification: CP-08 vs pre-existing

All 27 remaining full-suite failures also fail at the CP-08 merge base `653abff`; none is caused by
CP-08 and none exercises the harness contract.

| Count | Module / area | Cause | Owner |
|---|---|---|---|
| 4 | `test_contracts` — registry identity/status schema (`EXP-16`, `EXP-26`, `EXP-QOOPIA-MEMORY`, `EXP-UX-UI-SKILLS`) | registry-schema drift introduced by the #110/#112 reconciliation | registry/CP-09 recovery (open PR #115) |
| 21 | `test_dashboard_registry_views` — missing mobile views for `FAIL`/`PARTIAL`/`RETIRED` + rendered dashboard text drift (`EXP-12`, `EXP-13`, `EXP-23`, `EXP-24`, `EXP-29`, `EXP-S2C-01`) | committed Reladraw/dashboard artifacts not regenerated after registry edits | dashboard ritual / CP-09 recovery |
| 2 | `test_registry_to_reladraw` — committed diagram and mobile views stale | same generated-artifact drift | dashboard ritual / CP-09 recovery |

Two of the 21 rows name `EXP-29`, but they assert **generated dashboard view freshness**
(`next_action` text in `portfolio.svg` / `status-pass.svg`), not harness behaviour; they fail
identically at `653abff`.

## Boundary check

| Area | Status |
|---|---|
| Production code | unchanged |
| Governance / contracts / gates | unchanged |
| Router | unchanged |
| Secrets / credentials | unchanged; 0 secret-pattern hits in the CP-08 diff |
| Infrastructure / deploy config | unchanged (`wrangler.jsonc`, `.github/**` untouched) |
| Agent authority | unchanged; no new source of truth, memory service, database, runtime or scheduler |
| Registry | **unchanged** by CP-08 (deferred owner decision — see O-1) |

## Observations (not CP-08 defects)

- **O-1 — canonical state still frames CP-08 as pending.** `EXPERIMENT_REGISTRY.json` keeps
  `next_action` = "CP-08 … follow owner instruction in PR #108", `result_summary` ends with
  "CP-08 … proposed in draft PR #108, not yet implemented", `pr_or_issue_links` lists #65/#108 but
  not #111, `updated_at` = 2026-10-16; `STATUS.md` line 124 still reads "Nearest single action (as of
  2026-10-16): complete EXP-29 CP-08 …". CP-08 deliberately deferred this. Consequence: the packet's
  registry-derived `now.nearest_action` / `resume.next_action` still read as unfinished work, so a
  fresh session could wrongly propose repeating CP-08. Digest freshness cannot catch this by design —
  the sources are simply still saying it.
- **O-2 — `generated_against` is point-in-time.** The committed packet records
  `arena/dce03808…` / `653abff`. It is informational and excluded from freshness; re-running the
  publishing ritual on another branch rewrites those bytes (observed and reverted during acceptance).
- **O-3 — the ritual writes in place.** `exp29_proof.py` writes `evidence/*.json` and republishes
  `ARENA_CONTEXT.*` inside the repository; an acceptance/proof run must restore the tree afterwards
  (`git checkout -- experiments/exp-29-arena-bootstrap-harness`).
- **O-4 — 27 pre-existing failures are outside EXP-29** and are being handled by the CP-09 recovery
  branch (PR #115, open, `CONFLICTING`, marked HOLD/do not merge). They must not be repaired inside
  an EXP-29 checkout.

## Closure readiness (prepared, NOT applied)

Owner authorization is required before any of the following is executed. Recommended as **one
bounded closure checkpoint** (name is the owner's call; `CP-09` is already in use by the recovery
work in PR #115):

1. Reconcile canonical state in the same change: `EXPERIMENT_REGISTRY.json` (`next_action`,
   `result_summary`, `pr_or_issue_links` += PR #111, `updated_at`) and `STATUS.md` line 124.
2. Keep the token `CP-08` inside the registry `next_action` — `tests/test_exp29_bootstrap.py`
   (`test_committed_packet_agrees_with_the_registry_authorized_action`) and
   `exp29_proof.CURRENT` pin `EXP-29/CP-08`; otherwise both must be updated inside the same
   checkpoint (test-first, per governance §17).
3. Refresh the `## Next authorized action` section of `RESULTS.md` to the post-acceptance state
   (complete paragraph, contains `CP-08`, ends with `.`).
4. Re-publish the derived packet with the documented ritual (`exp29_proof.py cp02`) so
   `ARENA_CONTEXT.*` is `FRESH` and rebuild-identical again, then refresh `evidence/*.json`.
5. Regenerate the Reladraw/dashboard views (`scripts/registry_to_reladraw.py`, dashboard build) —
   only after, or together with, the CP-09 recovery so the 27 pre-existing failures are not
   re-baselined by accident.
6. Re-run this acceptance matrix; expected end state: focused 42 OK, full-suite failures below 27
   only through the CP-09 repairs, packet `FRESH`.

Suggested registry `next_action` shape (proposal only, **not applied**):

> CP-08 accepted (PR #111, merge 94eeed9) and the EXP-29 experiment is closed at CP-08 with
> PASS / REUSE_COMPONENT. Next: owner decision on adoption (automatic per-session packet
> generation, GLOBAL lesson promotion, runtime integration); no merge, deploy, or production
> integration without authorization.

## Rollback

Nothing canonical was changed. Deleting this file removes the record; the committed packet, the
evidence set and the test baseline are unaffected.

## Next action (single)

Owner authorizes one bounded closure checkpoint that reconciles `EXPERIMENT_REGISTRY.json` +
`STATUS.md` + the `RESULTS.md` next-action paragraph and re-publishes the derived packet, sequenced
with the CP-09 recovery so the dashboard/Reladraw ritual is run once against a healthy baseline.
