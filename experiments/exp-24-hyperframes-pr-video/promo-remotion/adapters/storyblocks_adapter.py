#!/usr/bin/env python3
"""EXP-24 Phase 2 — Storyblocks adapter (thin, optional).

Only two jobs: say whether a licensed provider is usable here, and search it.
The pipeline never imports this at render time, so an unavailable provider degrades
into a recorded blocker instead of a broken build.

MUST NEVER: drive image/video generation as a substitute for footage.

Environment (credentials are never committed):
  STORYBLOCKS_PUBLIC_KEY / STORYBLOCKS_PRIVATE_KEY   API key pair
  STORYBLOCKS_API_BASE                                optional, default api/v2
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

API_BASE = os.environ.get("STORYBLOCKS_API_BASE", "https://api.storyblocks.com/api/v2")
PUBLIC_KEY = os.environ.get("STORYBLOCKS_PUBLIC_KEY")
PRIVATE_KEY = os.environ.get("STORYBLOCKS_PRIVATE_KEY")


class ProviderUnavailable(RuntimeError):
    pass


def availability() -> tuple[bool, str]:
    """(usable, exact reason). A blocked provider is a recorded outcome, not an error."""
    if not PUBLIC_KEY or not PRIVATE_KEY:
        return False, ("no STORYBLOCKS_PUBLIC_KEY / STORYBLOCKS_PRIVATE_KEY in the environment "
                       "(credentials were not supplied to this execution environment)")
    try:
        urllib.request.urlopen(API_BASE, timeout=8)
        return True, "reachable"
    except urllib.error.HTTPError as exc:
        return True, f"reachable (HTTP {exc.code} on an unauthenticated probe)"
    except Exception as exc:  # noqa: BLE001 - report the real network state
        return False, f"provider host not reachable from this sandbox: {exc}"


def search(keywords: str, limit: int = 5) -> list[dict]:
    usable, reason = availability()
    if not usable:
        raise ProviderUnavailable(reason)
    params = {"APIKEY": PUBLIC_KEY or "", "EXPIRES": str(int(time.time()) + 300),
              "keywords": keywords, "content_type": "video", "results_per_page": str(limit)}
    ordered = "&".join(f"{k}={v}" for k, v in sorted(params.items()))
    signature = hmac.new((PRIVATE_KEY or "").encode(), ordered.encode(), hashlib.sha256).hexdigest()
    url = f"{API_BASE}/stock/videos/search?{ordered}&{urllib.parse.urlencode({'Signature': signature})}"
    with urllib.request.urlopen(url, timeout=20) as response:
        return json.loads(response.read().decode("utf-8")).get("results", [])


if __name__ == "__main__":
    usable, reason = availability()
    print(f"storyblocks: {'AVAILABLE' if usable else 'UNAVAILABLE'} — {reason}")
    if len(sys.argv) > 2 and sys.argv[1] == "--search" and usable:
        for hit in search(sys.argv[2]):
            print(json.dumps({k: hit.get(k) for k in ("id", "title", "duration")}, ensure_ascii=False))
    sys.exit(0 if usable else 3)
