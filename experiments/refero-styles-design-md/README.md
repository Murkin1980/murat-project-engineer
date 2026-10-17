# Refero Styles -> DESIGN.md — bounded Arena experiment
Date: 2026-10-08
Status: QUEUED / NOT EXECUTED
New Idea Filter: REUSE_COMPONENT

Sources:
- https://pimenov.ai/knowledge/refero-styles-biblioteka-design-md/
- https://styles.refero.design/

## Fit and reuse
Existing preferred UI references: Refero Styles and Uiverse.io. Existing projects have their own UI conventions. Do not create a universal design system, new repository, service or MCP integration. Reuse existing CSS tokens, components, mobile QA and project documentation. Preserve project-local source of truth.

## Test hypothesis
A small, verifiable project-local DESIGN.md synthesized from chosen Refero references and existing tokens helps an agent improve one Business Discovery Rich Message with fewer style inconsistencies and mobile regressions than the same task without the design contract.

## Bounded MVP
1. Select one existing Business Discovery Rich Message with baseline screenshot, component tree, tokens, mobile behavior and test status. Do not redesign the full app.
2. Review Refero licensing/terms, use references as inspiration, do not copy proprietary assets or layouts verbatim.
3. Draft a compact experimental DESIGN.md covering typography, colors, spacing, components, states, responsive rules, a11y and explicit non-goals; reconcile with existing design tokens and instructions rather than superseding them.
4. Compare A/B on the *same* message and task scope: current guidance versus DESIGN.md-guided change in isolated branches or fixtures. Avoid changing production assets.
5. Validate at phone width and desktop width: long text, empty/error/loading states, tap targets, contrast, layout overflow, no hidden actions; run existing tests.
6. Record screenshots, objective defects, change size, time/compute usage where observable, and reviewer preference. Separate measurable results from subjective judgments.
7. Terminal RESULT PASS/PARTIAL/FAIL/BLOCKED; ADOPTION ADOPT_WITH_CHANGES/HOLD/REJECT; owner approves any wider rollout.

## Gates
- No replacement of existing design system, no global instructions or mandatory new dependency.
- No new repo or infrastructure. No production deployment as part of experiment.
- Deep-change requires explicit owner approval if a global design contract, architectural rule, or design-system migration is proposed.
- One object -> one identity -> many representations: don't introduce a second parallel source of truth for component definitions.

Priority: P1 within UI/Rich Messages experiments, below active production blockers.
