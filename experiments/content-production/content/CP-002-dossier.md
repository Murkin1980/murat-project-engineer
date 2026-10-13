# CP-002 — Исследовательское досье: Казахский корпус → KazNLP → KazLLM
Дата среза: 2026-10-13. Статус: RESEARCH / NO ARTICLE / NO CONTACT SENT.
MPE disposition: EXTEND_EXISTING (сохранение в уже открытой content-production ветке, без нового repo или runtime).

## Задача исследования
Восстановить происхождение KLC (2013), его техническую, юридическую и кадровую судьбу; проследить проекты KazNLP и KazLLM и проверить **наличие документированной связи между данными**. Исходная гипотеза о «китайской Qwen под капотом» не доказана; доступная документация KazLLM указывает на Llama 3.1. Не смешивать корпус, дообучение базовой LLM и обучение с нуля.

## Каталог источников: сохранены URL назначений
Реестр ниже включает подтверждённые научные публикации, первичные источники и исследовательские входы. Факт существования ссылки не гарантирует, что она ведёт к полному открыто лицензированному набору данных.

| ID | Источник / предмет | URL | Значение |
|---|---|---|---|
| S01 | KLC, EMNLP 2013, карточка в ACL Anthology | https://aclanthology.org/D13-1104/ | Исходная публикация, все шесть авторов |
| S02 | KLC, исходный PDF | https://aclanthology.org/D13-1104.pdf | Аннотация, метод, исторические университетские email |
| S03 | KLC, университетская карточка | https://research.nu.edu.kz/en/publications/assembling-the-kazakh-language-corpus/ | Подтверждение исследовательской аффилиации |
| S04 | KLC, ResearchGate копия | https://www.researchgate.net/publication/264545351_Assembling_the_Kazakh_Language_Corpus | Публикация загружена участником исследования |
| S05 | Новостной подкорпус KLC, репозиторий | https://github.com/makazhan/kazcorpus-news | 55 352 документа, 14 939 567 токенов; условия смотреть в LICENSE |
| S06 | Инструменты KazNLP | https://github.com/makazhan/kaznlp | Исходники проекта NLP, лицензии проверить |
| S07 | Профиль Makazhanov на GitHub | https://github.com/makazhan | Другие датасеты и репозитории |
| S08 | KazNLP, NU, SPECOM 2020 | https://research.nu.edu.kz/en/publications/kaznlp-a-pipeline-for-automated-processing-of-texts-written-in-ka/ | Авторский состав и функциональность |
| S09 | KazNLP DOI / издатель | https://doi.org/10.1007/978-3-030-60276-5_63 | Сборник Springer |
| S10 | Character-Aware Neural Morphological Disambiguation, ACL 2017 | https://aclanthology.org/P17-2105/ | Развитие методов морфологического анализа |
| S11 | Manual vs Automatic Bitext Extraction, LREC 2018 | https://aclanthology.org/L18-1606/ | Параллельные корпуса |
| S12 | Sign Language Corpus Retrospective, LREC-COLING 2024 | https://aclanthology.org/2024.signlang-1.12/ | Продолжение сотрудничества Макажанова и Есенбаева, отдельная языковая область |
| S13 | PDF публикации 2024 | https://aclanthology.org/2024.signlang-1.12.pdf | Аффилиации и адреса исследователей на момент публикации |
| S14 | Edinburgh 2022 thesis, университетский архив | https://era.ed.ac.uk/handle/1842/43060 | Context restriction for low resource neural morphological analysis |
| S15 | GitHub диссертационной работы 2021, MPhil (указание автора) | https://github.com/makazhan/uoe-mphil_thesis | ВАЖНО: не называть работу PhD без отдельного подтверждения |
| S16 | ISSAI KazLLM | https://issai.nu.edu.kz/kazllm/ | Национальная модель, история и происхождение |
| S17 | Модель KazLLM на Hugging Face | https://huggingface.co/issai/LLama-3.1-KazLLM-1.0-70B | Проверить базу, ограничения лицензии, модельную карточку |
| S18 | ISSAI объяснение от 2026-02-13 | https://issai.nu.edu.kz/2026/02/13/issai-explains-kazllm-why-kazakhstan-built-its-own-large-language-model/ | Передача неисключительной лицензии Astana Hub |
| S19 | Национальный корпус (отдельный проект) | https://qazcorpus.kz/header/jalpyMalimeten.php | Не отождествлять с KLC |
| S20 | Government announcement KazLLM | https://www.gov.kz/memleket/entities/aidc/press/news/details/902638?lang=ru | Официальные заявления, проверить версию датасета |

## Карта шести участников KLC 2013 и контактные пути
Публичные адреса ниже опубликованы самими авторами в PDF 2013 года; **исторические, работоспособность неизвестна**.
- Olzhas Makhambetov: omakhambetov@nu.edu.kz; ACL https://aclanthology.org/people/olzhas-makhambetov/unverified/ ; имя в LinkedIn-каталоге https://www.linkedin.com/pub/dir/%2B/Makhambetov (идентичность без точного профиля не подтверждена). Нынешняя работа неизвестна.
- Aibek Makazhanov: aibek.makazhanov@nu.edu.kz; GitHub https://github.com/makazhan ; LinkedIn https://kz.linkedin.com/in/aibek-makazhanov-63aa0061 ; ResearchGate https://www.researchgate.net/publication/264545351_Assembling_the_Kazakh_Language_Corpus . LinkedIn показывает Smartcall; срок актуальности работодателя требует прямой проверки. Высокий приоритет для первого контакта.
- Zhandos Yessenbayev: zhyessenbayev@nu.edu.kz; официальный BINUS https://international.binus.ac.id/binus-people/zhandos-yessenbayev-b-sc-m-sc-ph-d/ ; также https://international.binus.ac.id/computer-science/binus-people/zhandos-yessenbayev-ph-d/ . BINUS: Subject Content Coordinator, официальная страница — сильный академический канал контакта. Высокий приоритет.
- Bakhyt Matkarimov: bmatkarimov@nu.edu.kz; NU https://research.nu.edu.kz/en/persons/bakhyt-matkarimov/ (официальный профиль, PhD, Leading Researcher, Laboratory of biosensors and bioinstruments). Приоритет как участника и институционального проводника.
- Islam Sabyrgaliyev: islam.sabyrgaliyev@nu.edu.kz; LinkedIn https://kz.linkedin.com/in/isabyr ; указан SmartVend, видна активность в профессиональных постах 2026; работодатель не подтверждён непосредственно. Возможный комфортный канал — LinkedIn.
- Anuar Sharafudinov: anuar.sharaphudinov@nu.edu.kz (именно это написание в авторском PDF); профиль ACL https://aclanthology.org/people/anuar-sharafudinov/unverified/ . Современный работодатель и идентифицированный публичный профиль не найдены.

**Социальная публичность:** наличие LinkedIn активности ≠ согласие выступать публично. Подтверждённых Facebook или Reddit профилей у этих шести авторов пока нет; не приписывать однофамильцев. Не собирать личные телефоны, непубличные адреса или несанкционированные сведения.

## Заметка о квалификациях
Эдинбургский архив 2022 использует слово thesis, но это само по себе НЕ доказывает PhD. Авторский GitHub прямо указывает MPhil defended 2021. Отдельно удостоверить вид степени, дату и отношение к депонированному PDF.

## Неразрешённые исследовательские узлы
1. Полная версия KLC: нынешний владелец, копии, лицензия, корпусная аннотация и доступ.
2. Связь KLC 2013 → KazNLP 2020: какие тексты/разметка фактически повторно использованы?
3. Связь KLC/KazNLP → ISSAI KazLLM: записи о датасетах, дата-линейдж, авторское подтверждение.
4. Доля казахского, русскоязычного и английского материала в KazLLM; происхождение Llama весов и этапы continued pretraining vs SFT.
5. Национальная модель: правовой статус, некоммерческая лицензия, коммерческое развёртывание Astana Hub, модельные карточки, метрики сравнения.
6. Архив PhD/MPhil и научная биография каждого автора; оригинальная NU research page — не обязательно диссертация.
7. Пользовательская история: установить, какого именно автора пользователь обнаружил несколько лет назад, не утверждая это заранее.
8. Версии, даты и владельцы упомянутых наборов данных; не смешивать 135 млн слов, 250 млн словоупотреблений и 150 млрд токенов.

## План этапов (NO OUTREACH YET)
R1: библиографическая полнота и скачивание разрешённых первичных работ; сохранить source_id/даты/постоянные URL.
R2: техническая реконструкция корпуса и дата-линейджа, проверка открытого доступа.
R3: исследовательская карта авторов и публикаций, уточнение академических степеней и аффилиаций.
R4: реестр пробелов и вопросов по каждому автору с источниками; подготовить нейтральный запрос на интервью.
R5: только после явного согласия автора проекта — адресное обращение к исследователям по их публичным каналам.
R6: полученные ответы, право цитирования и редакционная сверка; только после этого написать мастер-статью и сценарий.

## Черновая структура будущего материала (НЕ писать пока)
Личная точка входа → корпус 2013 → карта участников → развитие инструментов → революция трансформеров → модель KazLLM → собственность и лицензии → проверенная линия данных → выводы с обозначенными неизвестными.

Предпочтение контакта по теме: Makazhanov (GitHub/LinkedIn), Yessenbayev (BINUS/academia), Sabyrgaliyev (активный LinkedIn), Matkarimov (официальный NU); остальных искать дальше. Не делать психологических выводов об их желании общаться.
