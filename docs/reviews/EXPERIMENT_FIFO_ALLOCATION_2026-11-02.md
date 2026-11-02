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
