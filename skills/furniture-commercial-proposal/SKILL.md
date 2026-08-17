---
name: furniture-commercial-proposal
version: 1.0.0
description: Create, validate, localize, package, and deploy furniture commercial proposals from user-supplied sketches/photos, dimensions, quantities, and prices using the locked established Liquid Glass design.
---

# Furniture Commercial Proposal

## Purpose

Create client-ready online commercial proposals (КП) for furniture from sketches/photos and structured position data supplied by the user. The output is a static, mobile-friendly, multilingual Cloudflare Pages site with one card per furniture position, per-position prices, a price table, language switcher, WhatsApp CTA, and print/PDF support.

This skill extends the existing Interactive KP / Murat Project Engineer workflow. Do not create a new repository or parallel design system for this task.

## Non-negotiable design rule

The current КП visual style is LOCKED and canonical. Do not redesign, restyle, modernize, re-theme, simplify, or replace it unless the user explicitly asks for a design change and the deep-change gate is passed.

Use `references/DESIGN_LOCK.md` as the source of truth for the established style. Content may change; the visual language must not drift.

## Trigger

Use this skill when the user asks to create an online furniture КП / commercial proposal from one or more of:

- furniture sketches;
- furniture photos;
- dimensions;
- material / color / hardware notes;
- quantity;
- price;
- client name;
- one, two, or three requested languages;
- Cloudflare deployment and a shareable public link.

## Intake workflow

1. Treat every uploaded image as source material, not as an image-generation request.
2. Never regenerate, stylize, redraw, crop destructively, or replace a user-supplied sketch/photo unless explicitly asked.
3. Work position-by-position when the user is supplying data sequentially.
4. After each position, keep a position ledger with:
   - sequential position number;
   - exact product name;
   - dimensions in the user's stated order;
   - quantity;
   - unit price;
   - source image;
   - material/color/hardware notes explicitly supplied or visually unambiguous;
   - any unresolved field.
5. Ask only for missing information that is needed. Do not repeatedly ask for data already supplied.
6. Do not infer a price or quantity.
7. Do not silently alter dimensions shown in an image if the user separately states different dimensions. Flag the conflict and use the user's latest explicit statement after confirmation when material.

## Position data contract

Each position should normalize to:

```yaml
position: 1
name: "Шкаф для документов"
dimensions:
  width_mm: 800
  depth_mm: 420
  height_mm: 1900
quantity: 2
unit_price_kzt: 69700
image: "assets/01-shkaf-documents.webp"
material: "ЛДСП, светлый дуб"
features:
  - "две двери"
  - "внутренние полки"
notes: null
```

If dimension orientation is ambiguous, retain a display string exactly as given by the user rather than guessing semantic width/depth/height.

## Language behavior

- The user chooses the language set: one, two, or three languages.
- Do not add languages that were not requested.
- The first requested/default language becomes `index.html`.
- Additional languages use short stable filenames such as `ru.html`, `kz.html`, `tr.html`, `en.html`.
- Translate labels and prose, but keep dimensions, quantities, prices, model names, company names, and material codes accurate.
- Language switching must preserve the same position order and content semantics across all versions.

## Canonical page structure

Keep the established order:

1. Sticky header with КП mark, title, navigation, language switcher, WhatsApp CTA.
2. Hero section with commercial-proposal eyebrow, main title, short lead, actions, metadata, and representative image.
3. "What is included" benefit cards.
4. Furniture position cards, one per position.
5. Price table.
6. Terms / agreement panel.
7. Final CTA.
8. Footer.

Each position card contains:

- source sketch/photo;
- position badge;
- exact product name;
- unit price;
- quantity;
- dimensions;
- material / key features if known;
- concise description based only on supplied/visible facts.

Do not display a grand total unless the user explicitly requests it. The canonical КП format emphasizes the price of each position separately.

## Image handling

1. Preserve each user-supplied source image.
2. Copy assets to safe ASCII filenames in `assets/` (`01-name.webp`, `02-name.webp`, etc.).
3. Prefer optimized WebP/JPEG/PNG files rather than base64 for deployed Cloudflare sites.
4. Compress only enough for fast loading while keeping text, dimension arrows, labels, and furniture details readable.
5. For technical sketches with dimension callouts, ensure the entire annotated drawing is visible; do not crop dimension text off-screen.
6. For normal photos, use the canonical photo presentation.
7. A standalone single-HTML version with embedded images is optional and should only be generated when useful/requested; if generated, compress images first.

## Build outputs

Create a clean deployment directory, for example:

```text
kp-<client-or-topic>-<date>/
  index.html
  ru.html          # if requested
  kz.html          # if requested and not index
  tr.html          # if requested
  en.html          # if requested
  assets/
    01-....webp
    02-....webp
    ...
```

Also create a ZIP archive for backup / Direct Upload when appropriate.

## Mandatory QA before deployment

Do not deliver until all checks pass:

1. Every requested position is present exactly once and in the correct order.
2. Every displayed price and quantity matches the ledger.
3. Every language has the same number of positions.
4. Every local image path resolves.
5. Every rendered `<img>` has non-zero `naturalWidth` and `naturalHeight`.
6. No source sketch/photo is accidentally replaced by a generated image.
7. No dimension annotation is cropped in a way that changes meaning.
8. Language links work.
9. WhatsApp link works and points to the configured business number.
10. "Save to PDF" / print works without broken layout.
11. Check desktop and mobile widths.
12. No horizontal page overflow except inside the intentionally scrollable price table on small screens.
13. Site opens from a local HTTP server, not only from `file://`.
14. ZIP integrity check passes.
15. After Cloudflare deployment, verify the public URL and at least all language pages return successfully and images render.

If an image fails to render, fix the asset path/format and re-run QA. Never tell the user it is fixed without actually testing it.

## Cloudflare deployment

Use `references/CLOUDFLARE_DEPLOY.md`.

The expected final outcome is a working public `https://...pages.dev` or configured custom-domain URL. Return that link to the user.

If Cloudflare credentials/integration are unavailable in the current environment, do not invent a deployment URL. Prepare the verified deployment folder + ZIP, state the exact blocker, and preserve all outputs for later deployment.

## Design change gate

Any request to change typography, palette, glassmorphism, card architecture, spacing system, hero composition, navigation model, or general visual identity is a deep design change relative to this skill.

Stop and request explicit approval before changing the locked design. Normal content changes, position count changes, language changes, client branding text, and new furniture images are not design changes.

## Completion response

When successful, return:

- public Cloudflare URL;
- languages included;
- number of positions;
- deployment archive link if useful;
- only meaningful caveats, if any.

Keep the handoff concise. The public URL is the primary deliverable.
