# Canonical Furniture КП Design Lock

Status: LOCKED / ESTABLISHED

This file defines the visual style that must be reused for furniture commercial proposals.

## Visual identity

- Style: premium light Liquid Glass / glassmorphism.
- Mood: clean, architectural, furniture-focused, warm-neutral.
- Background: warm ivory/beige gradients with soft wood and green ambient radial light.
- Primary ink: dark slate / near black.
- Accent: warm wood brown.
- Secondary accent: deep muted green.
- Cards: translucent white glass surfaces, large rounded corners, subtle white borders, soft deep shadows, blur/saturation.
- CTA: dark near-black or wood gradient, pill-shaped controls.
- Typography: Inter/system sans stack, very bold display hierarchy through weight/letter-spacing rather than a decorative font.

## Canonical design tokens

```css
:root{
  --bg0:#f3efe8;
  --bg1:#ebe3d6;
  --ink:#111827;
  --ink-soft:#334155;
  --muted:#64748b;
  --line:rgba(255,255,255,.48);
  --line-dark:rgba(15,23,42,.10);
  --glass:rgba(255,255,255,.46);
  --glass-strong:rgba(255,255,255,.64);
  --dark:#101418;
  --wood:#b9824d;
  --wood-2:#7c4a25;
  --green:#1f4d43;
  --radius:30px;
  --shadow:0 24px 70px rgba(15,23,42,.16);
  --shadow-soft:0 14px 36px rgba(15,23,42,.10);
}
```

## Background contract

```css
body{
  color:var(--ink);
  background:
    radial-gradient(circle at 12% 10%, rgba(185,130,77,.30), transparent 28rem),
    radial-gradient(circle at 88% 6%, rgba(31,77,67,.20), transparent 26rem),
    radial-gradient(circle at 70% 70%, rgba(255,255,255,.82), transparent 35rem),
    linear-gradient(135deg,var(--bg0),var(--bg1));
}
```

## Glass contract

```css
.glass{
  background:linear-gradient(135deg,rgba(255,255,255,.72),rgba(255,255,255,.32));
  border:1px solid var(--line);
  box-shadow:var(--shadow);
  backdrop-filter:blur(22px) saturate(145%);
  -webkit-backdrop-filter:blur(22px) saturate(145%);
}
```

## Geometry contract

- Main page width: max 1200 px with responsive side margins.
- Hero radius: 38 px desktop, ~28 px compact mobile.
- Furniture card radius: 32 px desktop, ~26 px mobile.
- Buttons: fully pill-shaped.
- Hero desktop grid: approximately `1.08fr / .92fr`.
- Position card desktop grid: image area about 410 px + content column.
- One furniture position card per row on desktop.
- Mobile collapses hero/cards to one column.

## Furniture card contract

- Large source image on the left on desktop.
- Content on the right.
- Position badge on image.
- Name is large and bold.
- Unit price is a dark gradient chip with white text.
- Specifications use small translucent sub-cards/chips.
- Description sits in a translucent rounded panel.
- Hover may apply a very mild image scale effect only.

For annotated technical sketches, the source image may use a contain-style fit inside the same canonical image frame solely to keep labels/dimension arrows visible. This is a content-fit exception, not a redesign.

## Responsive contract

At about 980 px:

- hero, position cards, and terms become one column;
- benefits reduce to two columns;
- spec/meta grids become one column;
- tables may scroll horizontally.

At about 620 px:

- side margins reduce;
- hero padding reduces;
- benefits become one column;
- nonessential header navigation hides while language and primary CTA remain usable.

## Print contract

- Hide sticky header and interactive action controls.
- Remove glass blur/shadows for print.
- Avoid splitting a position card across pages when possible.
- Hide the hero image if necessary for concise print output.

## Forbidden drift

Without explicit user approval, do not:

- switch to dark mode;
- change accent colors;
- introduce a different component library/theme;
- replace glass surfaces with flat cards;
- use a different hero layout;
- convert cards into dense tables;
- introduce animated backgrounds, 3D, carousels, or dashboard UI;
- add marketing sections unrelated to the КП;
- change the style because a newer design trend exists.

The design is intentionally stable. Future КПs should feel like the same product with different content.
