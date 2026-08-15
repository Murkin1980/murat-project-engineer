# Munder Difflin controlled architecture pilot — RUN-10

Date: 2026-08-15  
Disposition: **EXPERIMENT**  
Pilot result: **FAIL**  
Overall adoption decision: **REUSE_PATTERN**

## Executive conclusion

Munder Difflin 0.4.3 was downloaded from the official GitHub release, hash-verified, launched on Windows with `DO_NOT_TRACK=1`, and pointed at a clean local clone of Murat Project Engineer. Before execution, autonomy, telemetry, semantic memory, schedules, auto-update, Freeflow, auto-compaction, and reflection were disabled.

The required three-role benchmark did not start. Munder repeatedly spawned its GOD/Codex process and immediately archived it after a natural exit with code 0. Running Codex directly in a PTY remained alive, so the failure is specific to the Munder/Codex launch path in this environment. No benchmark repository files were changed.

The pilot therefore fails its acceptance gate. Source inspection still identifies reusable patterns, but direct adoption or architecture replacement is unjustified.

## Reproducibility record

- Munder release: `v0.4.3` (2026-08-13).
- Source tag/commit: `v0.4.3`, `fc0cd3a8bacdbf9cad1eb3f780250f91f86d59f2`.
- Portable binary SHA-256: `E99E375C4905DACB23302A91E2F30ED5686D023D62F4028FB32F4554A3AE7D2B` (official and local values matched).
- MPE baseline: `408f94915f997bf9e9ec87e53987a15e5d09b6af`.
- Isolated benchmark clone: `C:\tmp\munder-pilot\benchmark-mpe`.
- Isolated hive: `C:\tmp\munder-pilot\hive`.
- Source inspection clone: `C:\Projects\munder-difflin-pilot-source`.
- Provider: Codex; model configured by Munder: `gpt-5-codex`.
- Privacy: local-first gate passed with telemetry disabled and `DO_NOT_TRACK=1`; no MPE production data or secrets were intentionally supplied.

## Mode A — benchmark

Required roles: Architect, Coder/Analyst, Reviewer. Actual functional roles started: **0/3**. Munder created only its GOD record; that process exited before receiving the benchmark task. Repeated launch attempts produced spawn/archive events only.

| Metric | Result |
|---|---:|
| Benchmark completion | FAIL |
| Acceptance criteria | FAIL |
| Rework cycles | 0 |
| Agent collisions | 0 |
| Human interventions | 3 |
| Interruption recovery | PARTIAL |
| Repository changes | 0 |

Interruption recovery is partial because configuration and hive state survived process restart, but no in-flight role task existed to resume and the GOD process continued to exit.

## Mode B — source and architecture analysis

The MIT-licensed Electron/TypeScript source implements a PTY manager, filesystem hive, atomic mailboxes, append-only events, optional per-agent worktrees, task board, schedules, memory, telemetry/cost collection, and a steer/constrain/stop breaker. These are materially broader runtime responsibilities than MPE, whose documented boundary is a bounded policy/coordinator layer inside Codex.

Focused source tests were attempted after `npm install`. Installation failed because `better-sqlite3@11.10.0` had no prebuilt binary for Node 24 and the local Visual Studio installation lacked the required C++ toolset/SDK. The focused suite consequently reported 0/20 passing because `typescript` was unavailable. This is an environment/build-compatibility result, not evidence that all 20 product tests are defective.

## Safety findings

1. Onboarding enabled telemetry, semantic memory, autonomous mode, and an hourly scheduled mission by default. These settings conflicted with this pilot and were disabled before benchmark execution.
2. For Codex, Munder's autonomous mode maps to `--dangerously-bypass-approvals-and-sandbox`; this was not enabled.
3. Munder generated eight local Codex hooks. Seven were trusted after source review; `PreToolUse` was left inactive, so approval interception and circuit-breaker enforcement cannot be considered verified.
4. The portable Windows binary is unsigned. Integrity was controlled through the official SHA-256 comparison.
5. The bootstrap copied a large Codex configuration/plugin tree into the per-agent home, increasing duplicated state and review surface.

## Acceptance gates

| Gate | Result | Evidence |
|---|---|---|
| Three functional roles | FAIL | 0/3 roles reached a working terminal |
| Observable handoffs | FAIL | No task execution or handoff occurred |
| Worktree isolation | NOT OBSERVABLE | Implemented in source; never exercised |
| Budget enforcement | NOT OBSERVABLE | Implemented/configurable; never exercised |
| Circuit breaker/approval | NOT OBSERVABLE | Benchmark never ran; PreToolUse inactive |
| Interruption recovery | PARTIAL | Hive/config persisted; task did not resume |
| Privacy/local-first | PASS | Isolated paths, telemetry off, DO_NOT_TRACK |
| No deep change | PASS | No MPE architecture or production state changed |

## Recommended next action

Do not integrate Munder as MPE's orchestrator. Preserve the current MPE boundary. Reuse only selected patterns after independent design review: typed atomic mailbox envelopes, a compact append-only event vocabulary, and explicit per-agent lifecycle/worktree metadata. File a minimal upstream reproduction for the Windows Codex immediate-exit behavior and repeat only a smoke pilot after a fix, with all autonomy, memory, schedules, and telemetry disabled by construction.

