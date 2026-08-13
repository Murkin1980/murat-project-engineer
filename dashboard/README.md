# Murat Project Portfolio Dashboard

Interactive mobile-first portfolio map for Murat Project Engineer.

## Live dashboard

https://murat-project-engineer.muriktl.workers.dev

## Local preview

Open `dashboard/public/index.html` in a browser or run:

```bash
npx wrangler dev
```

## Deploy

Merges to `main` trigger the GitHub Actions workflow in `.github/workflows/deploy-dashboard.yml` when `CLOUDFLARE_API_TOKEN` and `CLOUDFLARE_ACCOUNT_ID` are configured.

Manual deploy (requires `CLOUDFLARE_API_TOKEN`):

```bash
npx wrangler@4.110.0 deploy
```

## Data update ritual

The portfolio data is embedded in `dashboard/public/index.html`. Update the snapshot as part of the weekly portfolio ritual and redeploy.
