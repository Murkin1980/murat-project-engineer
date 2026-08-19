# Stage 3 — Synthetic Stakeholder Evaluation

Status: PLANNED / POST-STAGE-2
Date added: 2026-08-19
MPE New Idea Filter disposition: `EXTEND_EXISTING`

## Position in the roadmap

This stage is intentionally deferred until Stage 2 is completed and `STAGE2_EXPERIMENT_REVIEW.md` has produced an architecture decision.

Current order remains:

1. Complete EXP-12 prospective validation.
2. RUN-13 — Goal + Run Contract.
3. RUN-14 — Typed Handoff / Gate / Evidence / Terminal State.
4. RUN-15 — Validator Hardening + Negative Tests.
5. RUN-16 — Context Provenance.
6. RUN-17 — Review / Approval Contract.
7. RUN-18 — Trace ↔ run_id Observability Contract.
8. RUN-19 — Run-Level Audit Dashboard.
9. RUN-20 — Stage 2 Governed Delivery Capstone.
10. Complete Stage 2 review and architecture decision.
11. Then begin controlled Synthetic Stakeholder / Persona Evaluation experiments.

Synthetic personas must not be mixed into EXP-12 CLEARS validation because EXP-12 measures triage accuracy and approval classification on real tasks. Mixing synthetic-persona quality into that experiment would confound two separate hypotheses.

## Goal

Evaluate whether MPE-governed outputs remain useful, understandable, safe and robust across heterogeneous simulated users, experts and stakeholders.

The goal is not to make synthetic personas authoritative. They are an evaluation layer that may expose blind spots, usability failures, domain-specific risks and stakeholder conflicts before human review or production release.

## Core hypothesis

A controlled population-style evaluation can find materially different defects and concerns than a single generic Reviewer, while MPE governance keeps the simulation reproducible, auditable and bounded.

## Candidate stakeholder/persona classes

Initial evaluation pool should include a deliberately diverse set such as:

- legal professional;
- accountant / finance specialist;
- medical professional for healthcare-related products only;
- software / technical specialist;
- small-business owner;
- ordinary non-technical customer;
- low digital-literacy user;
- older user;
- power user;
- security/privacy reviewer;
- process auditor;
- accessibility-oriented reviewer;
- procurement / operations stakeholder;
- customer-support perspective.

Personas must be task-relevant. Do not invoke medical, legal or other specialist personas when the target artifact does not involve that domain.

## Candidate external systems and research inputs

Revisit the synthetic-persona / simulation systems previously researched, including Tencent-, Google- and MiraFish-like approaches and other multi-persona / social-simulation projects discovered during MPE research.

Before implementation, re-verify the current state, licensing, reproducibility, API/runtime requirements and whether each system can be reused as:

- a persona source;
- a simulation runtime;
- a benchmark/dataset source;
- an evaluation pattern only;
- or should be rejected.

Do not copy an external platform wholesale. Prefer reusable evaluation patterns and adapters behind MPE contracts.

## Proposed experiment sequence

### S3-EXP-01 — Persona Contract

Define a minimal machine-readable persona/stakeholder contract containing:

- persona/stakeholder id;
- role/domain;
- task-relevant background;
- goals;
- constraints;
- evaluation lens;
- prohibited assumptions;
- source/provenance;
- version.

Success criterion: persona definitions are reproducible and auditable rather than free-form roleplay prompts.

### S3-EXP-02 — Multi-Persona Review Baseline

Run one already-governed artifact through a small fixed set of personas and compare findings against a standard independent Reviewer.

Measure:

- unique valid findings;
- duplicate findings;
- false positives;
- contradictory recommendations;
- useful rework caused;
- human-review burden.

### S3-EXP-03 — Population Diversity Test

Increase persona diversity and test whether broader simulated populations reveal additional issue classes or only add noise/cost.

Stop expanding the population when marginal useful findings fall below an agreed threshold.

### S3-EXP-04 — Domain Specialist Evaluation

Use task-relevant specialist personas on a domain project such as MebelLegal or MebelDocs.

Synthetic specialist findings must remain advisory and require deterministic/domain checks or qualified human review before being treated as valid.

### S3-EXP-05 — UX / Customer Simulation

Use Kitchen/Furniture Configurator or another customer-facing workflow to test usability across non-technical, low-digital-literacy, older and power-user profiles.

Measure comprehension failures, dead ends, ambiguous terminology, missing guidance and unnecessary friction.

### S3-EXP-06 — Stakeholder Conflict / Trade-off Test

Run the same governed delivery through conflicting stakeholder lenses, for example:

- customer vs operations;
- speed vs compliance;
- product vs security;
- sales vs legal;
- novice vs power user.

Require MPE to preserve findings and trade-offs as evidence rather than silently collapsing them into one answer.

### S3-EXP-07 — Synthetic Evaluation Gate

Experiment with a bounded optional gate that can require synthetic stakeholder evaluation for selected task classes.

It must not become a mandatory universal gate unless evidence shows measurable value at acceptable cost and false-positive rate.

## Recommended first target projects

After Stage 2, use projects that expose different stakeholder surfaces:

1. **Kitchen / Furniture Configurator** — best first UX and customer-population candidate.
2. **MebelLegal KZ** — legal/compliance specialist evaluation.
3. **MebelDocs AI** — accounting/operator/non-technical workflow evaluation.
4. **Business Discovery** — later, for multi-stakeholder business hypothesis testing once MPE evaluation semantics are stable.

Do not start with Business Discovery if the evaluation layer itself is still unstable; first validate it on bounded products with observable acceptance criteria.

## MPE integration model

Synthetic stakeholder evaluation should plug into the existing governance layer as an evaluation/review capability, not become a parallel orchestration system.

Preferred flow:

`Governed Run → validated artifact → selected persona set → independent persona findings → deduplication/aggregation → deterministic/domain checks → human review where needed → evidence record → gate/result`.

MPE remains responsible for:

- selecting when the evaluation is warranted;
- recording persona versions and provenance;
- evidence capture;
- review/gate policy;
- terminal decision semantics.

External simulators remain replaceable execution/evaluation adapters.

## Metrics

Track at minimum:

- unique valid findings per persona/group;
- precision / false-positive rate;
- useful rework rate;
- overlap with standard Reviewer findings;
- stakeholder-conflict rate;
- human adjudication burden;
- token/runtime/cost overhead;
- escaped defect reduction where observable;
- stability/repeatability across identical runs;
- marginal value of adding more personas.

## Guardrails

- Synthetic personas are not humans and must not be represented as real user research.
- Do not treat synthetic demographic or professional behavior as ground truth.
- Do not infer protected or sensitive traits about real users from persona outputs.
- Specialist personas do not replace qualified legal, medical, accounting, security or other professional review where such review is required.
- Preserve provenance and versioning for persona definitions and external simulation systems.
- Keep findings observable; do not store hidden chain-of-thought.
- No autonomous production approval from synthetic persona consensus.
- No new persistent runtime, scheduler or generic workflow engine solely to support this stage without a separate deep-change decision.

## Exit criteria

Stage 3 should be considered successful only if controlled experiments show that synthetic stakeholder evaluation produces incremental, reproducible, decision-useful findings at acceptable cost and false-positive burden.

Possible final dispositions:

- `KEEP_AS_OPTIONAL_EVAL`;
- `PROMOTE_FOR_SELECTED_TASK_CLASSES`;
- `ADJUST_PERSONA_MODEL`;
- `RESEARCH_MORE`;
- `STOP`.

The intended product contribution is a governed **Synthetic Stakeholder Evaluation Layer** for MPE — not a synthetic-user product and not a replacement for real user testing.