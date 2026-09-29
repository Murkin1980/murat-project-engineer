# Findings

**Experiment:** `privetmaket-backend-recon`  
**Result:** `PARTIAL`  
**Date:** 2026-09-29 UTC  
**Security boundary:** `PASS` — no auth bypass, exploitation, enumeration or state-changing request was performed.

## Executive summary

Публичная поверхность показывает единую online-модель: пользователь создаёт параметризованный шкаф/стеллаж/стол/деталь, получает быстрый расчёт и может добавить проект в корзину, запросить проверку, оплатить по банковской ссылке и передать заказ в собственное или партнёрское производство. Публично описаны производственные файлы: PDF, деталировка, схемы присадки, карта раскроя, XLS и B3D/Basis. PMplanner явно позиционируется как SaaS/partner layer поверх конструктора PrivetMaket.

При этом exact API architecture не подтверждена: нет network trace, raw JS bundle, current response headers или отдельного API hostname. Поэтому framework/backend/API не угадываются.

## 1. Как устроен frontend?

**FACT:** Публичный HTML/рендеринг даёт серверные страницы с интерактивным constructor/planner UI. `/shkaf` показывает 3D-performance panel, габариты, сетку ячеек, материалы и большой набор опций; пользователь может менять doors/drawers, rear wall, base, edges, hardware and notes. [EVIDENCE-001](evidence/frontend/EVIDENCE-001-homepage.md), [EVIDENCE-002](evidence/frontend/EVIDENCE-002-constructor.md)

**UNKNOWN:** framework, bundler, bundle structure, exact 3D library and component architecture. Нет безопасно сохранённого source/bundle evidence. [EVIDENCE-017](evidence/headers/EVIDENCE-017-headers-and-network-limitations.md)

## 2. Есть ли отдельный backend API?

**FACT:** Есть отдельная серверная application boundary с public routes для auth, basket, orders, users, partners, planner и export/help workflows. [EVIDENCE-003](evidence/endpoints/EVIDENCE-003-robots-and-route-surface.md), [EVIDENCE-004](evidence/endpoints/EVIDENCE-004-auth-and-basket.md)

**UNKNOWN:** отдельный API/BFF hostname и JSON contract. `privetmaket.ru` route surface не равен отдельному backend API. Точных `/api`, `/graphql`, `/v1`, `/v2` запросов не наблюдалось. [EVIDENCE-017](evidence/headers/EVIDENCE-017-headers-and-network-limitations.md)

## 3. Какие API endpoints видны?

**FACT:** Надёжно видны public GET routes: `/`, `/shkaf`, `/garderob`, `/planner`, `/raspil`, `/katalog`, `/login`, `/reg`, `/submit`, `/robots.txt`, sitemap, export/help routes. [API_MAP.md](API_MAP.md), [EVIDENCE-003](evidence/endpoints/EVIDENCE-003-robots-and-route-surface.md)

**UNKNOWN:** методы и тела пересчёта, сохранения, добавления модуля, order submit и export generation. Не следует называть route `/default/index/pricecache` или `/orders` REST API без trace evidence.

## 4. Как устроена authentication boundary?

**FACT:** Конструктор и catalog доступны до логина; отдельные login/registration pages и personal-cabinet links существуют. Public help/legal pages place project/order parameters and status in the user's cabinet. Robots lists users/orders/partners/login as non-indexed route families. [EVIDENCE-004](evidence/endpoints/EVIDENCE-004-auth-and-basket.md), [EVIDENCE-003](evidence/endpoints/EVIDENCE-003-robots-and-route-surface.md), [EVIDENCE-009](evidence/frontend/EVIDENCE-009-partners-and-production.md)

**UNKNOWN:** cookie naming, session/JWT mechanism, exactly which actions require account, CSRF behavior. None was collected.

## 5. Где предположительно хранятся проекты?

**FACT:** Public pages expose “save project”, planner room/project state and a personal cabinet for order/project parameters and statuses. [EVIDENCE-008](evidence/frontend/EVIDENCE-008-planner.md), [EVIDENCE-009](evidence/frontend/EVIDENCE-009-partners-and-production.md)

**STRONG_INFERENCE:** at least some project/order state is persisted beyond a single visible render, likely in an account/server-side store; the implementation could include session/browser state for anonymous drafts. Database, object storage and retention model are **UNKNOWN**.

## 6. Как работает расчёт цены?

**FACT:** Public constructor advertises immediate calculation. Published formula describes material + edge + hardware multiplied by work markup, with material area, waste/material groups, edge length/type and hardware affecting cost. [EVIDENCE-002](evidence/frontend/EVIDENCE-002-constructor.md), [EVIDENCE-005](evidence/frontend/EVIDENCE-005-pricing.md)

**UNKNOWN:** client-side vs server-side vs hybrid calculation, exact rules endpoint, rounding, delivery formula and authoritative recalculation at checkout. Do not treat the formula article as an API specification.

## 7. Как устроен мебельный конструктор?

**FACT:** It supports multiple furniture modes, dimensions at millimetre granularity, cells/partitions, material per component, doors/drawers, handles, rear wall, plinth/legs, tabletop/roof, edge protection, wall fixing, hinges/drawer slides, special-use flags, comments and production selection. It also offers room planning and ready-made editable templates. [EVIDENCE-002](evidence/frontend/EVIDENCE-002-constructor.md), [EVIDENCE-008](evidence/frontend/EVIDENCE-008-planner.md)

**FACT:** Published constraints are treated as technological rules: sheet size/material limitations, compatibility warnings and final manual production check. [EVIDENCE-005](evidence/frontend/EVIDENCE-005-pricing.md), [EVIDENCE-006](evidence/frontend/EVIDENCE-006-exports.md)

## 8. Какие сервисы участвуют в оформлении заказа?

**FACT:** Flow is constructor/catalog → basket → contact/order data → manager/technologist review → payment link → bank-side payment. The order page publicly names Tinkoff for payment, and the site says an electronic receipt follows payment. [EVIDENCE-007](evidence/endpoints/EVIDENCE-007-order-payment.md)

**FACT:** Delivery/assembly are separate services; own and partner productions are described, and the legal offer defines partner/agent orders. [EVIDENCE-009](evidence/frontend/EVIDENCE-009-partners-and-production.md)

**UNKNOWN:** Tinkoff API/redirect host, CRM host/current integration, webhook, shipment API and exact order orchestration.

## 9. Есть ли признаки production/export pipeline?

**FACT:** Strong public signs exist: PDF drawing/detailing, drilling scheme, cut map, XLS list of parts/materials/hardware/fasteners and B3D Basis model are explicitly described. Public partner list and production-selection UI support a handoff to own/partner manufacturing. [EVIDENCE-006](evidence/frontend/EVIDENCE-006-exports.md), [EVIDENCE-009](evidence/frontend/EVIDENCE-009-partners-and-production.md), [EVIDENCE-014](evidence/frontend/EVIDENCE-014-public-b3d-link.md)

**STRONG_INFERENCE:** the product has a production-document generation boundary, possibly a queue/generator service, but its transport and implementation are unknown.

**UNKNOWN:** current direct CNC/`.b3d`/`.xls` export service, worker topology and machine integrations. A historical public article mentions a custom CRM and planned CNC-oriented SaaS work; it is not current live proof. [EVIDENCE-015](evidence/frontend/EVIDENCE-015-historical-architecture.md)

## 10. Какие решения полезны существующим проектам Murat?

1. Reuse the existing `skills/furniture-commercial-proposal/` input/position/price-table/print contract; do not redesign the locked Liquid Glass system. [EVIDENCE-018](evidence/frontend/EVIDENCE-018-murat-comparison.md)
2. Add deterministic furniture-rule validation before any AI explanation or quote; this aligns with the existing Personalized Assessment Engine experiment's `Ask → Understand → Calculate → Diagnose → Explain → Recommend → Convert` pattern. [EVIDENCE-018](evidence/frontend/EVIDENCE-018-murat-comparison.md)
3. Treat `DRAFT → REVIEW → APPROVED_FOR_PAYMENT → PRODUCTION` as a human-safe state machine rather than making payment/production automatic by default.
4. Keep a single normalized project object capable of customer preview plus production exports; add manifests and evidence rather than copying PrivetMaket code.
5. Use ready templates plus custom dimensions to lower first-session friction; this can extend existing furniture proposal work.
6. Defer partner-routing, live payment and CNC/export integration until a separate New Idea Filter/deep-change review.

No production feature, payment integration or configurator has been implemented by this experiment.
