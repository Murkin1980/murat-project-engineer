# EXP-30 — HtmlVR / «Семь минут» pilot edit test

Status: PLANNED / NOT EXECUTED
Disposition: EXPERIMENT
Added: 2026-10-15
Upstream: https://github.com/AntSed/HtmlVR
Owning experiment repository: `Murkin1980/murat-project-engineer`
Canon source (read-only): `Murkin1980/AI-serial-v2/episodes/01_SEVEN_MINUTES/SCENE_MAP.md`
Related: EXP-23 Papermorph, EXP-24 HyperFrames, `docs/REUSABLE_DERIVED_ARTIFACT_PATTERN.md`

## Owner request and purpose

Assess whether HtmlVR can assemble a short reproducible AI-serial video from the *actual approved pilot* of «Семь минут», with agent-editable HTML/video/audio timeline. **Do not** build a new editor, video backend, hosted service, repository, or persistent integration. The experiment is an isolated renderer/adapter comparison against our existing EXP-24 path.

## New Idea Filter record

- Decision: **EXPERIMENT**.
- Active project: AI-serial-v2, MPE experiment suite, EXP-24 existing video assembly workflow.
- Extension/reuse: reuse EXP-24 and the proven source → stable scene/beat → asset slots → render → QA contract; prefer an adapter, not duplicate orchestration or storage.
- Duplicate risk: HtmlVR overlaps Remotion/HyperFrames video assembly. Adoption requires demonstrated incremental benefit.
- Business/user value hypothesis: produce a reviewable short teaser with fewer manual timeline edits or clearer programmatic editability. Measure setup time, edit time, deterministic repeatability, and render success, not invented VRUs.
- MVP: one 20–30s teaser segment with exactly 3 approved source scenes, no new production infrastructure.
- Priority: below active production blockers; bounded Arena task only.
- Deep-change: no gate triggered by isolated read-only research/fixture/render. **STOP** before any change to canonical scenario, platform/runtime, deployment, new dependency inside production, recurring cost, production integration, or new repository; request explicit approval.

## Canonical scene selection (source locked)

Read the current source at the SHA recorded during execution:
`https://github.com/Murkin1980/AI-serial-v2/blob/main/episodes/01_SEVEN_MINUTES/SCENE_MAP.md`

- **E01-S004** — state-TV newsroom, **08:02**: cleaner's small action causes the envelope to fall and reach the wrong desk.
- **E01-S005** — **08:07–08:08**: young producer opens the envelope too early; document text: «Я принял решение не участвовать...»; calls Arman.
- **E01-S006** — Almaty, **08:09**: Arman Seytov wakes to the call; exchange «Он уходит.» / «Кто?» / «Президент.»; conclude with the title «СЕМЬ МИНУТ».

These facts are scene-map anchors, **not invented replacement screenplay dialogue**. Any missing shot-level detail is labeled experimental previs and remains noncanonical. Do not relocate people/times, change the event order or invent political claims. This is an alternate-history fiction; label test footage as fiction/previsualization.

## CP-01A — Recon / source & environment (Arena)

1. Read `AGENTS.md`, `docs/governance/SCOPE-CHANGE-CONTROL.md`, `docs/NEW_IDEA_FILTER_POLICY.md`, `docs/REUSABLE_DERIVED_ARTIFACT_PATTERN.md`, this instruction, EXP-24's approved test/adapter pattern, and the actual canonical scene map. Read any further mandatory docs identified by AGENTS.md.
2. Freeze source refs: AI-serial-v2 scene-map commit SHA; HtmlVR upstream commit/tag/license; EXP-24 comparison refs.
3. Audit HtmlVR read-only: how clips/timing/transitions/audio/JSON API work; exact browser/Node/FFmpeg/Python dependencies; headless support; offline determinism; export entrypoint, license. Identify whether Arena can run it without elevated privileges/external credentials. Do not install system services or modify production.
4. Prepare an explicit 20–30s **beat ledger** mapping E01-S004, S005, S006 to at least three stable beat IDs; list every omitted source fact or invented placeholder; separate authoritative facts from timings and derived visual choices.
5. Report CP-01A PASS / PARTIAL / BLOCKED with blockers and go/no-go for the bounded test. Do not quietly skip unavailable binary requirements.

## CP-01B — Minimal motion proof (only if CP-01A passes)

Build a non-production, isolated fixture and 20–30s MP4 if feasible:
- distinct visual beats for dropping envelope, opening/call, Arman's answer and title;
- use only approved/copyright-safe synthetic/placeholder assets, track provenance;
- title/captions legible at 360px mobile width, output ideally 16:9;
- audio: speech/audio placeholders acceptable if explicitly labeled; never invent a canon voice actor recording;
- stable scene and asset-slot identifiers; timings and edits as derived manifests;
- demonstrate 1 timing-only and 1 per-beat asset replacement without changing unrelated beats;
- run the render twice and compare video properties/output; log whether file hash is stable and, if not, explain expected encoder variation;
- inspect resultant frames, sound timing, and ffprobe metadata where available;
- compare with EXP-24 HyperFrames/Remotion: setup/render time, effort to adjust, visual fidelity, dependency burden, repeatability.

Do **not** claim PASS based only on generated HTML/JSON; inspect the actual MP4 or mark PARTIAL/BLOCKED.

## Evidence / acceptance

Store report, provenance, source ledger, manifests, command log, tool version hashes and a small playable output if allowed by repository size policies. Never commit heavyweight media without assessing repository policy. Status table: READY / WARNING / BLOCKED per source coverage, runtime, export, audio, mobile, minimal-diff edit and comparison. Include objective acceptance:

- all three canonical scenes and ordering mapped; zero unmarked additions;
- 20–30 seconds target, report exact duration;
- reproducible render commands and an inspected playable MP4;
- proof edits change only intended timeline/asset entries;
- no change to source screenplay;
- explicit recommendation **ADOPT_COMPONENT / ADOPT_WITH_CHANGES / HOLD / REJECT** backed by evidence.

## Stop and handoff

Stop after CP-01A if dependencies or source are unavailable. Stop after CP-01B evidence collection; **do not** integrate HtmlVR into AI-serial-v2 automatically. Report STATE, EVIDENCE, CHANGES, RESULT, BLOCKER, NEXT ACTION, HANDOFF, branch and PR links. Never merge/deploy without owner instruction.
