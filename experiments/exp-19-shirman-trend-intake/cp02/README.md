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
