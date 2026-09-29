# EVIDENCE-003 — robots.txt and public route surface

**Sources:**
- https://privetmaket.ru/robots.txt
- https://privetmaket.ru/sitemap.xml
- https://privetmaket.ru/default/index/pricecache (read-only GET)

**Collected:** 2026-09-29 UTC  
**Method:** public GET only

## Observed

`robots.txt` names route families including `/users/`, `/user/`, `/orders`, `/login`, `/planner/`, `/partners/`, `/default/index/pricecache`, `/default/calculatorparams/`, `/default/options`, `/uploads/projects/` and other controller-like paths. It also publishes a sitemap URL.

The sitemap request returned a public sitemap-like response with product/help routes. A read-only GET to `/default/index/pricecache` returned an HTML table shell without rows in this observation.

## Interpretation

These paths are evidence of a public route taxonomy, not a REST/JSON API contract. No auth bypass was attempted against any disallowed route.

**Confidence:** FACT for the text/GET observations; UNKNOWN for methods, authorization and purpose of individual route families.
