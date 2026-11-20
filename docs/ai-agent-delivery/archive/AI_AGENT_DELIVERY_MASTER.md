# AI Agent Delivery & Search Visibility — Portfolio Master Plan

Версия 1.0 · 20 ноября 2026 · DRAFT / research & planning · MPE: **EXTEND_EXISTING** (предварительное решение, до проверки портфеля).

## 1. Цель и решение MPE
Повысить доступность, корректность цитирования и реальные коммерческие заявки для публичных сайтов портфеля, не изменяя назначение закрытых приложений. Повторно использовать существующие SEO/GEO, AI Readiness, Cloudflare и GitHub. Не создавать новый репозиторий, AI-поддомен или отдельную платформу. Проверить CP-SEO-GEO-01/CP-AI-READ-01 Murat House и другие действующие наработки. Бизнес-ценность измеряется квалифицированными лидами и стоимостью, а не только цитатами. Приоритет P0 для аудита/безопасности, P1 для пилота, P2 для сложного edge. Deep-change, новые затраты и инфраструктура требуют отдельного согласия. Текущий документ не является разрешением на изменения.

## 2. Исследование рынка
| Решение | Механизм | Доказательства и ограничения |
|---|---|---|
| Akamai + Scrunch | CDN routing, упрощённый HTML и синтез релевантных материалов | +364% небрендовой видимости, +85% цитирований, +38% уникальных запросов с цитатами, +133% относительной видимости в ChatGPT; отчёт участников, не независимая гарантия [S01–S02] |
| Adobe Brand Visibility | Edge Optimize, CDN, восстановление отсутствующего агентам HTML | DEPT: 61% mention rate, 29% citation rate, 27 500 referral visits; неназванный ритейлер, смешанное вмешательство [S03–S04, S26] |
| Arm + BrightEdge Agent Edge | Verified agents получают Markdown, Googlebot и люди — обычный HTML | Подтверждён механизм из кейса вендора; сопоставимый контролируемый эффект не установлен [S05] |
| Runpod + Scrunch | Мониторинг, исправление проблем доступности и оптимизация | Четырёхкратный рост по отчёту поставщика; нельзя приписать исключительно edge [S06] |
| Cloudflare | Accept negotiation HTML → Markdown, policy, bot analytics | Доступность механизма подтверждена документацией; эффект на цитирование не гарантирован [S17–S22] |
| Netlify | Prerender для SPA | Альтернатива для доступности HTML, не доказательство эффекта AXP [S23] |

Вывод: сначала shared canonical HTML и измерения, затем native Markdown, кастомный edge только при доказанном пробеле. Не копировать коммерческий продукт целиком. Не сравнивать абсолютные метрики разных исследований без одинакового знаменателя, периода и контрольной группы.

## 3. Платформенная матрица (проверена 20.11.2026)
| Платформа | Поиск | User retrieval / browser | Обучение / контроль | Наблюдение |
|---|---|---|---|---|
| Google | Googlebot, индексируемый HTML и snippet eligibility | Не требуется специальная Markdown версия для Search | Google-Extended и отдельный Search generative AI control; проверить их области | GSC generative AI impressions, SEO reports [S07–S10] |
| OpenAI | OAI-SearchBot, официальные IP | ChatGPT-User; подписанный cloud browser отдельно | GPTBot; OAI-AdsBot только при рекламе | Тесты ChatGPT Search, referral utm_source=chatgpt.com при наличии, logs [S11–S12,S25] |
| Anthropic | Claude-SearchBot | Claude-User, Claude-Agent browser отдельно | ClaudeBot | Claude web search samples, referrals, logs [S13] |
| Microsoft | Bingbot, индекс, IndexNow | Copilot retrieval: не предполагать отдельного UA без документации | Проверить актуальные Bing snippet/AI controls перед изменением | Bing AI Performance, intents, topics, citation share, compare [S14–S15,S24] |
| Perplexity | PerplexityBot, официальные IP | Perplexity-User; правила robots для user fetch могут отличаться | Не считать поискового бота training bot; проверять документацию | Search samples, referrals, logs [S16] |

Google: руководство май 2026; с 31 августа глобальное развёртывание новых отчётов и контроля, в ноябре уточнение: Google Search не использует llms.txt. FAQ rich results больше не показываются; полезный FAQ для читателя остаётся допустим. Gemini app и Google Search AI features измерять отдельно. Bing: AI Performance февраль, расширение июнь 2026. Cloudflare: access policies и managed robots обновлены 2 ноября, Markdown — 9 ноября. Не считать API выдачу эквивалентной потребительским продуктам. Не утверждать, что все агенты запрашивают text/markdown.

## 4. Архитектура и политика хостов
Один canonical URL → исходный HTML (SSG/SSR по текущему стеку) → опциональное согласование Markdown на CDN → условный verified-agent HTML только если нужен. Браузерные агенты получают интерактивный сайт. Все варианты используют один утверждённый набор фактов. Контент не зависит от доверия к поддельному UA. Закрытые пути защищены Access/auth и origin; не превращать robots/noindex в security.

| Предварительный hostname | Класс / действие |
|---|---|
| salamat-mebel.kz | public, предлагаемый пилот |
| bek-mebel.kz, tuba.kz, murat.house | public, последующий rollout |
| murathouse.kz | возможный alias; проверить canonical и redirect |
| house.salamat-mebel.kz, ai.salamat-mebel.kz | selective/unknown до проверки назначения |
| projects.salamat-mebel.kz, tender.salamat-mebel.kz | private-кандидаты; подтвердить публичные пути отдельно |
| salamat-soft.pages.dev | unknown/possible alias; проверить текущий бренд и canonical |
| остальные *.pages.dev, *.workers.dev, Studio, admin, staging | инвентаризация, private/alias по факту; неизвестное не открывать |

Не утверждать, что домены активны или проксируются через Cloudflare без проверки. Для Bek Mebel проверить PS.kz/Plesk и DNS, не переносить CDN автоматически. Robots scope — отдельный origin; sitemap/canonical/редиректы по каждому хосту. Не разрешать wildcard на всю зону. Для публичных материалов предложено разрешить search и user retrieval, training не разрешать до согласования владельца. Cloudflare может добавлять разрешающий Content-Signal по умолчанию при Markdown conversion; определить origin header явно, сверить актуальный синтаксис и managed robots. Сигналы использования не являются технической защитой. Проверять WAF, bot policies, подписанные агенты и стоимость по тарифу, без общего bypass. Кешировать варианты раздельно; приватные ответы не кешировать публично.

## 5. Пилот и измерения
Пилот предложен на Salamat Mebel: коммерческая мебель, бюджетная мебель для аренды, кухня для собственной квартиры, существующие страницы услуг. RU/KZ, Алматы. 30–50 запросов, 5–10 URL при наличии сопоставимой контрольной группы. Baseline 2–4 недели, observation 6–8 недель ориентировочно. Разделить изменение самого текста и механизм доставки; поэтапные сравнения с контрольной группой. Не использовать одинаковые статьи на нескольких брендах. Порог +5 п.п. citation rate относительно контроля — предложение для предварительного утверждения, не обещание. Источники измерений и формулы в CP-01/06. Нулевая утечка и отсутствие критических регрессий обязательны. Внешние API и платные платформы не включать без бюджета.

## 6. Чекпоинты и зависимости
Идентификаторы CP-AID-xx относятся к данному плану; не считаются зарегистрированными в GitHub. Перед реализацией проверить фактическую нумерацию и governance. Все статусы PLANNED.

| ID | Название | Приоритет | Зависимости | Цель |
|---|---|---|---|---|
| [CP-AID-00](checkpoints/CP-AID-00.md) | Portfolio Preflight | P0 | нет | Инвентаризация и проверка существующих решений до любых изменений. |
| [CP-AID-01](checkpoints/CP-AID-01.md) | Baseline & Measurement | P0 | 00 | Создать воспроизводимый исходный уровень до изменения контента. |
| [CP-AID-02](checkpoints/CP-AID-02.md) | Host Security & Crawl Policy | P0 | 00, 01 | Разделить поиск, извлечение по запросу и обучение; закрыть внутренние поверхности. |
| [CP-AID-03](checkpoints/CP-AID-03.md) | Public Content & Canonical HTML | P1 | 02 | Сделать первичный HTML полезным для всех клиентов, прежде чем создавать варианты доставки. |
| [CP-AID-04](checkpoints/CP-AID-04.md) | Native Agent Delivery Pilot | P1 | 03 | Проверить встроенный Markdown for Agents на ограниченном публичном scope. |
| [CP-AID-05](checkpoints/CP-AID-05.md) | Conditional Edge HTML Experiment | P2 | 04 | Только при доказанном пробеле native delivery проверить ограниченный аналог AXP. |
| [CP-AID-06](checkpoints/CP-AID-06.md) | Evaluation & Rollout | P1 | 04; 05 если применим | Оценить инкрементальную пользу и расширять только подтверждённое решение. |
| [CP-AID-07](checkpoints/CP-AID-07.md) | Platform Watch & Maintenance | P1 | 06 | Поддерживать актуальность стандарта без нового сервиса по умолчанию. |

Порядок: 00 → 01 → 02 → 03 → 04 → (05 только по gate) → 06 → 07. Разрешён только read-only preflight как первый шаг по этому плану; дальнейшие записи требуют действующего разрешения. Не выполнять merge/deploy автоматически. Для каждoго CP фиксировать SHA, тесты, evidence, changed files, блокеры, независимый review. При конфликте с foundation или deep-change — остановка и явное согласие. При FAIL/CONDITIONAL блокирующего критерия следующий CP не запускать.

## 7. Ограничения и решения без явного указания
Исследованы публичные первоисточники и vendor cases, но не проведён live-аудит DNS, GitHub, Cloudflare, Search Console, Bing Webmaster Tools и реального трафика. Не подтверждены тарифы и доступы, номера CP, текущие цены и sitemap. Выбор Salamat Mebel, размеры выборки, длительность, пороги, запрет обучения по умолчанию — инженерные предложения, не утверждённые настройки. Не заявляется доказанная поддержка специального формата каждой платформой. Ни одна настройка сайта не изменена. Регулярное обновление описано, но расписание не создано.

## 8. Источники
Все ссылки проверены в исследовании 20.11.2026; кейсы поставщиков отмечены выше. Перед реализацией сверять текущую редакцию.
- S01: https://scrunch.com/case-studies/akamai-5x-brand-presence-in-ai-search-results/
- S02: https://www.akamai.com/resources/customer-story/akamai-ai-brand-presence
- S03: https://www.dept.global/case/turning-an-adobe-website-into-an-ai-ready-discovery-engine/
- S04: https://experienceleague.adobe.com/en/docs/brand-visibility/using/resources/optimize-at-edge/overview
- S05: https://help.brightedge.com/resources/case-studies/arm-agent-edge-case-study
- S06: https://scrunch.com/case-studies/
- S07: https://developers.google.com/search/docs/fundamentals/ai-optimization-guide
- S08: https://developers.google.com/search/updates?hl=en
- S09: https://support.google.com/webmasters/answer/16908024?hl=en
- S10: https://support.google.com/webmasters/answer/16984139?hl=en-GB
- S11: https://developers.openai.com/api/docs/bots
- S12: https://developers.openai.com/commerce/agent-access
- S13: https://support.claude.com/en/articles/8896518-does-anthropic-crawl-data-from-the-web-and-how-can-site-owners-block-the-crawler
- S14: https://www.bing.com/webmasters/help/ai-performance-9f8e7d6c
- S15: https://www.bing.com/indexnow
- S16: https://docs.perplexity.ai/docs/resources/perplexity-crawlers
- S17: https://developers.cloudflare.com/fundamentals/reference/markdown-for-agents/
- S18: https://developers.cloudflare.com/bots/additional-configurations/block-ai-bots/
- S19: https://developers.cloudflare.com/bots/additional-configurations/managed-robots-txt/
- S20: https://developers.cloudflare.com/bots/reference/bot-verification/web-bot-auth/
- S21: https://developers.cloudflare.com/ai-crawl-control/features/manage-ai-crawlers/
- S22: https://developers.cloudflare.com/ai-crawl-control/reference/bots/
- S23: https://docs.netlify.com/build/build-with-ai/overview/
- S24: https://blogs.bing.com/search/2026/6/New-AI-Visibility-Insights-in-Bing-Webmaster-Tools-Intents-Topics-Citation-Share-Compare/
- S25: https://help.openai.com/en/articles/12627856
- S26: https://experienceleague.adobe.com/en/docs/brand-visibility/using/resources/optimize-at-edge/cloudflare-byocdn

## 9. Полные задания чекпоинтов

---

# CP-AID-00 — Portfolio Preflight

Версия: draft 1.0 | 20.11.2026 | Статус: PLANNED | Приоритет: P0

MPE decision: EXTEND_EXISTING (предварительно, проверяется в CP-00).
ID локальный для программы; перед регистрацией сверить номера репозитория.
Зависимости: нет.

## Цель
Инвентаризация и проверка существующих решений до любых изменений.

## Задание исполнителю (Work / Codex / Arena)
- Прочитать governance, AGENTS, FOUNDATION, ARCHITECTURE, действующие CP/EXP и историю SEO/GEO, CP-AI-READ-01, CP-SEO-GEO-01; сверить фактические ID и SHA.
- Сопоставить репозитории, DNS, Cloudflare zones, proxy status, origin/hosting, routes, тарифы, Access, WAF, кеш, текущие robots и redirects; включить не только salamat-mebel.kz, bek-mebel.kz, tuba.kz, murat.house, murathouse.kz, но все обнаруженные subdomains, pages.dev, workers.dev, staging и алиасы.
- Зафиксировать hostname, owner, repo, назначение, публичные пути, canonical, политика поиска/обучения/агентов, источник истины, стоимость, неизвестные данные. Не извлекать секреты.
- Проверить реальные HTTP-ответы публичных URL, с JS и без, canonical, sitemap, языки, индексацию; закрытые URL тестировать только разрешёнными способами.
- Выявить конфликт с существующими компонентами и архитектурой, определить пилот и контроль, представить владельцу карту рисков и точные номера CP.

## Evidence / артефакты
Реестр всех обнаруженных хостов; матрица доступа и пробелов; evidence HTTP/DNS, SHA и источники; список недоступных данных; утверждённый scope пилота.

## Критерии приёмки
Ни один неизвестный хост не получает разрешение по умолчанию; проверены имеющиеся CP; read-only.

## Governance и остановка
Читать актуальные правила проекта до работы. Не создавать новый репозиторий, платные ресурсы или менять фундаментальную архитектуру без отдельного согласия. Не выполнять merge/deploy, изменение DNS/WAF/Access и секретов без разрешения согласно действующим правилам. Сохранять точный SHA, scope, список файлов, команды и результаты тестов, блокеры, rollback. Статус PASS / CONDITIONAL / BLOCKED / SKIPPED; независимое принятие. Не переходить к следующему CP при блокере.

## Источники (проверены 20.11.2026)
- S07: https://developers.google.com/search/docs/fundamentals/ai-optimization-guide
- S17: https://developers.cloudflare.com/fundamentals/reference/markdown-for-agents/
- S18: https://developers.cloudflare.com/bots/additional-configurations/block-ai-bots/
- S21: https://developers.cloudflare.com/ai-crawl-control/features/manage-ai-crawlers/

---

# CP-AID-01 — Baseline & Measurement

Версия: draft 1.0 | 20.11.2026 | Статус: PLANNED | Приоритет: P0

MPE decision: EXTEND_EXISTING (предварительно, проверяется в CP-00).
ID локальный для программы; перед регистрацией сверить номера репозитория.
Зависимости: 00.

## Цель
Создать воспроизводимый исходный уровень до изменения контента.

## Задание исполнителю (Work / Codex / Arena)
- 30–50 фиксированных запросов RU/KZ: кухни, аренда, шкафы, торговое оборудование, локальные запросы; брендовые отдельно от небрендовых. Одинаковая география Алматы, язык, режим поиска, дата, модель/поверхность, повторения.
- 5–10 целевых URL и сопоставимые контрольные URL с близкими темами/трафиком; исходное окно 2–4 недели по возможности. Новые статьи без истории выделить отдельно.
- GSC Generative AI performance (показы; отсутствие отчёта ≠ ноль), Bing AI Performance (цитаты, grounding queries, темы, доля), Cloudflare traffic, аналитика рефералов и лидов; проверить доступность аккаунтов.
- CSV/JSONL: run_id, query_id, language, region, platform, mode, timestamp, eligible, brand_mention, citations[], competitor_mentions, error, evidence_ref. Лиды без PII, источник/UTM и ограничение атрибуции WhatsApp.
- Оценить бюджет, частоту ручной проверки и разрешённость API; API и потребительские ответы не смешивать. Нет скрейпинга закрытых интерфейсов или обхода лимитов.

## Evidence / артефакты
Версионированный набор запросов, контрольная группа, сырые обезличенные данные, baseline, методика и критерии решения.

## Критерии приёмки
У каждого наблюдения есть дата и знаменатель; ошибки отдельно, нулевые значения не подставлены вместо недоступных данных.

## Governance и остановка
Читать актуальные правила проекта до работы. Не создавать новый репозиторий, платные ресурсы или менять фундаментальную архитектуру без отдельного согласия. Не выполнять merge/deploy, изменение DNS/WAF/Access и секретов без разрешения согласно действующим правилам. Сохранять точный SHA, scope, список файлов, команды и результаты тестов, блокеры, rollback. Статус PASS / CONDITIONAL / BLOCKED / SKIPPED; независимое принятие. Не переходить к следующему CP при блокере.

## Источники (проверены 20.11.2026)
- S10: https://support.google.com/webmasters/answer/16984139?hl=en-GB
- S14: https://www.bing.com/webmasters/help/ai-performance-9f8e7d6c
- S24: https://blogs.bing.com/search/2026/6/New-AI-Visibility-Insights-in-Bing-Webmaster-Tools-Intents-Topics-Citation-Share-Compare/
- S25: https://help.openai.com/en/articles/12627856
- S01: https://scrunch.com/case-studies/akamai-5x-brand-presence-in-ai-search-results/

---

# CP-AID-02 — Host Security & Crawl Policy

Версия: draft 1.0 | 20.11.2026 | Статус: PLANNED | Приоритет: P0

MPE decision: EXTEND_EXISTING (предварительно, проверяется в CP-00).
ID локальный для программы; перед регистрацией сверить номера репозитория.
Зависимости: 00, 01.

## Цель
Разделить поиск, извлечение по запросу и обучение; закрыть внутренние поверхности.

## Задание исполнителю (Work / Codex / Arena)
- Для каждого hostname утвердить классы public/selective/private/alias/unknown. Default deny для private/unknown; selective — явный allowlist публичных путей.
- Проверить robots.txt по каждому origin, GSC generative AI control, Google-Extended, Bing index/snippet controls, Cloudflare managed robots/Bot Preference Sync и конфликт правил.
- Рекомендация, не согласованная политика: публичный поиск разрешить, пользовательское чтение разрешить на публичных GET/HEAD, обучение запретить до решения владельца. Не полагаться на robots как на защиту.
- Проверять идентичность через verified bot / официальные IP/DNS/подпись там, где доступно; UA — лишь признак. Не давать blanket WAF skip, не обходить Access, не публиковать API/admin/preview.
- Проверить редиректы технических дублей или noindex для публичных дублей по ситуации; приватные зеркала закрыть авторизацией. Robots disallow не удаляет уже индексированный URL гарантированно.
- Сделать экспорт текущих правил и обратимый план; до изменения продакшена получить разрешение в соответствии с governance.

## Evidence / артефакты
Матрица bot × host × path, diff, backup, результаты негативных тестов (поддельный UA, анонимный доступ, приватный path, origin bypass).

## Критерии приёмки
0 приватных данных в ответах; поиск публичных страниц не блокируется ошибочно; 401/403 или авторизация для закрытых путей; rollback проверен.

## Governance и остановка
Читать актуальные правила проекта до работы. Не создавать новый репозиторий, платные ресурсы или менять фундаментальную архитектуру без отдельного согласия. Не выполнять merge/deploy, изменение DNS/WAF/Access и секретов без разрешения согласно действующим правилам. Сохранять точный SHA, scope, список файлов, команды и результаты тестов, блокеры, rollback. Статус PASS / CONDITIONAL / BLOCKED / SKIPPED; независимое принятие. Не переходить к следующему CP при блокере.

## Источники (проверены 20.11.2026)
- S09: https://support.google.com/webmasters/answer/16908024?hl=en
- S11: https://developers.openai.com/api/docs/bots
- S12: https://developers.openai.com/commerce/agent-access
- S13: https://support.claude.com/en/articles/8896518-does-anthropic-crawl-data-from-the-web-and-how-can-site-owners-block-the-crawler
- S16: https://docs.perplexity.ai/docs/resources/perplexity-crawlers
- S18: https://developers.cloudflare.com/bots/additional-configurations/block-ai-bots/
- S19: https://developers.cloudflare.com/bots/additional-configurations/managed-robots-txt/
- S20: https://developers.cloudflare.com/bots/reference/bot-verification/web-bot-auth/
- S22: https://developers.cloudflare.com/ai-crawl-control/reference/bots/

---

# CP-AID-03 — Public Content & Canonical HTML

Версия: draft 1.0 | 20.11.2026 | Статус: PLANNED | Приоритет: P1

MPE decision: EXTEND_EXISTING (предварительно, проверяется в CP-00).
ID локальный для программы; перед регистрацией сверить номера репозитория.
Зависимости: 02.

## Цель
Сделать первичный HTML полезным для всех клиентов, прежде чем создавать варианты доставки.

## Задание исполнителю (Work / Codex / Arena)
- Аудит SSG/SSR/prerender текущего стека; использовать существующие шаблоны, не переписывать приложение.
- В исходном HTML должны присутствовать название, услуги, география, цены с датой/условиями, материалы, сроки только подтверждённые, контакт, примеры и ссылки. Реальные фото с alt, разрешением на публикацию и корректными URL.
- RU/KZ — отдельные корректные локализованные URL при необходимости, self-canonical, hreflang только для эквивалентных страниц; семантические headings, таблицы, внутренние ссылки.
- Schema.org Organization/LocalBusiness, Service, Article, BreadcrumbList, Product/Offer лишь при соответствии реальным товарам/ценам; не добавлять фальшивые отзывы, не обещать FAQ rich results.
- Проверить Google Business Profile и Bing Places, NAP, sitemap lastmod только при реальном изменении, IndexNow после публикации (если поддерживается), корректные 404/redirect.
- Пилот: коммерческая мебель, бюджетная мебель для аренды, кухня для собственной квартиры; не публиковать старый прайс автоматически. Не дублировать одинаковые статьи по всем брендам.

## Evidence / артефакты
Diff существующего контента, parity manifest фактов, список URL, результаты проверки HTML без JS, structured data, sitemap, canonical и mobile.

## Критерии приёмки
Все критические факты доступны посетителю и в initial HTML; нет фиктивных сведений; контрольная группа не изменена без фиксации.

## Governance и остановка
Читать актуальные правила проекта до работы. Не создавать новый репозиторий, платные ресурсы или менять фундаментальную архитектуру без отдельного согласия. Не выполнять merge/deploy, изменение DNS/WAF/Access и секретов без разрешения согласно действующим правилам. Сохранять точный SHA, scope, список файлов, команды и результаты тестов, блокеры, rollback. Статус PASS / CONDITIONAL / BLOCKED / SKIPPED; независимое принятие. Не переходить к следующему CP при блокере.

## Источники (проверены 20.11.2026)
- S07: https://developers.google.com/search/docs/fundamentals/ai-optimization-guide
- S08: https://developers.google.com/search/updates?hl=en
- S15: https://www.bing.com/indexnow
- S23: https://docs.netlify.com/build/build-with-ai/overview/

---

# CP-AID-04 — Native Agent Delivery Pilot

Версия: draft 1.0 | 20.11.2026 | Статус: PLANNED | Приоритет: P1

MPE decision: EXTEND_EXISTING (предварительно, проверяется в CP-00).
ID локальный для программы; перед регистрацией сверить номера репозитория.
Зависимости: 03.

## Цель
Проверить встроенный Markdown for Agents на ограниченном публичном scope.

## Задание исполнителю (Work / Codex / Arena)
- Проверить доступность и ограничения функции в фактическом тарифе/zone; применять Configuration Rules по точному hostname и allowlist путей, не включать глобально.
- Согласовать Content-Signal; проверить заголовок на origin и в HTML/Markdown, managed robots. Cloudflare может добавлять разрешающее обучение значение по умолчанию, если origin его не задаёт.
- Выполнить GET с Accept: text/html и Accept: text/markdown, сравнить status, тип, Vary, кеш, canonical/ссылки, основные факты и JSON-LD; оценить размер и время ответа.
- Тестировать неизвестный UA, смешанный Accept, 404, 301, cookies, авторизацию, query, gzip, cache warm/cold, повтор запросов в обратном порядке; сохранять реальные evidence без секретов.
- Проверить реальные журналы запросов: есть ли целевые платформы, запрашивающие Markdown. Синтетический curl доказывает доступность формата, но не использование платформой.
- Rollback: отключить только пилотное правило, при необходимости очистить только затронутый кеш; обычный HTML остаётся рабочим.

## Evidence / артефакты
Матрица тестов HTML/MD, конфигурационный diff, замеры, журналы и rollback evidence.

## Критерии приёмки
0 утечек, 0 подмен фактов, корректные варианты кеша; при отсутствии Markdown fallback в HTML; нет необоснованного утверждения о росте цитат.

## Governance и остановка
Читать актуальные правила проекта до работы. Не создавать новый репозиторий, платные ресурсы или менять фундаментальную архитектуру без отдельного согласия. Не выполнять merge/deploy, изменение DNS/WAF/Access и секретов без разрешения согласно действующим правилам. Сохранять точный SHA, scope, список файлов, команды и результаты тестов, блокеры, rollback. Статус PASS / CONDITIONAL / BLOCKED / SKIPPED; независимое принятие. Не переходить к следующему CP при блокере.

## Источники (проверены 20.11.2026)
- S17: https://developers.cloudflare.com/fundamentals/reference/markdown-for-agents/
- S18: https://developers.cloudflare.com/bots/additional-configurations/block-ai-bots/
- S19: https://developers.cloudflare.com/bots/additional-configurations/managed-robots-txt/

---

# CP-AID-05 — Conditional Edge HTML Experiment

Версия: draft 1.0 | 20.11.2026 | Статус: PLANNED | Приоритет: P2

MPE decision: EXTEND_EXISTING (предварительно, проверяется в CP-00).
ID локальный для программы; перед регистрацией сверить номера репозитория.
Зависимости: 04.

## Цель
Только при доказанном пробеле native delivery проверить ограниченный аналог AXP.

## Задание исполнителю (Work / Codex / Arena)
- Gate: если первоначальный HTML уже доступен или агенты не испытывают проблем, пропустить CP. Не создавать новый repo/Worker без проверки переиспользования, архитектуры и согласия при deep-change/затратах.
- Использовать существующий build/SSR/Worker/HTMLRewriter если пригоден. Единый источник контента; только чистый HTML с теми же публичными фактами, без скрытых рекламных утверждений и автоматически придуманных ответов.
- Применять к разрешённым GET/HEAD и проверенным retrieval-агентам; Googlebot/Bingbot и браузерные агенты получают стандартный HTML. Не основывать доступ на одном User-Agent. Не применять к protected маршрутам, формам или API.
- Изолировать CDN/cache key по варианту и hostname/path; для персонализированных ответов исключить общий кеш. Не рассчитывать только на Vary при кастомной конфигурации. Сохранять статус, security headers, robots/canonical, ссылки, media metadata.
- Автоматический semantic parity test и негативные тесты; ограничение трафика, fail-open к исходному публичному HTML при ошибке преобразования, fail-closed для приватных путей.
- Отдельная группа сравнения с native-only; не менять одновременно тексты и delivery без маркировки. Не имитировать браузер/бот для обхода защиты.

## Evidence / артефакты
ADR с gate, технический diff, тесты parity/security/cache, ограничения стоимости, механизм выключения и результаты независимого review.

## Критерии приёмки
0 критических регрессий, подтверждённая потребность, независимый review PASS и отдельное согласие на релиз; иначе SKIPPED/HOLD.

## Governance и остановка
Читать актуальные правила проекта до работы. Не создавать новый репозиторий, платные ресурсы или менять фундаментальную архитектуру без отдельного согласия. Не выполнять merge/deploy, изменение DNS/WAF/Access и секретов без разрешения согласно действующим правилам. Сохранять точный SHA, scope, список файлов, команды и результаты тестов, блокеры, rollback. Статус PASS / CONDITIONAL / BLOCKED / SKIPPED; независимое принятие. Не переходить к следующему CP при блокере.

## Источники (проверены 20.11.2026)
- S01: https://scrunch.com/case-studies/akamai-5x-brand-presence-in-ai-search-results/
- S04: https://experienceleague.adobe.com/en/docs/brand-visibility/using/resources/optimize-at-edge/overview
- S05: https://help.brightedge.com/resources/case-studies/arm-agent-edge-case-study
- S17: https://developers.cloudflare.com/fundamentals/reference/markdown-for-agents/
- S20: https://developers.cloudflare.com/bots/reference/bot-verification/web-bot-auth/
- S26: https://experienceleague.adobe.com/en/docs/brand-visibility/using/resources/optimize-at-edge/cloudflare-byocdn

---

# CP-AID-06 — Evaluation & Rollout

Версия: draft 1.0 | 20.11.2026 | Статус: PLANNED | Приоритет: P1

MPE decision: EXTEND_EXISTING (предварительно, проверяется в CP-00).
ID локальный для программы; перед регистрацией сверить номера репозитория.
Зависимости: 04; 05 если применим.

## Цель
Оценить инкрементальную пользу и расширять только подтверждённое решение.

## Задание исполнителю (Work / Codex / Arena)
- Наблюдение 6–8 недель ориентировочно, одинаковый протокол тестовой и контрольной группы. Сравнить изменения до/после между группами; указать сезонность, алгоритмические изменения, малые выборки и разброс.
- Mention rate = ответы с брендом / валидные ответы; citation rate = ответы с ссылкой на собственный canonical / валидные ответы; share of voice = упоминания бренда / суммарные упоминания фиксированного набора конкурентов (отдельно определить правила счёта).
- Раздельно: GSC показы, Bing citation counts, verified crawler hits, AI referral sessions, квалифицированные лиды, расходы/lead. Не приравнивать упоминания к продажам.
- Предложенный gate: положительное изменение citation rate относительно контроля (ориентир +5 п.п., если baseline позволяет), стабильность обычного SEO и UX, 0 security/parity regressions; достаточно наблюдений и подтверждение на повторных замерах. Порог утвердить до теста, при неопределённости продлить или остановить.
- При PASS переносить только одобренный компонент по одному hostname; сначала другие публичные коммерческие домены, затем public paths смешанных. Алиасы и закрытые хосты исключены.
- Отдельный отчёт владелец/ревьюер; не считать CP принятым по самооценке исполнителя.

## Evidence / артефакты
Отчёт с абсолютными числами, знаменателями, сравнением групп, стоимостью, ограничениями, решением expand/hold/rollback и журналом rollout.

## Критерии приёмки
Владелец утверждает вывод; изменения по одному хосту с rollback; при ухудшении безопасности немедленный откат.

## Governance и остановка
Читать актуальные правила проекта до работы. Не создавать новый репозиторий, платные ресурсы или менять фундаментальную архитектуру без отдельного согласия. Не выполнять merge/deploy, изменение DNS/WAF/Access и секретов без разрешения согласно действующим правилам. Сохранять точный SHA, scope, список файлов, команды и результаты тестов, блокеры, rollback. Статус PASS / CONDITIONAL / BLOCKED / SKIPPED; независимое принятие. Не переходить к следующему CP при блокере.

## Источники (проверены 20.11.2026)
- S01: https://scrunch.com/case-studies/akamai-5x-brand-presence-in-ai-search-results/
- S10: https://support.google.com/webmasters/answer/16984139?hl=en-GB
- S14: https://www.bing.com/webmasters/help/ai-performance-9f8e7d6c
- S24: https://blogs.bing.com/search/2026/6/New-AI-Visibility-Insights-in-Bing-Webmaster-Tools-Intents-Topics-Citation-Share-Compare/
- S25: https://help.openai.com/en/articles/12627856

---

# CP-AID-07 — Platform Watch & Maintenance

Версия: draft 1.0 | 20.11.2026 | Статус: PLANNED | Приоритет: P1

MPE decision: EXTEND_EXISTING (предварительно, проверяется в CP-00).
ID локальный для программы; перед регистрацией сверить номера репозитория.
Зависимости: 06.

## Цель
Поддерживать актуальность стандарта без нового сервиса по умолчанию.

## Задание исполнителю (Work / Codex / Arena)
- Раз в месяц и перед очередным rollout проверять официальные changelog Google, OpenAI, Anthropic, Microsoft, Perplexity, Cloudflare; новые форматы и агенты проверять прежде чем менять allowlist.
- Версионировать source registry: URL, дата проверки, статус, изменение, затронутые hosts, необходимость approval. Фиксировать изменения IP/DNS/подписей и managed rules.
- Проверять robots, sitemap, цены, canonical, redirects, публичный HTML, Markdown и приватные пути после деплоя; интегрировать в существующие CI checks, если совместимо.
- Отчёт месячного состояния и инцидентов; переиспользовать существующий Dashboard только для агрегированного read-only статуса после проверки архитектуры. Не строить новую платформу аналитики без отдельного фильтра.
- Новые стандарты (MCP, commerce protocols, browser actions) рассматривать отдельно: они не являются обязательным условием цитирования и не должны открывать внутренние API.

## Evidence / артефакты
Журнал обновлений, набор регрессионных проверок, owner и периодичность; предложение изменений с diff.

## Критерии приёмки
Нет незадокументированных policy changes; все источники датированы; секреты не попадают в evidence.

## Governance и остановка
Читать актуальные правила проекта до работы. Не создавать новый репозиторий, платные ресурсы или менять фундаментальную архитектуру без отдельного согласия. Не выполнять merge/deploy, изменение DNS/WAF/Access и секретов без разрешения согласно действующим правилам. Сохранять точный SHA, scope, список файлов, команды и результаты тестов, блокеры, rollback. Статус PASS / CONDITIONAL / BLOCKED / SKIPPED; независимое принятие. Не переходить к следующему CP при блокере.

## Источники (проверены 20.11.2026)
- S07: https://developers.google.com/search/docs/fundamentals/ai-optimization-guide
- S08: https://developers.google.com/search/updates?hl=en
- S11: https://developers.openai.com/api/docs/bots
- S12: https://developers.openai.com/commerce/agent-access
- S13: https://support.claude.com/en/articles/8896518-does-anthropic-crawl-data-from-the-web-and-how-can-site-owners-block-the-crawler
- S14: https://www.bing.com/webmasters/help/ai-performance-9f8e7d6c
- S16: https://docs.perplexity.ai/docs/resources/perplexity-crawlers
- S17: https://developers.cloudflare.com/fundamentals/reference/markdown-for-agents/
- S18: https://developers.cloudflare.com/bots/additional-configurations/block-ai-bots/
- S20: https://developers.cloudflare.com/bots/reference/bot-verification/web-bot-auth/