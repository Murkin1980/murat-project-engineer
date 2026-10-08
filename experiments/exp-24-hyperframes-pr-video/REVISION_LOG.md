# REVISION_LOG — Salamat Mebel promo (EXP-24 Phase 2)

Owner-directed revisions and scope corrections, in order. Every entry records the
request, the interpreted change set, what changed, what was intentionally
preserved, and the resulting artifact.

---

## REV-000 — Scope correction: generated stills produced before HARD SCOPE CONTRACT

**Type:** scope correction (owner-added hard contract, 2026-10-08)
**Trigger:** `SALAMAT_PROMO_ARENA_TASK.md` § HARD SCOPE CONTRACT — "Media-source authority",
"Generative media — explicit allowlist only", "No generative fallback for stock failure",
"Maximum generative budget before owner review".
**Detected:** 2026-10-08, during CP-07 (before any preview was assembled or rendered).

### Deviation

Before the hard contract existed on the branch, the media-fallback path generated **10 still
stills** to stand in for Storyblocks footage (`tools/media_assets.py`, provider
`arena-generate-image`). This violates the contract in three ways:

1. it converts blocked stock scenes into generated images (§ No generative fallback for stock failure);
2. 9 of the 10 assets are in **explicitly disallowed categories** (kitchens, interiors, CNC,
   production/workshop, workers/assembly, client consultation, hardware/details, hands on
   materials, measuring);
3. it exceeds the pre-review budget of **3 generated visual assets**.

### Action taken (minimal-diff correction, no restart)

- The generation batch was stopped. No further image or video generation is performed.
- All 10 assets are classified **UNUSED** — none is compliant with the allowlist, so none is preserved
  in the composition, the manifests or the repository working tree.
- Assets were moved out of the tracked tree to
  `.artifacts/exp-24-salamat-promo/unused-generative/` (git-ignored), each with a recorded SHA-256 so
  the deviation stays auditable without shipping non-compliant media:

| # | Asset | SHA-256 (first 16) | Classification | Disallowed category |
| --- | --- | --- | --- | --- |
| 1 | `01-hook-kitchen.png` | `804314954ef40e57` | UNUSED | kitchens / interiors |
| 2 | `02-hook-wide-interior.png` | `d3db5ba76fed9e0a` | UNUSED | interiors |
| 3 | `03-process-measure.png` | `68b3965d764eb9e8` | UNUSED | hands touching furniture/materials (measurement) |
| 4 | `04-measure-consult.png` | `43a3a007c98e967a` | UNUSED | client consultation |
| 5 | `05-materials-samples.png` | `00cb8a9cbf30c4f8` | UNUSED | hardware/detail + hands on materials |
| 6 | `06-craft-panels.png` | `ca956c5bd93a75ee` | UNUSED | furniture production |
| 7 | `07-craft-cnc.png` | `c318b5feeab604e2` | UNUSED | CNC/cutting |
| 8 | `08-craft-edge.png` | `f34f7a01bf9cf1fb` | UNUSED | edgebanding/detail footage |
| 9 | `09-craft-hardware.png` | `64130458c0509566` | UNUSED | hardware/detail footage |
| 10 | `10-craft-assembly.png` | `c11f83c2e91477e6` | UNUSED | workers / assembly |

- `public/assets/img/` (the 1080p JPEG masters derived from those stills) was deleted from the tracked tree.
- No asset was silently normalised: the deviation is recorded here and in `SALAMAT_PROMO_RESULTS.md`.

### Corrected media policy now in force

| Priority | Source | Status in this environment |
| --- | --- | --- |
| 1 | REAL LICENSED VIDEO — **Storyblocks first** | `BLOCKED_PROVIDER` (no credentials, provider host unreachable) — queries + search URLs recorded per scene |
| 2 | other explicitly approved licensed real footage | not available |
| 3 | existing owner/project media | none supplied for this fixture |
| 4 | bounded neutral placeholder, **for pipeline testing only** | in use: per-scene "search slate" cards rendered by Remotion (no imagery, no fake footage) |
| 5 | generative media (allowlist only) | used for **3** branded motion graphics, all in-house Remotion code |

### Generative budget accounting (before owner review)

| Generative asset | Allowlist category | Reason | Kind |
| --- | --- | --- | --- |
| `brand-logo-reveal` | logo reveal | brand opening beat of block A; cannot be stock footage | in-house Remotion motion graphic |
| `brand-transition` | abstract branded transition | single brand wipe between block C and block D; serves as the film's one designed transition | in-house Remotion motion graphic |
| `brand-end-card` | branded end card | closing CTA frame required by block F | in-house Remotion motion graphic |

**Generated imagery count: 0 / 3 budget used. Generated video count: 0.**
No asset #4 will be created without explicit owner authorization.

### Preserved compliant work

- CP-06 storyboard structure, claims policy, block structure, per-scene Storyblocks queries and
  fallback queries, source grounding.
- Contract validator, timeline builder, media/provider adapter scaffolding, Remotion project.
- All of it is provider-neutral: resolving Storyblocks later changes the media manifest only.

### Resume point

Earliest incomplete mandatory checkpoint = **CP-07 (media manifest)**, then CP-08. No later checkpoint
was executed; no preview/render artifact was produced before the manifest existed.
