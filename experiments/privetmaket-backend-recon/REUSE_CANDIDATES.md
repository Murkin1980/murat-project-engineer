# Reuse Candidates

Цель — перенять архитектурные/product patterns, а не код, тексты, бренд или proprietary implementation PrivetMaket. Любая реализация после этого исследования должна пройти New Idea Filter отдельно.

## 1. Parametric furniture input contract

**Pattern:** единый параметризованный объект мебели с габаритами, ячейками/модулями, материалом, фасадами, кромкой, фурнитурой и технологическими ограничениями.

**Observed implementation:** публичный конструктор задаёт ширину/высоту/глубину, количество ячеек, материалы по деталям, двери/ящики, заднюю стенку, цоколь, столешницу, кромку, крепления и особые пожелания. [EVIDENCE-002](evidence/frontend/EVIDENCE-002-constructor.md)

**Problem it solves:** превращает сложный индивидуальный заказ в проверяемый набор входных параметров и уменьшает ручное согласование.

**Relevant existing Murat project:** `skills/furniture-commercial-proposal/` и его `INPUT_CONTRACT.md`; также будущие furniture/configurator workstreams, но отдельного готового Salamat Mebel/Qulpinay проекта в checkout не найдено.

**Reuse potential:** HIGH for schema discipline and validation; do not copy implementation.

**Complexity:** MEDIUM–HIGH, because compatibility rules and production constraints must be explicit.

**Minimal experiment:** описать один synthetic wardrobe/table JSON contract plus deterministic validation for dimensions/material compatibility; no live target integration.

## 2. Immediate quote with rule breakdown

**Pattern:** цена меняется вместе с параметрами, а публично объяснена как `(material + edge + hardware) * work markup`, with material area, edge length, hardware and waste/production factors.

**Observed implementation:** constructor advertises instant price; pricing article names the components, material groups, edge options and markup; exact execution location is unknown. [EVIDENCE-005](evidence/frontend/EVIDENCE-005-pricing.md)

**Problem it solves:** shortens quote turnaround and makes an interactive commercial proposal possible.

**Relevant existing Murat project:** `skills/furniture-commercial-proposal/` (position prices, price table, print/PDF). `CODEX_PERSONALIZED_ASSESSMENT_ENGINE_V0_EXPERIMENT.md` is a reusable deterministic-rule precedent, not a furniture calculator.

**Reuse potential:** HIGH as a bounded rule/calculation layer; preserve manual review where rules do not cover the project.

**Complexity:** MEDIUM.

**Minimal experiment:** synthetic pricing fixture with 3 materials, edge rules and 2 hardware options; compare deterministic output to a manually checked baseline.

## 3. Export-first production handoff

**Pattern:** one project produces customer-visible visual output plus production artifacts: PDF/detailing, cut map, drilling scheme, XLS/BOM and B3D/Basis model.

**Observed implementation:** public pages explicitly list those formats and partner factories; downloadable sample B3D is publicly linked but raw file is not stored here. [EVIDENCE-006](evidence/frontend/EVIDENCE-006-exports.md), [EVIDENCE-014](evidence/frontend/EVIDENCE-014-public-b3d-link.md)

**Problem it solves:** removes re-drawing between sales, customer approval and production; supports both own production and local partners.

**Relevant existing Murat project:** `skills/furniture-commercial-proposal/` for customer-facing artifacts; existing MPE evidence/contract discipline for manifest/hash/review gates.

**Reuse potential:** MEDIUM–HIGH at architecture/pipeline level; format generation is a separate deep implementation.

**Complexity:** HIGH, due geometry correctness and machine/partner compatibility.

**Minimal experiment:** generate a synthetic BOM/CSV/PDF-like checklist from one frozen furniture fixture; human-review output, no CNC or vendor submission.

## 4. Manager review as an explicit gate before payment

**Pattern:** customer can design online, but payment link is activated after a human/technologist validates material availability and structural constraints.

**Observed implementation:** public order guide says request is checked, materials/constructive reliability are reviewed, then a payment link is sent; legal pages state parameters remain in personal cabinet and price/availability are confirmed before prepayment. [EVIDENCE-007](evidence/endpoints/EVIDENCE-007-order-payment.md), [EVIDENCE-009](evidence/frontend/EVIDENCE-009-partners-and-production.md)

**Problem it solves:** protects against unsupported geometry, stale materials and irreversible production mistakes while preserving fast self-service.

**Relevant existing Murat project:** MPE deep-change/human-gate policy and `CODEX_PERSONALIZED_ASSESSMENT_ENGINE_V0_EXPERIMENT.md` deterministic assessment pattern.

**Reuse potential:** HIGH as a product/workflow pattern; no new runtime needed.

**Complexity:** LOW–MEDIUM.

**Minimal experiment:** add a manual-review state machine to a synthetic proposal fixture: `DRAFT → REVIEW → APPROVED_FOR_PAYMENT → PRODUCTION`, with explicit rejection reasons.

## 5. Partner-production network with local execution

**Pattern:** central project/configuration layer can route orders/files to own or regional partner production; customer can use local partner or download files.

**Observed implementation:** PMplanner and PrivetMaket pages describe partner production, regional list, contractor/agent orders and partner-configured materials/prices. [EVIDENCE-009](evidence/frontend/EVIDENCE-009-partners-and-production.md), [EVIDENCE-010](evidence/frontend/EVIDENCE-010-pmplanner.md)

**Problem it solves:** reduces delivery distance and lets a digital configurator serve many regions without one factory everywhere.

**Relevant existing Murat project:** future configurable furniture project; currently no checked-out partner-routing service and no Salamat/Qulpinay implementation evidence.

**Reuse potential:** MEDIUM as a later extension, not a first MVP.

**Complexity:** HIGH (contracts, quality, pricing, liability, delivery, partner isolation).

**Minimal experiment:** compare 2 synthetic production destinations using the same fixture and export manifest; no live partner contact or order dispatch.

## 6. Two-layer customer flow: configure or start from a ready solution

**Pattern:** catalog templates are editable in the same constructor, so a user may start from an example or from scratch.

**Observed implementation:** public catalog links ready-made projects to “open in constructor”; constructor pages expose catalogue/ready solution links. [EVIDENCE-001](evidence/frontend/EVIDENCE-001-homepage.md), [EVIDENCE-002](evidence/frontend/EVIDENCE-002-constructor.md)

**Problem it solves:** lowers first-session effort without removing customisation.

**Relevant existing Murat project:** `skills/furniture-commercial-proposal/` (position-level content) and any future configurator extension inside the existing MPE portfolio.

**Reuse potential:** HIGH as a UX/product pattern.

**Complexity:** MEDIUM.

**Minimal experiment:** create three synthetic templates that map into the existing furniture proposal input contract; measure missing fields and manual corrections.

## Priority and non-goals

1. First: extend existing furniture proposal/input contracts and deterministic validation.
2. Second: prove one pricing + review workflow on synthetic data.
3. Third: explore production export only after geometry correctness is proven.
4. Partner network, API integration and live order automation remain out of scope until a separate filter/deep-change review.

No new repository, backend, payment integration or live configurator is authorized by this recon.
