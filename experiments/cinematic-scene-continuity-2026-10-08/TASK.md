# Experiment candidate — Cinematic Scene Continuity

Status: **REGISTERED / NOT RUN**  
Date: 2026-10-08  
Murat Project Engineer New Idea Filter: **EXPERIMENT**  
Owner project: **AI-serial-V2**  
Execution venue: **Arena**, isolated branch and bounded run.  
No new repository, independent memory service, pipeline replacement or production integration.

## Source and hypothesis

User-supplied video: `1000803733.mp4` (2026-10-08, retained in conversation/library; not copied into Git). The clip demonstrates a workflow described as **Banana Pro Director / Cinema World Builder**: obtain multiple complementary camera angles from a consistent scene description. Names, vendor claims, technical availability, terms, licensing and actual compatibility **must be independently verified** before adoption; video is demonstration evidence, not a production test.

**Hypothesis:** structured director/world prompts + a scene identity anchor can improve consistency between sequential shots and reduce production time/cost versus current per-shot generation.

## MPE filter

- Existing projects: AI-serial-V2 (scene/canon authority), Murat Image Prompt (visual prompt template), AI-microtask-factory (checks), EXP-24 HyperFrames (assembly; currently PARTIAL owing to missing Chrome/FFmpeg).
- Extend existing: yes — add a bounded prompt/shot-planning technique to the present AI-serial pipeline if validated.
- Reuse: character bios/canon, prompt skeleton, existing video engines and quality gates.
- Duplication avoided: no new character registry, agent, orchestrator, memory store or video-generation application.
- Business value: fewer regeneration attempts, more accepted seconds per budget, stronger continuity; **not yet measured**.
- Minimal MVP: 1 approved scene, 5 camera angles, 2 methods, one matched budget.
- Priority: medium/high for AI-serial; downstream only for Salamat Mebel commercials and Murat House.
- Deep-change: **NO** at experiment-only prompt/asset level. Any canonical visual-rule change, new pipeline, dependency, production rollout, or architecture migration requires separate explicit owner approval.

## CP-01 to CP-05 — bounded Arena task

1. **CP-01 Inventory and verify.** Read AI-serial-V2 canon + current production methodology + Murat Image Prompt and EXP-24 findings. Identify the actual upstream skills/tools referred to in the video, their provenance, license, limitations and whether functionality is just prompting or includes a runtime. No unverified installation.
2. **CP-02 Freeze test.** Choose one *already approved* scene from episode 2 «Технократы» (no canon rewrite). Freeze scene, character identities, costumes, location, lighting, visual style and reference assets. Five fixed shot types: wide, medium, close-up, over-the-shoulder, camera-movement.
3. **CP-03 A/B.** Baseline: current shot-by-shot method. Candidate: structured director/world continuity prompts. Same scene, model/provider where possible, shot count, budget/time limit and seed/reference control; document unavoidable confounders. No uncontrolled regeneration loop.
4. **CP-04 Measure.** For every shot, record character identity consistency, costume/location continuity, coherence of camera grammar, style compliance (watercolour environment, 3D moving subject), temporal artefacts, attempts, human correction minutes, generation cost and accepted output seconds. Store prompt variants and repeatable evaluation rubric.
5. **CP-05 Decide.** Output `PASS`/`PARTIAL`/`FAIL`/`BLOCKED`, with evidence and adoption verdict `ADOPT`/`ADOPT_WITH_CHANGES`/`DO_NOT_ADOPT`. Only suggest rollout if quality has not degraded and there is a defensible reduction in time or cost; preliminary 20% reduction is a test target, not a demonstrated result.

## Stop conditions and deliverables

- Stop if rights, licensing or content availability are unclear, a needed reference is missing, credentials/payment are required, scene or character canon would change, or execution would cross a DEEP-CHANGE gate.
- Do not modify production, merge, deploy, invoke paid APIs without budget approval, invent citations, or present a storyboard as finished video.
- Experiment deliverables: `TASK.md`/upstream audit, frozen test fixtures, shot list, prompts, A/B results, cost/consistency table, limitations, and a one-page `RESULTS.md` decision.
- EXP-24's render blocker (Chrome/FFmpeg) is independent: still-image continuity checks may proceed without promising a render.

## Downstream reuse (only after PASS)

1. AI-serial-V2: controlled director-style prompt module layered on Murat Image Prompt.
2. AI-microtask-factory: continuity QA rubric as a reusable validation component.
3. Salamat Mebel: second small A/B test for multiple angles of one furniture product, without implying exact CAD/dimensional fidelity.
4. HyperFrames EXP-24: shot/storyboard input only once its runtime dependencies and clean lint are resolved.

**Current status: registered only; no Arena execution or merge authorized by this registration.**
