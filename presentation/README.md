# MPE × Business Discovery interactive presentation

Static public presentation for entrepreneurs.

## MPE New Idea Filter

Decision: `EXTEND_EXISTING`.

The presentation is intentionally kept inside `murat-project-engineer`. It does not create a parallel product, backend, database, or new repository.

## Storytelling presentation

- Single static `index.html`
- Eight-screen, mobile-first storytelling flow
- Fully centralized RU/KZ content and interface copy
- Previous/next controls, progress, section picker, and keyboard navigation
- Interactive Business Discovery → MPE pipeline and business scenario
- Responsive layouts verified at 360×800, 390×844, and 1440px desktop
- No external JavaScript dependencies
- No backend and no secrets

## Cloudflare Pages

Recommended configuration:

- Repository: `Murkin1980/murat-project-engineer`
- Production branch: `main`
- Build command: leave empty
- Build output directory: `presentation`
- Root directory: repository root

Pages project name: `mpe-business-discovery`

After the first deploy, attach a custom domain only if needed. The initial `*.pages.dev` URL is sufficient for MVP validation.
