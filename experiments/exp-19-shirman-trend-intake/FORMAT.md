# EXP-19 / CP-01 — Agent-Readable Signal Format Specification

- **Specification Version**: 1.0.0
- **Purpose**: Define the minimal, token-efficient, unambiguous agent-readable format for trend intake cards.
- **Target Consumer**: AI Agent Coordinators, Backlog Grooming Agents, and MPE New Idea Filter evaluators.

---

## 1. Design Principles

1. **Self-Contained Context**: An agent reading a single signal card must have 100% of the information required to run the Murat Project Engineer New Idea Filter without fetching additional web pages or files.
2. **Token Efficiency**: Must minimize LLM prompt token consumption when batching 10–50 signals into an agent prompt window.
3. **Deterministic Parsing**: Fields must use fixed key names and strict enum sets to prevent agent parsing errors or hallucinated dispositions.
4. **Dual Representation**:
   - **Markdown Card Format** (Optimized for human readability and LLM context injection).
   - **JSON Schema Format** (Optimized for programmatic validation in Python/TypeScript scripts).

---

## 2. Canonical Markdown Card Format

Every signal entry in `SIGNALS.md` must adhere to this exact 10-field Markdown structure:

```markdown
### SIG-XX: [Title]
- **source**: <URL or Feed Origin>
- **title**: <Descriptive Title>
- **what_changed**: <1-2 sentences on what actually changed/was released>
- **why_it_may_matter**: <1-2 sentences on relevance to MPE / Murat AI Stack>
- **candidate_project**: <Target repository name or "None">
- **reuse_or_extend_path**: <Specific reuse/extension mechanism or "N/A">
- **measurable_value**: <Quantifiable user/business outcome or "None">
- **MVP/experiment**: <Smallest test path or "N/A">
- **deep_change**: <true | false>
- **New Idea Filter decision**: <EXTEND_EXISTING | REUSE_COMPONENT | MERGE | EXPERIMENT | HOLD | NEW_REPOSITORY | REJECT>
```

---

## 3. Field Specification & Constraints

| Field Name | Type | Required | Allowed Values / Pattern | Description |
| :--- | :--- | :--- | :--- | :--- |
| `source` | string (URI) | Yes | Valid HTTP/HTTPS URL | Original source link from Shir-man digest or direct repo/site. |
| `title` | string | Yes | Plain text (10–100 chars) | Short, unambiguous descriptive title. |
| `what_changed` | string | Yes | 1–2 plain sentences | Factual description of what changed or was shipped. No promotional hype. |
| `why_it_may_matter` | string | Yes | 1–2 plain sentences | Core hypothesis on why this signal is relevant to Murat AI Stack. |
| `candidate_project` | string | Yes | Active repo name or `"None"` | Target project (e.g. `murat-project-engineer`, `ai-microtask-factory`, `mebelflow-ai`, `mebeldocs-ai`, `minibase-cloudflare`). |
| `reuse_or_extend_path` | string | Yes | Plain text | Concrete mechanism for re-using or extending existing code/playbooks. |
| `measurable_value` | string | Yes | Plain text with metrics | Measurable metric (e.g., token reduction, latency cut, error reduction). |
| `MVP/experiment` | string | Yes | Plain text | Minimal test plan to validate before committing development effort. |
| `deep_change` | boolean | Yes | `true` or `false` | Indicates if implementation requires architectural deep change (DB, crawler, new repo, daemon). |
| `New Idea Filter decision` | enum | Yes | `EXTEND_EXISTING`<br>`REUSE_COMPONENT`<br>`MERGE`<br>`EXPERIMENT`<br>`HOLD`<br>`NEW_REPOSITORY`<br>`REJECT` | Mandatory primary disposition as per `docs/NEW_IDEA_FILTER_POLICY.md`. |

---

## 4. Machine-Readable JSON Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "MPE_Trend_Signal_Card",
  "type": "object",
  "required": [
    "id",
    "source",
    "title",
    "what_changed",
    "why_it_may_matter",
    "candidate_project",
    "reuse_or_extend_path",
    "measurable_value",
    "mvp_experiment",
    "deep_change",
    "new_idea_filter_decision"
  ],
  "properties": {
    "id": {
      "type": "string",
      "pattern": "^SIG-[0-9]{2,3}$"
    },
    "source": {
      "type": "string",
      "format": "uri"
    },
    "title": {
      "type": "string",
      "minLength": 5,
      "maxLength": 120
    },
    "what_changed": {
      "type": "string",
      "minLength": 10
    },
    "why_it_may_matter": {
      "type": "string",
      "minLength": 10
    },
    "candidate_project": {
      "type": "string"
    },
    "reuse_or_extend_path": {
      "type": "string"
    },
    "measurable_value": {
      "type": "string"
    },
    "mvp_experiment": {
      "type": "string"
    },
    "deep_change": {
      "type": "boolean"
    },
    "new_idea_filter_decision": {
      "type": "string",
      "enum": [
        "EXTEND_EXISTING",
        "REUSE_COMPONENT",
        "MERGE",
        "EXPERIMENT",
        "HOLD",
        "NEW_REPOSITORY",
        "REJECT"
      ]
    }
  },
  "additionalProperties": false
}
```

---

## 5. Token Efficiency & Context Window Analysis

| Format | Avg Tokens per Card | 15 Cards Total Tokens | Context Window Impact (128k LLM) | Agent Readability Rating |
| :--- | :--- | :--- | :--- | :--- |
| **Raw Web HTML / Scraped Feed** | ~550 tokens | ~8,250 tokens | ~6.4% | Low (Noise, navigation clutter) |
| **Verbose JSON (Formatted)** | ~340 tokens | ~5,100 tokens | ~4.0% | Medium (Braffold overhead) |
| **Canonical Markdown Card (FORMAT.md)** | **~175 tokens** | **~2,625 tokens** | **~2.0%** | **High (Optimal key-value density)** |

### Efficiency Gain:
- Using the Markdown Key-Value Card format yields a **~68% reduction in tokens** compared to raw feed ingestion and a **~48% reduction** compared to verbose JSON.
- An agent can digest up to **50 trend signals in a single 10k token turn** while retaining full precision for filtering.

---

## 6. Automated Agent Intake Workflow

```text
[Shir-man Feed / Web Digest]
         │
         ▼ (Intake Agent / Script)
[Compact Markdown Card Format (FORMAT.md)]
         │
         ▼ (MPE New Idea Filter Evaluation)
[New Idea Filter Decision Assigned]
         │
    ┌────┴──────────────────────────┐
    ▼                               ▼
[Actionable Shortlist]      [Noise / Reject / Hold]
 (EXTEND/REUSE/EXPERIMENT)    (Saved in SIGNALS.md archive)
    │
    ▼
[Project Backlog Item / Experiment Task Packet]
```

---

## 7. Compliance Examples

### Valid Card Example:
```markdown
### SIG-01: Reladraw
- **source**: https://github.com/reladraw/reladraw
- **title**: Reladraw — Text-based diagram language using relative positions
- **what_changed**: Released a text diagram format based on relative constraints instead of absolute coordinates.
- **why_it_may_matter**: Prevents agent layout bugs during architecture diagram generation.
- **candidate_project**: murat-project-engineer
- **reuse_or_extend_path**: Add Reladraw template to playbooks/VERIFIED.md for agent architecture artifacts.
- **measurable_value**: Zero rendering syntax errors; saves ~10 mins per diagram edit.
- **MVP/experiment**: Generate 3 architecture handoffs using Reladraw syntax.
- **deep_change**: false
- **New Idea Filter decision**: REUSE_COMPONENT
```

### Invalid Card Example (Rejection Causes):
- Missing `New Idea Filter decision` enum value.
- Missing `deep_change` boolean flag.
- Vague `what_changed` ("Great new tool to improve productivity!").
- Missing `candidate_project` mapping.
