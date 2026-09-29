# EXP-19 / CP-02 — Reladraw as a visual layer over existing MPE data

- **Decision**: EXTEND_EXISTING · **Result**: PARTIAL · **Date**: 2026-09-29
- **Tool**: `reladraw@0.13.0` (external, run via `npx`; not added as an MPE dependency)

## Prototype
| File | Role |
|---|---|
| `scripts/registry_to_reladraw.py` | Read-only generator: registry JSON → `.reladraw` text |
| `portfolio.reladraw` | Generated diagram source (do not edit; freshness checked by test) |
| `portfolio.svg` | Rendered with `npx reladraw@0.13.0 portfolio.reladraw -o portfolio.svg` |
| `portfolio-mobile-390px.png` | Same SVG scaled to a 390px phone width |
| `tests/test_registry_to_reladraw.py` | Coverage + stale-diagram + dependency checks |

Regenerate: `python scripts/registry_to_reladraw.py --out experiments/exp-19-shirman-trend-intake/cp02/portfolio.reladraw`

## Data reused (single source of truth, nothing copied)
`experiments/EXPERIMENT_REGISTRY.json` only: `owning_project` → project container, `status` → column,
`experiment_id` + `name` → card, `next_action` → "→ next step" line, free-text EXP-id mentions → dashed "waits on" edge.

## What can be generated automatically
| Element | Auto? | Notes |
|---|---|---|
| Projects | YES | from `owning_project` (3) |
| Experiments | YES | all 19, 0 manual edits |
| Statuses | YES | columns + colour style per status |
| Next step | YES, truncated | `next_action` shortened to 48 chars; full text stays in the registry |
| Dependencies | **PARTIAL (inferred)** | registry has no `depends_on`; regex over free text finds 1 edge (EXP-STAGE3-SYNTHETIC → EXP-12). Unreliable as a real dependency graph |
| Layout | YES | relative placements only; rendered first try with no errors or hand-tuning |

## Mobile / readability
- Desktop (1619×1302 SVG): readable; status colours plus columns scan well.
- Phone 390px, fit to width: scale ≈0.24 → ~3–4px text, **unreadable** without pinch-zoom. The SVG is standalone, so zoom works, but that is not a mobile view.
- Mitigation within the same generator (not done): one diagram per project/status (a vertical single column), or `theme: high-contrast-light` + fewer chars.

## Deep change
**No.** A new canonical data layer is not needed for projects/statuses/next steps.
A real dependency graph would need an optional `depends_on: [EXP-id]` field in the existing registry — a small schema extension that needs owner approval. It is not a new data layer, so this is not `BLOCKED_BY_DEEP_CHANGE`. It was not added here.

## Findings
1. Reladraw works as a pure view layer: registry → text → SVG. No service, repo, or DB.
2. Deterministic text output is diffable and testable (the freshness test fails if the registry changes and the diagram is stale).
3. The dependency gap is a data gap, not a Reladraw gap.
4. Mobile needs split views; one portfolio-wide diagram is desktop-only.

---

# CP-03: Mobile-readable views (same PR #35)

- **Result**: PASS · registry schema unchanged · no `depends_on` · the desktop `portfolio.*` files are byte-identical to CP-02.
- **Approach**: one view **per status**, a single column of cards (wrap 26 chars, project shown as a short label on each card).
- **Generate**: `python scripts/registry_to_reladraw.py --mobile-dir experiments/exp-19-shirman-trend-intake/cp02/mobile`, then `npx reladraw@0.13.0 <file>.reladraw -o <file>.svg`.

| View | SVG width | Cards |
|---|---|---|
| `mobile/status-pass` | 355px | 5 |
| `mobile/status-ready_to_test` | 346px | 3 |
| `mobile/status-planned` | 355px | 7 |
| `mobile/status-hold` | 355px | 4 |

**390px check**: every SVG is ≤355px wide, so it renders 1:1 on a 390px screen (no downscale). Text stays at 14px monospace and reads without zoom
(`*-390px.png` are renders at that size). Before this it was ~0.24× scale and 3–4px text.
Next step is extended from 48 to 70 characters, because the narrow column has vertical room.

**Tests** (`tests/test_registry_to_reladraw.py`): each experiment appears in exactly one view; committed views match the registry; SVG width ≤390 and 14px text; registry has no `depends_on`.

**Findings**: per-status beats per-project on mobile (MPE alone holds 17/19 experiments, so a project view would be one very long column).
The inferred dependency edge is dropped from the mobile views because it crosses views; the dependency is still mentioned in the card text ("Complete EXP-12…").

---

# CP-04: Integrate Reladraw views into the existing MPE dashboard

- **Decision**: EXTEND_EXISTING · **Result**: PASS
- **Integration point**: the existing static `dashboard/public/index.html`; the new `#registry` section is reachable from its existing sticky navigation.
- **Desktop**: the full portfolio SVG is embedded in the dashboard and linked as a standalone SVG for the native 1619px view.
- **Mobile**: four expandable per-status views are embedded; SVG widths are 346–355px with 14px text, and the responsive frame preserves their native size at 390px without zoom.
- **Provenance**: `dashboard/public/registry/*.svg` are generated deployment copies of the validated CP-02 renders. Tests compare each dashboard render byte-for-byte with CP-02 and separately verify the Reladraw sources against `experiments/EXPERIMENT_REGISTRY.json`.
- **Guardrails**: registry and schema unchanged; no `depends_on`, manually maintained duplicate registry state, service, database, queue, worker, or repository added. Reladraw remains a regeneration-time tool only.
- **Verification**: full suite passed (330 tests; 1 platform-specific skip); `python scripts/validate_package.py .` passed; static preview returned HTTP 200 for the dashboard and all five SVG assets.
