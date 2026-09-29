# EVIDENCE-004 — Authentication and basket boundary

**Sources:**
- https://privetmaket.ru/login/
- https://privetmaket.ru/reg/
- https://privetmaket.ru/submit/

**Collected:** 2026-09-29 UTC  
**Method:** public GET only; no credentials or form values used

## Observed

- Login page contains email/password fields and links to password recovery/registration.
- Registration page contains public labels for name, email, password, phone and region; no data was entered.
- Basket page is publicly viewable and showed an empty basket with links to catalogue/constructor.
- Constructor content links to login/registration for relevant actions.

## Interpretation

Anonymous browsing and construction are separated from personal-cabinet/account operations. The exact action-by-action auth matrix is UNKNOWN.

**Confidence:** FACT for page/field presence; UNKNOWN for session/cookie/CSRF mechanism.
