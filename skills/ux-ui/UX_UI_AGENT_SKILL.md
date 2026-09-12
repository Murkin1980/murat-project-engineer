# UX/UI Agent Skill — MPE Edition

## 1. Purpose

Use this skill for UI/UX planning, implementation, review, redesign, responsive work, accessibility, design tokens, component specifications, and screenshot/reference-based work. It is a compact reasoning and quality layer for any coding agent. It does not replace project governance, application architecture, or a project's visual source of truth.

Apply only the sections relevant to the task; do not load or enforce the whole skill for an unrelated change.

## 2. Authority Order

Resolve conflicts in this order:

1. MPE governance, Task Packet, approval, checkpoints, and deterministic gates.
2. Project rules and repository instructions (`AGENTS.md`, `FOUNDATION.md`, and equivalent).
3. The target project's `DESIGN.md` and existing implementation/tokens.
4. This UX/UI Agent Skill.
5. External references and inspiration.

A project-specific `DESIGN.md` remains authoritative for that project. This skill is subordinate and must not silently change MPE risk classification, approval, evidence, or deep-change rules.

## 3. Request Router

Select the smallest applicable route:

| Request | Use first | Verify |
|---|---|---|
| New screen | Existing design system, core UX principles, token/component contracts | responsive, a11y, functional flow, render evidence |
| Redesign | Redesign workflow, taste rules, existing behavior | before/after behavior and visual inspection |
| Component design | Component contract, existing components, a11y | applicable states, keyboard behavior, edge cases |
| UI implementation | Framework adapter contract, existing stack/tokens | build/tests, rendered states, responsive behavior |
| Design review | Review rubric, core UX, a11y | findings with evidence, not invented scores |
| Accessibility review | Accessibility contract | keyboard, focus, semantics, contrast, motion |
| Design-system creation | Token contract, existing system, interop mapping | alias resolution, modes, contrast, adoption path |
| Token work | Primitive → semantic → component contract | references, light/dark, contrast, generated output if present |
| Responsive/mobile work | Responsive contract | 390px-class viewport, overflow, touch, density |
| Screenshot/reference replication | Reference workflow | design language transfer, not product copying |

## 4. Core UX Principles

- Make the primary user goal obvious; establish hierarchy through content, scale, spacing, grouping, and emphasis.
- Prefer clear affordances, predictable interaction, useful feedback, and recoverable errors over decoration.
- Preserve working behavior and domain meaning during visual work.
- Handle the full content range: loading, empty, error, success, long text, missing data, many items, and permission differences.
- Reduce cognitive load: one primary action per context where possible, concise labels, progressive disclosure, and sensible defaults.
- Use familiar patterns unless the task has a reason to diverge; explain consequential deviations.
- Treat copy, focus order, keyboard behavior, and responsive behavior as part of the design, not post-processing.

## 5. Anti-AI-Slop / Taste Rules

Taste is a decision aid, not an absolute style law. Follow the project's design direction first.

Avoid or justify:

- meaningless gradients, glows, neon accents, blur, or glass effects;
- the same rounded card repeated for every piece of content;
- excessive nested cards, pills, badges, borders, shadows, or decorative icons;
- generic dashboard composition, uniform grids, template-like hero sections, or arbitrary asymmetry;
- weak typography hierarchy, low information density where scanning matters, or excessive whitespace where it hides relationships;
- decoration without a product function, random animation, or color used as the only state signal.

Before implementation, state the intended visual direction and at least one deliberate choice that prevents a generic result. Use variation in composition, density, typography, or emphasis only when it improves comprehension or expresses the brief.

## 6. Design Token Contract

Prefer this dependency direction:

```text
primitive values → semantic roles → component-scoped tokens → UI code
```

- **Primitives** hold raw palette, type scale, spacing scale, radii, elevation, and motion values.
- **Semantic tokens** express intent such as `surface.page`, `text.primary`, `action.primary`, `border.focus`, or `feedback.error`.
- **Component tokens** express scoped use such as a button's background, input's focus border, or dialog's elevation.

UI code should consume semantic/component tokens, not unexplained raw colors, dimensions, shadows, or timings. Preserve the repository's token format; DTCG-style `$type`, `$value`, and alias references are useful when the project already uses them, but introducing DTCG is not required by this skill.

Cover as applicable: colors and contrast pairs, typography (family/size/weight/line-height), spacing, radius, borders, shadows/elevation, control sizing, breakpoints, and motion. Dark mode should swap semantic roles while keeping primitives reusable; verify contrast again rather than merely inverting colors. Keep aliases resolvable and avoid duplicating unchanged theme values.

## 7. Component Contract

For each interactive component, specify anatomy, variants, content constraints, responsive behavior, and only the states that can occur:

- default;
- hover (when a hover device exists);
- active/pressed;
- `focus-visible`;
- disabled;
- loading;
- selected/expanded/checked;
- error/invalid.

Explicitly mark inapplicable states as N/A. State changes must communicate through more than color where needed. Define behavior for long labels, empty content, async failure, repeated activation, and missing optional data. Reuse an existing component before creating a duplicate.

## 8. Accessibility Contract

Use WCAG 2.2 as the target orientation and apply the project's required conformance level.

Check:

- sufficient text and non-text contrast, including focus, hover, disabled conventions, dark mode, and meaningful chart data;
- semantic HTML and correct accessible names, labels, descriptions, roles, and relationships;
- keyboard reachability and operation, logical focus order, visible `focus-visible`, Escape behavior, and focus management for overlays;
- ARIA only when native semantics are insufficient, with states kept synchronized;
- error identification and recovery, status announcements where needed, and no information conveyed by color alone;
- readable type, zoom/reflow, text expansion, language/RTL considerations when relevant;
- touch targets and spacing appropriate to the platform and task;
- `prefers-reduced-motion`: remove travel and unnecessary motion, but retain the state change and feedback.

Do not claim an automated audit passed without running it. Treat manual keyboard and visual inspection as complementary evidence.

## 9. Responsive/Mobile Contract

Use mobile-first when it matches the product. Design behavior, not just smaller dimensions.

At minimum, inspect a 390px-class viewport and the project's supported desktop width. Check for horizontal overflow, fixed-width assumptions, clipped text, intrinsic control widths, wrapping, zoom/reflow, and readable hierarchy. Decide how navigation, actions, filters, dialogs, sidebars, dense tables, charts, and multi-column layouts transform. Use stacking, collapse, priority actions, off-canvas patterns, or a table-to-list fallback deliberately. Do not rely on hover for essential actions. Preserve comfortable touch interaction and avoid making mobile a degraded afterthought.

## 10. Framework Adapter Contract

First identify the framework, styling system, component library, rendering constraints, and existing tokens. Preserve the current stack and conventions. Adapt the design to React, Vue, Svelte, Angular, native, vanilla CSS, or another stack as appropriate; never change framework, Tailwind/shadcn/etc., or styling architecture merely to obtain a visual result. New dependencies or a new UI framework require explicit project approval.

## 11. Existing Design System First

Before adding UI:

1. Read the project's `DESIGN.md` and applicable project instructions.
2. Inspect existing tokens, primitives, components, patterns, and usage examples.
3. Reuse and extend existing components before adding variants or duplicates.
4. Use **Refero Styles** for broad visual direction and design-system inspiration.
5. Use **Uiverse.io** only for a concrete reusable component or effect pattern, and adapt it to project tokens, accessibility, and behavior; it is not the project's visual authority.
6. Record intentional deviations and their reason.

## 12. Screenshot / Reference Workflow

For a screenshot or reference, first extract layout/composition, hierarchy, spacing rhythm, typography, palette, borders, radius, elevation, density, component patterns, responsive clues, and likely interaction states. Separate observed facts from guesses. Transfer the design language and useful pattern, not the source product's branding, content, implementation, or accidental pixels. Reconcile the result with `DESIGN.md`, existing components, accessibility, and real content lengths.

## 13. Redesign Workflow

Use an audit-first loop:

```text
SCAN → DIAGNOSE → DIRECTION → APPLY → VERIFY
```

- **SCAN:** inventory screens, behavior, components, tokens, breakpoints, and evidence.
- **DIAGNOSE:** identify hierarchy, usability, consistency, accessibility, responsive, and visual problems; rank by user impact.
- **DIRECTION:** choose a small number of visual/interaction decisions tied to the brief.
- **APPLY:** make the smallest coherent implementation; preserve working behavior.
- **VERIFY:** compare before/after where possible, exercise interactions, inspect desktop/mobile, and recheck accessibility.

Do not replace a whole screen when a local, lower-risk change solves the problem.

## 14. Design Review Rubric

Review with findings, not pseudo-precision. For each finding cite the location, observed issue, user impact, severity, and recommended change. Consider:

- hierarchy and scanability;
- consistency with project language and component reuse;
- usability, clarity, feedback, and error recovery;
- accessibility and inclusive interaction;
- responsive behavior and content resilience;
- visual quality, composition, density, and intentionality;
- token discipline and theme readiness;
- implementation correctness and preserved functionality.

Use labels such as blocker, high, medium, or low only when supported by evidence. Numerical scores are optional summaries, never objective measurements.

## 15. Implementation Rules

- Preserve functionality, data contracts, security boundaries, and working behavior.
- Prefer existing components and tokens; add a new one only with a clear reuse case.
- Avoid gratuitous dependencies and new toolchains.
- Do not make backend, database, authentication, production write-path, or infrastructure changes to solve a UI problem.
- Keep the diff minimal and coherent; do not rewrite unrelated screens.
- Do not bypass MPE approval, checkpoints, Task Packet scope, deterministic gates, or evidence requirements.
- Keep generated artifacts and validation scripts project-local; this skill does not require installing the upstream repository.

## 16. Verification Gates

Minimum UI Definition of Done, adjusted to task scope:

```text
build/tests (if applicable)
+ responsive check
+ accessibility check
+ render/browser evidence
+ visual inspection
+ functional interaction check
```

Run existing repository checks first. Apply token, contrast, hardcoded-style, theme-reference, component-spec, render, keyboard, overflow, and reduced-motion validators only when they already exist in the project or their addition is separately approved. Do not create a new validation toolchain or claim checks that were not run.

## 17. Browser Evidence

For a substantial visual change, capture before/after when possible. Inspect at least one desktop width, one 390px-class mobile width, and a meaningful interactive state (for example focus, error, loading, open, or selected). Check real content, not only the happy-path fixture. Pixel-perfect automation can support review but cannot replace visual inspection or functional evidence.

## 18. Output Contract for the Agent

After a UI task, report briefly:

- what was wrong;
- what changed;
- existing components reused;
- tokens used or added;
- accessibility impact;
- responsive result;
- validation/tests actually run;
- browser/render evidence;
- changed files;
- remaining risks or follow-up.

## 19. External Reference Map

- **Project `DESIGN.md`** — project-specific visual source of truth.
- **Refero Styles** — broad visual direction and design-system inspiration.
- **Uiverse.io** — concrete UI component/effect patterns to adapt, not authority.
- **`plugin87/ux-ui-agent-skills`** — upstream knowledge source for this selective adaptation.
- **MPE** — governance, Task Packet, approval, evidence, checkpoints, and terminal state.

## 20. Provenance

- **Upstream:** https://github.com/plugin87/ux-ui-agent-skills
- **Version:** v2.5.1
- **Upstream commit SHA:** `2ffb677aa02b225c8a3da1b7f31d9ebb7c38f1dd`
- **License:** MIT (upstream `package.json` and README)
- **Imported/adapted:** 2026-09-12
- **Method:** selective adaptation; not full vendoring. This file is an agent-neutral knowledge layer and has no runtime dependency on the upstream repository.
