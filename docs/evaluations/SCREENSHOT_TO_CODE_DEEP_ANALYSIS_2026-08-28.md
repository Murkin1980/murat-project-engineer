# Deep Analysis — abi/screenshot-to-code

Date: 2026-08-28
Source reviewed: `abi/screenshot-to-code`
Pinned source tree: `d026163f586dfa8c5c10d28c36edd59a9d3b0e88`
MPE primary disposition: `EXPERIMENT`

## Executive conclusion

`screenshot-to-code` is no longer best understood as a simple screenshot-to-prompt generator. The current architecture is a bounded front-end coding agent with provider abstraction, tool calling, mutable single-file state, image/asset tools, Playwright rendering, streaming UI updates, cost ceilings, run recording, and iterative self-correction.

The strongest reusable idea for Murat AI projects is not the hosted product, full UI, or FastAPI service. It is the pattern:

`visual reference -> generation agent -> tool calls -> file state -> browser render -> multimodal visual inspection -> targeted edit -> final artifact`

Recommendation: do not fork or embed the full repository now. Run a controlled experiment that compares this pattern against the current Codex visual implementation workflow on an existing real project. If the experiment passes, reuse only the minimum components/patterns needed.

## 1. New Idea Filter

### Existing-project overlap

This capability overlaps existing work rather than defining a new product boundary:

- Interactive KP / Qulpinay Style: rapid reconstruction of proposal and landing UI references.
- furniture-site work: reproduction/adaptation of visual references.
- Business Discovery Progressive Workspace: reference-driven dashboard prototyping.
- furniture configurator / MebelFlow UI: rapid UI prototype reconstruction.
- Codex visual workflow: generation, inspection, correction, and production hardening.

### Duplication risk

A new standalone Murat screenshot-to-code service would duplicate:

- AI provider orchestration;
- code-generation workflow;
- visual preview tooling;
- image handling;
- frontend editor UI;
- deployment/runtime concerns already handled elsewhere.

### Business value to validate

The measurable value is development acceleration, not a new user-facing product.

Primary target: reduce manual UI reconstruction/rework time by at least 30% while preserving or improving visual fidelity and production readiness.

### Deep-change check

No deep-change is needed for a bounded offline/branch experiment.

Deep-change would be triggered only if the pattern were promoted into a new persistent orchestration service, shared autonomous runtime, workflow engine, or authority layer. That is explicitly out of scope.

## 2. Repository structure

The repository is a two-part application:

- `frontend/`: React 18 + TypeScript + Vite, CodeMirror, Zustand, Radix primitives, preview/editor UX.
- `backend/`: Python/FastAPI, WebSockets, model provider SDKs, agent runtime, prompt construction, image processing, evaluation support, and Playwright browser rendering.

Important backend areas:

- `backend/agent/engine.py` — main iterative agent loop.
- `backend/agent/providers/` — provider adapters for OpenAI, Anthropic, Gemini.
- `backend/agent/tools/` — canonical tool definitions and runtime execution.
- `backend/prompts/` — system and task-specific prompt construction.
- `backend/routes/generate_code.py` — generation entry surface.
- `backend/ws/` — streaming transport/status messaging.
- `backend/fs_logging/` — filesystem run/evidence logging.
- `backend/evals/` — evaluation runner/data support.
- `backend/preview_screenshot*` / screenshot tool path — Playwright-backed visual verification.

This separation is useful: the agent/tool layer can conceptually be evaluated independently from the product UI.

## 3. Core agent architecture

`AgentEngine` is the central coordinator.

Observed behavior:

1. Seed an in-memory `AgentFileState` from current input/history.
2. Extract still-image inputs and make them available to the tool runtime.
3. Create a provider-specific session through a provider factory.
4. Enter an iterative tool-use loop with a hard maximum of 30 steps.
5. Stream assistant/thinking/tool deltas to the frontend.
6. Execute tool calls against a controlled runtime.
7. Append tool results back into the provider session.
8. Continue until the model returns no further tool calls.
9. Return the file-state HTML as the final product.
10. Fail if the run ends without usable output.

The engine also enforces a generation cost ceiling where provider usage is priceable.

### Important design property

The model does not directly own the final artifact as chat text. It is strongly encouraged to operate through file tools. This reduces accidental full-regeneration during small revisions and creates an inspectable mutation path.

## 4. Tool model

The canonical tools are more important than the model list.

### `create_file`

Creates the main HTML file once for a new artifact.

### `edit_file`

Uses exact-string replacement, supports batches, generates a unified diff, and reports the first changed line.

This is a strong reusable pattern for controlled UI refinement because it discourages whole-file rewrites after every correction.

### `extract_assets`

Uses visual descriptions to extract tightly cropped assets from input screenshots. The tool is exposed only when actual still-image inputs exist.

This is materially better than embedding the reference screenshot as a background or generating fake replacements for logos/product imagery.

### `generate_images`

Generates missing imagery through an external image model path.

### `edit_images`

Supports independent image editing/upscaling tasks in batches.

### `remove_backgrounds`

Separates foreground assets when transparency is needed.

### `screenshot_preview`

Renders the current file through a headless browser and returns full-page desktop and mobile screenshots as multimodal tool results.

### `retrieve_option`

Allows one generated variant to reference another variant's full HTML.

## 5. Visual self-correction loop

This is the most relevant architectural feature for Murat projects.

The system prompt instructs the agent to call `screenshot_preview` after create/edit operations when available. The preview tool renders both desktop and mobile versions and sends them back to the model as image parts.

The agent can then inspect problems such as:

- spacing;
- wrong colors;
- overlaps;
- layout mismatch;
- mobile breakage;
- asset sizing.

It can then call `edit_file` and repeat.

### Critical limitation

This is visual self-review, not a deterministic visual-diff scorer.

The preview tool itself does not compute SSIM, pixel difference, perceptual distance, DOM-layout distance, or a numeric match score against the source screenshot. The model visually judges its own result.

For our experiment, objective or at least independently rated fidelity metrics must therefore be added externally.

## 6. Prompt architecture

The system prompt establishes several strong constraints:

- chat responses stay concise;
- code changes go through tools rather than raw code chat output;
- new artifacts use one full-file creation;
- updates use targeted exact edits;
- screenshot verification is expected after meaningful changes;
- source assets should be extracted where possible;
- image generation must not be abused to recreate the whole screenshot;
- selected live-DOM elements can be used as locators for targeted edits.

This shows that much of the product quality comes from workflow discipline, not merely stronger vision models.

## 7. Provider abstraction

The agent supports multiple provider sessions behind a factory/adapter boundary.

Current repository documentation and dependencies indicate OpenAI, Anthropic, and Gemini code-generation paths, with Replicate used for several image operations.

For Murat projects, provider abstraction itself is not the main adoption target because the existing AI stack already has routing/provider concerns. Re-implementing this layer would create duplication.

Reusable lesson: keep tool semantics canonical and provider-specific formatting isolated behind adapters.

## 8. File-state model

The runtime centers on one main HTML file.

Benefits:

- simple state surface;
- easy rendering;
- easy diff generation;
- low coordination complexity;
- model can reason about a bounded artifact.

Limitations for our production projects:

- does not map directly to multi-file Next/React/component architectures;
- standalone CDN React/Tailwind patterns are prototype-oriented;
- production code still requires migration into the target repository structure;
- a visually successful result may still have poor semantic component boundaries.

Therefore, generated HTML should be treated as a prototype/reference implementation, not necessarily production architecture.

## 9. Frontend/product architecture

The frontend is a substantial product in its own right:

- React/Vite application;
- CodeMirror editor;
- state management via Zustand;
- UI primitives via Radix;
- preview and generation flows;
- variant handling;
- screenshot/video input UX;
- WebSocket-driven generation updates.

This is precisely why a full fork is not recommended. Most of this UI duplicates surfaces we do not need.

## 10. Backend/runtime dependencies

Important dependencies include:

- FastAPI / Uvicorn;
- WebSockets;
- OpenAI SDK;
- Anthropic SDK;
- Google GenAI SDK;
- Playwright;
- Pillow / HEIF support;
- MoviePy for video workflows;
- HTTP clients;
- Langfuse.

The full product has a much larger operational footprint than the reusable pattern we need.

## 11. Screen-recording mode

The product supports screen recordings as an input path and can use them to infer a functional prototype rather than only a static layout.

Potential future relevance:

- reproducing interactions from reference furniture sites;
- reconstructing configurator behavior;
- deriving prototype interaction flows from product demos.

This should not be part of the first experiment. Static screenshot reconstruction is a smaller and more measurable test.

## 12. Evaluation architecture

The repository documents an evaluation dataset of 16 screenshots and a rating UI with 1–4 human scoring. Repeated runs can be averaged for model/prompt comparisons.

This is useful but insufficient as our primary acceptance method because:

- the documented metric is subjective;
- the dataset is generic rather than furniture/KP specific;
- the historical evaluation procedure does not measure migration effort into our production repository;
- it does not measure total operator corrections.

Our experiment must therefore add product-relevant metrics.

## 13. Strong reusable patterns

### A. Agent file-state + tool loop

Strong candidate for reuse as a conceptual pattern.

### B. Mandatory browser-render feedback

Very strong candidate. It converts code generation from one-shot output into implementation + inspection.

### C. Desktop + mobile verification in the same loop

High value and cheap to understand.

### D. Asset extraction before hallucinated replacement

High value for proposals, furniture landing pages, logos, textures, material swatches, and UI references.

### E. Targeted edit instead of whole-artifact regeneration

High value for preserving successful sections and reducing regressions.

### F. Provider-neutral canonical tools

Architecturally sound, but likely already overlaps our routing strategy. Reuse the pattern, not their provider layer.

### G. Per-run cost ceiling and run recording

Useful pattern for controlled experiments and AI-cost discipline.

## 14. Patterns not recommended for direct adoption

Do not directly adopt as defaults:

- whole React/Vite editor product;
- separate FastAPI service solely for screenshot-to-code;
- a new shared runtime daemon;
- their provider-routing layer;
- single-file CDN React as production architecture;
- dependence on Gemini/Replicate across all Murat projects;
- subjective self-review as the only quality gate.

## 15. Fit by active project

### Interactive KP / Qulpinay Style — strongest first target

Why:

- bounded visual artifacts;
- existing real output to compare;
- strong importance of visual fidelity;
- relatively simple business logic;
- easy rollback;
- direct economic value if iteration gets faster.

Recommended first experiment target.

### Furniture landing/site workflow — strong second target

Especially useful when a visual/video reference is supplied.

### Business Discovery Progressive Workspace — later

Useful for prototyping, but current Business Discovery architecture and Stage work are more valuable than introducing another experimental variable now.

### MebelFlow/configurator — later

Potentially high value, but interaction/state complexity makes it a worse first benchmark.

## 16. Proposed experiment architecture

Experiment ID: `EXP-S2C-01`

No new repository.

Run the same reference through two paths:

### Baseline A — current Codex visual workflow

Reference screenshot -> Codex implementation -> current visual checks -> final prototype.

### Candidate B — screenshot-to-code pattern

Reference screenshot -> bounded visual coding agent/pattern -> browser preview -> targeted corrections -> handoff to Codex for production adaptation.

The candidate does not need to deploy the full upstream application. A local/temporary execution of upstream or a minimal controlled extraction of its workflow is acceptable, whichever produces the cleanest evidence with least integration effort.

## 17. Metrics

Required metrics:

1. time to first visually usable prototype;
2. time to production-ready handoff;
3. number of manual correction instructions;
4. number of generation/edit cycles;
5. independent visual-fidelity rating;
6. desktop fidelity;
7. mobile fidelity;
8. asset accuracy;
9. production migration effort;
10. regressions introduced during corrections;
11. AI/API cost when observable;
12. total human intervention time.

Optional metric if tooling is easy to add:

- perceptual screenshot distance / image similarity score.

## 18. Pass criteria

`PASS` only if all are true:

- at least 30% reduction in human reconstruction/rework time OR a clearly equivalent time with materially higher fidelity;
- no regression in mobile usability;
- no unacceptable production-code migration burden;
- generated assets/content do not rely on screenshot-as-layout cheating;
- workflow remains bounded and does not introduce new persistent runtime infrastructure;
- evidence is reproducible from the recorded fixture/reference.

`REWORK` if there is visible value but the workflow needs one bounded correction, for example better asset handling or objective visual scoring.

`FAIL/HOLD` if it mainly shifts work from initial coding to cleanup/migration or requires a new runtime service to be useful.

## 19. Minimum experiment fixture

Use one real visual reference already relevant to Murat's furniture work.

Preferred fixture order:

1. one-screen Interactive KP / Qulpinay-style layout;
2. furniture landing hero/configurator screen;
3. only after a PASS, a multi-screen or video interaction fixture.

Do not begin with Business Discovery or a complex multi-state configurator.

## 20. Security and operational notes

- Treat reference screenshots as input artifacts; do not persist customer-sensitive screenshots in public fixtures.
- Do not commit API keys.
- Do not let generated code fetch unknown scripts/assets without review.
- Review external CDN and image URLs before production reuse.
- Preserve license notices if source code is actually copied; upstream repository is MIT licensed.
- Separate conceptual pattern reuse from literal source-code reuse in the experiment evidence.

## 21. Final recommendation

Primary disposition remains `EXPERIMENT`.

The upstream repository is valuable because it demonstrates a practical visual coding loop, not because Murat needs another standalone generator product.

The highest-value path is:

`reference -> bounded visual agent -> asset extraction -> create -> render desktop/mobile -> inspect -> targeted edit -> repeat -> Codex production adaptation`

Run `EXP-S2C-01` first against Interactive KP / Qulpinay-style work. If the experiment passes, the likely final disposition changes from `EXPERIMENT` to `REUSE_COMPONENT`, specifically for the browser-feedback loop, controlled edit semantics, asset-first reconstruction, and run evidence patterns.

## Evidence reviewed

Upstream repository and files at source tree `d026163f586dfa8c5c10d28c36edd59a9d3b0e88`:

- `README.md`
- `backend/agent/engine.py`
- `backend/agent/tools/definitions.py`
- `backend/agent/tools/runtime.py`
- `backend/agent/tools/screenshot_preview.py`
- `backend/prompts/system_prompt.py`
- `backend/pyproject.toml`
- `frontend/package.json`
- `Evaluation.md`
- repository tree including `backend/routes`, `backend/ws`, `backend/evals`, `backend/fs_logging`, `design-docs`, and frontend generation surfaces.
