/**
 * EXP-24 Phase 2 — mobile-first typography and safe areas.
 *
 * The film is reviewed on a phone at an effective 360 px player width.
 * Scale factor from the 1920 px master: 360 / 1920 = 0.1875.
 * Sizes below are chosen so the on-phone size stays legible:
 *   caption 112 px -> 21 px   (short phrases, max 2 lines)
 *   title   144 px -> 27 px
 *   label    88 px -> 16.5 px (never smaller; no service/debug text anywhere)
 *   cta      80 px -> 15 px
 */
export const TYPE = {
  title: 144,
  subtitle: 84,
  caption: 112,
  label: 88,
  cta: 80,
  brand: 176,
} as const;

export const SAFE = {
  marginX: 120,
  marginTop: 96,
  /** Bottom band reserved for captions; nothing else may enter it. */
  captionBandTop: 1080 - 300,
  captionBandBottom: 1080 - 72,
} as const;

export const COLORS = {
  ink: "#0F0E0C",
  paper: "#F4EFE6",
  brass: "#C8A15A",
  graphite: "#2A2723",
} as const;

/** Caption phrasing: never more than two lines, never more than ~44 chars per line. */
export const CAPTION_MAX_CHARS_PER_LINE = 44;
export const CAPTION_MAX_LINES = 2;
