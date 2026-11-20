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