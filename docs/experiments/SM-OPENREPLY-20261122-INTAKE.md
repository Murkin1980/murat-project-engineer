# SM-OPENREPLY-20261122 — OpenReply Instagram lead automation

Status: UNNUMBERED / DRAFT — registration only. Candidate next number EXP-51 is not assigned; canonical main ended at EXP-50 at preflight. Recheck FIFO including earlier open PRs before allocation.

Owner: Salamat Mebel; potential reuse Bek Mebel. MPE decision: REUSE_COMPONENT. Proposed priority P2, after active EXP-48/49; budget $0 additional. No deep change for documentation only.

Source: https://github.com/diwenne/openreply

Hypothesis: a bounded comment-to-DM pattern can reduce manual lead handling and route qualified enquiries into existing furniture estimate tooling without duplicating CRM, calculator or hosting. Compare EXP-25 Atomic CRM, EXP-49 estimate tools and existing social publishing workflow; publishing is not inbound lead handling. Portfolio-wide overlap remains to be verified. No new repository, service or infrastructure authorized.

CP-01 (requires separate execution authorization): read-only upstream audit, verify license, pinned revision, Meta permissions, messaging constraints, security, deployment dependencies, existing CRM and calculator overlap. Determine cheapest reusable component or pattern and document blockers. No credentials, installation or external messages.

CP-02 (separate approval): synthetic offline comparison of manual vs proposed routing on 20 fictional comment scenarios; include duplicates, opt-out, unsupported intent and invalid input. Proposed pass: at least 18/20 correct routes, zero unauthorized sends, zero duplicate lead events, and median operator handling time reduced by at least 30% against measured manual baseline. Record evidence and costs; no real customer data. Real conversion remains unverified until separately approved pilot.

CP-03 (separate approval): evaluate prospect-to-estimate and qualified lead conversion only if platform rules, data protection, infrastructure and cost gates permit. No live traffic, deployment, Meta connection, recurring cost or security boundary changes without owner approval.

Registration handoff: confirm all earlier eligible original PRs, deduplicate, refresh main, allocate next available ID atomically under the existing guard, update canonical registry and derived views, run CI/Python/dashboard and independent review for final SHA. Do not merge until authorized and gates pass. Arena not authorized.
