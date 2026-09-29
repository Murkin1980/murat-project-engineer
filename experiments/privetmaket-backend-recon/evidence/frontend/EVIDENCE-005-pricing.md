# EVIDENCE-005 — Pricing and manufacturing rules

**Source:** https://privetmaket.ru/283-kak_schitaetsya_stoimost_i_kak_mojno_sekonomit_pri_proektirovanii_shkafov_i_stolov

**Collected:** 2026-09-29 UTC  
**Method:** public help/article retrieval; no calculator submission

## Observed

The page says the constructor calculates price automatically and describes a simplified formula:

`TOTAL = (MATERIAL + EDGE + HARDWARE) * WORK MARKUP`

It further describes material area and waste coefficient, material groups/availability, edge length/type, hardware, labor/production/packaging/tax/management factors and configurable options. The constructor itself displays a price/range while exposing parameter and material controls.

## Interpretation

The price model is rules-driven and furniture-specific. Whether authoritative calculation runs in browser, backend, or a hybrid is UNKNOWN.

**Confidence:** FACT for published formula and public price UI; STRONG_INFERENCE for a structured rules engine; UNKNOWN for transport/location.
