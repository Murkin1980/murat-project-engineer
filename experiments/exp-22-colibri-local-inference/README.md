# EXP-22 — Colibri local inference / Brio routing

Status: PLANNED  
Decision: EXPERIMENT  
Owner: Murat Project Engineer  
Executor: Arena  
Source: https://justvugg.github.io/colibri/  
Upstream: https://github.com/JustVugg/colibri

## Why

Evaluate Colibri as a bounded local inference provider for existing MPE systems, not as a new platform or repository.

The useful hypothesis is not "run the biggest possible local model". The useful hypothesis is:

> Can Colibri execute narrow, repetitive classification/routing decisions locally, with acceptable quality and latency, while reducing cloud-model cost and preserving existing provider interfaces?

Primary reuse targets:
- `murat-ai-orchestrator`
- `ai-microtask-factory`
- MPE governance/status classification
- later, only if proven: document/tender routing tasks

## New Idea Filter

Primary disposition: **EXPERIMENT**

- Existing project fit: strong; belongs in MPE experiments.
- Extend existing: yes; candidate provider behind current orchestration, not a parallel orchestration stack.
- Reuse: OpenAI/Anthropic-compatible API surface and Brio-style constrained decisions are the main candidates.
- Duplication risk: high if Colibri becomes its own control plane; therefore prohibited.
- Measurable value: cloud-cost reduction, deterministic constrained output, local availability.
- MVP: three bounded tests only.
- Priority: exploratory; do not displace currently blocked production work.
- Deep-change: none authorized. Any provider/source-of-truth change requires a separate decision.

## Experiment scope

### CP-01 — Brio status classifier

Test a fixed fixture set where the expected output is exactly one of:

- READY
- WARNING
- BLOCKED

Compare Colibri output against the current reference decision process.

Capture:
- model and exact revision
- hardware
- latency
- RAM/VRAM/storage footprint
- accuracy / disagreement count
- malformed-output count
- reproducibility notes

### CP-02 — Agent routing decision

Given a small frozen set of MPE tasks, constrain Colibri to choose one destination from an explicit list of existing agents/services.

No new agents may be invented by the experiment.

Measure:
- routing accuracy
- ambiguity handling
- latency
- determinism/repeatability
- token/cloud-cost avoided versus reference path

### CP-03 — Existing-provider compatibility

From an isolated test harness, call Colibri through its compatible HTTP interface as a candidate provider.

Goal: prove that one low-risk inference operation can be switched between the existing cloud provider and Colibri without redesigning the calling application.

Do not alter production routing.

## Success criteria

PASS only if all are true:

1. At least one bounded MPE operation reaches acceptable quality versus the reference path.
2. Output remains schema/constrained-choice safe for the tested task.
3. Local execution is operationally simpler or materially cheaper for that task.
4. Integration can be expressed as an adapter/provider extension, not a parallel platform.
5. No production source of truth or deployment topology changes are needed for the proof.

## Failure / stop criteria

STOP or FAIL if:
- setup cost exceeds the value of the narrow task;
- latency makes the workflow impractical;
- quality materially trails the reference path;
- hardware/storage requirements are unreasonable for intended deployment;
- compatibility requires invasive changes;
- Arena discovers a deep-change requirement;
- the experiment starts duplicating `murat-ai-orchestrator`.

## Guardrails

- No new repository.
- No production deployment.
- No production traffic.
- No secrets committed.
- No autonomous background service.
- No replacement of existing orchestrator/router.
- No model download larger than needed for the smallest useful proof without documenting the reason first.
- Prefer a small supported MoE model for the first run.
- Pin model/version and record exact hashes/revisions where practical.
- Keep all evidence under this experiment directory.

## Expected evidence

Arena should add, as evidence is produced:

- `FINDINGS.md`
- `evidence/environment.md`
- `evidence/cp01-results.json`
- `evidence/cp02-results.json`
- `evidence/cp03-results.json`

## Final decision

Arena must finish with exactly one recommendation:

- REUSE_COMPONENT — adopt Colibri as an optional inference provider/component;
- HOLD — promising, but blocked by hardware/performance/quality;
- REJECT — no measurable value for our workflows.

A PASS does **not** authorize production integration.
