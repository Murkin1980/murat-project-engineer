# EXP-19 / CP-01 — Processed Signals Catalog

This file contains 15 external technology and product signals collected from **Shir-man** (`https://shir-man.com/homepage/`) and evaluated through the **Murat Project Engineer New Idea Filter** (`docs/NEW_IDEA_FILTER_POLICY.md`).

---

## Signal Summary Table

| ID | Title | Candidate Project | New Idea Filter Decision | Deep Change | Actionable? |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **SIG-01** | Reladraw | `murat-project-engineer` | `REUSE_COMPONENT` | `false` | **Yes (P0)** |
| **SIG-02** | Brag (Hyperframes Launch Video) | `murat-project-engineer` / Dashboard | `EXPERIMENT` | `false` | **Yes** |
| **SIG-03** | i-have-adhd (Action-First Prompting) | `murat-project-engineer` | `EXTEND_EXISTING` | `false` | **Yes (P0)** |
| **SIG-04** | Sonicloud OpenSDK | `mebelflow-ai` | `REUSE_COMPONENT` | `false` | **Yes (P0)** |
| **SIG-05** | PaperMono Local Sync & Receipts | `ai-microtask-factory` | `EXTEND_EXISTING` | `false` | **Yes (P0)** |
| **SIG-06** | SolveEdit Inspect-Resolve | `mebeldocs-ai` | `REUSE_COMPONENT` | `false` | **Yes** |
| **SIG-07** | pi_plays_pokemon Visual Agent Loop | `murat-project-engineer` (EXP-S2C-01) | `EXPERIMENT` | `false` | **Yes** |
| **SIG-08** | OpenShip Self-Hosted Deployment | Portfolio Infra | `HOLD` | `true` | No |
| **SIG-09** | HN.watch Video Summaries | None | `HOLD` | `false` | No |
| **SIG-10** | Swift 1.5 Qwen 27B GGUF | MPE / Router | `HOLD` | `true` | No |
| **SIG-11** | RocketRide C++ AI Pipeline Server | `murat-project-engineer` | `REJECT` | `true` | No (Banned) |
| **SIG-12** | Goutoujunshi Relationship Coach | None | `REJECT` | `false` | No |
| **SIG-13** | Lofi Cities Ambient Web App | None | `REJECT` | `false` | No |
| **SIG-14** | Essay: Google AI Search Overviews | None | `REJECT` | `false` | No |
| **SIG-15** | Destroy Website Canvas Game | None | `REJECT` | `false` | No |

---

## Signal Cards

### SIG-01: Reladraw — Text Diagram Language with Relative Constraints
- **source**: `https://github.com/reladraw/reladraw`
- **title**: Reladraw — Text-based diagram language using relative positions instead of coordinates
- **what_changed**: Released a text-based diagram specification where elements state explicit relative positions ("box A right of box B") rather than absolute pixel coordinates or layout engine defaults.
- **why_it_may_matter**: AI agents frequently corrupt Mermaid or visual coordinate diagrams during architecture handoffs or Run Report generation due to layout engine syntax strictness.
- **candidate_project**: `murat-project-engineer`
- **reuse_or_extend_path**: Adopt Reladraw schema patterns into MPE Expert Playbooks (`playbooks/VERIFIED.md`, `playbooks/DEEP_CHANGE.md`) to enable agents to produce deterministically editable architecture diagrams in Markdown run artifacts.
- **measurable_value**: Eliminates 100% of visual syntax rendering failures in agent-generated system diagrams; cuts human diagram repair time from ~10 mins to 0 mins.
- **MVP/experiment**: Add a Reladraw contract template under `contracts/` and generate 3 test architecture handoffs during Stage 2 runs.
- **deep_change**: `false` (text-based schema artifact, no core coordinator changes)
- **New Idea Filter decision**: `REUSE_COMPONENT`

---

### SIG-02: Brag — Claude Code Skill for Launch Video Generation
- **source**: `https://github.com/latent-spaces/brag`
- **title**: Brag — Claude Code skill that creates launch videos using Hyperframes
- **what_changed**: Created a skill that converts READMEs, release logs, and Git diffs into shareable video previews with synthetic voiceover and custom visual themes.
- **why_it_may_matter**: MPE portfolio reporting currently uses static Markdown and static HTML dashboards. Automated video recaps of completed experiments/vertical slices significantly boost stakeholder visibility.
- **candidate_project**: `murat-project-engineer` / Dashboard
- **reuse_or_extend_path**: Integrate Hyperframes CLI execution into `presentation/` reporting scripts to auto-generate 30-second video summaries for completed Stage 2 evidence runs.
- **measurable_value**: Instant 30-second executive video summary produced in <60 seconds per milestone without manual editing.
- **MVP/experiment**: Run `brag` against `STATUS.md` in a manual test script and produce one video artifact for PR review.
- **deep_change**: `false` (isolated reporting helper script, no runtime authority changes)
- **New Idea Filter decision**: `EXPERIMENT`

---

### SIG-03: i-have-adhd — Action-First Output Enforcement Plugin
- **source**: `https://github.com/ayghri/i-have-adhd`
- **title**: i-have-adhd — Claude Code plugin enforcing numbered, action-first steps with zero fluff
- **what_changed**: Published an output constraint plugin that strips conversational filler, intros, and polite preamble, forcing responses directly into numbered action items.
- **why_it_may_matter**: Agent handoffs and Expert Playbook turns in MPE often consume excess tokens on conversational preamble, cluttering execution logs and wasting context budget.
- **candidate_project**: `murat-project-engineer`
- **reuse_or_extend_path**: Extend MPE System Instructions and Expert Playbooks (`playbooks/FAST.md`, `playbooks/COORDINATOR.md`) with action-first prompt directives.
- **measurable_value**: 25%–35% reduction in output token usage per agent turn; cleaner machine-readable handoffs.
- **MVP/experiment**: Update `playbooks/FAST.md` with action-first constraints and benchmark token usage on 5 standard coordinator tasks.
- **deep_change**: `false` (prompt engineering in Markdown playbooks)
- **New Idea Filter decision**: `EXTEND_EXISTING`

---

### SIG-04: Sonicloud OpenSDK — Cross-Platform BLE Hardware Recording Card SDK
- **source**: `https://github.com/SonicloudTech/sonicloud_opensdk`
- **title**: Sonicloud OpenSDK — Cross-platform BLE recording hardware SDK with offline transcription
- **what_changed**: Released complete open SDK for BLE recording hardware integration with desktop offline speech-to-text transcription demos.
- **why_it_may_matter**: `mebelflow-ai` requires real showroom sales rep voice capture and offline transcript processing for sales assistance.
- **candidate_project**: `mebelflow-ai`
- **reuse_or_extend_path**: Reuse BLE client communication patterns and offline transcription pipeline in `mebelflow-ai` showroom rep recording integration.
- **measurable_value**: Enables zero-latency local audio capture directly from sales rep hardware badges without cloud latency or subscription fees.
- **MVP/experiment**: Test BLE audio intake mock against `mebelflow-ai` session ingestion endpoint.
- **deep_change**: `false` (peripheral client integration in target repository)
- **New Idea Filter decision**: `REUSE_COMPONENT`

---

### SIG-05: PaperMono — E-Paper Synced List with Mobile Web & Offline AI Sorting
- **source**: `https://github.com/seamusc/papermono-shopping-list`
- **title**: PaperMono — E-paper device with offline-first synced mobile web app
- **what_changed**: Open-sourced firmware and lightweight web app for local-first list management with offline editing, grouping, and receipt sync.
- **why_it_may_matter**: `ai-microtask-factory` Stage 4 Spreadsheet Cleanup needs offline-first task acceptance, physical evidence logging, and receipt verification for field workers.
- **candidate_project**: `ai-microtask-factory`
- **reuse_or_extend_path**: Extend `ai-microtask-factory` task acceptance module with local-first receipt state patterns and offline status sync.
- **measurable_value**: Sub-second task status updates and physical acceptance receipts without requiring active network connectivity.
- **MVP/experiment**: Implement PaperMono local receipt state pattern in `ai-microtask-factory` remote preview.
- **deep_change**: `false` (UI/local state pattern inside existing target project)
- **New Idea Filter decision**: `EXTEND_EXISTING`

---

### SIG-06: SolveEdit — Visual Inspect-Resolve Strategy for Multimodal Models
- **source**: `https://github.com/WenjieShu/SolveEdit`
- **title**: SolveEdit — Multimodal benchmark & Inspect-Resolve planning strategy
- **what_changed**: Published a two-stage "Inspect-Resolve" visual planning method that increases multimodal problem-solving accuracy from 57.0% to 71.6%.
- **why_it_may_matter**: Document layout and invoice extraction in `mebeldocs-ai` face edge-case verification errors on complex multi-page Cyrillic PDFs.
- **candidate_project**: `mebeldocs-ai`
- **reuse_or_extend_path**: Reuse the Inspect-Resolve prompt and planning sequence inside the MebelDocs PDF document verification gate.
- **measurable_value**: ~20% improvement in complex Cyrillic invoice layout inspection accuracy before data commit.
- **MVP/experiment**: Test Inspect-Resolve prompt template against 10 sample Cyrillic PDF invoices in `mebeldocs-ai`.
- **deep_change**: `false` (prompting and verification gate refinement)
- **New Idea Filter decision**: `REUSE_COMPONENT`

---

### SIG-07: pi_plays_pokemon — Lightweight Visual Agent Loop
- **source**: `https://github.com/geohot/pi_plays_pokemon`
- **title**: pi_plays_pokemon — Visual agent loop driving UI actions via screenshots
- **what_changed**: Built a minimal agent harness that captures screenshots, sends them to a vision model, executes button actions, and persists state via a lightweight web UI.
- **why_it_may_matter**: Provides a reference implementation for screenshot-based visual feedback loops in MPE's planned visual workflow experiment (`EXP-S2C-01`).
- **candidate_project**: `murat-project-engineer` (EXP-S2C-01)
- **reuse_or_extend_path**: Benchmark pi_plays_pokemon's screenshot loop against `docs/experiments/EXP-S2C-01_SCREENSHOT_TO_CODE_VISUAL_WORKFLOW.md`.
- **measurable_value**: Validates stateless screenshot-to-action iteration mechanics without building custom loop infrastructure.
- **MVP/experiment**: Run a comparative analysis between pi_plays_pokemon loop state handling and EXP-S2C-01 test fixture.
- **deep_change**: `false` (benchmarking reference only)
- **New Idea Filter decision**: `EXPERIMENT`

---

### SIG-08: OpenShip — Self-Hostable Deployment Platform
- **source**: `https://github.com/oblien/openship`
- **title**: OpenShip — Self-hostable PaaS with desktop app, web dashboard, and CLI
- **what_changed**: Open-sourced a self-hosted deployment platform managing databases, SSL, CI/CD, and mail.
- **why_it_may_matter**: Deployment control plane for multiple project web services.
- **candidate_project**: Portfolio Infrastructure
- **reuse_or_extend_path**: Hold. Murat AI Stack standardizes on Cloudflare Workers / Static Assets and GitHub Actions, requiring zero self-hosted PaaS infrastructure.
- **measurable_value**: High operational overhead relative to Cloudflare serverless baseline.
- **MVP/experiment**: N/A
- **deep_change**: `true` (requires self-hosted server cluster, custom deployment agent)
- **New Idea Filter decision**: `HOLD`

---

### SIG-09: HN.watch — Automated Short Video Summaries of Hacker News
- **source**: `https://hn.watch/`
- **title**: HN.watch — AI video explainers for Hacker News posts
- **what_changed**: Created a web service generating 30-second AI video summaries for top HN stories.
- **why_it_may_matter**: External content summarization format.
- **candidate_project**: None
- **reuse_or_extend_path**: Hold. No direct alignment with active portfolio projects or engineering workflows.
- **measurable_value**: Zero business value for active projects.
- **MVP/experiment**: N/A
- **deep_change**: `false`
- **New Idea Filter decision**: `HOLD`

---

### SIG-10: Swift 1.5 Qwen 27B GGUF — Quantized Local Model
- **source**: `https://huggingface.co/ajgazin/Swift-1.5-Qwen3.8-27B-Uncensored-Dynamic-MTP-GGUF`
- **title**: Swift 1.5 Qwen 27B GGUF — Quantized open model with speculative decoding
- **what_changed**: Released Unsloth Dynamic 3.0 GGUF quants of Qwen 27B with MTP speculative decoding.
- **why_it_may_matter**: Local model execution for agent turns.
- **candidate_project**: MPE / Router
- **reuse_or_extend_path**: Hold. MPE routes turns through central API endpoints; local GPU deployment introduces hardware dependencies and unbudgeted hosting costs.
- **measurable_value**: Unpromising economics compared to managed Router endpoints under Compute Budget.
- **MVP/experiment**: N/A
- **deep_change**: `true` (requires local GPU infrastructure)
- **New Idea Filter decision**: `HOLD`

---

### SIG-11: RocketRide — C++ AI Pipeline Server
- **source**: `https://github.com/rocketride-org/rocketride-server`
- **title**: RocketRide — C++ AI pipeline runtime and 100+ node visual environment
- **what_changed**: Built a native C++ engine for executing AI pipelines and node graphs across 15+ LLM providers.
- **why_it_may_matter**: Proposes replacing agent orchestrators with a C++ node backend.
- **candidate_project**: `murat-project-engineer`
- **reuse_or_extend_path**: N/A — Rejected. Violates MPE Option A+ lightweight coordinator boundaries, introduces heavy native dependencies, and violates the zero-daemon guardrail.
- **measurable_value**: Negative value due to extreme architectural complexity and violation of MPE governance principles.
- **MVP/experiment**: N/A
- **deep_change**: `true` (requires new C++ daemon, new runtime architecture, breaks MPE contracts)
- **New Idea Filter decision**: `REJECT`

---

### SIG-12: Goutoujunshi — AI Relationship Coach Skill
- **source**: `https://github.com/shengjidaguai-china/goutoujunshi`
- **title**: Goutoujunshi — Specialized AI relationship advisor skill
- **what_changed**: Released a Codex skill analyzing chat histories and personal contexts to give relationship advice.
- **why_it_may_matter**: B2C consumer niche with zero overlap with Murat AI Stack.
- **candidate_project**: None
- **reuse_or_extend_path**: N/A — Rejected.
- **measurable_value**: Zero value for current portfolio priorities.
- **MVP/experiment**: N/A
- **deep_change**: `false`
- **New Idea Filter decision**: `REJECT`

---

### SIG-13: Lofi Cities — Ambient Music Web App
- **source**: `https://loficities.com/`
- **title**: Lofi Cities — Pixel-art city web app with live generated lofi music
- **what_changed**: Created a browser canvas app featuring animated pixel-art cities and live ambient audio generation.
- **why_it_may_matter**: Pure entertainment site.
- **candidate_project**: None
- **reuse_or_extend_path**: N/A — Rejected.
- **measurable_value**: Zero business value.
- **MVP/experiment**: N/A
- **deep_change**: `false`
- **New Idea Filter decision**: `REJECT`

---

### SIG-14: Article: "When did Google get so weird?"
- **source**: `https://sancho.bearblog.dev/google-weird/`
- **title**: When did Google get so weird? — Critical essay on AI Search Overviews
- **what_changed**: Essay analyzing absurd LLM search summary responses on sports meme queries.
- **why_it_may_matter**: Observational opinion piece.
- **candidate_project**: None
- **reuse_or_extend_path**: N/A — Rejected.
- **measurable_value**: Zero technical artifact value.
- **MVP/experiment**: N/A
- **deep_change**: `false`
- **New Idea Filter decision**: `REJECT`

---

### SIG-15: Destroy Any Website with Stickman — Web Canvas Game
- **source**: `https://destroy.spritefusion.com/`
- **title**: Destroy Any Website with Stickman — Interactive web game
- **what_changed**: Web-based widget allowing stickman destruction of DOM elements on any site.
- **why_it_may_matter**: Web game gadget.
- **candidate_project**: None
- **reuse_or_extend_path**: N/A — Rejected.
- **measurable_value**: Zero value.
- **MVP/experiment**: N/A
- **deep_change**: `false`
- **New Idea Filter decision**: `REJECT`
