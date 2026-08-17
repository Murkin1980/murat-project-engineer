# Cloudflare Pages Deployment

## Preferred path

Deploy the verified static output directory to Cloudflare Pages using the user's existing Cloudflare project/integration when available.

Before creating any new Pages project, check whether an appropriate existing КП deployment project can be reused. Prefer reuse when it does not overwrite an unrelated active proposal.

## Wrangler path

Current Cloudflare Pages Direct Upload supports deploying a folder of static assets with Wrangler.

Typical sequence:

```bash
npx wrangler pages project list --json
npx wrangler pages deploy <OUTPUT_DIRECTORY> --project-name=<PROJECT_NAME>
```

If the project does not exist and a new project is justified:

```bash
npx wrangler pages project create
npx wrangler pages deploy <OUTPUT_DIRECTORY> --project-name=<PROJECT_NAME>
```

Use `wrangler login` when interactive authentication is required. In CI, use the established Cloudflare account ID/API token mechanism instead of embedding secrets in the repository.

Wrangler uploads a directory, not a ZIP. A ZIP is for backup or dashboard drag-and-drop.

## Naming

Prefer a stable, readable slug based on the proposal/client/date, e.g.:

`kp-ai-hanym-20260817`

Avoid personally sensitive data beyond what is already appropriate for the client-facing proposal.

## Post-deploy verification

After deployment:

1. capture the production URL reported by Cloudflare;
2. request/open `index.html` through that URL;
3. test every language link;
4. verify every image loads;
5. test one desktop and one mobile viewport;
6. test WhatsApp CTA;
7. confirm no 404/asset path errors;
8. only then send the public URL to the user.

Never report deployment success based only on a local build.
