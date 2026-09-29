# API / Public Route Map

**Important:** в доступном execution context не был получен browser Network trace (чекпоинт CP-02 классифицирован как `BLOCKED` по сетевому захвату). Поэтому таблица отделяет **наблюдаемые GET routes** от возможных API. URL route не называется API без evidence о method/content type/JSON response.

Confidence: `FACT`, `STRONG_INFERENCE`, `WEAK_INFERENCE`, `UNKNOWN`.

## Public routes observed

### Endpoint: `https://privetmaket.ru/`

- **Method:** GET
- **Observed from:** public landing page retrieval
- **Purpose:** public furniture storefront/constructor entry and editable ready solutions
- **Authentication:** no for page view; checkout/auth boundary unknown
- **Input:** none observed
- **Output:** HTML/interactive page content with catalog links, images and constructor entry
- **Evidence:** EVIDENCE-001
- **Confidence:** FACT

### Endpoint: `https://privetmaket.ru/shkaf`

- **Method:** GET
- **Observed from:** public constructor page
- **Purpose:** parametric cabinet/shelving/wardrobe configurator and quote UI
- **Authentication:** page accessible without login; save/order/export requirements not fully tested
- **Input:** public UI fields for dimensions, cells, materials, options and notes; no request body captured
- **Output:** HTML plus browser-side interactive 3D WebGL configuration UI (`EVIDENCE-019`); displayed price and basket/save/export controls
- **Evidence:** EVIDENCE-002, EVIDENCE-019, CP02_NETWORK_MANIFEST, CP02_ACTION_TRACE
- **Confidence:** FACT

### Endpoint: `https://privetmaket.ru/garderob`

- **Method:** GET
- **Observed from:** public linked constructor page
- **Purpose:** wardrobe-focused constructor variant
- **Authentication:** public page view; action boundary unknown
- **Input:** dimensions, material, rear wall, edge, filling and door/drawer options visible in UI
- **Output:** HTML/interactive constructor UI
- **Evidence:** EVIDENCE-002
- **Confidence:** FACT

### Endpoint: `https://privetmaket.ru/planner`

- **Method:** GET
- **Observed from:** public planner page and constructor navigation
- **Purpose:** room planner with rooms, furniture placement and project save/cart language
- **Authentication:** public page view; persistence/auth boundary unknown
- **Input:** room dimensions, furniture placement and object parameters
- **Output:** HTML/interactive planner UI
- **Evidence:** EVIDENCE-008
- **Confidence:** FACT

### Endpoint: `https://privetmaket.ru/raspil`

- **Method:** GET
- **Observed from:** public constructor navigation and standalone service page
- **Purpose:** detail/cutting constructor for individual parts
- **Authentication:** page view public; order submission not attempted
- **Input:** length/width, material, edge and rounding options visible in UI
- **Output:** HTML/interactive detail calculator UI
- **Evidence:** EVIDENCE-013
- **Confidence:** FACT

### Endpoint: `https://privetmaket.ru/katalog`

- **Method:** GET
- **Observed from:** public catalog link
- **Purpose:** ready-made project/catalogue; projects can be opened and changed in constructor
- **Authentication:** public page view
- **Input:** catalogue selection
- **Output:** HTML, images, model/project links and public prices on some cards
- **Evidence:** EVIDENCE-001
- **Confidence:** FACT

### Endpoint: `https://privetmaket.ru/login/`

- **Method:** GET
- **Observed from:** public login page and constructor link
- **Purpose:** personal cabinet authentication boundary
- **Authentication:** page itself public; credentials required to enter, not used in this experiment
- **Input:** email/password fields are visible; no values sent
- **Output:** HTML login form
- **Evidence:** EVIDENCE-004
- **Confidence:** FACT

### Endpoint: `https://privetmaket.ru/reg/` and `/users/index/add/...`

- **Method:** GET for page view
- **Observed from:** public registration page and login link
- **Purpose:** account registration boundary
- **Authentication:** registration creates/uses an account; not performed
- **Input:** public form labels include name, email, password, phone and region; no values stored
- **Output:** HTML registration form
- **Evidence:** EVIDENCE-004
- **Confidence:** FACT

### Endpoint: `https://privetmaket.ru/submit/`

- **Method:** GET
- **Observed from:** public basket page and constructor/planner links
- **Purpose:** basket/order entry point
- **Authentication:** empty basket view public; submission boundary unknown
- **Input:** basket state and order/contact data are referenced; no data entered
- **Output:** HTML basket; empty state was observed
- **Evidence:** EVIDENCE-004
- **Confidence:** FACT

### Endpoint: `https://privetmaket.ru/770-besplatnie_cherteji_shkafov_stellajei_polok_komodov_i_td/`

- **Method:** GET
- **Observed from:** public help page
- **Purpose:** instructions and commercial description for drawing/Basis export
- **Authentication:** page public; download entitlement not exercised
- **Input:** project selected in constructor/catalogue (described, not submitted)
- **Output:** documentation describing PDF, detailing, drilling, cut map, XLS and B3D outputs
- **Evidence:** EVIDENCE-006
- **Confidence:** FACT

### Endpoint: `https://privetmaket.ru/primer_modeli_Privetmaket.b3d`

- **Method:** GET (public link; binary was not copied)
- **Observed from:** public Basis-model page
- **Purpose:** public sample Basis-Mebelshchik model
- **Authentication:** public link according to page; no private project retrieval attempted
- **Input:** none
- **Output:** binary B3D sample; not persisted in repository
- **Evidence:** EVIDENCE-014
- **Confidence:** FACT

### Endpoint: `https://privetmaket.ru/robots.txt` and sitemap link

- **Method:** GET
- **Observed from:** public robots retrieval
- **Purpose:** crawler policy and public route taxonomy
- **Authentication:** public
- **Input:** none
- **Output:** disallowed route families include users, orders, login, partners, planner and several default/controller paths; sitemap link is present
- **Evidence:** EVIDENCE-003
- **Confidence:** FACT for text; not evidence that each route is an API

### Endpoint: `https://privetmaket.ru/default/index/pricecache`

- **Method:** GET
- **Observed from:** public robots-listed route retrieved read-only
- **Purpose:** route name suggests price-cache/admin-like surface; returned a public HTML table shell without price rows in this observation
- **Authentication:** unknown; no login/bypass attempted
- **Input:** none
- **Output:** HTML table shell
- **Evidence:** EVIDENCE-003
- **Confidence:** FACT for observed GET; purpose remains UNKNOWN

### Endpoint family: `/orders`, `/users/`, `/partners/`

- **Method:** UNKNOWN for the underlying order/account/partner operations
- **Observed from:** robots route entries and public links to personal cabinet/partner pages
- **Purpose:** likely order, account and partner workflows
- **Authentication:** likely restricted for user-specific operations; not tested
- **Input:** unknown
- **Output:** unknown
- **Evidence:** EVIDENCE-003, EVIDENCE-007, EVIDENCE-009
- **Confidence:** STRONG_INFERENCE for existence of route families; UNKNOWN for API contract

## Not observed / must not be presented as fact

- `/api/`, `/graphql`, `/v1/`, `/v2/` exact endpoints: **UNKNOWN**.
- `POST`/JSON methods for recalculation, save, order, export or payment: **UNKNOWN**.
- WebSocket/SSE channels: **UNKNOWN**.
- Separate API hostname: **UNKNOWN** (all observed actions stay on apex `privetmaket.ru`).
- Cookies, authorization headers, JWT or session identifiers: intentionally not collected.

A future Network-only continuation may add endpoint entries after redaction, but must not submit forms or cross the authentication boundary.
