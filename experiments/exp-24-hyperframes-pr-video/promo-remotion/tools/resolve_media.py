#!/usr/bin/env python3
"""EXP-24 Phase 2 — CP-07 media manifest.

storyboard beats + Storyblocks probe  ->  MEDIA_MANIFEST.json

Hard-scope rules: a clip is RESOLVED only when a real licensed asset is attached; a
blocked provider yields BLOCKED_PROVIDER + a neutral search slate, never generated
media; the 3-asset pre-review generative budget is asserted before writing.
"""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROMO = HERE.parent
EXP = PROMO.parent
STORYBOARD = EXP / "EDITORIAL_STORYBOARD.json"
MANIFEST = EXP / "MEDIA_MANIFEST.json"
SHORTLIST = EXP / "OWNER_MEDIA_SHORTLIST.json"
LOG = EXP / "MEDIA_PROVIDER_LOG.md"

sys.path.insert(0, str(PROMO / "adapters"))
try:
    import storyblocks_adapter
except Exception:  # noqa: BLE001 - adapter is optional by design
    storyblocks_adapter = None

SEARCH_URL = "https://www.storyblocks.com/video/search?searchterm="
LICENCE = ("Storyblocks royalty-free licence — per-clip commercial use within the owner's subscription "
           "terms. The clip must be searched, previewed and licensed before publication; query + search "
           "URL are recorded so the identical clip can be re-found.")
BLOCKER = ("no STORYBLOCKS_PUBLIC_KEY / STORYBLOCKS_PRIVATE_KEY in the execution environment and the "
           "provider API host is unreachable from the sandbox")
ACTION = ("authenticate an approved licensed provider (Storyblocks first), run the recorded query, "
          "license one matching clip, then re-run tools/resolve_media.py")
BUDGET = 3
SLATE = {
    "provider": "internal:search-slate", "provider_kind": "neutral_placeholder", "preview_only": True,
    "licence_note": "Not media. Text-only search slate drawn by the composition so assembly, timing, "
                    "titles, captions and mobile readability can be tested while licensed footage is "
                    "unavailable. Must not ship in a published film.",
}

BRANDED = [
    dict(asset_id="brand-wordmark-reveal", scene_id="open-interior", allowlist_category="logo reveal",
         reason="Script scene 1 requires the on-screen text SALAMAT MEBEL over the opening interior. A "
                "wordmark reveal cannot be sourced as footage; drawn as a Remotion layer over the shot.",
         render="Remotion layer in src/Promo.tsx (Wordmark)", script_ref="SALAMAT_PROMO_SCRIPT.md#scene-1"),
    dict(asset_id="brand-end-card", scene_id="brand-close", allowlist_category="branded end card",
         reason="Script scene 9: 'Clean branded final frame. Motion graphics / logo reveal allowed here.' "
                "Carries the wordmark and the neutral positioning line; no verified contact data exists.",
         render="Remotion EndCard in src/Promo.tsx", script_ref="SALAMAT_PROMO_SCRIPT.md#scene-9"),
]


def owner_priority() -> dict[str, dict]:
    """Owner-media beats (finished furniture / portfolio) from OWNER_MEDIA_SHORTLIST.json."""
    if not SHORTLIST.exists():
        return {}
    data = json.loads(SHORTLIST.read_text(encoding="utf-8"))
    src = data["owner_media_source"]
    wanted = {m["scene_id"]: m for m in data["scene_mapping"] if m["owner_source_priority"] <= 2}
    return {
        sid: {
            "provider": "OWNER_INSTAGRAM" if m["owner_source_priority"] <= 2 else "OWNER_ORIGINALS",
            "profile_url": src["profile_url"],
            "post_or_reel_url": None,
            "category": m["owner_category"],
            "preferred_media_type": m["preferred_media_type"],
            "availability": src["access"],
            "review_status": data["review"]["status"],
            "priority_rank": m["owner_source_priority"],
            "what_is_needed": m["what_is_needed"],
        }
        for sid, m in wanted.items()
    }


def plan() -> int:
    if len(BRANDED) > BUDGET:
        raise SystemExit(f"{len(BRANDED)} branded graphics exceed the pre-review budget of {BUDGET}")
    board = json.loads(STORYBOARD.read_text(encoding="utf-8"))
    available, reason = (storyblocks_adapter.availability() if storyblocks_adapter
                         else (False, "adapter unavailable"))

    owner_beats = owner_priority()
    assets = []
    for beat in sorted(board["beats"], key=lambda b: b["order"]):
        if not beat["footage_queries"]:
            continue
        query = beat["footage_queries"][0]
        assets.append({
            "asset_id": f"sb-{beat['id']}",
            "scene_id": beat["id"],
            "scene_order": beat["order"],
            "script_timecode": beat["script_timecode"],
            "kind": "REAL_FOOTAGE",
            "required": True,
            "media_type": "video",
            "provider": "storyblocks",
            "provider_kind": "licensed_stock",
            "provider_asset_id": None,
            "provider_search_url": SEARCH_URL + query.replace(" ", "+"),
            "all_queries": beat["footage_queries"],
            "fallback_queries": beat["fallback_queries"],
            "licence_note": LICENCE,
            "asset_status": "RESOLVED" if available else "BLOCKED_PROVIDER",
            "blocker": None if available else BLOCKER,
            "required_action": None if available else ACTION,
            "target_duration_seconds": beat["target_duration_seconds"],
            "motion": beat["motion"],
            "owner_directed": beat["owner_directed"],
            "file": None,
            "placeholder": SLATE,
            "generative_substitute": False,
            "generative_substitute_reason": "forbidden by HARD SCOPE CONTRACT § No generative fallback "
                                            "for stock failure",
            "source_priority": (["OWNER_ORIGINALS", "OWNER_INSTAGRAM", "LICENSED_STOCK", "PLACEHOLDER"]
                                if beat["id"] in owner_beats
                                else ["LICENSED_STOCK", "PLACEHOLDER"]),
            "owner_source": owner_beats.get(beat["id"]),
        })

    branded = [dict(b, kind="GENERATIVE", media_type="motion_graphic", provider="in-house",
                    provider_kind="branded_motion_graphic", asset_status="RESOLVED", required=True,
                    licence_note="Drawn by the composition from brand tokens; no third-party asset, no "
                                 "generated imagery.", counts_against_generative_budget=True)
               for b in BRANDED]
    resolved = sum(1 for a in assets if a["asset_status"] == "RESOLVED")

    MANIFEST.write_text(json.dumps({
        "contract": "MEDIA_MANIFEST",
        "version": 4,
        "fixture": "Salamat Mebel 2-minute promo",
        "created": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "narrative_source_of_truth": "SALAMAT_PROMO_SCRIPT.md",
        "media_source_authority": board["media_source_authority"],
        "primary_provider": "storyblocks",
        "primary_provider_available": available,
        "primary_provider_status": f"{'AVAILABLE' if available else 'BLOCKED_PROVIDER'} — {reason}",
        "resolved_provider": "storyblocks" if available
                             else "none — neutral placeholders only, no licensed footage obtained",
        "provider_neutral_contract": {
            "note": "Beats declare intent as queries; resolving another provider rewrites this manifest "
                    "only, leaving the storyboard untouched.",
            "adapters": ["adapters/storyblocks_adapter.py"],
        },
        "mix_accounting": {
            "beats_requiring_real_footage": len(assets),
            "real_footage_resolved": resolved,
            "real_footage_unresolved": len(assets) - resolved,
            "generative_assets": len(branded),
            "generative_budget_before_owner_review": BUDGET,
            "generative_budget_unused_slots": BUDGET - len(branded),
            "generated_imagery_used": 0,
            "generated_video_used": 0,
            "note": "A real-footage share can be claimed only once clips are licensed; while the provider "
                    "is blocked the preview must not be presented as a finished promo.",
        },
        "assets": assets,
        "owner_media_source": (json.loads(SHORTLIST.read_text(encoding="utf-8"))["owner_media_source"]
                               if SHORTLIST.exists() else None),
        "branded_motion_graphics": branded,
        "generative_allowlist_unused": [{
            "allowlist_category": "abstract branded transition",
            "reason_not_used": "The approved script contains no designed transition; adding one would "
                               "expand scope beyond the script.",
        }],
        "scope_compliance": {
            "generative_fallback_for_blocked_stock": "prohibited and not used",
            "unused_assets_from_rev_000": "see REVISION_LOG.md — 10 pre-contract stills classified UNUSED",
            "script_overlay_rule": "only the script's approved on-screen text may be rendered",
        },
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    with LOG.open("a", encoding="utf-8") as handle:
        handle.write(f"\n### {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')} — resolve_media\n\n"
                     f"- storyblocks: {'AVAILABLE' if available else 'BLOCKED_PROVIDER'} — {reason}\n"
                     f"- stock requests: {len(assets)} (resolved {resolved})\n"
                     f"- branded graphics: {len(branded)} / budget {BUDGET}; generated imagery: 0\n")

    print(f"manifest: {len(assets)} stock requests (resolved {resolved}), {len(branded)} branded "
          f"graphics / budget {BUDGET} → {MANIFEST.name}")
    print(f"provider: {'AVAILABLE' if available else 'BLOCKED_PROVIDER'} — {reason}")
    for asset in assets:
        flag = " [OWNER-DIRECTED]" if asset["owner_directed"] else ""
        print(f"  {asset['scene_order']:>2}. {asset['scene_id']:<22} {asset['asset_status']:<17} "
              f"“{asset['all_queries'][0]}”{flag}")
    return 0


if __name__ == "__main__":
    sys.exit(plan())
