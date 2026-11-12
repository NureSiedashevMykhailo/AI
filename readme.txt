========================================================================
ДИСЦИПЛІНА: ШТУЧНИЙ ІНТЕЛЕКТ У ПРОГРАМНІЙ ІНЖЕНЕРІЇ (ШуПІ)
Проєкт: Mini Issue Tracker
Виконавець: Студент гр. ПЗПІ-23-9 Сєдашев Михайло (Siedashev Mykhailo)
Репозиторій: https://github.com/NureSiedashevMykhailo/AI
========================================================================

------------------------------------------------------------------------
ЧАСТИНА I. ЛАБОРАТОРНА РОБОТА №01 (Tag: lab01-spec)
Тема: Вимоги та проєктування з AI-асистентом. Від неструктурованого
      запиту замовника до перевірюваної специфікації
Каталог артефактів: docs/
Зовнішній аудит і верифікація (ChatGPT Review):
https://chatgpt.com/share/6aeb09ee-cbf8-83eb-be5f-f7d017623845
------------------------------------------------------------------------

1. docs/requirements.md (v1.0 APPROVED — Single Source of Truth)
   - Межі MVP (FR-01 – FR-07, резерв FR-08 на ЛР4), виключення (Out of Scope) та журнал
     уточнень вимог (Рішення замовника vs Технічні рішення автора).
   - Нефункціональні вимоги (NFR-01 – NFR-04) із розмежуванням встановлення та автономного
     рантайму й ізоляцією тестової БД (tmp_path / :memory:).
   - 8 User Stories (US-01 – US-07 для MVP та US-08 для Future/LR4) і 19 атомарних критеріїв
     приймання Given-When-Then (включно з AC-01-03 для збереження даних після перезапуску,
     AC-04-02..04 для PATCH та виконавців, AC-07-03 для хронологічного перегляду коментарів).
   - Формальний контракт даних, повна матриця переходів 3x3, семантика PATCH
     (missing vs null, extra="forbid", схемна та транзакційна атомарність) і каталог
     HTTP-кодів (200, 201, 404, 409, 422).

2. docs/architecture.md (v1.0 APPROVED)
   - C4 Component-Level схема з 3 основних компонентів:
     1) API Layer (api/routes.py, schemas.py)
     2) Service Layer (services/issue_service.py)
     3) Database / Repository Layer (db/repository.py, models.py)
     та ізольованої точки розширення ClassifierService (Stub) під ЛР4.
   - Реляційна ER-діаграма (Mermaid) для 3 сутностей: USER, ISSUE, COMMENT
     із коректною кардинальністю необов'язкового виконавця (USER |o..o{ ISSUE).
   - Архітектурні рішення ADR-01 (SQLite та ізоляція tmp_path / :memory: у pytest) і ADR-02
     (відокремлення AI-класифікатора від бізнес-транзакцій).

3. docs/api-contract.md (v1.0 APPROVED)
   - Повна специфікація 9 обов'язкових маршрутів REST API (GET /health, GET /users,
     POST /issues, GET /issues, GET /issues/{id}, PATCH /issues/{id},
     PATCH /issues/{id}/status, POST /issues/{id}/comments, GET /issues/{id}/comments)
     із JSON-схемами та прикладами успішних і помилкових відповідей.

4. docs/traceability.csv
   - Наскрізна матриця простежуваності вимог (FR -> US/AC -> Component/API -> Future test).
   - Атомарне покриття всіх сценаріїв FR-01 – FR-07 та резерву FR-08 (US-08 / AC-08-01):
     Coverage = (7 / 7) * 100% = 100%.

5. docs/ai-log.md
   - Журнал взаємодії з AI-асистентом Google Antigravity IDE (Режим: Agentic Mode) —
     Gemini 4 Argon із фіксацією промптів, відхилених позапланових пропозицій, прийнятих
     уточнень, а також протокол зовнішнього аудиту з ChatGPT (Запис 6).

6. docs/lab-01.md
   - Фінальний стислий звіт з ЛР-01 (мета, таблиця власного аналізу до звернення до AI,
     ключові інженерні рішення, кейси перевірки AI, результати верифікації та самоперевірки
     специфікації із посиланням на сесію ChatGPT, метрика Coverage = 100% та посилання на
     артефакти за тегом lab01-spec).


========================================================================
ЧАСТИНА II. ПРАКТИЧНЕ ЗАНЯТТЯ: ВІД СПЕЦИФІКАЦІЇ ДО ПЕРЕВІРЕНОГО UX/UI-МАКЕТА
Тема: Mini Issue Tracker (Release MVP US-01 – US-08)
========================================================================

1. ПОСИЛАННЯ НА МАКЕТ ТА ПРОТОТИП
------------------------------------------------------------------------
- Figma Design File
  https://www.figma.com/design/yedfcvc9PcUheD1bg9EJRZ/Mini_Issue_Tracker_UX_UI?node-id=0-1&t=IxK0pyfAql2mcBXA-1

- Figma Prototype
  https://www.figma.com/proto/yedfcvc9PcUheD1bg9EJRZ/Mini_Issue_Tracker_UX_UI?node-id=4-4595&t=H98kuFxKCuZxtRqR-1&scaling=min-zoom&content-scaling=fixed&page-id=0%3A1&starting-point-node-id=4%3A4595

2. РЕЄСТР ЗДАВАЛЬНИХ АРТЕФАКТІВ ПРАКТИЧНОГО ЗАНЯТТЯ
------------------------------------------------------------------------
1. 01_Input_Pack_v0.1.md
   - Повний аналітичний відбір вимог із вихідної специфікації SD_Spec.docx.
   - Покриває всі 8 US, рівно 33 змістовні AC, UI-релевантні BR, виключення та Q-ID.
2. 02_Screen_Map_v0.1.md
   - Архітектура інтерфейсу: 3 продуктових екрани, 1 модалка, 3 стани списку, 9 фреймів.
   - Повна матриця переходів T-01..T-20 та текстові User Flows.
3. Decision_Log.md (v1.0 APPROVED)
   - Формальний журнал архітектурних та проєктних рішень (D-01..D-12) згідно з Додатком B1 методички.
   - Повне погодження рішень щодо демонстраційної симуляції входу (S-01), ліміту Title 50 символів, правила Assignee Only, послідовності передумов та порядку сортування.
4. 03_Screen_Contracts.md (v1.0 APPROVED)
   - Формальні контракти поверхонь для розробника (C-ID, Visible data, States).
   - Матриця ролей (Permission Matrix) із суворим закріпленням права Assignee Only для зміни статусу (AC-07.4, DEF-01).
   - Матриця переходів статусів (BR-08.1), предикат Important та повна таблиця Traceability (33 AC).
   - Тестові сценарії TC-01..TC-16 (з декомпозицією TC-08a/b) та межами доказовості.
5. 04_Plan_Review.md
   - Критична рецензія плану до початку макетування.
   - Виявлення та фіксація дефектів DEF-01 (AC-07.4) та DEF-02 (послідовність передумов призначення).
   - Схвалення переходу до фази Figma (Контроль B: PLAN READY).
6. 05_Figma_Brief_v1.0.md
   - Компактний самодостатній англомовний бриф для генератора Figma Agent.
   - Жорсткі обмеження, структура шарів, узгоджені тестові дані (7 базових задач) та acceptance checklist.
7. 06_Review_Report_and_Defects.md
   - Фінальний звіт аудиту відповідності макета вимогам (Контроль D).
   - Таблиця доказів PASS/FAIL (включно з AC-07.3), Usability спостереження та закритий Defect/Change Log.
8. 07_Prototype_Test_Record.md
   - Протокол ручного проходження сценаріїв у режимі Figma Present (T-01..T-10, повний граф 4 переходів T-05).
   - Мінітест зі стороннім користувачем та чітке розмежування симуляції від бекенду.
9. AI_Interaction_Log.md
   - Детальний журнал усіх звернень до моделей штучного інтелекту (Google Antigravity / Gemini 3.8 Flash, Figma Agent).
   - Фіксація повних промптів, верифікацій рішень, лімітів та підтвердження відтворюваності.
10. BEFORE_REVIEW.fig
    - Первинний локальний резервний знімок усього файлу Figma Design одразу після F1.
11. figma_response.txt
    - Повний збережений звіт генератора Figma Agent про створені компоненти та припущення.


========================================================================
ЧАСТИНА III. ЛАБОРАТОРНА РОБОТА №02
Тема: Реалізація сервісу з AI-асистентом та проєктування Agent Skill
Мітки етапів: lab02-skill-v0 (1e31f86), lab02-ai-draft (d775c03)
Каталоги артефактів: app/, tests/, .agents/skills/tracker-slice/, docs/
Зовнішня перевірка (ChatGPT Review):
https://chatgpt.com/c/6af622e1-90a0-83ed-9d15-edc2df280d1b
========================================================================

1. app/ (database.py, main.py, schemas.py, services.py, routes.py, __init__.py)
   - Реалізація REST API сервісу Mini Issue Tracker на FastAPI, Pydantic v2 та SQLite
     (залежності зафіксовані в requirements-lock.txt, Python 3.11+ / перевірено на 3.13.1).
   - Покриття всіх 9 обов'язкових маршрутів контракту ЛР1 (FR-01 – FR-07):
     * Каркас і здоров'я: GET /health (200 OK), ініціалізація SQLite у lifespan,
       PRAGMA foreign_keys = ON, ідемпотентний seed користувачів (1: Agent A, 2: Agent B).
     * Зріз A: GET /users, POST /issues, GET /issues, GET /issues/{id}.
     * Зріз B: PATCH /issues/{id} (атомарність, extra="forbid", {} як no-op / 409 для CLOSED),
       PATCH /issues/{id}/status (матриця переходів 3x3, заборона повернення з CLOSED).
     * Зріз C: POST /issues/{id}/comments, GET /issues/{id}/comments (дозволено для CLOSED).
     * Зріз D: фільтрація GET /issues?status=...&priority=... за логікою AND
       (matches_status, matches_priority).
   - Межі обсягу: FR-08 (ClassifierService) зарезервовано на ЛР4.

2. tests/ (conftest.py, test_issues.py, test_comments.py, test_users.py)
   - 112 автотестів pytest на ізольованій тимчасовій SQLite БД (tmp_path / "test.db")
     із перевіркою сценаріїв T01–T14, GET /users, ізоляції lifespan, порядку помилок
     422 -> 404 -> 409, заборони bool як int та персистентності між перезапусками create_app.
   - Перевірки після фінальних змін:
     * .\.venv\Scripts\python.exe -m pytest -q -> 112 passed
     * .\.venv\Scripts\python.exe -m ruff check app tests --select E4,E7,E9,F,I -> All checks passed!

3. .agents/skills/tracker-slice/ (SKILL.md, references/slices.md)
   - Agent Skill для покрокової реалізації вертикальних зрізів A–D Mini Issue Tracker.
   - Тестування тригера на Кроці 0: 4/4 (100% — 2 позитивні й 2 негативні запити).
   - Еволюція v0 -> v1 (62fd03c): перенесення references/slices.md всередину теки скіла,
     додавання database.py до дозволених файлів зрізів B і C, заміна заглушок на реальні
     ID з docs/requirements.md та додавання GET /users до Зрізу A.

4. docs/lab-02.md
   - Фінальний звіт з ЛР-02: покриття FR-01–FR-07, результати Кроку 0, використання
     tracker-slice у зрізах A–D, обґрунтування v0 -> v1, порівняння lab02-ai-draft і
     фінальної версії, аналіз мікроексперименту, результати pytest і ruff та точні
     відповіді на 8 контрольних питань методички ЛР2.

5. docs/experiment-lr2.csv
   - Таблиця порівняльного мікроексперименту (no-AI vs AI + Skill):
     matches_status (73 с, no-AI, 3/3, 0 правок) проти matches_priority (84 с, AI + Skill, 3/3).

6. docs/traceability.csv
   - Оновлена матриця простежуваності: заглушки майбутніх тестів замінено на реальні імена
     тестових функцій із tests/test_issues.py, tests/test_comments.py та tests/test_users.py
     (T01–T14, GET /users, lifespan).

7. docs/ai-log.md
   - Продовження журналу взаємодії з AI-асистентом для ЛР-02 (Записи 6–17: тестування Skill,
     Крок 1, Зрізи A–D, формування звітності, фінальні виправлення та зовнішня перевірка
     у ChatGPT) зі збереженням усіх записів ЛР-01.

8. README.md
   - Інструкція розгортання та локального запуску (.venv, requirements-lock.txt,
     uvicorn app.main:app на 127.0.0.1:8000, pytest, ruff), приклади API-запитів і навчальні обмеження.
