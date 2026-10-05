# Task Packet: Pimenov.ai Architecture Extensions

**Date:** 2026-10-05  
**Decision:** EXTEND_EXISTING  
**Owner:** Murat Project Engineer  
**Status:** PROPOSED / READY FOR IMPLEMENTATION  
**Scope:** MPE only. No new repository.

## Goal

Transfer the highest-value architectural patterns identified in the current Pimenov.ai knowledge base into the existing Murat Project Engineer architecture without introducing a parallel orchestration system.

## Non-goals

- Do not create a new repository.
- Do not introduce a daemon, scheduler, generic workflow engine, persistent agent runtime, memory service, or MCP server as part of this packet.
- Do not replace the existing Experts / Teams / Playbooks / Review Gates model.
- Do not add vector DB or knowledge graph infrastructure.
- Do not move MPE source-of-truth into Notion.
- Do not introduce Digital Employee / Dots abstractions yet.
- Do not auto-merge implementation changes.

## Changes to design

### 1. Agent Runtime Decision Matrix

Add a small decision document describing when MPE should route execution to:
- ChatGPT
- Codex / codex exec
- Agents API
- Codex app-server / equivalent long-running runtime

The matrix must evaluate: process owner, tool execution location, state ownership, continuation after failure, isolation, approvals, observability, deterministic verification, and stop/recovery behavior.

This is a routing aid, not a new runtime abstraction.

### 2. New Idea Filter as executable Skill

Extend the existing MPE New Idea Filter with an explicit anti-roadmap layer.

Required checks:
- existing active project
- extension possibility
- reusable component
- duplicate capability/infrastructure
- measurable business value
- smallest useful experiment/MVP
- priority versus current portfolio
- deep-change impact
- explicit "do not build" constraints

Required terminal decisions:
EXTEND_EXISTING, REUSE_COMPONENT, MERGE, EXPERIMENT, HOLD, NEW_REPOSITORY, REJECT.

The filter must fail closed when a deep-change or fundamental architectural conflict is detected.

### 3. Research → Execute → Review Playbook

Add or extend a Playbook for substantial implementation:
1. Research source-of-truth and constraints.
2. Produce a bounded implementation plan / Task Packet.
3. Execute the smallest sufficient change.
4. Run deterministic checks.
5. Perform independent semantic review.
6. Emit one terminal state and Run Report.

The reviewer must not rely solely on executor claims.

### 4. Evidence-first Review Gate

Extend Review Gates with an explicit rule:

**Agent claims are not evidence.**

Examples:
- "tests passed" requires captured command result / exit status.
- "file updated" requires diff or read-back evidence.
- "deployment succeeded" requires deployment evidence plus health/read-back check.
- "requirement completed" requires traceable acceptance evidence.

Missing evidence must remain UNKNOWN/UNVERIFIED, not be converted to success.

### 5. Lightweight knowledge model

Document a minimal Git-native model for:
- Ideas
- Decisions
- Experiments
- Knowledge
- Skills

Do not implement a database. Reuse existing repository artifacts and source-of-truth conventions.

This is preparation for a later experiment, not a memory-service implementation.

## Acceptance criteria

- Existing MPE architecture remains intact.
- No new repository or parallel orchestration layer is introduced.
- Runtime choice is explicit and documented for substantial agent tasks.
- New Idea Filter can produce all seven terminal decisions.
- Anti-roadmap constraints are represented without embedding private personal data into public project files.
- Substantial execution has Research → Execute → Deterministic Check → Independent Review.
- Review gates distinguish evidence from agent assertions.
- Existing validation commands still pass.
- Changes are delivered as a focused PR with no unrelated refactor.

## Implementation order

**Phase A — documentation/contracts only**
1. Runtime Decision Matrix.
2. New Idea Filter / anti-roadmap contract.
3. Research → Execute → Review Playbook.
4. Evidence-first Review Gate.
5. Lightweight knowledge model.

**Phase B — minimal executable support**
Only if Phase A exposes a concrete gap:
- encode the Filter as a Skill;
- add deterministic validation for terminal decision schema;
- add evidence fields to the existing Run Report.

No Phase B work should start automatically if it requires a deep architectural change.

## Verification

Run:
- `python scripts/validate_package.py .`
- `python -m unittest discover -s tests -v`

Then inspect the diff for:
- unrelated files,
- duplicated orchestration,
- new runtime/database dependencies,
- weakened fail-closed behavior,
- oversized changes.

## Rollback

Remove/revert only the files and code introduced by this packet. Existing projects, Router configuration, credentials, and external runtimes remain untouched.

## Source

The packet is based on the October 2026 review of Pimenov.ai materials concerning agent runtime selection, anti-roadmaps/skills, role separation, evidence-based agent verification, memory architecture, ChatGPT plugins/MCP, and Cloudflare implementation patterns.

Pimenov-derived ideas are inputs to MPE design, not authoritative architecture. MPE's existing boundaries and Murat Project Engineer rules remain authoritative.
