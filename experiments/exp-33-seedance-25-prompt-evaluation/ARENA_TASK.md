# EXP-33 — Seedance 2.5 Prompt Writing / AI-Serial Evaluation

Date: 2026-10-16
State: PLANNED (no generation executed)
MPE primary disposition: REUSE_COMPONENT
Repository: `Murkin1980/murat-project-engineer`
Owning product: existing AI-Serial Studio / AI-serial-V2; no changes to either product in this experiment.

## New Idea Filter
- Existing capabilities: AI-Serial Studio already has scene/beat/asset workflow; EXP-23 and EXP-24 established source → stable beats → asset slots → QA → minimal-diff revision.
- Reuse: official Seedance 2.5 prompting methodology and possibly the `sd25-pe` Skill, after review, only as an optional prompt technique.
- Duplication avoided: no new repository, video pipeline, storyboard data store, character database, provider gateway, credentials, UI, or deployment.
- Business value to test: fewer retries and lower cost per *accepted* scene with stable character identity and requested camera behavior. No numeric improvement is assumed in advance.
- Smallest MVP: one sanitized, owner-approved short beat from the existing pilot “Seven Minutes”; three prompt arms, same inputs and target conditions; research-only dry run before any paid generation.
- Priority: bounded R&D supporting AI-serial; do not preempt current production blockers or existing P0 work.
- Deep-change: none for documentation / offline comparison. Any new model API, installation of third-party executable Skill, account credentials, paid run, video publishing, or production integration requires separate review/approval.

## Verified source and caveats
- ByteDance/Lark: https://bytedance.larkoffice.com/docx/A88jd0B47oAd8zxWp5ycZFMfnxh
- BytePlus linked technical docs: https://docs.byteplus.com/en/docs/ModelArk/2607689
- Observed guide title: “Dreamina Seedance 2.5 Prompt Writing Guide”.
- Document states a core formula: subject + action/event + scene + visual style + camera + audio.
- It describes limits up to 30 images (each ≤4K), up to 10 reference videos (combined ≤30s), up to 10 audio clips (combined ≤30s), and up to 50 materials overall, subject to access/product behavior verification.
- Assign explicit roles to references: @Image for appearance or scene, @Video for motion/camera/pacing, @Audio for voice/ambience. Exclude unwanted attributes carried over from each reference.
- Official example suggests local installation via `npx --yes skills@latest add "https://arkdocs-en.tos-ap-southeast-1.volces.com/skills/" --skill sd25-pe --yes`; **do not run it in CP-01**.
- Guide itself warns prompting does not override inherent model limits; stability, realism, camera execution and outcomes are not guaranteed.
- Guide availability, pricing, license, model access and Skill trust have NOT been independently proven.

## Checkpoints
### CP-01 — Source, compatibility, security and no-cost prompt fixture
Read AGENTS.md, docs/governance/SCOPE-CHANGE-CONTROL.md, docs/NEW_IDEA_FILTER_POLICY.md, docs/REUSABLE_DERIVED_ARTIFACT_PATTERN.md, this file, and the relevant existing EXP-23/24 source/beat contracts. Verify guide provenance / date / latest model availability. Review the Skill source only as nonexecuted text (inspect file manifests, dependencies, scripts, permissions, network/telemetry, license, remote code and supply chain; do not execute `npx`). Identify an already-authorized, non-spoiler, sanitized pilot beat; if not verifiable, make a clearly marked synthetic analogue and document the substitution. Reuse stable scene and beat IDs, record reference provenance and exclusion clauses. Prepare prompt variants A (ordinary), B (guide structured), C (Skill-optimized **only if source is safe and offline execution is explicitly authorized; otherwise static manual approximation marked distinct, NOT claimed as Skill output**). Fix common shot goal and rubric. No model calls, API keys, runtime modifications or purchases.

**CP-01 output:** `CP-01_REPORT.md` and `fixture/README.md` (may include prompt templates). Include provenance, access observations, legal/security notes, real-vs-synthetic label, exact ready-to-run comparison recipe, costs/availability unknowns, and blockers. Gate: PASS only if fully reproducible and no prohibited access/installation; otherwise PARTIAL/BLOCKED.

### CP-02 — Controlled A/B/C evaluation (separately authorized)
Only after owner authorizes access/cost. Hold constant scene, references, duration, resolution, output settings, seeds if exposed, and evaluation rubric. Record every attempt and actual credits/tenge/USD where available, retries and latency. No cherry-picking; evaluate blind where practical. Do not call manually authored C an actual Skill result. Capture consent/licensing for every asset.

### CP-03 — Evaluate findings / adoption decision
Rubric (0–5 per criterion): scene canon fidelity; subject identity continuity; event and cut order; camera compliance; visual style; voice/sound consistency; reference leakage; artifacts. Record attempted/accepted count and actual cost per accepted clip. Compare against A baseline; no benefit claims without observed outcomes. Disposition: ADOPT_WITH_CHANGES / KEEP_EXPERIMENTAL / DO_NOT_ADOPT with risks and reproducibility. A PASS is not proof of production readiness.

### CP-04 — Optional integration proposal, not implementation
Only if CP-02/03 justify it and owner approves. Specify smallest extension to existing prompt profile / source→beat→asset contract. No automatic editing of pilot canon, no public publishing, no new repository, no provider/runtime modification without deep-change check.

## CP-01 Arena authoritative instruction
Work ONLY in `Murkin1980/murat-project-engineer`, branch `experiment/seedance-25-prompt-evaluation`. Follow the required reads above. Begin with CP-01 only; do not execute later checkpoints. Read current repository and active overlapping experiment PRs first. Do not duplicate EXP-23/24 structures or rewrite their fixtures. Create the CP-01 report and fixture under `experiments/exp-33-seedance-25-prompt-evaluation/`; keep changes small and confined. Evaluate the Lark guide and optional Skill source read-only. Use no external account auth, keys, paid generation, `npx`, install scripts, new services, or AI-serial private material unless access and provenance are independently verified. In case of unavailable source, describe blocker and provide synthetic fixture, without pretending it is canonical. Report STATE / EVIDENCE / CHANGES / RESULT / BLOCKER / NEXT ACTION / HANDOFF; include commit SHA, branch, PR status and tests where applicable. Do not merge/deploy. Stop at CP-01. Escalate for explicit approval if any protected boundary is reached.

## Acceptance and rollback
CP-01 acceptance: source links and direct observations cited, same controlled shot objective and explicit role mapping, three clearly distinguished arms with honest C status, risk/security checklist, no credentials or costs incurred, no canonical script mutation. Rollback: revert documentation-only branch/PR; none of the production surfaces are changed.
