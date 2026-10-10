# EXP-24 CP-13 — sanitized canonical fixture: E01-S005

Status: OWNER-AUTHORIZED DERIVED FIXTURE  
Purpose: allow Arena to execute the bounded EXP-24 single-agent pipeline without direct access to the private AI-serial repository.

## Provenance

- Canonical repository: `Murkin1980/AI-serial-v2` (private, read-only source)
- Canonical path: `episodes/01_SEVEN_MINUTES/TEASER_SCENE_SHEETS.md`
- Canonical blob SHA: `fd049ca5faafc31203cde607fbdb17bd6b17789b`
- Scene: `E01-S005`
- Canonical status: `APPROVED FOR VISUAL DEVELOPMENT`
- Derived on: 2026-10-10
- Derivation rule: no full private scene text is copied into this public repository; only the minimum production facts required for CP-13 are preserved.

If this fixture conflicts with the private canonical source, the private canonical source wins.

## Scene purpose

A routine office moment becomes the first information breach: a young state-TV producer discovers a sealed political document, realizes its significance, and contacts Arman.

## Production boundaries

- Location class: state television / small editorial work area.
- Time: early morning, approximately 08:07–08:08.
- Main subject: young producer.
- Background: a few ordinary coworkers may be present.
- Tone starts as routine work, then shifts to contained tension.
- Do not portray the producer as a conspirator.
- Visual tension should come from behavior, timing, props and reaction — not from exaggerated noir/thriller lighting.
- Lighting: neutral office light; shallow depth of field may isolate the subject after discovery.
- Key props: envelope, political document, phone, visible clock.
- Previous-scene continuity: the envelope has arrived on the wrong desk.
- Next-scene boundary: Arman’s response belongs to the following scene and must not be depicted here.
- Full document text must not be shown.
- Generated images/storyboards are derived production artifacts, not canon.

## Canonical action ledger

The 20 material source actions are represented below as normalized production actions. IDs and order are stable for EXP-24 coverage checks.

| Action ID | Normalized action |
|---|---|
| A01 | Producer notices an envelope on his desk. |
| A02 | He picks it up automatically. |
| A03 | He notices that it carries a future/open-later restriction. |
| A04 | He checks the current time. |
| A05 | He briefly assumes it may already be intended for preparation work. |
| A06 | He opens the envelope. |
| A07 | He removes the document. |
| A08 | He reads the document heading. |
| A09 | He scans through the document. |
| A10 | He reaches the key statement indicating the president will not continue into the next election cycle. |
| A11 | He freezes. |
| A12 | He rereads the key statement. |
| A13 | He looks around the room. |
| A14 | He checks the clock again. |
| A15 | He picks up the phone. |
| A16 | He finds the contact he needs. |
| A17 | He calls Arman. |
| A18 | He quietly gives a confidentiality warning. |
| A19 | He pauses. |
| A20 | He conveys that the president is leaving. |

Coverage requirement: every A01–A20 action must map to one visual beat or an explicitly documented grouped beat. No action may silently disappear.

## Dialogue handling

The private canonical wording is intentionally not copied into this public fixture.

For CP-13, preserve only these dialogue functions:
- D01: confidentiality warning;
- D02: concise statement that the president is leaving.

Do not invent additional dialogue.
Do not depict or generate Arman’s reply in this scene.

## Character / behavior constraints

Young producer:
- visually young adult;
- less formal than senior staff;
- ordinary working-state appearance;
- after reading: freezes, breathing changes, becomes visibly unsettled, checks surroundings;
- performance must remain restrained rather than melodramatic.

Do not infer or add permanent biography, family, ideology, political affiliation, or conspiratorial motivation.

## Visual continuity requirements

Must preserve:
- same envelope throughout the scene;
- envelope transitions sealed → opened;
- document transitions inside envelope → removed → read;
- phone appears only when the call action begins;
- clock/time-check motif can recur;
- subject identity/clothing should remain stable across generated assets;
- office continuity should remain stable across generated assets.

## Suggested bounded grouping for EXP-24

Arena may choose another grouping if all A01–A20 actions remain covered, but the preferred 4–6-beat structure is:

1. **B01 — notice / pickup**: A01–A05
2. **B02 — opening**: A06–A07
3. **B03 — reading / realization**: A08–A12
4. **B04 — check surroundings / time**: A13–A14
5. **B05 — phone / contact**: A15–A17
6. **B06 — disclosure / reaction hold**: A18–A20

This grouping is a production convenience, not canon.

## CP-13 use rule

Arena may use this file as the authoritative **bounded experiment fixture** when the private source repository is inaccessible from its sandbox.

Arena must:
- cite this fixture path and source blob SHA in EXP-24 evidence;
- treat it as derived from private canon, not as a new canon source;
- not modify AI-serial canon;
- not expand beyond E01-S005;
- not reconstruct missing private text;
- preserve 20/20 action coverage;
- continue the single-agent pipeline from Step 1.
