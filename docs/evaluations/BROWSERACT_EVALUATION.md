# BrowserAct controlled evaluation — RUN-08

## Decision

`MURAT_PROJECT_ENGINEER_NEW_IDEA_FILTER = REUSE_COMPONENT`

`BROWSERACT_DECISION = REUSE_COMPONENT`

BrowserAct earned a narrow, replaceable role as a public-web browser acquisition fallback. It is not an orchestrator, product dependency, source of truth, or mandatory research path. Normal HTTP/search remains first.

## Scope and safety

- Question: public offers and selling patterns used by custom-kitchen competitors serving Almaty.
- Data class: `PUBLIC_WEB_ONLY`.
- Allowed: read, navigate, extract.
- Not used: authentication, personal profiles, customer data, forms, messages, purchases, CAPTCHA bypass, proxy/stealth features.
- Raw evidence destination: compact RUN-08 dataset only; no HTML archive, cookies, profile, or session state committed.
- Privacy gate: `PASS`.

## Environment and installation

```yaml
windows_preflight:
  os: Windows
  shell: Windows PowerShell 5.1.22621.4111
  python_version: 3.13.2
  uv_available: true (0.11.24)
  node_version: 24.19.0
  npm_version: 11.17.0
  npx_available: true
  codex_environment: Codex Desktop with Codex Router
  browseract_skill_existing: false
  browseract_cli_existing: false
```

The official BrowserAct skill 2.0.2 was installed in the Codex agent environment and the CLI was installed with Python 3.12. CLI version: 1.4.0. The normal uv shim failed on the Cyrillic user path; the actual tool executable worked. No product repository dependency was added.

Official documentation and policy review established Windows/Codex support, local Chrome sessions, extraction, and public pricing. BrowserAct's policy permits processing of workflow/extraction/query data in service-backed modes; this pilot therefore remained public-only. Local Chrome was used without login or profile import.

## Two-path result

Ordinary public retrieval produced 27 usable records from eight source URLs across seven domains. Direct retrieval failed for Eco-Service and KÜCHENBAUER. BrowserAct loaded both pages and exposed traceable price, warranty, lead-time, financing, promotion, material, service-area, and CTA evidence. Thus 8/10 source URLs were `NORMAL_WEB_SUFFICIENT` and 2/10 were `BROWSERACT_REQUIRED` in this execution environment. The full sample contains ten source URLs across nine domains.

Bing browser search returned irrelevant results and was rejected. Yandex rendered useful public discovery results, but direct first-party pages were preferred for the dataset. No blocked source was bypassed.

```yaml
pilot_metrics:
  sources_attempted: 10
  pages_attempted: 11
  records_extracted: 29
  validated_records: 27
  partial_records: 2
  duplicate_records: 0
  failed_records: 0
  normal_web_sufficient: 8
  browseract_added_value: 0
  browseract_required: 2
  browseract_failed: 0
  blocked_sources: 0
  retries: 2
  human_interventions: 1
  total_runtime: "approximately 2 hours"
  browseract_runtime: "approximately 15 minutes"
  approximate_service_cost: "0 observed (local Chrome mode); external service cost not observable"
  validation_rate: "93.1%"
  useful_record_rate: 2.64
  browser_incremental_value_rate: "20%"
  failure_rate: "0%"
  duplicate_rate: "0%"
  cost_per_validated_record: "UNKNOWN"
```

The single human intervention was approval to create the isolated Chrome required by BrowserAct's confirmation gate. No intervention was needed during extraction.

## Stability and observability

Operator-observed same-session check: Eco-Service, KÜCHENBAUER, and Kagan were read twice at low frequency. Titles and extracted critical fields appeared unchanged (`STABLE`). Kagan's page title remained stable, while the narrow price regex did not match its wording. Compact repeat outputs were not committed, so this stability result is supporting operational evidence rather than independently reproducible dataset evidence.

Observability: `ADEQUATE`. URL, session, title, command outcome, retry, and extracted text were visible. Output can be very large and truncated; targeted extraction is required for reliable evidence. The uv shim failure was diagnosable and recoverable through the installed executable path.

## Agent fit

```yaml
agent_fit:
  skill_load: PASS
  bounded_scope: PASS
  structured_output: PASS
  safe_operation: PASS
  evidence_traceability: PASS
  run_report_compatibility: PASS
```

Codex Router was used for research/extraction normalization (`opencode-go/deepseek-v4-flash`). BrowserAct stayed outside Router authority and domain decisions.

## Market snapshot

1. Sample: 29 records from 10 public URLs across 9 domains; 27 validated and 2 partial.
2. Source mix: ten URLs across nine first-party/public manufacturer or retailer domains; marketplace discovery was not used as final evidence.
3. Pricing: 11 of 27 priced records use explicit starting-price framing. Offers use either whole-kitchen prices or price per linear metre; the catalog-heavy sample limits cross-company comparison.
4. Promotions: the preserved records show free measurement/3D project, bundled delivery/montage, and a site-order discount.
5. Financing: the two browser-recovered records mention bank-partner financing or 0% up to 24 months.
6. Lead time: observed claims range from 10 days to 2–8 weeks; some pages give broader 15–30-day guidance.
7. Warranty: the two browser-recovered records expose materially different claims (24 months and a 5-year headline); the sample is insufficient for a market-wide warranty pattern.
8. CTA: quote/order, callback, WhatsApp, and free measurement. A 3D project appears as a promotion, not as a separately validated CTA.
9. Missing/rare: complete price formulas, installation exclusions, delivery boundaries, and detailed payment schedules.
10. Limitations: a pilot sample is not a market census; catalog prices may represent different scopes. Eco-Service contains internally inconsistent headline/FAQ ranges and is flagged in notes.

## Compatibility, risks, and recommendation

Business Discovery compatibility: `YES`. Each record maps to raw evidence, validation, normalized evidence, and later scoring without changing the core model.

Deep change required: `NO`. No provider framework, queue, persistent service, datastore, scheduler, new repository, production integration, or Router authority expansion was created.

Recommended role: `Browser Evidence Acquisition`, invoked only after a normal-web failure or when browser-rendered public state materially changes evidence. Approved class/action remains `PUBLIC` + `READ/NAVIGATE/EXTRACT`. Keep Playwright/future providers substitutable behind the conceptual `BrowserAcquisitionAdapter` boundary.

Final cleanup: after separate explicit user confirmation, the isolated pilot Chrome `chrome_local_112664527734046828` was deleted and the BrowserAct browser list was verified empty. Retain the agent-level skill/CLI; do not roll out portfolio-wide.

## Sources

- https://docs.browseract.com/
- https://docs.browseract.com/agent-cli/introduction
- https://github.com/browser-act/skills
- https://skills.browseract.com/skills/browser-act-skills-browser-act
- https://www.browseract.com/privacy-policy
- https://www.browseract.com/pricing
- Dataset source URLs in `evidence/stage2/run-08/browseract_almaty_kitchen_snapshot.json`
