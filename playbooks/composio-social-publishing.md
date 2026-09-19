# Composio Social Publishing — Media Bridge Playbook

Status: ACTIVE / VERIFIED
Decision: EXTEND_EXISTING
Owner: Murat Project Engineer
Verified: 2026-09-19

## Purpose

Provide a repeatable route for publishing image/video content from ChatGPT-managed files to social platforms through Composio when the destination tool cannot consume a local `/mnt/data` path directly.

This playbook avoids creating parallel storage infrastructure when Composio's own temporary object storage is sufficient.

## Verified route

```text
ChatGPT Library / local working file
  -> send as temporary Gmail attachment
  -> Gmail account connected inside Composio
  -> GMAIL_FETCH_EMAILS (exact unique subject)
  -> GMAIL_GET_ATTACHMENT
  -> Composio temporary signed R2 URL
  -> Instagram media container
  -> Instagram publish
  -> post-publish verification
```

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

Do **not** create a dedicated Cloudflare R2 bucket/Worker only for this bridge while the Composio Gmail attachment route remains reliable.

Reason:

- Composio already stages the attachment in temporary R2 storage;
- the URL is short-lived;
- no new lifecycle, auth, cleanup, billing, or security surface is introduced;
- duplicating storage would violate the MPE default-over-invention rule without measurable benefit.

Escalate to a dedicated Cloudflare media bridge only if evidence shows recurring friction such as:

- Gmail attachment limits blocking required content;
- repeated account-routing failures;
- unacceptable latency;
- bulk publishing throughput needs;
- need for deterministic automatic expiry/cleanup across many files;
- another destination cannot consume the Composio temporary URL.

Such an escalation requires a new MPE filter decision before implementation.

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
