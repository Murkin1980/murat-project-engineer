# MPE Experiment Identity & Naming Standard

Status: ACTIVE / MANDATORY FOR NEW REGISTRATIONS
Date: 2026-11-02
MPE New Idea Filter: EXTEND_EXISTING
Scope: All new MPE-governed experiment intakes (ChatGPT, Work, Arena, Codex, GitHub and project-local drafts).
Source of truth: Existing `experiments/EXPERIMENT_REGISTRY.json`; no parallel registry.
Dependency: CP-REGISTRY-FIFO-INTEGRATION PR #126 is merged in `main` at
`76cfd29254656ff211524a816f7c7e72335520f1`; its allocation and provenance
must not be overwritten.

## Objective
Stop inconsistent, unnumbered and duplicate experiments from entering the portfolio. Keep the existing registry and schema intact; use a human-readable display convention without changing stored canonical IDs.

## Identity contract
1. Canonical identity: `experiment_id` assigned ONLY from the existing MPE canonical registry after uniqueness, collision, FIFO and scope checks. Existing ID strings are immutable; do NOT bulk-renumber, reformat or migrate existing entries.
2. Display heading: `EXP-<number> — <Owning Project> — <Short Descriptive Name>`, e.g. `EXP-46 — Business Discovery — HackerTube Evidence Methods`. Padding (such as EXP-046) is purely optional UI formatting and MUST NOT change the stored ID.
3. The canonical registry field `name` is a concise distinctive experiment title, not merely a project name and not a second ID. `owning_project`, `repo` and `experiment_path` identify ownership and location separately.
4. A project-local brainstorm/intake without a global ID uses a collision-resistant temporary intake key (e.g. `BD-HT-20261102`) explicitly labeled `UNNUMBERED / DRAFT`. It is NOT a globally registered EXP. No placeholder EXP ID.
5. One parent global number per independently scoped experiment. Subexperiments, checkpoint PRs and evidence PRs reuse parent ID with local sublabels; no number consumed unless separately approved as independent scope.
6. Retired/reserved numbers are never recycled without an explicit owner decision.

## Mandatory pre-registration gate — order matters
A. Read current governance, MPE canonical registry, latest merged FIFO allocation, and relevant pending integration PRs. Do not treat unmerged planned records as committed; do treat them as active collision claims.
B. New Idea Filter: inspect all active and historical experiments (canonical and unmerged PRs), same-goal synonyms, related components, duplicate infrastructure, business value, smallest measurable MVP, priority, deep-change risks.
C. Classify request: NEW_INDEPENDENT / EXTEND_EXISTING / DEPENDENT_EVIDENCE / DUPLICATE / INTAKE_ONLY / BLOCKED. If existing experiment covers the scope, reuse its ID and link source, no new number.
D. Identify authoritative first original GitHub PR for each independent proposal. Rank eligible unallocated proposals by original `created_at` UTC (earliest first). Commit timestamps, issue dates, renames and branch names do not supersede PR creation time. Cross-project intakes acquire FIFO position when submitted as eligible MPE intake PR, not backdated from project-local notes.
E. Determine next unreserved free number, checking canonical main, open PRs, pending integration assignments, historical aliases, retired IDs and same-number claims. Atomically re-check immediately before registration; any race/conflict => STOP/RECONCILE, not blind insertion.
F. Assign a short meaningful title with discriminating object and action/method; never use only a project name, generic 'AI test', or conflicting duplicate name. Record owner, problem, hypothesis, evidence, measurable success/failure threshold, source PR, dependencies and current status using the existing registry contract.
G. Validate schema, global ID uniqueness, references, provenance and derived views; read back committed data. Report assigned ID only when persisted. Never claim a draft or proposed assignment is canonical.

## Source-specific behavior
- ChatGPT / Work / Arena / Codex requests: first apply the same gate; can write a project-local intake draft, but cannot fabricate a globally assigned number before the MPE PR/intake and registration.
- Project-specific repositories: retain local task/branch labels; MPE registry is the single global experiment catalog. Project-local files should link back to the global ID only after registration.
- GitHub PR: detect another in-flight PR with equivalent objective before allocating; dependent PRs reuse parent ID, preserving unique evidence.
- Existing historic named experiment IDs such as EXP-ALEXANDRIA and EXP-RANKCONTROL: grandfather them, preserve identifiers and links; classify them separately in a later migration proposal if needed. No forced conversion under this rule.
- A candidate whose only distinguishable information is a project name is INTAKE_ONLY until specific objective and measurable hypothesis are given.

## Example
Before registration: `BD-HT-20261102 — HackerTube methods`, project Business Discovery; linked MPE PR #125.
After approved canonical registry integration (and a fresh FIFO check): `EXP-46 — Business Discovery — HackerTube Evidence Methods`; stored ID remains `EXP-46`, not `EXP-046`.
No research is launched by registration.

## Rollout and safeguards
- This standard augments existing governance; it does not alter the canonical ID schema.
- Enforcement remains a pre-registration procedure across every agent interface. A new cross-repository service, write authority, or automation is outside this standard and requires explicit owner approval through the deep-change gate.
- Implement through the existing registry, schema validation, canonical tests and derived-view checks; no new service, repository, registry, automation or infrastructure.
- Minimal acceptance: two identical requests resolve to the same prior experiment or one intake; two distinct requests receive ordered unique IDs by GitHub PR created_at; project-only names cannot masquerade as registered experiments; existing historical IDs stay intact; EXP-34 is never reused.
- No merge, deploy, old-PR closure or branch deletion authorized by this draft.
