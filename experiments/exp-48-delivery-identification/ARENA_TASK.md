# EXP-48 — Доставка и идентификация

## Primary disposition

**EXTEND_EXISTING**

## CP-01 — Контрольный снимок и извлечение полей

После отдельного разрешения владельца зафиксировать утверждённый публичный HTML-снимок, его SHA, регион, язык, версию клиента и список ожидаемых полей. Сравнить HTML с одной эквивалентной версией за проход по методу README. Передать независимому Codex контроль, образцы ответов, обезличенный журнал ошибок, долю верных полей, байты, время и затраты. Отдельно отмечать неподтверждённые запросы.

## Scope stop rules

- Await separate owner authorization for Arena and an agreed time and cost ceiling.
- Stop if the approved public snapshot or matched control is unavailable.
- Stop before changes to production, disclosure of private data or paid calls outside the approved ceiling.

## Approved inputs for CP-01

Owner approved the public root of salamat-mebel.kz, 30 minutes and $0 additional cost. Use the frozen files in evidence/cp-01. Present only one artifact per isolated trial, with the same client, locale, region and prompt: «Извлеки название бренда, город, основной заголовок страницы и количество лет опыта с указанным квалификатором. Верни только четыре поля JSON». The answer key is for the reviewer alone. Record original responses, elapsed time, UTF-8 output bytes and correct fields out of four separately per arm.
e70b9a19cd0ee34500eea2d6e9fa8bbaa0ef8d574203afa37225cb83f6b8c443  control.html
45a919e42c40b0c2fe8131c44fd22d064ec96bfb110a88e0a32a503cc1d205c3  variant.md
