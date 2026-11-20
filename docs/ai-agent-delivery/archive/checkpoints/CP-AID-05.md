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