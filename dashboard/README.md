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

The portfolio brief is an existing static snapshot embedded in `dashboard/public/index.html`. Update it as part of the weekly portfolio ritual and redeploy.

## Experiment Registry views

The `#registry` dashboard section is a read-only Reladraw presentation. Its only data source is `experiments/EXPERIMENT_REGISTRY.json`; the generated desktop portfolio and per-status mobile SVGs are served from `dashboard/public/registry/`. No registry data is maintained in the dashboard.

To refresh after a registry update, regenerate the checked CP-02 Reladraw sources and renders, then copy the SVGs into the static asset directory:

```bash
CP02=experiments/exp-19-shirman-trend-intake/cp02
python scripts/registry_to_reladraw.py --out "$CP02/portfolio.reladraw" --mobile-dir "$CP02/mobile"
npx --yes reladraw@0.13.0 "$CP02/portfolio.reladraw" -o "$CP02/portfolio.svg"
cp "$CP02/portfolio.svg" dashboard/public/registry/portfolio.svg
for src in "$CP02"/mobile/status-*.reladraw; do
  npx --yes reladraw@0.13.0 "$src" -o "${src%.reladraw}.svg"
  cp "${src%.reladraw}.svg" "dashboard/public/registry/mobile/$(basename "${src%.reladraw}").svg"
done
```

`reladraw` is a regeneration-time tool only; the dashboard deploy serves the committed static SVGs. `python -m unittest discover -s tests` checks registry freshness, dashboard references, render parity, and the 390px mobile dimensions.
