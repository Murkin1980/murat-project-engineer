#!/usr/bin/env python3
"""EXP-24 Phase 2 — CP-07 media specification (hard-scope compliant).

Media-source authority (SALAMAT_PROMO_ARENA_TASK.md § HARD SCOPE CONTRACT):

  1. REAL LICENSED VIDEO FOOTAGE — Storyblocks first        <- every ordinary scene
  2. other explicitly approved licensed real footage
  3. existing owner/project media
  4. bounded neutral placeholder (pipeline testing only)    <- used while (1) is blocked
  5. generative media, allowlist only                       <- max 3 before owner review

Consequences encoded here:
  * the storyboard supplies every stock request (query, duration, in/out intent) — this
    module only supplies provider/auth metadata;
  * a blocked provider yields UNRESOLVED entries + a neutral search slate, never
    generated imagery;
  * the generative list holds **2** branded graphics, both explicitly present in the
    owner script (scene 1 wordmark, scene 9 end card) — the third slot stays unused.
"""

from __future__ import annotations

STORYBLOCKS = {
    "provider": "storyblocks",
    "provider_kind": "licensed_stock",
    "licence_note": (
        "Storyblocks royalty-free licence — per-clip commercial use within the terms of the owner's "
        "subscription. A clip must be searched, previewed and licensed before publication. The exact "
        "query + search URL are recorded so the identical clip can be re-found and licensed."
    ),
    "search_base": "https://www.storyblocks.com/video/search?searchterm=",
}

PLACEHOLDER = {
    "provider": "internal:search-slate",
    "provider_kind": "neutral_placeholder",
    "licence_note": (
        "Not media. A neutral, text-only search slate drawn by the Remotion composition so assembly, "
        "timing, titles, subtitles and mobile readability can be tested while licensed footage is "
        "unavailable. It contains no generated imagery and must not ship in a published film."
    ),
}

BLOCKER = ("no STORYBLOCKS_PUBLIC_KEY / STORYBLOCKS_PRIVATE_KEY in the execution environment and the "
           "provider API host is unreachable from the sandbox")
REQUIRED_ACTION = ("authenticate an approved licensed provider (Storyblocks first), run the recorded "
                   "query, license one matching clip and re-resolve this manifest")

GENERATIVE_BUDGET = 3   # hard contract: maximum generated visual assets before owner review

BRANDED: list[dict] = [
    {
        "asset_id": "brand-wordmark-reveal",
        "scene_id": "open-interior",
        "allowlist_category": "logo reveal",
        "reason": ("Owner script scene 1 requires the on-screen text SALAMAT MEBEL over the opening "
                   "interior. A wordmark reveal cannot be sourced as real footage; it is an allowlisted "
                   "branded graphic drawn as a Remotion layer over the licensed shot (no generated imagery)."),
        "render": "Remotion layer over scene 1 footage",
        "in_out": "appears at 3.6 s, holds into the next beat",
        "script_ref": "SALAMAT_PROMO_SCRIPT.md#scene-1",
    },
    {
        "asset_id": "brand-end-card",
        "scene_id": "brand-close",
        "allowlist_category": "branded end card",
        "reason": ("Owner script scene 9: 'Clean branded final frame. Motion graphics / logo reveal "
                   "allowed here.' Carries the wordmark and the neutral positioning line; no verified "
                   "contact data exists, so no contact block is rendered."),
        "render": "Remotion composition BrandClose (src/BrandClose.tsx)",
        "in_out": "7.0 s closing card, tagline holds for the final 2 s",
        "script_ref": "SALAMAT_PROMO_SCRIPT.md#scene-9",
    },
]

# Allowlisted but NOT used: no scene in the approved script needs a designed transition,
# and the hard contract forbids doing more than the script requires.
ALLOWLISTED_UNUSED: list[dict] = [
    {
        "allowlist_category": "abstract branded transition",
        "reason_not_used": ("The approved script contains no designed transition. Adding one would be "
                            "scope expansion beyond the script, so the slot is left unused."),
    },
]


def assert_budget() -> None:
    if len(BRANDED) > GENERATIVE_BUDGET:
        raise SystemExit(
            f"refusing to build: {len(BRANDED)} branded graphics exceeds the pre-review generative "
            f"budget of {GENERATIVE_BUDGET}"
        )
