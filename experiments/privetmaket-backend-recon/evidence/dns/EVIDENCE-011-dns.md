# EVIDENCE-011 — Public DNS observations

**Sources:**
- https://dns.google/resolve?name=privetmaket.ru&type=A
- https://dns.google/resolve?name=privetmaket.ru&type=NS
- https://dns.google/resolve?name=privetmaket.ru&type=MX
- https://dns.google/resolve?name=privetmaket.ru&type=CNAME
- https://dns.google/resolve?name=pmplanner.ru&type=A
- https://dns.google/resolve?name=pmplanner.ru&type=NS

**Collected:** 2026-09-29 UTC  
**Method:** public DNS-over-HTTPS lookups; no port scan

## Observed

- `privetmaket.ru` A: `89.111.172.112`.
- `pmplanner.ru` A: `151.248.115.67`.
- Both queried domains return `ns1.reg.ru` and `ns2.reg.ru` as NS.
- `privetmaket.ru` MX: `mx.yandex.net`.
- No CNAME answer was returned for the queried apex `privetmaket.ru`.
- Public TXT includes mail-verification/SPF material; the exact verification value is intentionally not copied into evidence.

## Interpretation

Reg.ru is the observed authoritative DNS provider/resolver delegation signal. The two domains are not proven to share hosting: A records differ. CDN/reverse proxy/object storage remain UNKNOWN.

**Confidence:** FACT for queried records at collection time; no ownership inference beyond public page relationship.
