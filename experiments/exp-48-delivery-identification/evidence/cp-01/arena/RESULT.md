# CP-01 · Arena evidence, 2026-11-21

Disposition: EXTEND_EXISTING. Result: PARTIAL, closure blocked. This observation supersedes the historical dispatch blocker in ../RECORD.md. No verdict on EXP-48 as a whole.

| Supplied document | Model | Correct fields | Arena “Thought for” | Screenshot(s) |
|---|---|---:|---:|---|
| HTML | Gemini 4 Argon High | 4/4 | 6 s | 1000839807.jpg |
| HTML | MiMo v2.6 Pro | 4/4 | 3 s | 1000839808.jpg |
| Markdown | Gemini 4 Argon High | 4/4 | 8 s | 1000839809.jpg, 1000839810.jpg |
| Markdown | MiMo v2.6 Pro | 4/4 | 1 s | 1000839809.jpg, 1000839810.jpg |

All four rendered answers match the frozen key after whitespace normalization: Salamat Mebel, Алматы, Кухни и шкафы на заказ в Алматы, 12+ лет. Score: 16/16 over four repeated facts, zero field discrepancies. Owner identifies Markdown model order; the two Markdown frames share a session, but model headers are outside the frames. Session: https://arena.ai/c/01a1fc63-9604-7778-aae0-a126973b19c7 (Markdown only). HTML frames show another, truncated session ID.

Anonymized error log: preliminary URL-only retrieval, one SOURCE_UNAVAILABLE per model (1000839806.jpg). Excluded from supplied-document scoring. No request logs or verified crawler attribution; identification error rate unknown.

Both input digests pass ../SHA256SUMS. Rebuilding with pandoc 3.1.11.1 reproduces variant.md byte-for-byte. Input bytes: 42,028 → 24,294, saving 17,734 (42.2%). No inference about tokens or network traffic. Additional cost $0 per owner (0 KZT incremental); hours and total elapsed time unobserved.

Protocol deviations against ../../../ARENA_TASK.md: screenshot prompt starts in English whereas the frozen prompt is Russian. Full prompts, byte-identical pasted bodies, stable region/locale, client version across trials and concealment of the key cannot be verified from the captures. Snapshot acquisition metadata is in ../RECORD.md. Only rendered response samples survive in this packet. Exact original UTF-8 response bytes and elapsed request-to-completion time are unknown for every arm. Thinking times are UI observations. No reconstruction from rendered JSON or substitution of screenshot clock times.

Next authorized action: review this evidence. Closure requires resolution of the protocol gaps. Seek pre-existing raw exports or timing records if available. The approved task defines only CP-01. No subsequent trial authorized.

## Independent Codex review
A separate read-only Codex reviewer inspected the ea1a322 control package and the five original screenshots on 2026-11-21. Verdict: PARTIAL. Independently confirmed the two hashes, input sizes, field scores, thinking times and URL errors. Reviewer identified the missing elapsed times, exact UTF-8 outputs, prompt mismatch and unverified client/region/locale parity as closure gaps. Source: independent reviewer response in the owner's Work session. This is an evidence review, not a GitHub PR approval.
