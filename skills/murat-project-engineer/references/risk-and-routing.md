# Risk and execution routing

## FAST

Use for narrow, reversible, low-impact work. Select one Expert, run applicable deterministic checks, and report.

## VERIFIED

Use for meaningful changes, unfamiliar components, or semantic risk. Use Architect → Coder, deterministic gates, and an independent Reviewer when acceptance is not fully deterministic.

## DEEP-CHANGE

Use when the request affects MASTER, core architecture, Router authority, credentials/security, persistent agents, plugin boundaries, memory governance, or central runtime.

Produce analysis and a soft-compatible alternative, emit `DEEP_CHANGE_REQUIRES_USER_APPROVAL`, set `HUMAN_REQUIRED`, and stop implementation.

## Team routing

- One bounded Expert is the default.
- `software-standard`: planning and implementation covered by deterministic gates.
- `software-verified`: meaningful software work requiring independent semantic review.
- `research-verified`: consequential research requiring evidence review.
- Multi-solver is not a default team.
