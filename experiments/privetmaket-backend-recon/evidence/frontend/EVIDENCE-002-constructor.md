# EVIDENCE-002 — Public constructor UI

**Sources:**
- https://privetmaket.ru/shkaf
- https://privetmaket.ru/garderob
- https://r.jina.ai/http://privetmaket.ru/shkaf (public rendered retrieval used only for page text)

**Collected:** 2026-09-29 UTC  
**Method:** public GET/page rendering, no auth, no form submission

## Observed

The constructor exposes public controls/content for:

- width, height, depth and cell/partition counts;
- several furniture modes, including wardrobe, cabinet, shelving and table-related variants;
- body materials and a large material/decor catalogue;
- rear wall, plinth/legs, tabletop/roof and component offsets;
- doors, drawers, handles, glass/mirror, edge treatment and wall fixing;
- hinges, drawer slides, fasteners and removable shelves;
- special-use flags (balcony, wet room, wall-to-wall, suspended) and free-form wishes;
- a browser-facing 3D/performance panel and “BASKET/GO”/basket, save and drawing controls;
- public login/registration links associated with constructor actions.

## Interpretation

A browser-visible parametric model and rules-oriented UI are FACT. The frontend framework, exact calculation transport and internal object schema are UNKNOWN.

**Confidence:** FACT for visible controls; UNKNOWN for implementation details.
