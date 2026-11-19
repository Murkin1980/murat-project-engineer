# EXP-47 — Skill Multik: bounded explainer-video component evaluation

Date: 2026-11-19
Status: PLANNED / REGISTRATION ONLY
Primary MPE decision: EXPERIMENT
Owning product candidate: AI Serial Studio (`Murkin1980/AI-serial-v2`)
Canonical experiment registry: `experiments/EXPERIMENT_REGISTRY.json`
Upstream: https://github.com/artemiimillier/skill-multik

## Purpose and business value

Investigate whether selected source-grounded motion graphics, word-aligned cues, scene animation, and reusable character techniques from skill-multik can improve production of vertical 9:16 explainers for Salamat Mebel or Murat House without establishing another production pipeline. Measure human editing minutes, total cost per accepted 20–30-second clip, readability, reproducibility and asset reusability. No verified benefit is claimed at registration.

## Mandatory reuse / overlap check

1. Read current `Murkin1980/AI-serial-v2` foundation, architecture, agents instructions, canon and workspace defaults. Existing characters, canon, publishing and authorization are authoritative.
2. Reuse MPE `docs/REUSABLE_DERIVED_ARTIFACT_PATTERN.md`: canonical source → stable beats → optional word marks/cues → timings/asset slots → derived output → mobile QA → minimal-diff corrections.
3. Compare with EXP-23 and EXP-24 CP-13, including the prior Remotion preview and 360px QA; determine whether the upstream offers any *incremental* capability. Cross-check EXP-30 continuity and EXP-40 media work to avoid duplicate scope.
4. Do not modify AI Serial Studio unless the owning project passes an independent compatibility and deep-change review.

## CP-01 — read-only upstream and portfolio audit (not yet authorized for execution)

- Identify license and source provenance, install scripts, transitive dependency risks and externally executed commands.
- Map the exact role of Piratex AI, offered credits, ElevenLabs, Telegram, API keys and data transfer, identifying whether usage is optional or mandatory and whether it introduces costs.
- Check compatibility with existing render, speech, image, storage, authorizations, and media pipelines; document reusable components rather than adopting the whole skill.
- Produce a narrow comparison matrix against current AI Serial Studio and EXP-24 CP-13 with a go/no-go decision and proposed isolated trial budget.

## CP-02 — bounded isolated demo (separately authorized, NOT STARTED)

Only after a CP-01 PASS and owner-approved cost and credentials: produce **one** 20–30-second vertical explainer (`Как создаётся мебель на заказ`) using a sanitized script and non-sensitive approved assets. Measure accepted-output cost, human work saved, visual QA at 360px, word/visual synchronization, stable scene/beat IDs, deterministic rerender and one minimal-diff correction. Compare same fixture to the established approach. No automatic publishing or Telegram transfer.

## Stop / deep-change gates

Registration grants no permission to install the upstream, run `npx degit`, connect Piratex, share character photos/voices/canon, buy credits, expose secrets, deploy, merge, or change production. New infrastructure, recurring cost, auth/security changes, canon/source-of-truth changes, new repository, or replacement video pipeline require explicit owner approval. Never treat marketing credits or external trend claims as independently verified.

## Outcome

- **RESULT:** PLANNED, no experiment executed.
- **EVIDENCE:** upstream URL and existing MPE reuse pattern; measurement not yet available.
- **NEXT ACTION:** separately authorize CP-01 read-only audit, then review evidence before CP-02.
