# INSTAGRAM_MEDIA_AUDIT — Salamat Mebel promo (EXP-24)

Date: 2026-10-08
Owner-designated source: <https://www.instagram.com/salamat_mebelkz/>
Decision: **EXTEND_EXISTING** · Scope: `experiments/exp-24-hyperframes-pr-video/`

```text
ACCESS: BLOCKED_OWNER_MEDIA_ACCESS
CONTENT INSPECTED: NONE — no post, Reel, photo or caption was read
CANDIDATES FOUND: 0 (nothing was listed; no URL, caption or media id is invented anywhere in this audit)
REASON: the execution sandbox cannot reach Instagram, and Arena offers no Instagram connector
NEXT: owner uploads originals (attach to chat) or points the pipeline at a reachable copy
```

## 1. What was attempted, and what came back

| Attempt | Command / probe | Result |
| --- | --- | --- |
| Read the profile | `curl -sS https://www.instagram.com/salamat_mebelkz/` | **HTTP 000** — connection refused by sandbox egress policy |
| Alternative hosts | `www.instagram.com`, `instagram.com`, `graph.instagram.com`, `i.instagram.com` | all **HTTP 000** |
| DNS | `getent hosts www.instagram.com` | resolves (`2a03:2880:f36c:22:face:b00c:0:4420`) → the block is policy, not name resolution |
| Credentials | scan of the environment for `instagram\|meta_\|facebook` | **0 matches** — no account, token or API key exists here |
| Platform integration | Arena connector lookup for `instagram` | **unsupported** — no Instagram connector exists, so the profile cannot be read through a supported app either |
| Egress allowlist | — | this runtime may reach `github.com`, `codeload.github.com`, `api.github.com`, `registry.npmjs.org`, `pypi.org`, `files.pythonhosted.org` only |

**Nothing was bypassed.** No scraping endpoint, no private API, no session cookie, no anti-bot circumvention,
no login attempt, and no third-party downloader was used. The task forbids all of these, and the classifier
for "authorized access" here is: *public content that this runtime can actually fetch, or files the owner
supplies*.

## 2. What this audit therefore does NOT contain

This is deliberate, and it is the honest boundary of the artifact:

- no list of posts, Reels or highlight items;
- no follower/engagement or content-volume figures;
- no captions, project names or client names;
- no guessed media URLs or thumbnail links;
- no claim about image/video quality of anything on the profile.

Producing any of the above without reading the profile would be fabrication, which is worse than a recorded
blocker. `OWNER_MEDIA_SHORTLIST.json` therefore contains **requests** (what the film needs per scene) rather
than pretend candidates.

## 3. Why this is a delivery problem, not a pipeline problem

The pipeline side is ready and provider-neutral:

- `EDITORIAL_STORYBOARD.json` already declares footage intent per beat as queries;
- `MEDIA_MANIFEST.json` maps every beat to one required asset record with provider, licence note, in/out
  intent, motion, availability and review status;
- adding an owner source means setting `provider: OWNER_INSTAGRAM` + the file path on the existing records —
  no storyboard edit, no composition edit, no new infrastructure.

The only missing ingredient is the media itself. Ten beats now prefer owner material (see the shortlist);
the seven workshop/process beats stay Storyblocks-first, exactly as the task requires.

## 4. Media priority now recorded in the manifests

For finished furniture and portfolio beats:

1. owner's original photo/video files;
2. owner's Instagram Reels, videos and posts;
3. approved licensed stock footage where owner material is unavailable;
4. neutral placeholders for technical testing.

For production machinery, CNC, panel cutting and general workshop beats: **Storyblocks-first**, owner
material if it happens to cover the process well. Generative substitution stays forbidden for all of them.

## 5. How to unblock (two paths, both auditable)

| Path | What the owner does | Why it is preferred |
| --- | --- | --- |
| **A. Attach originals to this chat** | attach the files; they land in the workspace, and they are copied to `experiments/exp-24-hyperframes-pr-video/owner-media/` (git-ignored, so the repository stays free of binaries) | original bytes, no re-encoding, no new infrastructure |
| **B. GitHub release asset / repository path** | upload the media to a release asset or a folder in a repository this runtime can read | verifiable provenance, and the exact file can be re-fetched after a sandbox reset |

Drive, Dropbox, Instagram and similar links are **not** reachable from this runtime — they will be recorded
as blocked, not silently worked around.

## 6. Acceptance and rights checklist (applied when files arrive)

- provenance per file: source post/Reel URL (or "owner original, no public URL");
- category, target scene, aspect ratio, resolution, suggested in/out segment, quality assessment;
- source audio is muted in the composition; any music from a Reel must not travel into the film;
- privacy: no identifiable customers, staff faces, addresses, licence plates or client branding without consent;
- vertical (9:16) material is cropped to 16:9 — leave headroom, or supply horizontal if possible;
- no generative replacement for missing furniture/production/interior shots.

## 6a. Pilot scope (owner decision, 2026-10-08)

The owner limited the CP-07 owner-media pilot to **three real Salamat Mebel projects**. The per-scene mapping in
`OWNER_MEDIA_SHORTLIST.json` is unchanged, but the request to the owner is consolidated into three project
slots — one project can cover several scenes:

| Slot | Project type | Beats it would cover |
| --- | --- | --- |
| 1 | kitchen or kitchen-living room | open-interior, range-kitchen-storage, tactile-hero, materials-hardware |
| 2 | wardrobe / built-in storage or TV zone | range-home-rooms, open-detail, install-adjust |
| 3 | commercial / office, or a second finished interior | range-commercial, install-fitting, result-space |

Per project: one slow walkthrough (or 2–3 stills per room type) of the finished space, plus 1–2 detail/macro
moments (facade edge, handle, hinge, soft-close), optionally one installation or adjustment moment. Scenes
outside the pilot stay Storyblocks-first or on neutral placeholders.

**Current intake: 0 of 3 projects received.** No media has been attached to the conversation yet.

## 7. Status

```text
INSTAGRAM MEDIA AUDIT: BLOCKED_OWNER_MEDIA_ACCESS (0 candidates, nothing inspected)
RE-PROBE 2026-10-08: still blocked — TLS reset by egress policy on all four hosts (HTTP 000), DNS resolves
PILOT SCOPE: max 3 real Salamat Mebel projects (consolidated request, see §6a) · intake 0 of 3
DELIVERABLES: INSTAGRAM_MEDIA_AUDIT.md · OWNER_MEDIA_SHORTLIST.json · scene mapping inside both
SUBMISSION: chat attachment preferred (owner decision) — files land in the workspace, copied to owner-media/
STOP GATE: AWAITING_OWNER_MEDIA_REVIEW — no render, no CP-10…CP-12, no publishing
```
