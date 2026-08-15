# FreeBuff / Codebuff Architecture Patterns

Date: 2026-08-14  
Source: read-only clone of `CodebuffAI/codebuff`  
Extraction route: `opencode-go/deepseek-v4-flash` through Codex Router  
Critical review route: `gpt-5.6-sol` through Codex Router  
Decision: `REUSE_COMPONENT` (patterns only)

| Pattern | Codebuff evidence | MPE equivalent / duplication | Decision |
|---|---|---|---|
| Typed bounded role metadata | `agents/types/agent-definition.ts` | Markdown Experts/Teams; PARTIAL | REUSE_COMPONENT |
| Capped context discovery | `common/src/project-file-tree.ts`, `agents/file-explorer/*` | Context policy only; NONE | REUSE_COMPONENT |
| Workspace containment | `common/src/util/path.ts`, `sdk/src/run.ts`, file-filter tests | Temporary-team concept; PARTIAL | REUSE_COMPONENT |
| No-edit structured reviewer | `agents/reviewer/code-reviewer.ts`, `packages/agent-runtime/src/compact-history.ts` | Reviewer/Handoff contracts; HIGH | REUSE_COMPONENT |
| Bounded command evidence | `sdk/src/tools/run-terminal-command.ts` | Gate command records only; NONE | REUSE_COMPONENT |
| Step budget and mechanical compaction | `common/src/constants/agents.ts`, `packages/agent-runtime/src/compact-history.ts` | Playbook sequence; PARTIAL | REUSE_COMPONENT |
| Trace and judge evidence | `common/src/types/contracts/trace.ts`, `evals/buffbench/judge.ts` | Run/Experiment records; PARTIAL | REUSE_COMPONENT |
| Retry/interruption heuristics | `sdk/src/retry-config.ts`, `sdk/src/impl/stream-interruption.ts` | Bounded gate retry policy; PARTIAL | REUSE_COMPONENT |
| Abort-safe cleanup | `packages/agent-runtime/src/run-programmatic-step.ts`, `cli/src/utils/exit-cleanly.ts` | Rollback gate; PARTIAL | REUSE_COMPONENT |

## Recommended reuse form

Reuse only human-readable contracts and evidence fields:

1. Expert metadata may declare model profile, allowed tools, spawnable bounded roles, output contract, and context-history policy.
2. Context discovery should honor ignore files, cap tree size/results, prefer `AGENTS.md`, and record files selected.
3. VERIFIED/DEEP-CHANGE playbooks should record cwd/file containment, command timeout/output cap, step budget, interruption point, retry reason, and cleanup evidence.
4. Reviewer output remains non-editing and structured; reviewer raw work should not pollute candidate context.
5. Experiment Records may reference trace steps and, for consequential comparisons, two independent judge verdicts with disagreement visible.

## Held or rejected elements

`HOLD`: tree-sitter code-map index, QuickJS generator sandbox, terminal broker, telemetry pipeline, runtime retry loop. These require measured need and some cross current Stage 2 boundaries.

`REJECT`: copying the whole runtime, adding a daemon/control plane, terminal watchdog/broker ownership inside MPE, a new repository, persistent agents, or a second source of truth.

```text
patterns_worth_reusing: 9
FREEBUFF_PATTERN_DECISION: REUSE_COMPONENT
```

