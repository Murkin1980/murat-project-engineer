# EVIDENCE-008 — Planner and project-state language

**Source:** https://privetmaket.ru/planner

**Collected:** 2026-09-29 UTC  
**Method:** public GET/page rendering; no project submission

## Observed

The public page calls itself an online room planner, exposes room creation/copying, room dimensions, furniture placement and a link to save/add the room to the basket. It states that changes will be saved there and that the user can return to draft mode.

## Interpretation

A project/room state concept is public. The storage medium and exact save request are UNKNOWN. “Saved project” in the architecture diagram therefore means a product boundary, not a claimed database technology.

**Confidence:** FACT for UI text; STRONG_INFERENCE for persistence beyond a single static page; UNKNOWN for storage implementation.
