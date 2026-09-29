# Technology Map

**Research date:** 2026-09-29 UTC  
**Overall confidence:** `PARTIAL`

## Frontend

| Area | Result | Confidence | Evidence |
|---|---|---|---|
| Public delivery | HTML pages on `privetmaket.ru`; assets use same-origin `/public/images/` and `/uploads/images/` paths | FACT | EVIDENCE-001, EVIDENCE-002 |
| Constructor UI | Browser-facing parametric controls for dimensions, cells, materials, doors, drawers, hardware and notes | FACT | EVIDENCE-002 |
| 3D | A browser-rendered interactive 3D scene/performance panel is exposed by the constructor and planner | FACT | EVIDENCE-002, EVIDENCE-008 |
| Framework | Not identified from the available rendered pages | UNKNOWN | EVIDENCE-017 |
| Bundler / JS bundle structure | Not identified; raw bundles were not preserved or analyzed | UNKNOWN | EVIDENCE-017 |
| 3D library | WebGL/3D-like behavior is visible, but Three.js/Babylon/custom engine is not proven | UNKNOWN | EVIDENCE-002, EVIDENCE-017 |
| API base URL | No separate base URL observed in available page content | UNKNOWN | EVIDENCE-017 |
| GraphQL / REST / RPC | No exact API request was observed; route-level surface is documented separately | UNKNOWN | EVIDENCE-003, EVIDENCE-017 |
| WebSocket / SSE | Not observed | UNKNOWN | EVIDENCE-017 |

## Backend and application surface

- `FACT`: the public site has route-backed HTML pages for constructor, planner, catalog, authentication, basket, orders, users, partners and export/help workflows. [EVIDENCE-003](evidence/endpoints/EVIDENCE-003-robots-and-route-surface.md), [EVIDENCE-004](evidence/endpoints/EVIDENCE-004-auth-and-basket.md)
- `STRONG_INFERENCE`: the application has a server-side MVC-like route surface or equivalent controller/action routing. This is based on public paths such as `/default/index/pricecache`, `/users/index/...`, `/orders` and `/partners`, plus full HTML pages. It is not a framework identification. [EVIDENCE-003](evidence/endpoints/EVIDENCE-003-robots-and-route-surface.md)
- `UNKNOWN`: PHP/Yii/Laravel/Node or another backend framework. No current response header, source bundle or official technical documentation confirms it. [EVIDENCE-017](evidence/headers/EVIDENCE-017-headers-and-network-limitations.md)
- `FACT`: public pages describe automatic pricing and generated production documents. The execution location of those rules is unknown. [EVIDENCE-005](evidence/frontend/EVIDENCE-005-pricing.md), [EVIDENCE-006](evidence/frontend/EVIDENCE-006-exports.md)
- `FACT`: public legal/help pages describe account/personal-cabinet state, manager review, payment and partner-production workflows. [EVIDENCE-004](evidence/endpoints/EVIDENCE-004-auth-and-basket.md), [EVIDENCE-007](evidence/endpoints/EVIDENCE-007-order-payment.md), [EVIDENCE-009](evidence/frontend/EVIDENCE-009-partners-and-production.md)

## Infrastructure and DNS

| Signal | Observation | Confidence |
|---|---|---|
| `privetmaket.ru` A | `89.111.172.112` at collection time | FACT |
| `pmplanner.ru` A | `151.248.115.67` at collection time | FACT |
| Authoritative NS | Both domains answered with `ns1.reg.ru` and `ns2.reg.ru` | FACT |
| CNAME | No CNAME answer was returned for `privetmaket.ru` | FACT, limited to queried record |
| CDN / reverse proxy | No evidence in the available DNS/page material | UNKNOWN |
| Object/image storage | Public images observed on `privetmaket.ru` paths; separate object-storage host not observed | UNKNOWN |
| Email | `mail@privetmaket.ru` is public; DNS MX points to Yandex; public TXT includes Yandex/amoCRM mail SPF entries | FACT, source-level only |
| Payment | Order-help page names Tinkoff as the bank-side payment page; acquiring/API hostname not captured | FACT for named provider; API UNKNOWN |
| Analytics | Site says cookies/analytics are used; privacy policy names Yandex.Metrika as a possible service, not proof of current activation | FACT for policy text; provider activation UNKNOWN |

DNS evidence: [EVIDENCE-011](evidence/dns/EVIDENCE-011-dns.md). Privacy/analytics evidence: [EVIDENCE-016](evidence/frontend/EVIDENCE-016-privacy-and-analytics.md).

## Related public services

- `pmplanner.ru`: direct SaaS/partner landing page, explicitly links the PrivetMaket constructor and describes partner pricing/material configuration and production outputs. This confirms product relationship, not network co-location: [EVIDENCE-010](evidence/frontend/EVIDENCE-010-pmplanner.md).
- `konstruktor-shkafov.ru`: publicly linked in PrivetMaket content and has strong brand/review/director overlap. Separate IP/backend ownership is not established: [EVIDENCE-012](evidence/frontend/EVIDENCE-012-related-domains.md).
- `raspil59.ru`: public standalone cutting/detail service with online material/dimension table and an explicit testing/no-real-orders notice. Shared implementation is not established: [EVIDENCE-013](evidence/frontend/EVIDENCE-013-raspil.md).
- `b2b.pan-raspil.ru` and `mebelevich.com`: public partner embed examples named by PrivetMaket; not treated as PrivetMaket infrastructure: [EVIDENCE-009](evidence/frontend/EVIDENCE-009-partners-and-production.md).
