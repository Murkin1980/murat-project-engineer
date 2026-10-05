# Agent Runtime Decision Matrix

**Status:** ACTIVE / ROUTING AID  
**Date:** 2026-10-05  
**Scope:** Murat Project Engineer (MPE) execution routing.

## Purpose

This document provides a deterministic routing aid to evaluate when Murat Project Engineer (MPE) should route execution tasks to different execution runtimes. It is a routing policy and decision aid, not a new runtime abstraction or orchestration framework.

MPE does not implement an agent daemon, scheduler, persistent runtime, or workflow engine. Instead, MPE coordinates tasks across approved host runtimes based on task risk tier, isolation requirements, deterministic verification needs, and approval boundaries.

---

## Evaluation Dimensions

The decision matrix evaluates four candidate runtimes across nine structural dimensions:

1. **Process Owner:** Who or what initiates, controls, and supervises the execution process.
2. **Tool Execution Location:** Where shell, file, network, and tool commands actually execute.
3. **State Ownership:** Where conversation, context, intermediate artifacts, and durable state live.
4. **Continuation After Failure:** How recovery or rework occurs when a step, tool call, or gate fails.
5. **Isolation:** The security and workspace isolation boundary separating tasks, users, and environments.
6. **Approvals:** How human gates, sensitive tool approvals, and scope changes are intercepted and authorized.
7. **Observability:** How execution logs, model calls, token spend, and tool invocations are inspected.
8. **Deterministic Verification:** How independently and reliably test runners, linters, diffs, and verification commands can run.
9. **Stop/Recovery Behavior:** How abnormal terminations, timeouts, budget exhaustion, or explicit aborts are handled.

---

## Decision Matrix

| Dimension | ChatGPT | Codex / `codex exec` | Agents API | Codex app-server / Long-Running |
|---|---|---|---|---|
| **Process Owner** | Hosted OpenAI service / End-user UI session | Local developer / CI runner / Host terminal process | External API caller / Headless service orchestrator | Persistent host daemon / IDE background process |
| **Tool Execution Location** | Hosted sandbox / Browser plugin / MCP client bridge | Local host workspace / Dedicated Git worktree | Cloud container / Client-side webhook or function runner | Local host daemon with IPC/socket bridge to workspace |
| **State Ownership** | Ephemeral chat session & OpenAI account history | Git repository files, local contracts, ephemeral run logs | Server-side thread/run objects referenced by ID | Daemon memory, language-server index/AST, socket state |
| **Continuation After Failure** | Manual user prompting / Regenerate response in chat | Governed single rework cycle via Playbook; fail closed | Programmatic retry or poll status (`requires_action` / `failed`) | Daemon restart / Session reconnection / Watchdog reload |
| **Isolation** | High (cloud sandbox); no local filesystem access by default | Workspace/worktree boundary; local filesystem permissions | Container/thread-level API isolation; tenant scoped | Process boundary; risk of cross-task state leakage if dirty |
| **Approvals** | Interactive human-in-the-loop on each turn | Deterministic Review Gates; explicit human gate on DEEP-CHANGE | Programmatic webhook resolution or client polling gate | Protocol-level client permission prompts before tool action |
| **Observability** | Chat transcript (interactive, unstructured prose) | Local stdout/stderr, git diff, JSONL event trace, Run Report | Structured API step events, token usage in API response | Daemon log files, JSON-RPC traces, status socket events |
| **Deterministic Verification** | Low / Manual (user must verify claims externally) | High (direct terminal execution of linters, tests, hashes) | Medium (depends on caller-provided tool verification harness) | High (direct access to language-server diagnostics & test runner) |
| **Stop/Recovery Behavior** | Stop generation button; conversation abandonment | Process termination; clean git rollback (`git reset / checkout`) | Cancel run API call (`cancel_run`); run timeout limits | SIGTERM/SIGKILL of process group; worktree teardown |

---

## Runtime Routing Policies

### 1. ChatGPT
- **When to Route:**
  - Conversational brainstorming, early concept ideation, and architecture drafting.
  - Interactive exploratory analysis and non-code documentation brainstorming.
  - Ad-hoc prompt refinement, persona roleplay, or external inquiry where repository isolation is preferred.
- **When NOT to Route:**
  - Any task that requires automated, deterministic gate verification.
  - Software feature implementation, bug fixes, or repository file modifications.
  - Tasks requiring audit-grade run reports, signed handoffs, or reproducible execution records.

### 2. Codex / `codex exec` (Default MPE Execution Runtime)
- **When to Route:**
  - Standard MPE software features, bug fixes, and bounded refactoring (`FAST` and `VERIFIED` tiers).
  - Tasks requiring strict Git worktree isolation, local test execution, and deterministic Review Gates.
  - Tasks governed by Playbooks (`playbooks/software-feature.md`, `playbooks/verified.md`, `playbooks/fast.md`).
  - Package validation, schema verification, and local CLI tool operations.
- **When NOT to Route:**
  - Long-running continuous monitoring or background service tasks.
  - Tasks where headless external cloud orchestration without host terminal access is required.

### 3. Agents API
- **When to Route:**
  - Headless batch evaluations, automated backtests, and synthetic stakeholder runs (e.g., EXP-12, EXP-13).
  - External CI/CD webhooks and automated event-driven triage pipelines.
  - Parallel evaluation sweeps across multiple prompt variants or model families where local CLI spawning is inefficient.
- **When NOT to Route:**
  - Direct interactive development in a developer's local active worktree.
  - Tasks requiring interactive human debugging in the host terminal.

### 4. Codex App-Server / Long-Running Runtime
- **When to Route:**
  - Continuous IDE-integrated development assistance with active language-server (LSP) diagnostics.
  - Persistent devcontainer or preview server sessions requiring live reloading and fast incremental feedback.
  - Bounded multi-turn agent sessions where repeated process startup overhead is demonstrably prohibitive.
- **When NOT to Route:**
  - Unattended production execution without human presence or bounding watchdog.
  - Scenarios where shared daemon state or caching risks worktree contamination.
  - Tasks that can be executed cleanly and deterministically with one-shot `codex exec`.

---

## Architectural Invariants

1. **Routing Aid Only:** This matrix guides runtime selection. It does not create or instantiate a persistent agent runtime or workflow engine within MPE.
2. **Fail-Closed on Unknowns:** If a task's runtime requirements cannot be satisfied safely within approved boundaries, route to `codex exec` with `VERIFIED` tier or stop at `HUMAN_REQUIRED`.
3. **Agent Claims Are Not Evidence:** Regardless of the runtime chosen, self-reported success from an agent runtime is not treated as evidence. Verifiable tool/system output is mandatory for gate clearance.
4. **Git Remains Canonical:** No external runtime (ChatGPT cloud, Agents API thread, app-server cache) owns the authoritative state. Authoritative state lives strictly in Git repository artifacts.
