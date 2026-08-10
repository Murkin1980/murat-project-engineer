# Context Map

Purpose: progressive disclosure for Murat Project Engineer Experts. This file is documentation only; it is not a memory service or runtime interface.

## Source priority

When sources conflict, follow `context/PROJECT_CONTEXT.md` and the active project's source-of-truth rules. Stop rather than silently reconciling binding conflicts.

## Core sources

| Source | Read when | Mandatory for |
|---|---|---|
| `AGENTS_PLUGINS_MURAT_AI_STACK_MASTER.md` | The task touches Murat AI Stack architecture, boundaries, plugins, Router authority, or deep-change classification. | DEEP-CHANGE; architecture-sensitive VERIFIED tasks |
| nearest applicable `AGENTS.md` | Before modifying a target repository or workspace that provides local operating rules. | All modification tasks when present |
| `FOUNDATION.md` | The target project defines foundational product, legal, domain, or architecture constraints there. | VERIFIED/DEEP-CHANGE when present and relevant |
| `DESIGN.md` | The task changes behavior, interfaces, data flow, architecture, or approved design. | VERIFIED/DEEP-CHANGE design-sensitive work |
| `STATUS.md` | Before selecting current work or resuming an interrupted task. | All Stage 2 runs when present |
| `SESSION_NOTES.md` | Recent context may materially affect the task; verify freshness against stronger sources. | Optional; never sufficient alone for binding decisions |
| approved decision records | A prior decision may constrain implementation. | Tasks touching the recorded decision |
| relevant skills/plugin docs | A professional procedure or tool contract applies. | When that skill/plugin is invoked |

## By task class

### FAST
Read the nearest project rules and the smallest current source set needed to prove scope. Add architecture sources only if the task touches architecture boundaries.

### VERIFIED
Read current status plus relevant project rules, design/foundation material, and binding decisions before implementation. Preserve source references in the Run Report.

### DEEP-CHANGE
Read MASTER, nearest project rules, current status, relevant foundation/design decisions, and the deep-change procedure before doing any implementation. If explicit approval is absent, stop with `DEEP_CHANGE_REQUIRES_USER_APPROVAL`.

## Expert guidance

- Architect: prioritize MASTER/AGENTS/FOUNDATION/DESIGN/decisions.
- Coder: prioritize AGENTS/DESIGN/STATUS plus acceptance criteria and handoff references.
- Reviewer: read acceptance criteria, changed-file evidence, applicable gates, and the same binding sources that constrained implementation.
- Researcher: read the project question and provenance requirements first; external research never silently overrides project source-of-truth.

## Progressive disclosure rule

Do not preload every document. Read the smallest sufficient source set, then expand only when the task, risk tier, or a detected conflict requires it.

Private project context must not be sent to external/public services by default.
