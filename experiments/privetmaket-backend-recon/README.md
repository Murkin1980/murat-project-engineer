# EXPERIMENT — PrivetMaket Backend Recon

**Status:** PARTIAL  
**Decision:** `EXTEND_EXISTING`  
**Repository:** `Murat Project Engineer`  
**Experiment path:** `experiments/privetmaket-backend-recon/`  
**Research date:** 2026-09-29 UTC  
**New repository:** NO

## Goal

Картировать публично наблюдаемую архитектуру `privetmaket.ru`, связанные публичные сервисы и PMplanner, если связь подтверждается самим публичным сайтом. Это архитектурное исследование, а не penetration test.

Результат ограничен обычным публичным доступом: HTML/рендеринг страниц, ссылки, публичный `robots.txt`/sitemap, публичные DNS-записи и опубликованные описания продукта. Секреты, cookies, authorization headers, JWT, session IDs, персональные данные и сырые network traces не сохранялись.

## Почему PARTIAL, а не PASS

Публичная продуктовая и route-level архитектура картирована. Однако точная browser Network map не получена в этом execution context: нет доступного браузерного DevTools-трейса, а прямой `curl` из sandbox завершался `SSL_ERROR_SYSCALL`. Поэтому ниже явно отмечены неизвестные:

- реальные `POST`/JSON API paths и их тела;
- API base URL и отдельный BFF/API hostname;
- точное место выполнения пересчёта цены;
- framework/bundler и response headers;
- object storage/CDN, CRM и точный платёжный endpoint;
- WebSocket/SSE/GraphQL.

## Состав

- `SCOPE.md` — границы и правила исследования;
- `ARCHITECTURE.md` — evidence-backed Mermaid map и отдельные hypotheses;
- `FINDINGS.md` — ответы на десять вопросов задания;
- `API_MAP.md` — наблюдаемые публичные routes, отдельно от неподтверждённых API;
- `TECHNOLOGY_MAP.md` — технологии только с маркировкой confidence;
- `REUSE_CANDIDATES.md` — архитектурные/product patterns для существующих проектов;
- `UNKNOWNS.md` — закрытые вопросы и безопасные следующие шаги;
- `manifest.json` — список очищенных evidence;
- `evidence/` — короткие безопасные фрагменты, без raw trace и private data.

Сырые временные материалы, если они нужны для повторного исследования, должны оставаться только в `.artifacts/privetmaket-backend-recon/`, который gitignored.

## Безопасность

Выполнялись только безопасные GET/read-only наблюдения. Не выполнялись:

- login, регистрация, ввод контактов или оформление реального заказа;
- попытки получить доступ к чужим проектам/заказам;
- brute force, fuzzing, IDOR enumeration, injection, CAPTCHA/rate-limit/WAF bypass;
- POST/изменяющие запросы;
- сканирование портов, внутренних IP или закрытых endpoints.

## Current result

Главное подтверждённое наблюдение: PrivetMaket — не только витрина, а публичный параметризованный мебельный workflow: конструктор → корзина/заявка → менеджерская проверка → платёжная ссылка/эквайринг → собственное или партнёрское производство → доставка; отдельно есть экспорт PDF/XLS/B3D и партнёрская сеть. Exact API boundary remains unknown.

## CP-02

Continuation is defined in `CP-02_BROWSER_NETWORK.md`. Its only goal is sanitized anonymous browser Network evidence for the constructor. No implementation, authentication, state-changing requests, or protection bypass is in scope.
