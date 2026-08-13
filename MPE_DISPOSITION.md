# MPE Disposition — Portfolio Dashboard Integration

**Date:** 2026-08-13
**Project:** Murkin1980/murat-project-engineer
**Request:** Integrate the `murat-project-dashboard.zip` dashboard into this repository and deploy it as a Cloudflare Workers Static Assets site with GitHub auto-deploy.

## New Idea Filter result

**Primary disposition:** `EXTEND_EXISTING`

## Rationale

1. **Existing active project overlap.** The dashboard is explicitly an extension of `murat-project-engineer`. Its `next` step already states: *"Добавить Portfolio Dashboard как EXTEND_EXISTING."*
 2. **EXTEND / REUSE / MERGE before new construction.** The artifact adds no new runtime, no new repository, and no new product surface. It exposes the existing portfolio data as a read-only static UI served from the same repo.
 3. **No duplicate functionality.** No other project in the portfolio provides a portfolio map UI. The dashboard consumes the same data model the repository already maintains.
 4. **Measurable outcome.** A single URL where stakeholders can view project status, search/filter, and click through to GitHub repositories.
 5. **Smallest validation experiment.** Static HTML+JS, Cloudflare Workers Static Assets, and a GitHub Actions workflow on `push` to `main`. No backend, no persistence, no stateful Worker.
6. **Portfolio priority.** Supports the current Stage 2 experiment objective by making portfolio status observable and reviewable.
7. **Deep-change risk.** Low. The change adds a `dashboard/` static asset directory, `wrangler.jsonc`, and a GitHub Actions workflow. It does not modify Experts, Playbooks, gates, contracts, or the plugin manifest.

## Boundaries preserved

- No daemon, scheduler, workflow engine, persistent agent, memory service, or Router modification.
- No new repository created.
- Existing `scripts/validate_package.py`, tests, and plugin metadata remain untouched.
- Dashboard data remains a static snapshot updated through the weekly portfolio ritual, not a live API integration.
