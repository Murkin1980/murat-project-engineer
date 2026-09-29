# EVIDENCE-007 — Order and payment flow

**Sources:**
- https://privetmaket.ru/kak_sdelat_zakaz
- https://privetmaket.ru/oplata_i_dostavka

**Collected:** 2026-09-29 UTC  
**Method:** public help/legal/product page retrieval; no order or payment submitted

## Observed

The published flow is:

1. configure an object or choose a ready object;
2. add to basket;
3. provide basic order/delivery information;
4. wait for manager/technologist review of materials and construction;
5. receive a payment link by email;
6. pay on a bank acquiring page; the order-help page names Tinkoff;
7. receive an electronic receipt and the order is sent to production;
8. follow readiness/status in the personal cabinet; delivery/assembly follow separately.

The payment page says 100% prepayment for the described flow. No bank hostname, request, callback or token was collected.

## Interpretation

Human review is an explicit gate between self-service configuration and payment/production.

**Confidence:** FACT for the published workflow and named provider; UNKNOWN for integration/API details.
