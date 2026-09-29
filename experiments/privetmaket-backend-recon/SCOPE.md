# Scope — PrivetMaket Backend Recon

## Authorized scope

Исследование только публичной поверхности, доступной обычному посетителю сайта:

- `https://privetmaket.ru/` и публичные routes, на которые ведут страницы/robots/sitemap;
- `https://pmplanner.ru/`, только для проверки заявленной связи с PrivetMaket;
- публично обнаруженные `konstruktor-shkafov.ru` и `raspil59.ru`, только в пределах их публичных landing/workflow pages;
- публичный DNS-over-HTTPS lookup и публичные certificate/search records;
- опубликованные product/help/legal pages и публичные external articles.

## Explicitly out of scope

Не выполнялись и не будут выполняться в рамках этого эксперимента:

- credential use, login, account creation, password recovery, CAPTCHA interaction;
- POST/PUT/PATCH/DELETE, отправка формы, настоящий расчёт заказа или оплата;
- обход авторизации, rate limit, WAF/Cloudflare, IDOR enumeration;
- brute force, fuzzing, injection, privilege escalation;
- чтение чужих проектов/заказов, cookies, sessions, JWT, authorization headers;
- поиск server source code, database access, internal IP/ports;
- активное сканирование subdomains/ports;
- копирование исходного кода, proprietary assets или frontend bundles в Git.

## Evidence discipline

Каждый вывод должен ссылаться на `EVIDENCE-NNN`. Confidence values:

- `FACT` — прямо наблюдалось на публичном источнике;
- `STRONG_INFERENCE` — объясняет несколько фактов, но не наблюдалось напрямую;
- `WEAK_INFERENCE` — правдоподобная рабочая гипотеза;
- `UNKNOWN` — evidence недостаточно.

Сырые ответы web/curl не коммитятся. В репозитории остаются только короткие очищенные заметки. Случайно появившиеся secrets не сохраняются.

## Related-domain rule

Связь доменов не предполагается только по названию:

- `pmplanner.ru`: связь прямо заявлена на PMplanner landing page и подтверждена ссылкой на `privetmaket.ru`;
- `konstruktor-shkafov.ru`: ссылка обнаружена в публичном материале PrivetMaket; landing page использует бренд/директора/отзывы PrivetMaket — это сильная cross-site association, но не доказательство общей backend-инфраструктуры;
- `raspil59.ru`: обнаружен как отдельный публичный сервис распила с тем же адресом в Перми и ссылкой/контекстом мебельного workflow; общая backend-инфраструктура не подтверждена.

Партнёрские examples (`b2b.pan-raspil.ru`, `mebelevich.com`) зафиксированы как examples из публичной страницы, но не исследуются как часть PrivetMaket backend.

## Terminal state

`PARTIAL`: публичная route/product architecture map сохранена; network/API-level confirmation требуется отдельным безопасным браузерным сеансом без отправки изменяющих запросов.
