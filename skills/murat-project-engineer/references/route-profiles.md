# Coordinator-side route profiles

Profiles must resolve to an explicit model slug currently exposed by Codex Router. They do not modify Router configuration.

| Profile | Primary explicit slug | Allowed fallback | Use |
|---|---|---|---|
| `default` | `gpt-5.6-sol` | none; report unavailable | normal coordination and low-risk work |
| `cheap-research` | `opencode-go/deepseek-v4-flash` | `gpt-5.6-sol` | extraction, classification, deduplication |
| `coding` | `opencode-go/kimi-k2.7-code` | `gpt-5.6-sol` | implementation and tests |
| `strong-review` | `gpt-5.6-sol` | none; set `BLOCKED` or `HUMAN_REQUIRED` | architecture, security, semantic judgment |

These mappings reflect routes exposed in the current Codex/Codex Router environment on 2026-08-10. Revalidate availability before each run. Record the resolved slug and every fallback in the Run Report. Never copy credentials or bind an Expert permanently to a slug; definitions reference profiles, while the coordinator resolves profiles at run time.
