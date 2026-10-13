# WaveSpeed CP-01A — Safe evidence recovery handoff

**Status:** HANDOFF PREPARED; not applied to PR #102 by this Arena session.

**Repository:** `Murkin1980/murat-project-engineer`

**Target branch / PR:** `experiment/wavespeed-tool-evaluation` / Draft PR #102

**Source evidence commit:** `ed52d78afa52375ccd092dafc5bb4acbc8c4811e` on `arena/da37d1bf-murat-project-engineer`

**Prepared:** 2026-10-13

## Objective

Safely carry the already-existing `experiments/wavespeed-evaluation/RESULTS/CP-01.md` into PR #102, without duplicating or editing the WaveSpeed registration. Run the registry checks and EXP-29 build/verify on the actual PR branch, then stop. This is a recovery/handoff task only; it does not authorize W01–W10.

## Diagnosis and verified state

- PR #102 is `OPEN / DRAFT`, head `experiment/wavespeed-tool-evaluation` at `089e2873ced13893d0dc7282e187811f472f7b5a` when checked. The branch is unprotected and the authenticated repository permissions reported `push: true`; this does **not** authorize this Arena session to switch branches.
- `EXP-WS-01` is **not missing from the PR-head authoritative registry**. On the PR head, `experiments/EXPERIMENT_REGISTRY.json` is valid JSON with 40 unique entries, ten `EXP-WS-*` entries, and exactly one `EXP-WS-01`. It is `PLANNED`, points to `experiments/wavespeed-evaluation`, and says no integration/expense/production change. The other nine WaveSpeed trials are also registered as `PLANNED`.
- `main` and the current Arena checkout are at the pre-PR registry state: 30 unique entries and no WaveSpeed IDs. PR #102 is still open, so its registration changes are not present in `main`. Do **not** add another registration to compensate.
- The previous evidence commit `ed52d78afa52375ccd092dafc5bb4acbc8c4811e` has parent `ca16094b373c1b5dccb4988edafe11fcbb525517` and adds only `experiments/wavespeed-evaluation/RESULTS/CP-01.md`. That path returned 404 on the PR head at the time of this check, and it is not among PR #102's existing changed files. It is therefore a new-file addition, not an overwrite of the PR's registry, task, or README.
- The prior EXP-29 `StopIteration` is explained by running the helper on the Arena/main-based checkout, whose local registry lacks `EXP-WS-01`; it is **not** evidence that the PR's registration is malformed and is not a reason to change the EXP-29 helper.
- On this current Arena checkout, `python3 -m json.tool experiments/EXPERIMENT_REGISTRY.json` passed; local counts were `30 / 0` (total / WaveSpeed). PR-head registry JSON parsing and uniqueness checks passed with `40 / 10`, and `EXP-WS-01_count=1`. An EXP-29 build against the current Arena checkout again exited 1 with `StopIteration`; no packet was generated and no `FRESH` result is claimed.

## Exact Codex execution steps

Run these steps only in a Codex session explicitly attached to `experiment/wavespeed-tool-evaluation`. This Arena session remains pinned to `arena/da37d1bf-murat-project-engineer` and must not switch to, commit to, or push to the target branch.

1. **Read and confirm sources.** Read `AGENTS.md`, `docs/governance/SCOPE-CHANGE-CONTROL.md`, the mandatory MPE policies listed there, `experiments/wavespeed-evaluation/ARENA_TASK.md`, `README.md`, `experiments/EXPERIMENT_REGISTRY.json`, this file, and the cited evidence commit. Confirm PR #102 is still open/draft and inspect its current head before acting.
2. **Preserve the target branch.** Run `git status --short --branch`; require the active branch to be `experiment/wavespeed-tool-evaluation`. If it is wrong, start the correct Codex session rather than switching this session. If the worktree is dirty, stop and preserve the changes; do not use `reset --hard`, `clean`, forced checkout, or stash/drop operations. Fetch current remote refs and fast-forward only when the target branch is clean and strictly behind. If the PR head has advanced or diverged, inspect and stop rather than overwriting it.
3. **Check the patch preconditions.** Verify the PR head does not already contain `experiments/wavespeed-evaluation/RESULTS/CP-01.md`. If it exists, compare it with the source commit and preserve/reconcile; do not overwrite. Fetch the source branch and inspect the exact commit:

   ```bash
   git fetch origin experiment/wavespeed-tool-evaluation arena/da37d1bf-murat-project-engineer
   git cat-file -e ed52d78afa52375ccd092dafc5bb4acbc8c4811e^{commit}
   git show --stat --oneline ed52d78afa52375ccd092dafc5bb4acbc8c4811e
   git diff-tree --no-commit-id --name-status -r ed52d78afa52375ccd092dafc5bb4acbc8c4811e
   ```

   The expected source change is one added file only: `experiments/wavespeed-evaluation/RESULTS/CP-01.md`.
4. **Apply the minimal patch without rewriting history.** From the clean target branch, cherry-pick the source commit:

   ```bash
   git cherry-pick ed52d78afa52375ccd092dafc5bb4acbc8c4811e
   ```

   If there is a conflict, unexpected changed path, or a cherry-pick failure, stop and report it. Do not force, reset, overwrite, or open a competing PR.
5. **Validate registration without modifying it.** Run `python3 -m json.tool experiments/EXPERIMENT_REGISTRY.json >/dev/null`, then verify (using Python/JSON) that IDs are unique, `EXP-WS-01` exists exactly once, and the ten `EXP-WS-01`…`EXP-WS-10` registrations remain present. Record their current statuses; do not change statuses or add entries. If an intervening authorized change altered this state, preserve it and report rather than reverting it.
6. **Build and verify EXP-29 on the actual target branch.** Use the existing helper only:

   ```bash
   python3 experiments/exp-29-arena-bootstrap-harness/harness/bootstrap_builder.py build \
     --experiment EXP-WS-01 --checkpoint CP-01 \
     --out-json /tmp/wavespeed_ARENA_CONTEXT.json \
     --out-md /tmp/wavespeed_ARENA_CONTEXT.md
   python3 experiments/exp-29-arena-bootstrap-harness/harness/bootstrap_builder.py verify \
     --packet /tmp/wavespeed_ARENA_CONTEXT.json --json
   ```

   Only report bootstrap `FRESH` if the verifier actually returns `FRESH` (exit 0). If build/verify returns an error, `STALE`, or `REJECTED`, preserve the exact output and stop; do not alter EXP-29, governance, the registry, or the packet to force freshness. The target branch contains the experiment entry and task/readme, unlike the Arena/main-based checkout; a target-branch result has not yet been observed by this session.
7. **Check the patch and PR.** Run `git diff HEAD^ HEAD --check`, inspect `git show --stat --oneline HEAD`, `git status --short --branch`, and verify the only added path is the CP-01 report. Confirm PR #102's head now contains that commit/file and that the pre-existing registry, README, and task files remain. Push only with a normal fast-forward `git push origin experiment/wavespeed-tool-evaluation`; if rejected or remote advanced, stop—never force-push. Do not merge or deploy.
8. **Stop at CP-01A recovery.** Record READY only if the evidence file is on PR #102's existing branch and the registry/build/verify checks are recorded. Otherwise report BLOCKED with exact outputs. Do not execute CP-02 or any W01–W10 workload, access paid APIs, sign in, upload files, install software, bypass egress controls, or change production.

## Required completion report

Record these fields in the Codex response (and, if recovery succeeds, in a short dated addendum to the PR's CP-01 evidence only if needed to preserve the new validation record):

- **STATE** — whether the evidence commit was applied to the target branch.
- **EVIDENCE** — current PR head, registry counts/uniqueness, builder and verifier output, diff check.
- **CHANGES** — exact paths/commit; explicitly state if no target-branch changes were made.
- **RESULT** — READY only when all CP-01A conditions above pass; otherwise BLOCKED.
- **BLOCKER** — exact branch, permission, conflict, or validation issue.
- **NEXT ACTION** — only the minimum recovery step; do not advance checkpoints.
- **HANDOFF** — PR #102 URL and full commit SHA.

## Stop boundary

No registry edits or new `EXP-WS-01` entry; no EXP-29 or governance changes; no W01–W10 execution; no paid access, sign-in, upload, install, egress bypass, merge, competing PR, or deployment. Preserve all existing PR changes. If any precondition cannot be established safely, stop and return the blocker with the current PR head and worktree state.
