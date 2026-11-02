# WaveSpeed Evaluation — Arena checkpoint plan and first instruction

Status: REGISTERED / CP-01 AUTHORIZED FOR EXECUTION
Decision: **EXPERIMENT**
Owner: Murat Project Engineer
Repository: `Murkin1980/murat-project-engineer`
Branch: `experiment/wavespeed-tool-evaluation`
Canonical registration: `experiments/EXPERIMENT_REGISTRY.json`
Series: `experiments/wavespeed-evaluation/README.md`

## Goal
Determine which of ten registered WaveSpeed trials are executable in the current Arena runtime and which require a desktop, owner review, software, browser or physical equipment. Proceed in bounded checkpoints, retaining existing project components and measured value. **CP-01 only is authorized now**; later checkpoints are specifications, not permission to execute.

## Checkpoint chain

### CP-01 — Arena environment & vendor capability preflight (START HERE)
Read-only verification of repo, runtime and public WaveSpeed capabilities. Produce truthful capability matrix and go/no-go for W01–W10. Do not execute individual experiment workloads. Outputs: `RESULTS/CP-01.md` and optional sanitized machine-readable matrix `RESULTS/CP-01.json`.

### CP-02 — W01 LUT and W04 print-upscale pilot
After owner approval, execute frozen, privacy-safe reference fixtures against established baselines, measure color consistency/print suitability/cost. Preserve reference crops and hashes. No commercial footage upload without clearance.

### CP-03 — W02 video restoration and W03 CNC geometry pilot
After owner approval and CP-01 tool gates, compare bounded video enhancement with baseline; validate DXF geometrically only. Require explicit owner-approved PNG and physical machine verification before manufacturing-ready DXF claim.

### CP-04 — W05 3D bridge and W06 segmentation
After approval, test 3D model dimensions/format support and character isolation. Separate format compatibility from ability to import proprietary PRO100 .meb.

### CP-05 — W07 postproduction and W08 Kazakh transcription
After approval, test a 30–60s video workflow and a consented Kazakh-language speech sample, with real export and objective WER/time alignment measurements. Do not claim Kazakh language support from marketing.

### CP-06 — W09 document quality and W10 cross-device performance
After approval, use only synthetic/anonymized documents and controlled cross-device fixtures. No customer or financial data uploads; label devices not available as BLOCKED, not simulated PASS.

### CP-07 — Comparative evaluation and adoption recommendation
After approval, reconcile all checkpoints, measured baseline vs candidate value, provider/privacy/cost constraints, per-item PASS/PARTIAL/BLOCKED, disposition ADOPT/ADOPT_WITH_CHANGES/DO_NOT_ADOPT; propose bounded reuse in owning projects only. Do not integrate or deploy.

## CP-01 — Authorized Arena instruction

### Mandatory first reads
1. `AGENTS.md`, then `docs/governance/SCOPE-CHANGE-CONTROL.md`.
2. `docs/NEW_IDEA_FILTER_POLICY.md`, `docs/OPINIONATED_WORKSPACE_POLICY.md`, `docs/VALUE_UNIT_ECONOMICS.md`.
3. `experiments/EXPERIMENT_REGISTRY.json` WaveSpeed entries; this `ARENA_TASK.md`; series `README.md`.
4. Existing `experiments/exp-29-arena-bootstrap-harness/README.md`, `harness/bootstrap_builder.py`, and EXP-24 browser/FFmpeg findings if locatable. Read only relevant excerpts.

### Startup bootstrap
Use the existing EXP-29 deterministic helper — do not construct a second bootstrap mechanism. From a fresh synchronized checkout, attempt:
```bash
python3 experiments/exp-29-arena-bootstrap-harness/harness/bootstrap_builder.py build --experiment EXP-WS-01 --checkpoint CP-01 --out-json /tmp/wavespeed_ARENA_CONTEXT.json --out-md /tmp/wavespeed_ARENA_CONTEXT.md
python3 experiments/exp-29-arena-bootstrap-harness/harness/bootstrap_builder.py verify --packet /tmp/wavespeed_ARENA_CONTEXT.json
```
Use the packet only if `FRESH`; any STALE/REJECTED/error must be logged. Continue directly from canonical documents if helper cannot model a multi-experiment series; **do not alter EXP-29 or governance to force FRESH**. This is a non-authoritative derived packet and is not a prerequisite for the read-only audit.

### CP-01 ordered actions
1. Confirm actual checkout remote, branch, HEAD, clean/dirty state, PR #102 and read-only canonical registration. Preserve unrelated changes. If lacking access to intended repo/branch, report BLOCKED, no alternate repository.
2. Inventory executable tools and versions using harmless commands only: OS/architecture, CPU/RAM/disk (non-sensitive summary), Python, git, node, browser binaries and headless status, browser network/TLS, ffmpeg/ffprobe, image tools (ImageMagick/Pillow/OpenCV if installed), vector/DXF tools, video codecs and relevant GPU visibility. No installs or environment mutation.
3. Check `https://wavespeed.ai/free-tools/` and each W01–W10 candidate URL from README. For each, record actual HTTP/access result, visible feature/format limits, whether it runs locally in browser vs requires upload/login/credits, and whether live interaction is technically possible. Distinguish DOCUMENTED, OBSERVED, UNVERIFIED and BLOCKED. A reachable webpage is not proof a generator works. If public UI cannot be inspected, say so.
4. Create one row per W01–W10 with: required feature; URL; Arena dependencies; browser/headless possible?; privacy concerns; paid/credit risk; existing baseline candidate; status READY_TO_TEST / CONDITIONAL / BLOCKED / UNVERIFIED; what evidence is still needed; next checkpoint.
5. Identify minimum safe fixtures for first wave W01–W04 and the best available internal alternatives without touching customer data or running WaveSpeed transformations.
6. Write `RESULTS/CP-01.md` with summary, tools, links/date, complete matrix, explicit unknowns and next recommended *single* checkpoint. Save optional JSON only if it aids reproducibility. Do not change individual experiment statuses to PASS in the registry.

### CP-01 acceptance
PASS if (a) repository and governance confirmed; (b) all 10 rows completed with explicit observed/unknown distinction; (c) tool versions and major browser/TLS/video/3D risks reported; (d) free/paid/privacy claims not guessed; (e) W01–W04 next-test feasibility classified; (f) one reproducible evidence report committed on the same branch, no secrets/customer data, no experimental workloads, no production changes.
PARTIAL if some third-party UI or tooling is inaccessible but all attempted checks and blockers are documented.
BLOCKED if branch/repo is inaccessible or safe inspection cannot start. Do not convert uncertainty to PASS.

### Evidence/handoff format
STATE; EVIDENCE; CHANGES; RESULT; BLOCKER; NEXT ACTION; HANDOFF.
Report commands, exit codes, platform details (redacted), source links, observed timestamps, git diff scope, current commit SHA, and current PR link. Use `git diff --check` and available relevant repo validation only when feasible; don't repair unrelated failures. Update PR #102 by commits on its existing branch; **do not open competing PR, merge, deploy or modify production**.

## Scope stop rules
- Stop if any step requires cloud credits/payment, installing software, secrets, account sign-in, provider billing or new permissions.
- Stop if the action uploads identifiable people, confidential client records, financial documents or proprietary media without explicit authorization.
- Stop if changes are needed to MPE governance, EXP-29 internals, registry schema, central Router/runtime/Cloudflare/DNS, or to an owning production repository.
- Stop at CP-01 completion. Do not initiate CP-02 or any WaveSpeed workload without a fresh owner instruction.
- Physical cutting, CAD production acceptance and print approval are owner-controlled and never satisfied by simulation.

## Next authorized action
Run only CP-01 environment/vendor preflight; commit its evidence to current Draft PR #102 and return a concise handoff.
