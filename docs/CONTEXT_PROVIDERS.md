# Context Providers

Status: Stage 2A documentation only. This note does not define a runtime interface, dependency, memory service, or orchestration layer.

## Principles

- provider != memory
- provider != orchestrator
- providers are replaceable
- source provenance must remain observable
- private project context must not be sent to public services by default
- a provider supplies context; project source-of-truth decides authority

## 1. Project Context

Examples:
- Git project files
- `AGENTS_PLUGINS_MURAT_AI_STACK_MASTER.md`
- nearest `AGENTS.md`
- `FOUNDATION.md`
- `DESIGN.md`
- `STATUS.md`
- approved decision records

Use: binding or current project context. Prefer versioned sources and record provenance in handoffs/reports.

## 2. Repository Context

Primary provider: GitHub or local Git metadata/content.

Use: repository state, commits, branches, pull requests, issues, changed files, and review evidence when available.

Repository context does not become independent memory. Persist decisions only through the project's reviewed source-of-truth process.

## 3. Documentation Context

Examples:
- local documentation
- installed skills/plugin instructions
- versioned knowledge files

Use: procedures, contracts, domain references, and implementation guidance. Read only the smallest relevant subset.

Docsalot may be studied as a compatibility/reference idea, but Stage 2A does not require Docsalot and does not publish private project knowledge externally.

## 4. Live Web Context

Current category: web research tools used when freshness or external verification is required.

Possible future optional providers may include services such as Context.dev, subject to privacy, provenance, reliability, and deep-change review where applicable.

Stage 2A does not make any Live Web Context provider a core dependency.

## 5. User Context

Examples:
- explicit project decisions
- explicit preferences and constraints
- approvals required by the deep-change gate

User context is authoritative only for what the user actually decided or approved. Do not infer approval from convenience, prior architecture pressure, or model preference.

## Compatibility mapping

Workspace-style concepts map to existing MPE concepts without new runtime behavior:

- Expert -> bounded Expert contract
- Expert Team -> temporary per-run composition
- Playbook -> human-readable/versioned procedure
- Review Gate -> deterministic/semantic/human gate
- Run -> one measured execution with terminal state
- Artifact -> observable file/evidence reference

This mapping is for future Workspace compatibility only. It does not implement Workspace UI, queues, scheduling, durable agent lifecycle, or workflow execution.
