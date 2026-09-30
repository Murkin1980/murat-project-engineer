# EXP-18 — Pirate Face model resilience: findings

Contract: [`README.md`](./README.md) (mirrored from PR #31, unchanged).
Method and honesty rules: [`METHOD.md`](./METHOD.md).
Raw evidence: [`evidence/`](./evidence/) — authoritative run **36672975009**
(commit `e408717`, branch `arena/01a0f09e-murat-project-engineer`).

Verdict: **PASS**, with one recorded deviation (a git plumbing file that is not
part of the model artifact is absent from the torrent) and one environment
limitation (the authoring sandbox cannot reach either distribution path, so the
bounded test ran on an ephemeral GitHub-hosted runner).

---

## Step 1 — Model selected (recorded before retrieval)

| Field | Value |
| --- | --- |
| Model | `sentence-transformers/all-MiniLM-L6-v2` |
| Hugging Face repository | https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2 |
| Pinned revision | `1110a243fdf4706b3f48f1d95db1a4f5529b4d41` (recorded by the HF API as the repository `sha`, then re-fetched by revision) |
| License | `apache-2.0` — `cardData.license = apache-2.0` and tag `license:apache-2.0` (`04_hf_license_evidence.json`); not gated, not private |
| Size | 30 files, 976,948,716 bytes across formats; `model.safetensors` = 90,868,376 bytes (22,713,728 parameters) |
| Why this model | public, clearly permissive, small, exactly pinnable, and listed on Pirate Face with published checksums |

Selection happened before any retrieval and is recorded in the run transcript
(`00_run_transcript.log`, stage A).

## Step 2 — Canonical artifact over the normal Hugging Face path

The harness downloaded every path in the revision file list with
`curl https://huggingface.co/<repo>/resolve/<revision>/<path>` and hashed the
bytes it received (`06_canonical_manifest.json`).

| Field | Value |
| --- | --- |
| Repository | `sentence-transformers/all-MiniLM-L6-v2` |
| Revision | `1110a243fdf4706b3f48f1d95db1a4f5529b4d41` |
| Files | 30 (path, size, SHA-256 each) |
| Total bytes | 976,948,716 |
| Download wall time | 14 s (stage B) |
| Primary artifact | `model.safetensors`, 90,868,376 bytes |
| **HF_SHA256 (primary artifact, computed)** | `53aa51172d142c89d9012cce15ae4d6cc0ca6895895114379cacb4fab128d9db` |

Independent corroboration of the canonical values (`06b_hash_crosscheck.json`):

- Hugging Face's own recorded LFS `sha256` (`lfs.oid` in the tree API) for all
  15 LFS files matched the hashes computed from the downloaded bytes
  (`computed_manifest_matches_hf_recorded_lfs = true`, 0 mismatches).
- The same value `53aa5117…` is the LFS object id Hugging Face publishes for
  `model.safetensors` at this revision.

## Step 3 — Pirate Face distribution reference (what was actually observed)

From `https://pirateface.co/sentence-transformers/all-MiniLM-L6-v2`
(`07_pirateface_page.html`, fetched during the run):

| Observed on the page | Value |
| --- | --- |
| Listing | `sentence-transformers/all-MiniLM-L6-v2` |
| License shown | `apache-2.0` |
| Source revision shown | `1110a243fdf4706b3f48f1d95db1a4f5529b4d41` (same commit as pinned) |
| Magnet | `magnet:?xt=urn:btih:fed3a1e271827a2094b93ecbe738dbf3bd58c5cf&tr=udp%3A%2F%2Ftracker.pirateface.co%3A6969%2Fannounce&tr=http%3A%2F%2Ftracker.pirateface.co%3A6969%2Fannounce` |
| Info hash | `fed3a1e271827a2094b93ecbe738dbf3bd58c5cf` |
| Web seed in the advertised magnet | **none** (`magnet_has_web_seed_parameter = false`) |
| Checksum claim | "15 checksums" badge; 13 distinct SHA-256 values appear on the page |
| Swarm label | seeders shown by the site (count changes between page renders) |

Before retrieval the harness announced the info hash to the advertised tracker
(`07b_tracker_announce_before.json`): the tracker answered `ok` with
**18 seeders, 0 leechers, 18 peer entries**, observed at 05:21:xx UTC. This is
what the tracker *reported*; it is not by itself proof of retrievability — the
proof is the completed retrieval in step 4.

The captured `.torrent` metainfo (`14_torrent_identity.json`) shows:
29 payload files, 976,947,487 bytes, 1,864 pieces of 524,288 bytes, no `url-list`
web seed, `announce-list` = the two `tracker.pirateface.co:6969` URLs.

## Step 4 — Retrieval through Pirate Face

The harness ran the advertised magnet **unmodified** with aria2 1.37.0
(DHT + PEX + tracker). Download wall times are taken from the client log
(`07_D_pf_normal_aria2c.log`); the "stage wall" also includes a ~20 s idle
detection before the sampler stops the client.

| Stage | What was allowed | Result | Payload complete | Wall (payload) | Max speed seen |
| --- | --- | --- | --- | --- | --- |
| D — advertised magnet | everything | retrieving via the Pirate Face magnet succeeded | yes (29/29 files, 0 zero-byte) | 41 s stage / ~16 s transfer | 105.8 MB/s, 9 seeders, 24 connections |
| E — primary source lost | HF zone + Pirate Face web blocked, web seed absent | succeeded from the swarm + Pirate Face tracker | yes | 36 s stage / ~10 s transfer | 146.1 MB/s, 9 seeders, 39 connections |
| E2 — tracker lost too | HF + Pirate Face web + Pirate Face tracker blocked, DHT/PEX only | succeeded | yes | 96 s stage / ~69 s transfer | 38.8 MB/s, 8 seeders, 25 connections |

Client-recorded completion for each stage
(`07_<stage>_client_status.txt`): `aria2c_exit_code=0`,
`client_reported_payload_download_complete=yes`, no `INPR` result lines, and the
RPC sampler's last byte counter equal to the torrent's payload length. aria2's
own piece verification on the retrieved data finished successfully
(`12_piece_reverify.log`).

Missing / additional files: the torrent contains **29** of the 30 files in the
pinned revision. The only missing path is **`.gitattributes`** (1,229 bytes, a
Git attribute file); the arithmetic is exact — 976,947,487 (torrent payload) =
976,948,716 (HF revision) − 1,229. No extra payload files were produced; the
only extra entries in the download directories are the client's own `.torrent`
metainfo files, which are excluded from the payload comparison.

## Step 5 — Integrity comparison (deterministic)

Rules fixed before the run: strip the BitTorrent payload directory, exclude
`.torrent` metainfo, then require exact path-set equality and exact SHA-256
equality per file (`compare.py`, `13_comparison.json`,
`13b_dht_only_comparison.json`).

| Comparison | Files compared | SHA-256 identical | SHA-256 mismatched | Missing | Primary artifact hash |
| --- | --- | --- | --- | --- | --- |
| D (advertised magnet) vs canonical | 29 | 29 | 0 | `.gitattributes` | `53aa5117…` = canonical |
| E (swarm only, HF lost) vs canonical | 29 | 29 | 0 | `.gitattributes` | `53aa5117…` = canonical |
| E2 (DHT only) vs canonical | 29 | 29 | 0 | `.gitattributes` | `53aa5117…` = canonical |

- Every model file — weights (`model.safetensors`, `pytorch_model.bin`,
  `tf_model.h5`, `rust_model.ot`), ONNX and OpenVINO exports, tokenizer,
  configs, `README.md`, training script — is byte-identical to the canonical
  artifact.
- `file_set_identical` is **false** only because of the absent
  `.gitattributes`. That is reported as a deviation, not smoothed over.
- The retrieved bytes also match the checksums **Pirate Face itself publishes**:
  13 of 13 SHA-256 values printed on the listing page are present in the
  canonical manifest, including the weight file `53aa5117…`
  (`06b_hash_crosscheck.json`).
- Two independent retrievals in the same session (runs 36670736828 and
  36672975009) produced identical hashes; the metainfo identity check confirms
  the same info hash, piece table and file list in every stage
  (`same_piece_table_and_file_list_across_stages = true`).

## Step 6 — Bounded simulation of primary-source unavailability

Applied to the test host only (`/etc/hosts`), inside the same ephemeral runner:

- `huggingface.co`, `www.huggingface.co`, `cdn-lfs.huggingface.co`,
  `cdn-lfs-us-1.huggingface.co`, `cas-bridge.xethub.hf.co`, `hf.co`,
  `pirateface.co`, `www.pirateface.co` → `0.0.0.0`.
- Proof captured at run time (`09_source_loss_proof.txt`): HF API unreachable,
  Pirate Face web layer unreachable; the tracker's name resolution still worked.
- The torrent advertises **no web seed**, so there was no hidden HTTP fallback to
  Hugging Face or to Pirate Face's servers (also confirmed by
  `webseed_mentions_in_client_log=0`).

Outcome: the same pinned artifact was recovered from the swarm in stage E
(36 s) and again with the Pirate Face tracker blocked in stage E2 (96 s, DHT/PEX
only). Recovery does not depend on Pirate Face's web front end; it does depend on
peers still holding the data.

## Step 7 — Operational assessment

| Question | Observation |
| --- | --- |
| Retrieval reliability | 3/3 retrievals in the authoritative run completed and verified; a second full run reproduced the same hashes. A third run (36672153216) failed because of a **harness** defect, not the source — recorded in `evidence/run-36672153216/`. Overall: 3 good runs of 4 attempts, all failures attributable to the test rig. |
| Integrity verifiability | Strong: per-file SHA-256 against a pre-recorded canonical manifest, cross-checked against Hugging Face's recorded LFS object ids, against the checksums Pirate Face publishes, and independently by aria2's piece-table verification. |
| Dependence on external assumptions | The magnet/info hash must be recorded **before** an outage (Pirate Face's index itself reads from Hugging Face records). Availability then depends on third-party seeders; the tracker helps discovery but is not required (DHT-only worked). BitTorrent client + DHT-capable networking required on the recovering host. |
| Practical burden | Low for the tested model: ~20 s to fetch and verify ~976 MB in stage D, ~10 s in stage E, ~69 s DHT-only. The procedure is a magnet plus a checksum manifest — no service, no account, no registry. |
| Ongoing seeding required? | Not for this model: 18 seeders were reported by the tracker and 8–9 were actually used. If a project pins a model with no seeders, the fallback is worthless — this is a property of the swarm, not of the method, and was **not** tested for a low-demand model. |
| Meaningful resilience? | Yes, for popular permissively licensed models: the exact pinned bytes survived with Hugging Face, Pirate Face's web layer, and (in stage E2) the Pirate Face tracker all unreachable. It is an optional last-resort path, not a replacement for Hugging Face. |
| New infrastructure / dependencies | None added to the product. The experiment added only files under this experiment directory, plus a temporary CI workflow that is deleted in the same change set; installing aria2 on the ephemeral runner is test tooling, not a repository dependency. |

---

## OBSERVED

- Pinned revision, license and the 30-file Hugging Face artifact with per-file
  SHA-256 (`06_canonical_manifest.json`), matching Hugging Face's recorded LFS
  object ids for all 15 LFS files.
- Pirate Face listing, magnet, info hash `fed3a1e271827a2094b93ecbe738dbf3bd58c5cf`,
  absence of a web seed, and 13 checksum values that match the canonical bytes.
- Tracker answer before retrieval: 18 seeders.
- Three retrievals in run 36672975009, and three in run 36670736828, all
  producing 29/29 byte-identical files including `model.safetensors`
  `53aa51172d142c89d9012cce15ae4d6cc0ca6895895114379cacb4fab128d9db`.
- Swap-free reproduction with Hugging Face + Pirate Face web blocked, and again
  with the tracker blocked (DHT only).
- One failed attempt (run 36672153216) with truncated payloads, caused by the
  harness shutting aria2c down mid-transfer; the client log shows
  `281MiB/0.9GiB(30%)`, `not complete`, `INPR`.
- The torrent omits `.gitattributes`.

## INFERRED

- Pirate Face's torrents are generated from Hugging Face revisions and therefore
  cannot cover a model that Hugging Face never published, and listings can only
  exist while the source revision is resolvable.
- Because the retrieval worked with the tracker blocked, resilience for this
  model rests on the BitTorrent swarm (peers holding the data) rather than on
  Pirate Face's infrastructure.

## UNKNOWN

- Whether seeders will still exist months from now, or for a low-demand model —
  not tested; the observed "Needs a seeder" state of other Pirate Face listings
  suggests it will often not.
- Whether Pirate Face's operator could or would withdraw a listing/torrent.
- Whether the index continues to work if Hugging Face itself becomes
  permanently unavailable (the site states it records source revisions; that
  was not tested in an outage of this kind).
- Publisher identity: the page showed an unverified handle (`@sentence-transformers
  is reserved`), so the torrent's provenance was established only through the
  checksums, not through a verified account.

---

## Contract PASS criteria

| Criterion | Result |
| --- | --- |
| Same pinned model artifact retrieved through Pirate Face | Met — all 29 payload files, including the 90.9 MB weight file, byte-identical; the repository's `.gitattributes` is absent (deviation, recorded) |
| Integrity verified against recorded checksums | Met — per-file SHA-256 vs canonical manifest, HF LFS ids, Pirate Face page checksums, aria2 piece verification |
| Practical recovery path when the primary source is unavailable | Met — stage E (HF lost) and stage E2 (HF + Pirate Face web + tracker lost) both recovered the pinned artifact |
| No production architecture change or parallel registry | Met — experiment files only; temporary CI harness deleted; no product code, dependency, or routing touched |
| Operational burden low enough to keep as an optional resilience tool | Met with the seeder caveat above: a recorded magnet + checksum manifest, minutes of runtime, no infrastructure |

Deviations and limitations are stated above rather than folded into the verdict.

## Evidence index

| Run | Commit | Result |
| --- | --- | --- |
| [36670736828](https://github.com/Murkin1980/murat-project-engineer/actions/runs/36670736828) | `bef8985` | valid; retrievals complete and hash-identical; stages stopped by the harness budget |
| [36672153216](https://github.com/Murkin1980/murat-project-engineer/actions/runs/36672153216) | `5dcfacc` | **invalid**; harness aborted the transfer (kept as a defect record) |
| [36672975009](https://github.com/Murkin1980/murat-project-engineer/actions/runs/36672975009) | `e408717` | valid and authoritative; all stages exited cleanly |

Flat files in `evidence/` are from run 36672975009; earlier runs are preserved in
`evidence/run-36670736828/` and `evidence/run-36672153216/`.

## Next step (for the MPE decision, not taken here)

Keep Pirate Face as an optional, documented fallback for already-pinned
permissively licensed models: when a model is pinned, also record its magnet and
the canonical SHA-256 manifest with the pin, and verify hashes after any fallback
retrieval. Do not integrate it into production routing, do not build a registry,
and do not rely on it for low-demand models without first confirming seeders.

Registration status: the canonical entry lives in
`experiments/EXPERIMENT_REGISTRY.json` (`EXP-18` = PASS) and was merged with this
evidence. The registration-only PR #31 could not be merged — its branch predated
later registry entries and reformatted the registry file — so the registration
fields were carried over verbatim in a minimal reconciliation commit on the
execution branch, and PR #31 was closed as superseded after its contract README
was confirmed byte-identical on `main` (SHA-256
`89be8f273aa3c9ff690ee07b064c63696b9cdb890c18b3a2ee816a75241a3429`).
