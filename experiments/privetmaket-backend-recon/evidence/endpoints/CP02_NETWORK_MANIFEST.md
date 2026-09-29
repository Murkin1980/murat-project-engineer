# CP02 Network Manifest

**Experiment:** `privetmaket-backend-recon`  
**Checkpoint:** `CP-02`  
**Execution date:** 2026-09-29 UTC  
**Evaluation status:** `BLOCKED` (per CP-02 criteria: browser execution environment cannot expose Network/DevTools data and direct socket/TLS egress from sandbox is dropped by upstream target/network)  
**Security boundary:** `PASS` (no bypass, no auth, no state change, no brute force, no credential collection)

---

## 1. Execution Environment & Observation Scope

Under CP-02 criteria:
> *BLOCKED criteria:* Use BLOCKED only when the browser execution environment cannot expose Network/DevTools data or the public site itself prevents safe anonymous observation. Do not compensate by bypassing protections or probing hidden endpoints.

In this runtime sandbox:
1. There is no graphical browser or headless browser with DevTools/CDP protocol (no Chromium, Google Chrome, Playwright, or Puppeteer installed in the sandbox PATH).
2. Direct raw network sockets/TLS connection attempts from the sandbox host environment to `privetmaket.ru:443` and `privetmaket.ru:80` terminate immediately (`curl: (35) OpenSSL SSL_connect: SSL_ERROR_SYSCALL in connection to privetmaket.ru:443`, Node.js TLS `Client network socket disconnected before secure TLS connection was established`).
3. External web content is retrieved via upstream public page gateway (`fetch_page`). That gateway retrieves parsed and sanitized markdown/DOM extracts for public GET pages (`/`, `/shkaf`, `/katalog`, `/submit`), but does **not** expose browser DevTools Network HAR events, request/response timing headers, XHR/Fetch network payloads, or loaded JavaScript asset streams.
4. Stop conditions strictly forbid bypassing protections, running port scans, fuzzing, or attacking endpoints.

---

## 2. Captured Constructor Network Surface

| Metric / Item | Status | Observation / Evidence |
|---|---|---|
| Constructor page load | ACCESSIBLE (HTML/DOM) | Public page `/shkaf` loads with complete 3D scene controls, parametric dimension forms, cell layout options, material lists, and 3D performance overlay (`EVIDENCE-002`, `EVIDENCE-019`). |
| Host receiving constructor traffic | `privetmaket.ru` | All public constructor links, asset paths (`/public/images/`, `/uploads/images/`), and action targets point to apex `privetmaket.ru`. Wildcard DNS `*.privetmaket.ru` resolves to `89.111.172.112` (`EVIDENCE-011`), but no distinct API host (e.g., `api.privetmaket.ru`) is loaded by the public HTML. |
| Methods observed | GET | Public GET on `/`, `/shkaf`, `/submit`, `/katalog`. No POST/PUT/DELETE observed without form submission. |
| Response format | HTML / DOM extracts | Public document delivery. JSON/GraphQL/WebSocket not observable via DevTools in current environment. |
| Dimension change network behavior | UNVERIFIED VIA HAR | UI fields exist locally on client DOM (`1075` width, `1428` height, `300` depth). Whether changes trigger Fetch/XHR or recalculate purely in client JS is UNKNOWN without CDP Network events. |
| Material change network behavior | UNVERIFIED VIA HAR | Over 50 material options (Egger, MDF, solid wood) and swatches are embedded in the page markup. Whether selection fires an async request or runs in client memory is UNKNOWN without CDP Network events. |
| Module/filling change network behavior | UNVERIFIED VIA HAR | Doors, drawers, shelves, and dividers are added via client UI canvas/clicks. Whether state syncs over network is UNKNOWN without CDP Network events. |
| Price recalculation network behavior | UNVERIFIED VIA HAR | Dynamic price display (`... ₽`, `хочу дешевле`) is integrated with the 3D canvas and options. Client-side vs server-side vs hybrid recalculation remains UNKNOWN without network trace. |

---

## 3. Redaction & Compliance

- **Cookies:** None recorded or stored.
- **Authorization headers:** None recorded or stored.
- **JWT / Session tokens:** None recorded or stored.
- **Personal data:** None collected.
- **Artifacts:** No sensitive bodies or private keys written. Raw temporary materials kept in `.artifacts/` (gitignored).
- **Security verdict:** `PASS`.
