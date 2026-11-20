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