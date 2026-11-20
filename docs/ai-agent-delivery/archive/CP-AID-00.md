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