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

---

## Reconciliation addendum — 2026-10-31

Status: **INVENTORY VERIFIED / SAFE DOCUMENTATION UPDATE**

This addendum supersedes the 36-PR count above, which was a correct point-in-time
snapshot but is no longer current.  The repository currently has **38 open PRs**.
No PR was closed, retitled, rebased, merged, force-pushed, or deployed while
producing this addendum.

### Authoritative preflight facts

- `main` = `57a38b6277c155707aa6d935a54aac0196226ddb`.
- PR #115 is merged at that commit.  Its approved source
  `34827c9dfc2e17e8454114f1d339c902e54f7c00` and its recorded historical
  target `3bf900b4ad92a79945b5020cd1c4c63f02e04555` are both ancestors of the
  accepted result.
- PR #123 is a one-file, draft-only post-merge status synchronization based on
  the same `main`; it is not a recovery implementation and does not claim a
  deploy.
- `EXPERIMENT_REGISTRY.json` on `main` contains canonical numbered records
  through EXP-29.  No EXP-30…EXP-33 candidate is canonical.  EXP-34 remains
  intentionally unused: the owner chose **MERGE into Harness² #113**, not a new
  registry record.
- Every open head below was compared to the current `main`.  A non-mergeable
  state means its old base conflicts with current work; it is not evidence that
  the work has no value.

### Full open-PR classification

`PRIMARY` means the leading retained proposal for an identified scope;
`DEPENDENT` needs another PR's identity/instructions; `SUPERSEDED` is retained
as historical evidence but must not be integrated as-is; `DUPLICATE` repeats a
canonical outcome; `ACTIVE_INDEPENDENT` has an unrelated bounded scope; and
`NEEDS_REVIEW` needs an owner decision before it can become a merge candidate.

| PR | Classification | Experiment / checkpoint | Head SHA | Unique material and dependency | Current action |
|---:|---|---|---|---|---|
| #124 | PRIMARY | portfolio reconciliation | `83365f3` | This audit; base is current `main` | Keep as the single cleanup record; no registry mutation in this pass. |
| #123 | ACTIVE_INDEPENDENT | CP-09 post-merge status | `f5d53aa` | Nine factual `STATUS.md` lines; depends on #115 (satisfied) | Keep draft for separate owner decision; do not fold status claims into old checkpoint PRs. |
| #120 | NEEDS_REVIEW | MCC bounded agents / Survival ideas | `c946e50` | Namespaced registry candidate plus brainstorm; overlaps orchestration/Harness² boundaries | Preserve proposal; separate P0 security/deep-change decision before any integration. |
| #119 | NEEDS_REVIEW | claimed EXP-30 AI Process Discovery | `af910cb` | Grand Mebel read-only pilot protocol | Keep content, but no numeric allocation while EXP-30 collision remains. |
| #118 | NEEDS_REVIEW | claimed EXP-30 Nodecode portability | `6efdde6` | MPE-IR/JSON portability research plan | Keep content, but no numeric allocation while EXP-30 collision remains. |
| #117 | ACTIVE_INDEPENDENT | source-map awareness | `c50989c` | Small AGENTS clarification; no experiment | Safe documentation candidate after ordinary review; not part of ID reconciliation. |
| #116 | NEEDS_REVIEW | OpenViking vs EXP-29 | `af14b78` | One proposal-only retrieval comparison | Keep unnumbered proposal; compare first with EXP-15/26/27/29 and decide whether a new test is still justified. |
| #114 | SUPERSEDED | CP-09 recovery instruction | `15ac8d9` | Historical Arena instruction; #115 implemented/merged recovery | Preserve branch evidence; do not merge a now-stale task instruction. |
| #113 | PRIMARY | Harness² / CP-SI-01 | `b4b2b0c` | Owner-selected primary self-improvement line | Keep. EXP-34 is not to be created; each later checkpoint remains separately gated. |
| #108 | SUPERSEDED | EXP-29 CP-08 instruction | `7b6d8a7` | Historical instruction only | Preserve, but EXP-29 CP-08 and CP-09 closure are canonical on `main`; do not merge. |
| #107 | PRIMARY | proposed EXP-33 Seedance | `afa3c41` | Seedance plan plus registry candidate | Keep pending canonical allocation; no conflict with another EXP-33 candidate was found. |
| #106 | NEEDS_REVIEW | Arena coding-quality tracks | `fb7ba76` | Five independent research tracks | Retain, but map overlap with #113 and EXP-27/28/29 before any activation. |
| #105 | DEPENDENT | OpenMuse CP-01 evidence | `8721a3b` | Five unique audit/evidence files | Never close as duplicate: integrate only after/with #104's identity and a fresh conflict check. |
| #104 | PRIMARY | proposed EXP-32 OpenMuse | `4a798f4` | Registry record, CP-01 instruction, checkpoint map | Retain as identity owner for #105; branch name is wrong but content ID is EXP-32. |
| #103 | PRIMARY | proposed EXP-31 HtmlVR | `da885e3` | Seven Minutes bounded task | Retain; title/content say EXP-31 while branch name wrongly says exp-30. |
| #102 | NEEDS_REVIEW | WaveSpeed series | `089e287` | Ten-trial plan and Arena task | Compare with EXP-13 route/evidence contracts; no automatic merge or number change. |
| #98 | PRIMARY | proposed EXP-30 Crisp Diagrams | `25c8c37` | Crisp documentation pilot and registry candidate | Leading explicit EXP-30 claimant by creation order; retain pending owner confirmation. |
| #97 | NEEDS_REVIEW | brainstorm review policy | `268ca5a` | New governance policy | Requires explicit governance/deep-change review, not cleanup merge. |
| #92 | SUPERSEDED | EXP-13 Cloudflare preflight | `e6fab82` | Sanitized `CLOUDFLARE_AUTH_MISSING` evidence | Preserve as dated evidence; it cannot establish current credentials or be merged as a current result. |
| #90 | SUPERSEDED | EXP-13 Arena secret preflight | `47d676f` | Sanitized unsupported-secret evidence | Preserve dated evidence; later environment work requires a fresh preflight. |
| #73 | SUPERSEDED | EXP-29 CP-07 | `87e0bfa` | Earlier repair evidence, generated views and stale packet artifacts | Explicitly marked “do not merge”; later CP-08/#111 and CP-09/#115 supersede it. |
| #60 | ACTIVE_INDEPENDENT | REA reconnaissance intake | `82dc393` | Bounded feasibility note | Keep as unnumbered candidate; no collision or implementation. |
| #59 | ACTIVE_INDEPENDENT | Refero Styles intake | `9b1c7e5` | Bounded Rich Message proposal | Keep as unnumbered candidate. |
| #58 | ACTIVE_INDEPENDENT | Text-to-CAD intake | `920dceb` | Manufacturing benchmark proposal | Keep as unnumbered candidate; any CAM execution remains separately gated. |
| #57 | DUPLICATE | Pocock skills proposal | `0588161` | Original task proposal only | EXP-28 later audited the same source/patterns and closed PASS; preserve provenance, do not merge. |
| #56 | ACTIVE_INDEPENDENT | cinematic continuity | `3bc3166` | AI-serial bounded task | Keep unnumbered; belongs to a separate media decision stream. |
| #43 | SUPERSEDED | EXP-13 pilot attempt | `edf1fee` | Dated HUMAN_REQUIRED/no-spend attempt evidence | Preserve, but canonical EXP-13 remains READY_TO_TEST and no Pilot Batch is claimed executed. |
| #38 | NEEDS_REVIEW | OBS-01 governed entry code | `d72d321` | Eight production/governance code files and tests | Unique code, not an experiment-registration merge; needs fresh design, security, and conflict review. |
| #32 | SUPERSEDED | EXP-19 Shir-man intake | `724ea01` | Early registration/task | EXP-19 is canonical PASS with later CP-01 evidence; do not merge old registry state. |
| #27 | SUPERSEDED | EXP-07 Strix retry | `1f3930b` | Earlier retry evidence/test | Canonical EXP-07 outcome is PASS/HOLD for Strix; old baseline would overwrite current state. |
| #25 | DUPLICATE | AI Search / Entity readiness | `77930fb` | Registry-only historical delta | Current registry already carries the active portfolio state; no standalone merge. |
| #24 | SUPERSEDED | EXP-14 AnyJev candidate | `f61acc8` | Earlier Laya pre-registration amendment | EXP-14 later closed FAIL with a frozen-result boundary; do not reopen through this PR. |
| #19 | SUPERSEDED | EXP-16 Minimalist skills | `4aa3b83` | Original proposal | Canonical EXP-16 is RETIRED; preserve link only. |
| #14 | NEEDS_REVIEW | MPE × Business Discovery presentation | `8636d1f` | Large, isolated static presentation | Unique feature with a separate Pages implication; requires current product/deploy review. |
| #10 | NEEDS_REVIEW | EXP-13 evidence workflow | `630f0f5` | Legacy workflow/code and 25 files | Substantial unique code with a 185-commit divergence; cannot be safely treated as a registry cleanup. |
| #6 | SUPERSEDED | EXP-14 gateway bake-off plan | `3bb14ae` | Early planning docs | Later EXP-14 records/closure are canonical. |
| #3 | NEEDS_REVIEW | Compute Budget Gate | `5a844c9` | Schema, Python module, tests | Registry retains the experiment as HOLD, but implementation is not current `main`; separate technical review required. |
| #2 | SUPERSEDED | developer readiness | `0b1695f` | Early contributor scaffolding | Very old divergent baseline; preserve history, do not merge as-is. |

### EXP-30…EXP-34 identity reconciliation

| Requested/proposed ID | PR(s) | Actual content | Recommended state now |
|---|---|---|---|
| EXP-30 | #98 | Crisp Diagrams | **Provisional primary claimant.** Reserve no canonical ID until owner confirms the integration order. |
| EXP-30 | #116 | OpenViking comparison | **Collision.** Keep as an unnumbered proposal; it needs an independent filter decision after comparison with completed MPE context work. |
| EXP-30 | #118 | Nodecode portability | **Collision.** Keep as an unnumbered proposal pending a new allocation decision. |
| EXP-30 | #119 | AI Process Discovery | **Collision.** Keep as an unnumbered proposal pending a new allocation decision. |
| EXP-31 | #103 | HtmlVR; branch incorrectly says exp-30 | **Provisional coherent candidate.** Content and title agree on 31; no second EXP-31 claimant found. |
| EXP-32 | #104 → #105 | OpenMuse registration then CP-01 audit | **Ordered pair.** #104 owns identity/instructions; #105 contains unique evidence and is dependent. |
| EXP-33 | #107 | Seedance 2.5 | **Provisional coherent candidate.** No second EXP-33 claimant found. |
| EXP-34 | former self-improvement proposal | Harness² #113 | **Do not register.** Owner disposition is MERGE into #113; retain CP-SI-01…07 only there. |

This is a proposal, not a renumbering.  Historical IDs of completed experiments
remain untouched.  The next free number is deliberately not assigned to any
collision claimant in this document.

### Dependency and cleanup matrix

| Group | Retain / order | After independent verification and owner authorization |
|---|---|---|
| Current reconciliation | #124 | Update/review this audit first; no automatic merge. |
| CP-09 closure | #115 (merged) → #123 | Consider #123 only as a small, current-base status change; #114 is evidence-only superseded. |
| Harness² | #113 | Keep as the sole self-improvement line; do not create EXP-34 or activate later checkpoints automatically. |
| OpenMuse | #104 → #105 | Rebase/reconcile registry once; then carry the CP-01 evidence without losing its five files. |
| EXP-29 | canonical #111/#115 state; preserve #73/#108 | No merge of #73 or #108. Generated packets/evidence must be regenerated from canonical sources, never copied forward. |
| Closed-result duplicates | #57, #32, #27, #24, #19, #6 | Close-candidates only after owner review; their branches remain the historical evidence. |
| Dated preflight evidence | #90, #92, #43 | Close-candidates only after owner review; do not convert old environment observations into current readiness. |
| Numeric candidates | #98, #103, #104/#105, #107; #116/#118/#119 held | Decide the allocation once, then use one fresh integration PR per approved experiment. |
| Material code/features | #38, #3, #10, #14 | Separate technical reviews; they are not safe to combine with registry cleanup. |

### Verification performed

1. Read `AGENTS.md`, scope-change control, `STATUS.md`, canonical registry, and
   the original #124 audit.
2. Read current PR metadata and changed-file lists for all 38 open PRs; recorded
   each branch head and its current mergeability.
3. Compared each head to `main` using merge-base and name-status paths.  All
   legacy heads diverge from current `main`; no old branch was assumed safe just
   because its PR reports mergeable.
4. Verified #115 ancestry and #123's current-base, one-file scope.
5. Checked the high-risk collision pairs and canonical results: #104/#105,
   #108/#114/#115, #57/EXP-28, #32/EXP-19, and #73/EXP-29.

No registry or generated artifact changed, so Bootstrap FRESH, Dashboard/Reladraw
generation, and the full MPE test suite were not rerun for this documentation-only
classification.  They are mandatory before any future registry or derived-artifact
integration.

### Minimal next package

1. Owner confirms the proposed allocation order (or supplies a different one)
   for EXP-30…33, without allocating EXP-34.
2. Make one narrow integration decision for #104/#105, if OpenMuse evidence is
   to enter canonical history; do not merge either into a stale base as-is.
3. Review #123 independently as a current-base status-only change.
4. Authorize closures only from the identified close-candidate groups after a
   final head/SHA re-read.  No branch deletion is implied.
