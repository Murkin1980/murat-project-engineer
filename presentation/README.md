# MPE × Business Discovery interactive presentation

Static public presentation for entrepreneurs.

## MPE New Idea Filter

Decision: `EXTEND_EXISTING`.

The presentation is intentionally kept inside `murat-project-engineer`. It does not create a parallel product, backend, database, or new repository.

## MVP

- Single static `index.html`
- Responsive desktop/mobile layout
- RU/KZ language switch
- Interactive Business Discovery → MPE workflow
- No external JavaScript dependencies
- No backend and no secrets

## Cloudflare Pages

Recommended configuration:

- Repository: `Murkin1980/murat-project-engineer`
- Production branch: `main`
- Build command: leave empty
- Build output directory: `presentation`
- Root directory: repository root

Suggested Pages project name: `mpe-business-discovery`

After the first deploy, attach a custom domain only if needed. The initial `*.pages.dev` URL is sufficient for MVP validation.
