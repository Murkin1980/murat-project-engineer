---
playbook_id: composio-social-publishing
version: 1.0.0
supported_task_classes: [social-media-publishing, media-transfer]
risk_tier: VERIFIED
roles: [researcher, coder, reviewer]
sequence: [classify, prepare-media, publish, verify, report]
required_inputs: [source_media, destination_account, publication_request]
deterministic_gates: [artifact_exists, secrets_scan, acceptance_tests]
optional_semantic_review: true
human_gate_conditions: [irreversible_external_effect, destination_account_change]
max_rework_cycles: 1
terminal_states: [PASS, BLOCKED, HUMAN_REQUIRED, REWORK]
run_report_fields: contracts/RUN_REPORT.md
---

# Composio Social Publishing — Media Bridge Playbook

Status: ACTIVE / VERIFIED
Decision: EXTEND_EXISTING
Owner: Murat Project Engineer
Verified: 2026-09-19

## Purpose

Provide a repeatable route for publishing image/video content from ChatGPT-managed files to social platforms through Composio when the destination tool cannot consume a local `/mnt/data` path directly.

This playbook avoids creating parallel storage infrastructure when Composio's own temporary object storage is sufficient.

## Preferred route

```text
ChatGPT Library / local working file
  -> Cloudflare R2 bucket: salamat-temp-media
  -> temporary/publicly fetchable URL for the destination platform
  -> Instagram media container
  -> Instagram publish
  -> post-publish verification
  -> automatic R2 deletion after 7 days
```

Cloudflare R2 lifecycle is configured for all objects with an age of 604800 seconds (7 days).

## Verified fallback route

If direct transfer into R2 is unavailable in the current execution environment:

```text
ChatGPT Library / local working file
  -> temporary Gmail attachment
  -> Gmail account connected inside Composio
  -> GMAIL_FETCH_EMAILS (exact unique subject)
  -> GMAIL_GET_ATTACHMENT
  -> Composio temporary signed R2 URL
  -> Instagram media container
  -> Instagram publish
  -> post-publish verification
```

The Gmail bridge is fallback only, not the preferred user-visible workflow.

## Preconditions

- Destination social account is connected and ACTIVE in Composio.
- A Gmail account is connected and ACTIVE inside Composio.
- Source media exists in ChatGPT Library or the current runtime.
- Media is compatible with the destination platform.

Do not assume the Gmail account connected to ChatGPT is the same account connected inside Composio. Check the Composio connection first.

## Instagram Reel procedure

1. Resolve or materialize the source MP4 locally.
2. Prepare a platform-compatible MP4 only if needed. Preserve the original.
3. Send the prepared MP4 as a temporary Gmail attachment to the Gmail account that is connected inside Composio.
4. Use a unique exact subject so the bridge message can be found deterministically.
5. In Composio:
   - call `GMAIL_FETCH_EMAILS` using the exact subject and `has:attachment`;
   - obtain the real Gmail `messageId` and `attachmentId`;
   - call `GMAIL_GET_ATTACHMENT`.
6. Read the returned temporary signed object URL from the attachment result.
7. Create the Instagram Reel container with:
   - `video_url` = the temporary signed URL;
   - `media_type=REELS`;
   - `share_to_feed=true` when feed visibility is intended;
   - the final approved caption.
8. Publish with `INSTAGRAM_POST_IG_USER_MEDIA_PUBLISH`.
   - Use a non-zero wait.
   - For video, allow enough processing time rather than attempting immediate publish.
9. Verify with `INSTAGRAM_GET_IG_MEDIA`.
   - Confirm media ID.
   - Confirm permalink.
   - Confirm caption.
   - Confirm Reel/media product type.
   - Confirm feed-sharing state when applicable.
10. Treat verification as part of completion, not an optional extra.

## Critical pitfalls

### 1. Local path is not a Composio file key

Do not pass a local path such as:

```text
/mnt/data/video.mp4
```

as `video_file.s3key`.

A local runtime path is not a Composio-managed object key and returns a storage 404.

### 2. Use the temporary URL returned by Composio

The verified bridge output is a temporary signed R2 URL returned by `GMAIL_GET_ATTACHMENT`.

Pass that URL through `video_url` to the Instagram media-container action.

Do not persist or commit signed URLs. They are short-lived transport artifacts.

### 3. Hashtags must be verified after publishing

Despite tool-schema wording suggesting URL-encoding, a real publication on 2026-09-19 showed that passing `%23` produced literal `%23` in the Instagram caption.

Therefore:

- pass normal literal `#` characters in the caption;
- immediately read back the published media and inspect the caption;
- treat visible encoding artifacts as a failed verification.

### 4. Account mismatch

If the bridge message was sent to a different Gmail account than the one connected inside Composio, do not reconnect everything. Forward/send the temporary attachment to the already-active Composio Gmail account and continue.

### 5. Containers are not published media IDs

Keep these identifiers separate:

- creation/container ID;
- published media ID.

Use the creation ID only for publish.
Use the published media ID for verification/insights/permalink reads.

## Storage policy

Primary temporary media storage is the existing Cloudflare R2 bucket:

- bucket: `salamat-temp-media`
- storage class: `Standard`
- lifecycle rule: `delete-after-7-days`
- scope: all objects (empty prefix)
- expiration age: `604800` seconds / 7 days
- purpose: transient media transport for social publishing and similar connector workflows

The bucket is infrastructure reuse, not a new product or repository.

Rules:

- Do not store permanent business archives here.
- Do not store credentials or secrets in object names or metadata.
- Prefer short-lived access URLs when exposing media to third-party publishing APIs.
- Let lifecycle cleanup handle abandoned media automatically.
- Gmail attachment bridging remains fallback only when direct R2 transfer is unavailable.
- Preserve the original source file in its normal source-of-truth location when needed.

## Verified Relief Unit

```text
Name: Composio Social Media File Bridge
Status: VERIFIED
Work Atom before:
- manually search for a way to expose local media to the publishing connector
- retry incompatible local-path/file-key approaches
- reconnect unrelated storage systems

Relief:
- deterministic reusable transport path from ChatGPT file to Composio temporary object URL

Unlock Value:
- enables direct social publishing from prepared ChatGPT media

Reuse Multiplier:
- potentially reusable for other Composio tools that accept a public URL or FileUploadable object
```

## Evidence

Verified on a real Instagram Reel publication for Salamat Mebel on 2026-09-19.

Verification criteria achieved:

- media container created;
- Reel published successfully;
- permalink returned;
- Reel shared to feed;
- readback exposed a caption-encoding issue, producing the permanent rule to use and verify literal hashtags.

## Completion rule

A social publish is not PASS until the published object is read back and the important user-visible fields are confirmed.
