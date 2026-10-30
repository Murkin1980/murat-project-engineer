# MPE Experiment and PR collision audit — 2026-10-30

Status: READ-ONLY TRIAGE COMPLETE / REMEDIATION NOT AUTHORIZED
New Idea Filter: MERGE (consolidate overlapping proposals into existing MPE registry and checkpoint governance)
Scope: Murkin1980/murat-project-engineer only. No PR merges/closures, registry renumbering, branch deletion, deploy, or changes to competing proposals performed.

## Verified snapshot

- Canonical `experiments/EXPERIMENT_REGISTRY.json` on `main` has numbered records through EXP-29, which is PASS. EXP-30 through EXP-33 appear in pending PRs, not canonical `main`.
- GitHub open PR search returned **36 open PRs**. Count is a snapshot, not a complete guarantee about unindexed projects or local branches.
- PR #115 CP-09 recovery has already merged; merge SHA `57a38b6277c155707aa6d935a54aac0196226ddb`.
- PR #123 carries post-merge status sync as draft; not yet merged. No deploy authorized.
- Historical EXP-34 Self-Improving Harness proposal cancelled by owner: **MERGE** into Harness² PR #113. Do not register EXP-34. Preserve CP-SI-01…07.

## Collision matrix — do not assign numbers until reviewed

| Requested ID | PR | Topic | Verified PR branch / mergeable snapshot | Action |
|---|---|---|---|---|
| EXP-30 | #98 | Crisp Diagrams | experiment/exp-30-crisp-diagrams / false | NUMBER COLLISION, HOLD |
| EXP-30 | #116 | OpenViking vs EXP-29 context retrieval | experiment/openviking-context-evaluation-20261022 / true | NUMBER COLLISION; evaluate reuse with EXP-29 |
| EXP-30 | #118 | Nodecode Lisp Cells | experiment/nodecode-lisp-portability-20261025 / false | NUMBER COLLISION, HOLD |
| EXP-30 | #119 | AI Process Discovery | experiment/exp-30-ai-process-discovery / false | NUMBER COLLISION; assess overlap with existing AI Discovery intake |
| EXP-31 | #103 | HtmlVR Seven Minutes | experiment/exp-30-htmlvr-seven-minutes / false | Title/branch ID mismatch; verify content before retitling |
| EXP-32 | #104 | OpenMuse registration | experiment/exp-30-openmuse-component-evaluation / false | Title/branch ID mismatch; coordinate with #105 |
| EXP-32 | #105 | OpenMuse CP-01 audit | arena/9196ade0-murat-project-engineer / true | Dependent on #104; preserve audit evidence; choose primary PR only after review |
| EXP-33 | #107 | Seedance 2.5 | experiment/seedance-25-prompt-evaluation / false | Pending, not reserved on main |
| unnumbered | #113 | Harness² | experiment/harness2-self-improvement-lab / true | PRIMARY for self-improvement; former EXP-34 cancelled |
| unnumbered | #120 | MCC agent isolation / Survival / server ideas | experiment/mcc-bounded-agents-2026-10-29 / false | Keep bounded; compare with existing orchestration proposals |

## Existing-result / stale-work review queue

- #108 EXP-29 CP-08 task instruction: EXP-29 is already PASS; compare against canonical records and close superseded proposal only after verifying unique changes.
- #114 CP-09 recovery instruction: PR #115 already merged; audit whether it is documentation-only superseded. Do not blindly merge old checkpoint instruction.
- #73 EXP-29 CP-07 / EXP-22 fix: explicitly 'do not merge', currently conflict; review for unique valid state before any closure.
- #57 Pocock /retro patterns: compare to canonical EXP-28 PASS before any duplicate promotion.
- #32 EXP-19 older PR: compare to canonical EXP-19 PASS and current generated dashboard/Reladraw; no blind merge.
- #123 post-merge status: keep pending for targeted status reconciliation, do not treat as a new experiment.
- #102 WaveSpeed evaluation: reconcile with the existing EXP-13 and prior WaveSpeed work; do not assign a number without review.
- #106 Arena coding quality: cross-check Harness² #113, EXP-27/28/29, and independent test goals. Do not conflate an evaluation series with an entire infrastructure proposal.
- #117 Source Maps, #97 brainstorm policy, #92/#90/#43 EXP-13, older #2/#3/#6/#10/#14/#19/#24/#25/#27/#38/#56/#58/#59/#60 are still open and need owner-scope review before changing them.

## Proposed reconciliation protocol

1. Freeze number allocation: neither title, branch name nor draft PR alone is canonical ID ownership; canonical registered records and approved reservation records take precedence. No automatic renumber.
2. Build one row per PR recording PR/base/head SHA, scope, canonical experiment ID (if any), counterpart PRs, current state, unique diff, test/evidence links, deep-change risk, recommendation, and owner authorization.
3. Classify each PR as PRIMARY, DEPENDENT, SUPERSEDED, DUPLICATE, ACTIVE_INDEPENDENT, or NEEDS_REVIEW; **do not** conflate these classification labels with canonical experiment statuses.
4. For PR pairs (#104 + #105, #113 + cancelled EXP-34, #108 + completed EXP-29, #114 + merged #115), establish one owner and ordered checkpoints. Retain only nonduplicate contributions and provenance.
5. Resolve EXP-30 competing candidates through separate MPE New Idea Filter decisions; do not reserve free IDs on their behalf. EXP-31/32/33 remain provisional until registry integration and collisions resolved.
6. Before any code/data PR merge, run canonical registry schema validation, dashboard/Reladraw generation/consistency, EXP-29 packet freshness and focused/full tests. Do not overwrite `main` canonical closure or another active experiment.
7. Prefer one bounded integration PR per coherent experiment. Close old PRs only after verified content/links and explicit owner authorization. No forced rebases or branch deletions.
8. Deep-change gate for governance, system architecture, execution authority, security boundaries, source-of-truth changes, or new infrastructure.
9. Synchronize canonical project STATUS and portfolio monitor only after actual merges are verified; do not claim full portfolio sync before attributable evidence exists.

## Current recommendation and next authorized action

Prepare PR-by-PR read-only classification and a proposed ID allocation table, ordered by already-accepted work. Obtain owner approval **before** changing existing PR title, branch, registration, closing or merging PRs. Existing PR #113 remains the Harness² primary. Do not use EXP-34. No deploy.

Success criteria: no duplicate canonical numeric IDs; no multiple uncontrolled implementations for one objective; PR scope and provenance preserved; every proposed closure or merge backed by content diff and explicit owner approval.
