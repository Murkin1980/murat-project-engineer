# Brainstorm Capture & Twice-Weekly Review — proposed MPE rule

**Decision:** EXTEND_EXISTING. This rule is a proposal for MPE governance, not permission to implement a new service, database or bot.

## Default mode
All new ideas discussed in chat begin in **BRAINSTORM** state — including products, integrations, sites, agents, repositories, architecture and future features. Conversation and exploratory agreement are not approval to implement. Do not create repositories, branches, issues, pull requests, deployment jobs or change authoritative architecture **solely because an idea was discussed**.

## Idea records
Maintain ideas in the owning project's existing dedicated brainstorm/draft file if one exists. Reuse current structure; do not create parallel idea registers.
Suggested minimum attributes: stable idea ID, short title, date, owning project, problem/opportunity, brief idea, source conversation/reference (when available), evidence/unknowns, duplicates/related components, status, next question and last reviewed date.

**Stages:** BRAINSTORM → TRIAGE → APPROVED → EXECUTION (or HOLD / REJECT).
Only explicit owner approval can move an idea to APPROVED or EXECUTION. Before any substantial implementation apply MPE New Idea Filter (existing projects, extension, reuse, duplication, measurable value, small MVP, priority and deep-change gate) and issue exactly one decision label.
Do not silently convert an evolving brainstorm to product requirements or approved architecture. Keep historical decisions traceable.

## Review cadence
Twice weekly: Tuesday and Friday, approximately 10:00 Almaty time, unless owner changes schedule. Review drafts in accessible project repositories, not all code files. Target known brainstorm locations and filenames such as `BRAINSTORM*`, `IDEAS*`, `DRAFT_IDEAS*` and existing project-specific draft paths. Don't infer a missing file means no ideas; report coverage/access gaps. Avoid unrelated implementation files.

## Review criteria
- New ideas since prior review
- Unfinished ideas not touched for 2+ days (not every stale idea; prioritize relevance)
- Duplicates/cross-project consolidation and components already available
- Concrete benefit, low-cost test, current priority, deep-change concerns
- Ideas worth resuming, clarifying, parking or rejecting

## Report (short)
For each of up to 3–5 significant ideas, show: project, when raised, one-line summary, why revisiting matters, suggested next question and MPE preliminary disposition (not an implementation approval). Include count of ideas checked, checked repos, inaccessible repos, and what changed since prior scan. Ask conversationally e.g. "Мы обсуждали эту идею два дня назад — вернёмся к ней?" No automatic start, merge or deployment.

## Source and privacy rules
- Public repositories: only public-safe abstractions and sanitized records; never paste private chats, personal details or customer secrets.
- Use connected GitHub and available chat context as authorized; no fabricated scans or claims of full coverage.
- If cross-repository discovery is unavailable, explicitly name limitations.
- No new agent, infrastructure, schedule code, or indexing layer. Use existing review/reminder mechanism.
