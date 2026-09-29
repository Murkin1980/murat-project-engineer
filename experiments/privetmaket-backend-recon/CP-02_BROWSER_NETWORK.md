# CP-02 — Browser Network Capture

**Experiment:** `privetmaket-backend-recon`  
**Decision:** `EXTEND_EXISTING`  
**Scope:** anonymous, public, read-only browser observation only.

## Objective

Close the main unknown left by CP-01: determine the real browser-visible network boundary used by the furniture constructor.

The checkpoint must answer, with evidence where possible:

1. Which hosts receive constructor-related requests?
2. Which methods and paths are used?
3. Are responses HTML, JSON, GraphQL, WebSocket/SSE, or other?
4. Does changing dimensions/materials/modules trigger network requests?
5. Does visible price recalculation correlate with a network request?
6. Are project state, pricing, catalog, or rendering calls separable by route/host?
7. Which public JS bundle filenames and response headers are observable?

## Allowed actions

Use an ordinary fresh browser session without login.

Perform only these public interactions:

- load `/` and `/shkaf`;
- open the public constructor;
- open catalog / a public ready-made model;
- change one dimension;
- change one material;
- add or remove one module if the anonymous UI permits it;
- observe visible price changes;
- inspect Network metadata and anonymously loaded JS bundle names.

Do not submit forms, save projects, place orders, authenticate, pay, or cross any protected boundary.

## Capture fields

For each relevant browser request record only:

- timestamp/order;
- action that triggered it;
- method;
- host;
- path;
- status;
- request content type;
- response content type;
- request category (document/fetch/xhr/script/ws/other);
- response size if visible;
- purpose;
- confidence: FACT / STRONG_INFERENCE / UNKNOWN.

Do not commit full request/response bodies unless the body is demonstrably public, non-sensitive, minimal, and necessary as evidence.

## Redaction

Never store or commit:

- Cookie headers;
- Set-Cookie values;
- Authorization headers;
- JWT/session IDs;
- CSRF tokens;
- personal data;
- project/user/order identifiers;
- query parameters that contain secrets or user-specific values.

Replace any accidental sensitive value with `[REDACTED]`.

Raw HAR/network exports belong only in:

`.artifacts/privetmaket-backend-recon/cp02/`

This directory remains gitignored.

## Evidence outputs

Create only sanitized evidence under:

`experiments/privetmaket-backend-recon/evidence/endpoints/`

Recommended files:

- `CP02_NETWORK_MANIFEST.md`
- `CP02_ACTION_TRACE.md`
- `CP02_JS_ASSETS.md`
- `CP02_HEADERS.md`

Update existing:

- `API_MAP.md`
- `TECHNOLOGY_MAP.md`
- `ARCHITECTURE.md`
- `UNKNOWNS.md`
- `FINDINGS.md`
- `manifest.json`

Only update claims supported by captured evidence.

## PASS criteria

CP-02 is PASS only if all of the following are true:

- at least one real constructor-related browser request is captured;
- at least one request is tied to a concrete UI action;
- host + method + path + status + content type are recorded;
- it is possible to state with evidence whether dimension/material/module changes are network-backed or client-only for the observed action;
- pricing behavior is classified as FACT / STRONG_INFERENCE / UNKNOWN with direct trace evidence;
- no sensitive values are committed;
- security boundary remains PASS.

## PARTIAL criteria

Use PARTIAL if useful browser evidence is captured but one or more core questions remain unresolved, such as pricing location, project storage, framework, or API schema.

## BLOCKED criteria

Use BLOCKED only when the browser execution environment cannot expose Network/DevTools data or the public site itself prevents safe anonymous observation.

Do not compensate by bypassing protections or probing hidden endpoints.

## Stop conditions

Stop immediately if the next step would require:

- login or account creation;
- CAPTCHA/WAF/rate-limit bypass;
- POST/form submission that changes server state;
- guessing or enumerating IDs;
- accessing another user's data;
- payment;
- hidden/admin/partner routes;
- fuzzing, injection, brute force, or exploitation.

## Final result format

```
RESULT: PASS / PARTIAL / BLOCKED
CHECKPOINT: CP-02
EXPERIMENT: privetmaket-backend-recon

BROWSER_NETWORK: PASS / PARTIAL / BLOCKED
CONSTRUCTOR_REQUESTS:
PRICING_REQUESTS:
MATERIAL_CHANGE:
DIMENSION_CHANGE:
MODULE_CHANGE:
API_HOSTS:
CONTENT_TYPES:
JS_ASSETS:
HEADERS:
CLIENT_VS_SERVER_FINDINGS:
SECURITY_BOUNDARY: PASS / FAIL
UNKNOWN:
FILES_CHANGED:
BRANCH:
COMMIT:
PR:
```

Do not implement any PrivetMaket-like feature in Murat projects as part of this checkpoint. This checkpoint is evidence collection only.
