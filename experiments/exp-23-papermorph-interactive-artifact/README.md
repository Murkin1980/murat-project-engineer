# EXP-23 — Papermorph document → interactive artifact

Status: PLANNED  
Decision: EXPERIMENT  
Owner: Murat Project Engineer  
Executor: Arena / Claude Code  
Priority: after EXP-22 Colibri  
Source: https://www.reddit.com/r/ClaudeAI/comments/1wwhlgb/opus_55_can_oneshot_a_video_so_i_pushed_it_a/  
Upstream: https://github.com/DozenTwelve/Papermorph

## Why

Test whether Papermorph's agentic pipeline can turn a bounded source document into a useful, editable interactive multimedia artifact, and whether its reusable parts fit existing Murat projects.

The hypothesis is not "build our own Papermorph". The hypothesis is:

> Can we reuse the source → structure → storyboard → narration → procedural animation / interaction pattern to create higher-value artifacts from existing documents and scripts with low manual correction cost?

Primary reuse targets:
- Murat Project Engineer: book/document → skill workflows
- Murat House: interactive explanatory content
- AI-serial: script → storyboard / visual scene prototype
- later, only if proven: Business Discovery or training materials

## New Idea Filter

Primary disposition: **EXPERIMENT**

- Existing project fit: strong; belongs in MPE experiments.
- Extend existing: yes; evaluate as a reusable pipeline, not a new product.
- Reuse: source parsing, structured storyboard, narration, procedural animation, quiz/interaction generation.
- Duplication risk: high if rebuilt as a standalone platform; therefore prohibited.
- Measurable value: artifact quality, factual fidelity, editing cost, generation time, reuse across projects.
- MVP: one technical/business document plus one AI-serial script sample.
- Priority: run after EXP-22 Colibri.
- Deep-change: none authorized. No new repository, product, CMS, runtime, or content source of truth.

## Experiment scope

### CP-01 — Technical/business document fixture

Use one short, verifiable PDF or chapter with clear source facts.

Run the upstream Papermorph workflow as close to stock as practical.

Capture:
- exact source and version
- model / agent used
- generated structure and storyboard
- generated narration
- generated animation / interactive artifact
- factual errors / unsupported claims
- manual correction count
- generation and edit effort
- reproducibility notes

### CP-02 — AI-serial script fixture

Use one bounded existing AI-serial scene or short episode segment.

Goal:
- test script → storyboard transformation;
- inspect scene segmentation and visual continuity;
- evaluate whether procedural animation is useful for previsualization;
- do not alter AI-serial canon automatically.

Capture:
- scene coverage
- omitted/added story beats
- character/setting continuity issues
- amount of manual correction
- whether output is useful as storyboard/previs rather than final video

### CP-03 — Component extraction review

Identify the smallest reusable pieces worth carrying into existing projects.

Candidate components:
- source → structured outline
- outline → storyboard
- storyboard → narration
- storyboard → procedural animation spec
- interactive quiz/checkpoint generation
- artifact editability / regeneration by scene

For each candidate record:
- existing MPE/project component it would extend;
- duplication risk;
- coupling to Papermorph;
- licensing;
- minimum adapter surface;
- measurable benefit.

Do not copy or integrate components unless the experiment evidence supports it and the license permits it.

## Success criteria

PASS only if all are true:

1. The technical/business fixture remains factually faithful enough for practical use.
2. The generated artifact requires acceptably low manual correction.
3. At least one pipeline component is reusable inside an existing project without creating a parallel platform.
4. The AI-serial fixture is useful as storyboard/previsualization or clearly demonstrates why it is not.
5. The result is editable/regenerable at scene or section level rather than requiring full regeneration.
6. No deep-change or new repository is required for the proof.

## Failure / stop criteria

STOP or FAIL if:
- factual hallucination rate makes the artifact unsafe to trust;
- one-shot output looks impressive but requires heavy manual repair;
- useful behavior depends on opaque one-off prompts that cannot be reproduced;
- output is effectively a non-editable final video rather than a reusable pipeline;
- upstream coupling is too strong to reuse components cleanly;
- experiment starts duplicating MPE orchestration, CMS, or AI-serial infrastructure;
- Arena discovers a deep-change requirement.

## Guardrails

- No new repository.
- No production deployment.
- No new standalone product.
- No autonomous background service.
- No AI-serial canon change from generated output.
- No automatic publishing.
- Pin upstream revision used for the test.
- Record license and dependency constraints before reuse.
- Keep all evidence under this experiment directory.
- Prefer stock upstream behavior before modifications.
- Do not expand scope beyond the two fixtures until evidence is reviewed.

## Expected evidence

Arena should add, as evidence is produced:

- `FINDINGS.md`
- `evidence/upstream.md`
- `evidence/cp01-document-results.md`
- `evidence/cp02-ai-serial-results.md`
- `evidence/cp03-component-map.md`
- generated artifact links or bounded local outputs where appropriate

## Final decision

Arena must finish with exactly one recommendation:

- REUSE_COMPONENT — adopt one or more Papermorph pipeline components into an existing project;
- HOLD — promising, but blocked by quality, model, licensing, or workflow constraints;
- REJECT — no measurable value beyond a demo.

A PASS does **not** authorize production integration.
