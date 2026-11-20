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