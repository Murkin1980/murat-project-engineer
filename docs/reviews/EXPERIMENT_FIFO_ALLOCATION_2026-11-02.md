# FIFO global experiment-number allocation — owner rule (2026-11-02)

Status: PROPOSED MAPPING / PR-LEVEL RENAMES AND CANONICAL REGISTRY MUTATION NOT YET DONE
Source: owner decision 2026-11-02: earliest PR creation gets the earliest available number, with dependent PRs sharing one experiment ID.

## Rules
1. Preserve existing canonical EXP-01…EXP-29, including completed statuses.
2. Sort *eligible independent unnumbered proposals* by original PR created_at (UTC), not latest changes.
3. Dependency/follow-up PRs (e.g. #105 for #104) do not consume another ID.
4. Duplicates or already registered work (e.g. #57 versus EXP-28) do not consume a fresh ID.
5. Previously cancelled standalone EXP-34 is reserved/retired, NOT reused: owner previously decided to MERGE its underlying work into Harness² #113. A new owner decision would be required to reuse 34.
6. Do not renumber already approved canonical entries; do not create phantom EXP entries for an entire series of subtrials without a review.
7. Complete overlap/eligibility checks of #56/#58/#59/#60, #102, #106, #113 and #120 before persisting rows into canonical EXPERIMENT_REGISTRY.json. Preserve original PR provenance, evidence and all necessary references.

## Chronological candidate queue (creation times verified via GitHub PR metadata)

| Proposed ID | PR owner | Created UTC | Subject | Notes |
|---|---|---|---|---|
| EXP-30 | #56 | 2026-10-08 13:22:52 | Cinematic Scene Continuity | ACTIVE_INDEPENDENT in #124 audit; confirm no canonical overlap |
| EXP-31 | #58 | 2026-10-08 16:39:36 | Text-to-CAD DXF | independent candidate |
| EXP-32 | #59 | 2026-10-08 16:43:22 | Refero Styles | independent candidate |
| EXP-33 | #60 | 2026-10-09 03:10:46 | REA reconnaissance | independent candidate |
| EXP-34 | none | — | RESERVED: cancelled standalone self-improvement EXP-34 | Do not register/reuse without explicit override |
| EXP-35 | #98 | 2026-10-11 13:57:19 | Crisp Diagrams | former competing EXP-30 |
| EXP-36 | #102 | 2026-10-13 09:12:07 | WaveSpeed evaluation series | compare to EXP-13, series-versus-experiment identity |
| EXP-37 | #103 | 2026-10-15 11:59:42 | HtmlVR | former EXP-31; branch carries old name |
| EXP-38 | #104 with dependent #105 | 2026-10-15 19:17:39 | OpenMuse | former EXP-32; preserve #105 unique evidence |
| EXP-39 | #106 | 2026-10-16 05:05:26 | Arena coding-quality series | compare Harness², EXP-27–29 |
| EXP-40 | #107 | 2026-10-16 12:35:18 | Seedance 2.5 | former EXP-33 |
| EXP-41 | #113 | 2026-10-19 07:37:15 | Harness² | consolidates cancelled independent EXP-34 proposal; do not revive it |
| EXP-42 | #116 | 2026-10-22 17:14:28 | OpenViking | compare EXP-15/26/27/29 |
| EXP-43 | #118 | 2026-10-25 13:41:35 | Nodecode Lisp Cells | former EXP-30 |
| EXP-44 | #119 | 2026-10-29 02:57:44 | AI Process Discovery | former EXP-30 |
| EXP-45 | #120 | 2026-10-29 03:16:22 | MCC bounded agents | determine whether independent from Harness² |

Business Discovery / HackerTube draft BD-HT-20261102 is NOT a PR in this MPE repository and NOT assigned an EXP number; if submitted later, place it in FIFO queue at the actual intake PR creation timestamp, subject to deduplication and registration review.

Non-claimants: #57 is an EXP-28 duplicate, #105 is dependent on #104. Earlier #25 uses a named EXP-AI-SEARCH-ENTITY identifier; retain separately and audit its identity, rather than pretending it is in numbered FIFO queue. #102 and #106 may contain multiple trial tracks but count as one parent proposal until separate independent registrations are approved.

## Implementation gate
No competing PR rewrites, force pushes, merges, branch deletions, registry edits, or deployment from this mapping alone. Next step is a scoped registry migration proposal with full path/reference audit, ensuring renamed IDs, test fixtures and dashboard views remain consistent and canonical governance is preserved. Owner-approved FIFO is binding as ordering principle, but individual eligibility and dependencies still require evidence.


## Final reconciliation addendum — 2026-11-02

Status: **FIFO ALLOCATION RECONCILED / CANONICAL REGISTRY MUTATION PENDING MERGE OF A FRESH, SINGLE-SCOPE INTEGRATION PR.**

This addendum completes the eligibility review required by rule 7 above. It is a
safe documentary allocation only: it does **not** change main, rewrite any
proposal branch, retitle a PR, reserve a second source of truth, or authorize a
merge/deploy. The canonical registry continues to end at EXP-29 until an
approved integration applies the individual contract files and required derived
views together.

### Current GitHub basis

- The actual canonical registry on main contains numbered EXP records through
  EXP-29; completed records and their IDs are unchanged.
- PR creation times below were reread from GitHub PR metadata on 2026-11-02
  (UTC). The open-PR search was also repeated; no earlier eligible experiment
  PR appeared after the first FIFO table was written.
- #105 is one dependent evidence PR for #104 and consumes no separate ID.
- #57 remains a duplicate of completed EXP-28; #108/#114 are superseded
  checkpoint instructions; none consumes a new ID.
- The former standalone EXP-34 remains intentionally retired from allocation.
  Its self-improvement work is consolidated into the unique Harness² line #113;
  it must not be recreated or reused.
- #102 (one WaveSpeed parent series) and #106 (one Arena-quality parent series)
  are each assigned one parent ID only. Their internal trials/tracks are not
  globally numbered automatically.

### Allocated FIFO queue

| Canonical ID on future integration | Source PR(s) | Created UTC | Experiment / scope | Classification | Integration condition |
|---|---:|---|---|---|---|
| EXP-30 | #56 | 2026-10-08 13:22:52 | Cinematic Scene Continuity | ACTIVE_INDEPENDENT | Bring its single bounded contract forward without affecting AI-serial canon. |
| EXP-31 | #58 | 2026-10-08 16:39:36 | Text-to-CAD DXF manufacturing | ACTIVE_INDEPENDENT | Preserve the benchmark and CAM/deep-change stops. |
| EXP-32 | #59 | 2026-10-08 16:43:22 | Refero Styles Rich Message | ACTIVE_INDEPENDENT | Keep Business Discovery pilot bounded and reuse-oriented. |
| EXP-33 | #60 | 2026-10-09 03:10:46 | REA reconnaissance | ACTIVE_INDEPENDENT | Retain as a read-only feasibility intake. |
| EXP-34 | — | — | Cancelled standalone self-improvement proposal | RETIRED_NUMBER | Never allocate; historical owner decision is MERGE into Harness². |
| EXP-35 | #98 | 2026-10-11 13:57:19 | Crisp Diagrams | PRIMARY | Rename only at a fresh integration point; old claimed EXP-30 is a historical alias. |
| EXP-36 | #102 | 2026-10-13 09:12:07 | WaveSpeed evaluation series | ACTIVE_INDEPENDENT_PARENT | Preserve one parent record; do not manufacture IDs for W01–W10. |
| EXP-37 | #103 | 2026-10-15 11:59:42 | HtmlVR Seven Minutes | PRIMARY | Correct the former EXP-31/title-branch mismatch only in a fresh integration. |
| EXP-38 | #104 → #105 | 2026-10-15 19:17:39 | OpenMuse component evaluation | PRIMARY + DEPENDENT | #104 owns identity/instructions; carry #105's five unique evidence files without loss. |
| EXP-39 | #106 | 2026-10-16 05:05:26 | Arena coding-quality series | ACTIVE_INDEPENDENT_PARENT | Keep five tracks under one parent; cross-reference Harness² without merging scopes. |
| EXP-40 | #107 | 2026-10-16 12:35:18 | Seedance 2.5 prompt evaluation | PRIMARY | Correct former EXP-33 reference at fresh integration. |
| EXP-41 | #113 | 2026-10-19 07:37:15 | Harness² self-improvement lab | PRIMARY | Sole self-improvement line; retain E0–E5 and CP-SI-01…07. |
| EXP-42 | #116 | 2026-10-22 17:14:28 | OpenViking context retrieval | ACTIVE_INDEPENDENT | Keep proposal-only and compare to EXP-15/26/27/29 before execution. |
| EXP-43 | #118 | 2026-10-25 13:41:35 | Nodecode Lisp Cells portability | ACTIVE_INDEPENDENT | Preserve MPE-IR/JSON authority and bounded research gates. |
| EXP-44 | #119 | 2026-10-29 02:57:44 | AI Process Discovery | ACTIVE_INDEPENDENT | Keep Grand Mebel pilot read-only; no production measurement claim. |
| EXP-45 | #120 | 2026-10-29 03:16:22 | MCC bounded agents / Arena / Survival | ACTIVE_INDEPENDENT | Keep P0 security/deep-change gates; do not conflate with Harness². |

### Historical-to-canonical mapping

| Legacy proposal label | Canonical ID on future integration | Treatment |
|---|---|---|
| #98 EXP-30 | EXP-35 | Superseded claimed number; content retained. |
| #103 EXP-31 | EXP-37 | Superseded claimed number; content retained. |
| #104/#105 EXP-32 | EXP-38 | One identity plus dependent evidence. |
| #107 EXP-33 | EXP-40 | Superseded claimed number; content retained. |
| #116/#118/#119 EXP-30 | EXP-42 / EXP-43 / EXP-44 | Collision resolved strictly by source-PR creation time. |
| Former EXP-34 | no global EXP number | Retired; material is represented only by EXP-41 Harness². |

### HackerTube intake

BD-HT-20261102 — HackerTube Evidence-Method Discovery is an intake in
Murkin1980/business-discovery, not an MPE PR. No MPE created_at exists, and
therefore it receives **no EXP number today**. The next candidate number is
**EXP-46**, but it may be proposed only after an actual MPE intake PR is opened,
its exact GitHub creation timestamp is checked against then-current earlier
eligible proposals, and the existing Business Discovery / video-source scope is
confirmed non-duplicate. This task does not start that research experiment.

### Required safe integration sequence

1. Start from current main; do not merge or rebase these old proposal heads.
2. For each owner-approved experiment, copy/reconcile its contract into one
   fresh single-scope integration branch, using the ID above and preserving the
   source PR link plus any dependent evidence.
3. Update the canonical registry, matching experiment contract, STATUS, and
   applicable derived dashboard views in the same integration change.
4. Run registry/schema uniqueness checks, the relevant generated-view freshness
   checks, EXP-29 freshness where affected, and existing focused/full tests.
5. Re-read GitHub branch/PR/registry after the commit. Merge and deploy remain
   separately owner-authorized.

### Verification result

- Number uniqueness: **PASS** for EXP-30…EXP-45; EXP-34 is explicitly absent.
- Historical canonical EXP-01…EXP-29 preservation: **PASS** (read-only).
- Dependent evidence preservation plan: **PASS** (#104 → #105).
- No lost proposal: **PASS** for the checked FIFO candidates.
- Canonical registry / dashboard synchronization: **PENDING**, correctly
  deferred until a fresh integration branch exists; this document does not
  falsely claim it has changed.
