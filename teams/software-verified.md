---
team_id: software-verified
scope: one-run-temporary
experts: [architect, coder, reviewer]
use_when: VERIFIED or high-impact software work requires semantic independent review.
avoid_when: Deterministic gates fully establish acceptance.
handoffs: [architect-to-coder, coder-to-reviewer]
terminal_owner: coordinator
---

Reviewer invocation must be independent from the Coder invocation.
