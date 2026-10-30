# OpenCode Go egress note

**Egress status: `UNVERIFIED`**

The frozen EXP-13 route asset contains model slugs (`opencode-go/deepseek-v4-flash` and `opencode-go/kimi-k2.7-code`) but no provider base URL or outbound hostname. The route-profile documentation identifies Codex Router as the route source, but does not supply the upstream endpoint.

Accordingly, an expected hostname could not be established from the checked repository/runtime configuration, and no allowlist match can be assessed from the route data. No DNS lookup, network probe, HTTP request, or live provider call was made. This is **not** evidence that egress is allowed or blocked.

Re-check egress only after the owner/admin supplies or confirms the authoritative provider endpoint and secret configuration. This preflight does not authorize a provider request or route change.
