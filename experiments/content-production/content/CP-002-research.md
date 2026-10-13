---
id: CP-002
title: "Есть ли у Казахстана собственная языковая модель?"
state: RESEARCH_DRAFT
publication: BLOCKED_PENDING_FACTCHECK
date: 2026-10-13
---
# CP-002 — Казахский язык, корпус и национальная LLM

## Investigative hook
Несколько лет назад поиск машиночитаемого корпуса казахского языка вывел автора на исследовательские работы Назарбаев Университета. Сегодня страна объявляет о национальной KazLLM. Как связаны эти проекты, кому доступны данные и что значит «собственная» LLM?

## Confirmed research leads (with source links)
1. 2013, *Assembling the Kazakh Language Corpus*, Olzhas Makhambetov, Aibek Makazhanov et al.; проект корпуса более 135 млн слов, аннотированный подкорпус отдельно. https://research.nu.edu.kz/en/publications/assembling-the-kazakh-language-corpus/
2. Public extract of old KLC: kazcorpus-news, 55,352 docs / 14,939,567 alphabetic tokens (repository README). https://github.com/makazhan/kazcorpus-news
3. ISSAI KazLLM launched Dec 2024, 8B/70B, derivative of Meta Llama 3.1; license CC-BY-NC, not Qwen according to official model docs. https://issai.nu.edu.kz/kazllm/ and https://huggingface.co/issai/LLama-3.1-KazLLM-1.0-70B
4. ISSAI sources claim >150B multilingual training tokens, ~95% assembled/curated by its team; source overlap with 2013 corpus unverified. https://issai.nu.edu.kz/ru/kazllm-rus/
5. ISSAI Feb 2026 statement: research team says it transferred a non-exclusive license to Astana Hub in Dec 2024 and does not know downstream commercial deployments. https://issai.nu.edu.kz/2026/02/13/issai-explains-kazllm-why-kazakhstan-built-its-own-large-language-model/
6. Kazakh National Corpus separately claims 250M word usages; do not conflate it with KLC or KazLLM training set. https://qazcorpus.kz/header/jalpyMalimeten.php
7. Government announcement says 148B tokens, apparently differing from ISSAI >150B wording; resolve dataset version/date. https://www.gov.kz/memleket/entities/aidc/press/news/details/902638?lang=ru

## Questions to verify
- Was the user's remembered researcher Olzhas Makhambetov, Aibek Makazhanov, or another scholar? Check dissertations/affiliations; do not infer a PhD.
- Where is the complete 2013 corpus today? Licenses, download/API, annotated portion quality and reuse.
- Did KazLLM train on KLC 2013 or other national corpora? Ask ISSAI, the original KLC authors and data owners; do not assert reuse without evidence.
- What exactly was trained: continued pretraining / SFT of Llama weights versus training from random initialization? Inspect technical report, model card, and code.
- Which models labelled national/Kazakh use Llama, Qwen, other foundations? Specify project and version instead of generalized allegation.
- What rights belong to Kazakhstan, Astana Hub, NU, sponsors, and downstream users?
- What are procurement/funding and verified performance against baselines on reproducible Kazakh tests?
- What commercial use rights exist under KazLLM licenses?

## Suggested article acts
1. Personal search for a Kazakh NLP corpus years ago
2. 2013 KLC and work of early researchers
3. What a corpus actually is, why annotation matters; corpora vs model weights
4. The 2024 KazLLM announcement and Meta Llama lineage
5. 'National' may mean domestic adaptation and know-how rather than training from zero
6. Unanswered question: did older public linguistic infrastructure feed newer models?
7. Who owns, maintains, and can freely use both data and models?
8. Ending: sovereignty means reproducible, accessible and maintainable language infrastructure, not just branding

## Editorial safety
- No allegation of Qwen being secretly used for KazLLM without direct evidence.
- Distinguish 'architecture from Llama' vs 'weights adapted from Llama' after model artifacts review.
- Attribute sponsorship and government funding to specified project and timeframe, not all Kazakh AI programs.
- Seek comment from ISSAI, Astana Hub, KLC authors, ministries.
- Final publication only after fact-check and author approval.
