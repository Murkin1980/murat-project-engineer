#!/usr/bin/env python3
"""EXP-24 Phase 2 — Storyblocks adapter (licensed stock, preferred provider).

Narrow adapter, no framework:

  1. `availability()` — is a licensed-stock provider usable in this environment?
  2. `search(query)`   — resolve a storyboard footage query to candidate clips.
  3. `deliver(entry)`  — download a licensed clip for the manifest entry.

Nothing in the pipeline imports this module at render time: the storyboard stays
provider-neutral and `MEDIA_MANIFEST.json` records what was actually used, so an
unavailable provider degrades to a recorded blocker instead of a broken build.

Credentials are read from the environment only:

  STORYBLOCKS_PUBLIC_KEY  / STORYBLOCKS_PRIVATE_KEY   (API key pair)
  STORYBLOCKS_API_BASE    (optional override, default https://api.storyblocks.com/api/v2)

If credentials are absent, `main --check` prints the exact blocker and exits 3,
which is the documented, non-fatal path for this experiment.
"""

from __future__ import annotations

import hashlib
import hmac
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

API_BASE = os.environ.get("STORYBLOCKS_API_BASE", "https://api.storyblocks.com/api/v2")
PUBLIC_KEY = os.environ.get("STORYBLOCKS_PUBLIC_KEY")
PRIVATE_KEY = os.environ.get("STORYBLOCKS_PRIVATE_KEY")
TIMEOUT = 20


class ProviderUnavailable(RuntimeError):
    """Raised when the licensed-stock provider cannot be used in this environment."""


def availability() -> tuple[bool, str]:
    if not PUBLIC_KEY or not PRIVATE_KEY:
        return False, ("no STORYBLOCKS_PUBLIC_KEY / STORYBLOCKS_PRIVATE_KEY in the environment "
                       "(credentials were not supplied to this execution environment)")
    try:
        urllib.request.urlopen(API_BASE, timeout=8)
        return True, "reachable"
    except urllib.error.HTTPError as exc:  # host answered — reachable with auth
        return True, f"reachable (HTTP {exc.code} on unauthenticated probe)"
    except Exception as exc:  # noqa: BLE001 - report the real network state verbatim
        return False, f"provider host not reachable from this sandbox: {exc}"


def _signed_query(params: dict[str, str]) -> str:
    """Storyblocks-style signed query: sorted params + HMAC-SHA256 of the query string."""
    params = dict(params)
    params["APIKEY"] = PUBLIC_KEY or ""
    params["EXPIRES"] = str(int(time.time()) + 300)
    ordered = "&".join(f"{k}={v}" for k, v in sorted(params.items()))
    signature = hmac.new((PRIVATE_KEY or "").encode(), ordered.encode(), hashlib.sha256).hexdigest()
    return ordered + "&" + urllib.parse.urlencode({"Signature": signature})


def search(query: str, *, media_type: str = "video", limit: int = 5) -> list[dict]:
    ok, reason = availability()
    if not ok:
        raise ProviderUnavailable(reason)
    params = {
        "keywords": query,
        "content_type": media_type,
        "results_per_page": str(limit),
        "sort_by": "relevance",
    }
    url = f"{API_BASE}/stock/{'videos' if media_type == 'video' else 'images'}/search?{_signed_query(params)}"
    with urllib.request.urlopen(url, timeout=TIMEOUT) as response:
        payload = json.loads(response.read().decode("utf-8"))
    return payload.get("results", [])


def deliver(entry: dict, target_dir: Path) -> Path:
    """Download the licensed asset for one manifest entry."""
    if not entry.get("provider_asset_id"):
        raise ProviderUnavailable(
            f"scene {entry['scene_id']} has no selected provider asset id — run `search` first "
            f"and record the chosen id in the manifest"
        )
    ok, reason = availability()
    if not ok:
        raise ProviderUnavailable(reason)
    url = entry.get("provider_download_url")
    if not url:
        raise ProviderUnavailable(f"scene {entry['scene_id']}: no provider_download_url recorded")
    target_dir.mkdir(parents=True, exist_ok=True)
    target = target_dir / f"{entry['asset_id']}.mp4"
    with urllib.request.urlopen(url, timeout=120) as response, open(target, "wb") as handle:
        handle.write(response.read())
    return target


def main(argv: list[str]) -> int:
    ok, reason = availability()
    if len(argv) > 1 and argv[1] == "--check":
        print(f"storyblocks: {'AVAILABLE' if ok else 'UNAVAILABLE'} — {reason}")
        return 0 if ok else 3
    if len(argv) > 2 and argv[1] == "--search":
        if not ok:
            print(f"storyblocks: UNAVAILABLE — {reason}", file=sys.stderr)
            return 3
        for hit in search(argv[2]):
            print(json.dumps({k: hit.get(k) for k in ("id", "title", "duration", "thumbnail_url")},
                             ensure_ascii=False))
        return 0
    print(__doc__)
    print(f"status: {'AVAILABLE' if ok else 'UNAVAILABLE'} — {reason}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
