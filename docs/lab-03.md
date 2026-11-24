# Звіт з лабораторної роботи №03
**Тема**: Тестування, мутаційний аналіз, перевірка безпеки та верифікація висновків AI  
**Проєкт**: Mini Issue Tracker  
**Виконавець**: Студент гр. ПЗПІ-23-9 Сєдашев Михайло (`Siedashev Mykhailo`)  
**Репозиторій**: [NureSiedashevMykhailo/AI](https://github.com/NureSiedashevMykhailo/AI)  
**Цільовий стек**: Python `3.13.1`, FastAPI, Pydantic v2, SQLite, `pytest 9.2.0`, `coverage.py`, `Bandit 1.9.4`, `ruff`

---

## 1. Метадані експерименту та хеші комітів

Усі вимірювання покриття, мутаційного тестування, статичного аналізу безпеки (`Bandit`) та відновлювальних циклів `fail → fix → pass` виконано з фіксацією станів у Git та збереженням первинних артефактів у каталозі [`reports/lr3/`](../reports/lr3/):

| Етап / Статус | Гілка / Тег | Хеш коміту (короткий / повний) | Пов'язані артефакти в репозиторії |
| :--- | :--- | :--- | :--- |
| **Базова версія `R0`** | `main` (tag: `lab02-implemented`) | `5a26c01` (`5a26c01f91d03ed3ab1dc690747e19277d5e36cb`) | [`reports/lr3/coverage-t0.json`](../reports/lr3/coverage-t0.json), [`reports/lr3/bandit-r0.json`](../reports/lr3/bandit-r0.json) |
| **Зафіксований набір тестів `T1`** | `main` | `3a40ed8` (`3a40ed818c2ab524a98cf1b16b1abe7af2deec2b`) | [`tests/test_lr3_extensions.py`](../tests/test_lr3_extensions.py), [`reports/lr3/t-ai-draft.txt`](../reports/lr3/t-ai-draft.txt), [`reports/lr3/coverage-t1.json`](../reports/lr3/coverage-t1.json) |
| **Мутація `M1` → виправлення `M1`** | `lr3-m1` | `16fa4c7` → `4a08626` | [`reports/lr3/t0-m1.log`](../reports/lr3/t0-m1.log), [`reports/lr3/t1-m1.log`](../reports/lr3/t1-m1.log), [`reports/lr3/m1-fix.diff`](../reports/lr3/m1-fix.diff), [`reports/lr3/t1-m1-fixed.log`](../reports/lr3/t1-m1-fixed.log) |
| **Мутація `M2` (діагностика атомарності)** | `lr3-m2` | `31d16b2` | [`reports/lr3/t0-m2.log`](../reports/lr3/t0-m2.log), [`reports/lr3/t1-m2.log`](../reports/lr3/t1-m2.log) |
| **Мутація `M3` → виправлення `M3`** | `lr3-m3` | `dd9989a` → `5ccd73d` | [`reports/lr3/t0-m3.log`](../reports/lr3/t0-m3.log), [`reports/lr3/t1-m3.log`](../reports/lr3/t1-m3.log), [`reports/lr3/bandit-m3.json`](../reports/lr3/bandit-m3.json), [`reports/lr3/m3-fix.diff`](../reports/lr3/m3-fix.diff), [`reports/lr3/bandit-m3-fixed.json`](../reports/lr3/bandit-m3-fixed.json), [`reports/lr3/t1-m3-fixed.log`](../reports/lr3/t1-m3-fixed.log) |

---

## 2. Підсумкова таблиця експерименту (`T0` vs `T1` на базовій версії `R0`)

Порівняння базового тестового комплекту після ЛР2 (`T0` — файли `test_issues.py`, `test_comments.py`, `test_users.py`) із розширеним комплектом (`T1 = T0 + tests/test_lr3_extensions.py`) на незмінному коді застосунку `R0` (`5a26c01`):

| Показник | Базовий набір `T0` на `R0` (`5a26c01`) | Розширений набір `T1` на `R0` (`3a40ed8`) | Динаміка (`T0 → T1`) |
| :--- | :--- | :--- | :--- |
| **Пройдено / зібрано `pytest` на `R0`** | `135 / 135` (`100%`) | `145 / 145` (`100%`) | `+10` тестових випадків |
| **Покриття рядків (інструкцій) `app/`** | `312 / 319` (`97.81%`) | `319 / 319` (`100.00%`) | `+7` рядків (`+2.19` в.п., `0` пропущених) |
| **Покриття гілок (`branches`) `app/`** | `33 / 40` (`82.50%`) | `39 / 40` (`97.50%`) | `+6` гілок (`+15.00` в.п.) |
| **Інтегральне покриття `coverage.py` (`lines + branches`)** | `345 / 359` (`96.10%`) | `358 / 359` (`99.72%`) | `+13` елементів (`+3.62` в.п.) |
| **Виявлено мутацій / придатних (`Mutation Score`)** | `2 / 3` (`66.7%`) | `3 / 3` (`100.0%`) | `+1` критичний SQL-мутант (`+33.3` в.п.) |
| **Час повного прогону `pytest` на `R0`** | `5.19 с` | `5.76 с` | `+0.57 с` (`+11.0%`) |

> **Деталізація покриття за модулями (`coverage-t0.json` → `coverage-t1.json`)**: у `app/main.py` рядкове покриття зросло з `17/18` (`94.44%`) до `18/18` (`100.0%`), у `app/services.py` — з `79/81` рядків і `24/26` гілок (`96.26%`) до `81/81` рядків і `26/26` гілок (`100.0%`), у `app/database.py` — зі `100/104` рядків і `5/10` гілок (`92.11%`) до `104/104` рядків і `9/10` гілок (`99.12%`). Єдина непокрита гілка `26 → 29` у `app/database.py` відповідає режиму `init_db(":memory:")`, оскільки всі тести за `NFR-02` працюють із файловою БД у `tmp_path / "test.db"`. Модулі `app/routes.py` (`53/53`) та `app/schemas.py` (`63/63`, гілки `4/4`) мали `100.0%` в обох наборах.

### Зіставлення сценаріїв за контрактом ЛР1 (`T0` та розширення у `T1`)

Набір `T0` (`135` тестів) покривав основні функціональні сценарії `T01–T14` для `FR-01–FR-07`, однак мав точкові прогалини: відсутність перевірки `GET /health` (§2.1), відсутність спецсимволів SQL (прямого апострофа `'`) у `POST /issues` та `PATCH /issues/{id}`, відсутність ізольованої параметризації реопену `CLOSED`, комбінації `priority="high"` із `assignee_id=999` та захисних гілок `services.py` / `database.py`. До [`tests/test_lr3_extensions.py`](../tests/test_lr3_extensions.py) додано **10 тестових випадків** (`8` AI + `2` студента):

| № | Тестовий випадок у `tests/test_lr3_extensions.py` | Джерело | FR / AC / Розділ контракту | Перевірений маршрут / дія та очікуваний стан після повторного `GET` |
| :--- | :--- | :--- | :--- | :--- |
| 1 | `test_patch_issue_atomicity_valid_priority_with_invalid_assignee` | AI | `FR-03, FR-05, FR-07` / `AC-04-02, AC-04-03` | `PATCH /issues/{id}` із `{"priority": "high", "assignee_id": 999}` → `422`; повторний `GET` підтверджує `priority="low"`, `assignee_id=1` |
| 2 | `test_create_and_get_issue_with_apostrophe_in_title` | AI | `FR-01, FR-02, FR-07` / `AC-01-01, AC-03-01` | `POST /issues` із `{"title": "O'Brien"}` → `201`; повторний `GET /issues/{id}` повертає точний рядок `"O'Brien"` |
| 3 | `test_closed_issue_rejects_reopen_transitions[OPEN]` | AI | `FR-04` / `AC-05-02, AC-06-02` | `PATCH /issues/{id}/status` (`CLOSED → OPEN`) → `409`; повторний `GET` фіксує `status="CLOSED"` |
| 4 | `test_closed_issue_rejects_reopen_transitions[IN_PROGRESS]` | AI | `FR-04` / `AC-05-02, AC-06-02` | `PATCH /issues/{id}/status` (`CLOSED → IN_PROGRESS`) → `409`; повторний `GET` фіксує `status="CLOSED"` |
| 5 | `test_db_update_issue_empty_updates_returns_existing_row` | AI | `FR-03, FR-07` / `AC-03-01` (§6 п. 3) | `database.update_issue(db_path, id, {})` (`database.py:182`) повертає запис; повторний `GET` — `200 OK` без змін |
| 6 | `test_db_update_issue_unsupported_column_raises_value_error` | AI | `FR-03, FR-07` / `AC-04-02` (§6 п. 4) | `database.update_issue(..., {"status": "CLOSED"})` (`database.py:186`) кидає `ValueError`; повторний `GET` — `status="OPEN"` |
| 7 | `test_patch_issue_returns_404_when_row_missing_on_db_update` | AI | `FR-02, FR-03, FR-07` / `AC-03-02` (§7.2) | `PATCH /issues/999` при `rowcount == 0` (`database.py:200`, `services.py:132`) → `404`; повторний `GET /issues/999` → `404` |
| 8 | `test_patch_status_returns_404_when_row_missing_on_db_status_update` | AI | `FR-02, FR-04, FR-07` / `AC-03-02` (§7.2) | `PATCH /issues/999/status` при `rowcount == 0` (`database.py:223`, `services.py:158`) → `404`; повторний `GET /issues/999` → `404` |
| 9 | `test_student_health_endpoint_returns_ok` | Студент | `NFR-01` / Контракт §2.1 | `GET /health` (`app/main.py:24`) → `200 OK` та JSON `{"status": "ok"}` |
| 10 | `test_student_patch_issue_preserves_apostrophe_in_title` | Студент | `FR-03, FR-07` / `AC-04-01` | `PATCH /issues/{id}` із `{"title": "O'Brien's fix"}` → `200 OK`; повторний `GET /issues/{id}` повертає `"O'Brien's fix"` |

---

## 3. Матриця виявлення мутацій (Крок 5)

Для оцінювання чутливості наборів `T0` і `T1` в окремих гілках створено три придатні (нееквівалентні) контрольовані мутації, кожна з яких порушує конкретну вимогу контракту ЛР1:

| Мутація (гілка, коміт) | Внесений дефект | Виявлено в `T0`? | Виявлено в `T1`? | Тести-детектори та фактичний симптом з логів прогону |
| :--- | :--- | :--- | :--- | :--- |
| **`M1`** (`lr3-m1`, `16fa4c7`) | У `app/services.py` до `ALLOWED_STATUS_TRANSITIONS[CLOSED]` додано `IssueStatus.OPEN` (дозволено реопен закритої заявки з кодом `200`) | **Так** (`1 failed, 134 passed`, `t0-m1.log`) | **Так** (`2 failed, 143 passed`, `t1-m1.log`) | `T0`: `test_t08_status_transition_matrix_and_idempotency` (`assert 200 == 409`).<br>`T1`: додатково `test_closed_issue_rejects_reopen_transitions[OPEN]` (`assert 200 == 409`). |
| **`M2`** (`lr3-m2`, `31d16b2`) | У `app/services.py::update_issue` поля `(title, description, priority)` записуються в БД до перевірки існування `assignee_id` | **Так** (`1 failed, 134 passed`, `t0-m2.log`) | **Так** (`2 failed, 143 passed`, `t1-m2.log`) | `T0`: `test_t14_patch_atomicity_forbidden_fields_and_status_rejection[payload0]` (`title` став `'Valid New Title'`).<br>`T1`: додатково `test_patch_issue_atomicity_valid_priority_with_invalid_assignee` (`priority` став `'high'` замість `'low'`). |
| **`M3`** (`lr3-m3`, `dd9989a`) | У `app/database.py::insert_issue` поле `title` підставлено в `INSERT INTO issues` через f-string `VALUES ('{title}', ...)` замість `?` | **Ні** (`135 passed`, дефект пропущено, `t0-m3.log`) | **Так** (`1 failed, 144 passed`, `t1-m3.log`) | `T0`: жоден заголовок у базових тестах не містив апострофа `'`.<br>`T1`: `test_create_and_get_issue_with_apostrophe_in_title` впав із `sqlite3.OperationalError: near "Brien": syntax error`. |

---

## 4. Походження тестів у наборі `T1` (Крок 6)

Фінальний набір `T1` (`3a40ed8`) налічує **`145` тестових випадків**:
* **`135` тестів (`93.1%`) — успадковано з базового набору `T0`** без модифікації наявних тестових файлів (`test_issues.py`, `test_comments.py`, `test_users.py`).
* **`8` тестів (`5.5%`) — згенеровано AI-асистентом і прийнято без правок**. До першого запуску `pytest` первинний код було збережено у [`reports/lr3/t-ai-draft.txt`](../reports/lr3/t-ai-draft.txt). Кожен із 8 тестів пройшов ручну звірку очікуваних HTTP-кодів (`200`, `201`, `404`, `409`, `422`), прив'язки до `FR`/`AC` та обов'язкового оракула стану через повторний `GET /issues/{id}` за `docs/requirements.md` і `docs/api-contract.md`; розбіжностей між `t-ai-draft.txt` та першими 8 тестами у `tests/test_lr3_extensions.py` немає (`0` рядків правок).
* **`2` тести (`1.4%`) — написано студентом вручну** після аналізу залишкових білих плям: `test_student_health_endpoint_returns_ok` (закрив єдиний непокритий рядок `app/main.py:24` для маршруту `GET /health`) та `test_student_patch_issue_preserves_apostrophe_in_title` (перевірив безпечне збереження прямого апострофа під час `PATCH /issues/{id}`).

---

## 5. Картки дефектів та аналіз виправлень (Кроки 7–8)

### Картка дефекту M1 — Дозволений перехід `CLOSED → OPEN` (`fail → fix → pass` зі Skill)
* **Гілка та коміти**: `lr3-m1`, мутація `16fa4c7` → виправлення `4a08626`.
* **Симптом (`fail`, [`reports/lr3/t1-m1.log`](../reports/lr3/t1-m1.log))**: на запиті `PATCH /issues/{id}/status` із тілом `{"status": "OPEN"}` для закритої заявки тести `test_t08_status_transition_matrix_and_idempotency` і `test_closed_issue_rejects_reopen_transitions[OPEN]` падають з `AssertionError: assert 200 == 409`.
* **Процес виправлення (`Skill tracker-slice v1`, зріз B)**: у режимі чату агенту передано вивід падіння та гіпотезу щодо порушення матриці станів (§2.7 `docs/api-contract.md`, `AC-05-02`, `AC-06-02`). Агент визначив **Зріз B** за `.agents/skills/tracker-slice/references/slices.md`, вичитав лише цільові розділи `docs/`, зіставив причину з контрактом, сформував план із 4 пунктів і **зупинився на кроці 4 до підтвердження людиною**. Після підтвердження внесено мінімальний патч (`reports/lr3/m1-fix.diff`) без зміни тестів:
  ```diff
  --- a/app/services.py
  +++ b/app/services.py
  @@ -29,7 +29,6 @@ ALLOWED_STATUS_TRANSITIONS: dict[IssueStatus, frozenset[IssueStatus]] = {
           IssueStatus.CLOSED,
       }),
       IssueStatus.CLOSED: frozenset({
  -        IssueStatus.OPEN,
           IssueStatus.CLOSED,
       }),
   }
  ```
* **Перевірка (`pass`, [`reports/lr3/t1-m1-fixed.log`](../reports/lr3/t1-m1-fixed.log))**: спроба `CLOSED → OPEN` повертає `409 Conflict`, повторний `GET /issues/{id}` підтверджує статус `"CLOSED"`, повний прогін `T1` завершено з результатом **`145 passed`** (`6.26 с`).

### Картка дефекту M2 — Порушення атомарності часткового `PATCH /issues/{id}`
* **Гілка та коміт**: `lr3-m2`, мутація `31d16b2` (діагностична демонстрація часткового запису).
* **Відтворення та спостережуваний збій ([`reports/lr3/t1-m2.log`](../reports/lr3/t1-m2.log))**:
  1. **Стан до `PATCH`**: створено відкриту заявку з `priority="low"` та `assignee_id=1`.
  2. **Запит**: `PATCH /issues/{id}` із комбінованим пакетом `{"priority": "high", "assignee_id": 999}` повертає очікуваний код `422 Unprocessable Entity`.
  3. **Стан після повторного `GET /issues/{id}`**: база даних повертає **`priority="high"`** при `assignee_id=1` (`AssertionError: assert 'high' == 'low'` у `test_patch_issue_atomicity_valid_priority_with_invalid_assignee`; аналогічно в `test_t14_*` поле `title` змінилося на `'Valid New Title'`).
* **Архітектурний механізм збереження атомарності в `R0`**: у еталонній реалізації принцип «все або нічого» (`AC-04-02`, Розділ 6 п. 5 `docs/requirements.md`) забезпечується дворівнево: (1) повна перевірка всіх полів вхідного JSON (включно з `AssigneeId` у `IssueUpdate`) виконується на рівні схеми Pydantic **до** виклику `services.update_issue` та звернення до SQLite; (2) сам запис у `database.update_issue` виконується одним SQL-оператором `UPDATE` всередині контекстного менеджера `with conn:`, який автоматично виконує `COMMIT` лише за успіху всієї операції або `ROLLBACK` транзакції у разі помилки БД.

### Картка дефекту M3 — Непараметризований SQL у `insert_issue` (`fail → fix → pass`)
* **Гілка та коміти**: `lr3-m3`, мутація `dd9989a` → виправлення `5ccd73d`.
* **Симптом (`fail`, [`reports/lr3/t1-m3.log`](../reports/lr3/t1-m3.log))**: під час `POST /issues` із `{"title": "O'Brien"}` тест `test_create_and_get_issue_with_apostrophe_in_title` падає з необробленим винятком `sqlite3.OperationalError: near "Brien": syntax error` на рядку `VALUES ('{title}', ?, ?, ?, ?, ?)` у `app/database.py`. Набір `T0` цю мутацію повністю пропустив (`135 passed`, `t0-m3.log`).
* **Порівняння звітів сканера `Bandit` (`bandit-r0.json` → `bandit-m3.json` → `bandit-m3-fixed.json`)**:
  * У базовому [`reports/lr3/bandit-r0.json`](../reports/lr3/bandit-r0.json) та у виправленому [`reports/lr3/bandit-m3-fixed.json`](../reports/lr3/bandit-m3-fixed.json) зафіксовано **лише `1` хибне спрацювання (`FP`) `B608`** у `app/database.py:196` (`update_issue`, де назви колонок жорстко обмежені білим списком `UPDATABLE_ISSUE_COLUMNS`, а значення параметризовані; див. Розділ 7).
  * У дефектному [`reports/lr3/bandit-m3.json`](../reports/lr3/bandit-m3.json) до нього додалося **реальне спрацювання (`TP`) `B608: hardcoded_sql_expressions`** (`Severity: MEDIUM`, `Confidence: MEDIUM`, `CWE-89`) у функції `insert_issue` (виклик `conn.execute` у `app/database.py:104`, f-string у рядках `105–115`; сумарно `2` попередження), яке **повністю зникло** після повернення параметризації `?` ([`reports/lr3/m3-fix.diff`](../reports/lr3/m3-fix.diff), зниження `2 → 1` до базового стану `R0`):
  ```diff
  --- a/app/database.py
  +++ b/app/database.py
  @@ -102,7 +102,7 @@ def insert_issue(
       try:
           with conn:
               cursor = conn.execute(
  -                f"""
  +                """
                   INSERT INTO issues (
                       title,
                       description,
  @@ -111,9 +111,9 @@ def insert_issue(
                       assignee_id,
                       created_at
                   )
  -                VALUES ('{title}', ?, ?, ?, ?, ?)
  +                VALUES (?, ?, ?, ?, ?, ?)
                   """,
  -                (description, status, priority, assignee_id, created_at),
  +                (title, description, status, priority, assignee_id, created_at),
               )
  ```
* **Перевірка (`pass`, [`reports/lr3/t1-m3-fixed.log`](../reports/lr3/t1-m3-fixed.log))**: `POST /issues` повертає `201 Created`, повторний `GET /issues/{id}` повертає точний рядок `"O'Brien"` без спотворень чи екранування, повний прогін `T1` — **`145 passed`** (`5.42 с`).

---

## 6. Аналіз безпеки та меж довіри (Крок 10)

| Напрям перевірки | Реалізований захисний механізм у `app/` та `tests/` | Спосіб верифікації / Доказ | Статус |
| :--- | :--- | :--- | :--- |
| **Спецсимволи та параметризація SQL** | Усі значення в `app/database.py` передаються виключно через `?`-плейсхолдери `sqlite3`; імена полів у `update_issue` обмежені `UPDATABLE_ISSUE_COLUMNS` | Тести з апострофом `"O'Brien"` (`POST`) і `"O'Brien's fix"` (`PATCH`), тест `ValueError` на недозволену колонку, `bandit-m3-fixed.json` | **Захищено** |
| **Відсікання невірного входу (`422`)** | Схеми Pydantic v2 з `extra="forbid"`, `StrictInt` (заборона `bool` і рядкових чисел), `strip_whitespace=True`, строгі `Enum`, порядок `422 → 404 → 409` | Параметризовані негативні тести `T02`, `T06`, `T10`, `T11`, `T14` та тест атомарності з `assignee_id=999` | **Захищено** |
| **Межі довіри `author_id` / `assignee_id`** | Користувачі `[1, 2]` є синтетичним довідником; клієнтський `author_id` у тілі запиту перевіряє лише належність до `{1, 2}` і **не є автентифікацією чи RBAC** | Явно задокументовано як обмеження навчального скоупу в `docs/requirements.md` (§1.2) та перевірено на відхилення ID поза `{1, 2}` (`422`) | **Контрольоване обмеження** |
| **Секрети, конфігурація та логи помилок** | У коді відсутні паролі, API-ключі чи токени; помилки `404`/`409` повертають контрольований `detail` без витоку SQL-запитів чи шляхів ФС; `int64` overflow повертає `404` | Ручний аудит `app/*.py`, `bandit -r app` (`0` знахідок `B105–B107`), тести `test_sqlite_int64_overflow_*` | **Безпечно** |
| **Ізоляція тестової бази даних** | Фікстури `db_path` і `client` у `tests/conftest.py` створюють окремий `tmp_path / "test.db"` на кожен тест; `init_db` викликається лише в ASGI `lifespan` | `test_create_app_does_not_initialize_db_before_lifespan` (`test_users.py`), незмінність робочого `data/app.db` після всіх прогонів (`NFR-02`) | **Ізольовано** |

---

## 7. Реєстр висновків AI та сканера безпеки (Крок 11)

Усі твердження AI-асистента та статичного аналізатора `Bandit` перевірялися емпірично за артефактами покриття, логами `pytest` та інспекцією вихідного коду:

| № | Джерело | Версія коду | Твердження | Статус | Фактичний доказ |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | `Bandit` (`B608`) | `R0` (`5a26c01`), `M3-fixed` (`5ccd73d`) | Можлива SQL-ін'єкція у `app/database.py:196` (`f"UPDATE issues SET {assignments} WHERE id = ?"`) | **Спростовано (`FP`)** | `assignments` містить лише назви колонок, відфільтровані через `UPDATABLE_ISSUE_COLUMNS` (`database.py:184–186`, доведено тестом `ValueError`), а всі значення передаються параметризовано у `params`. |
| 2 | `Bandit` (`B608`) | `M3` (`dd9989a`) | Можлива SQL-ін'єкція у `insert_issue` (`app/database.py:104`, f-string рядків `105–115`: `VALUES ('{title}', ?, ?, ?, ?, ?)`) | **Підтверджено (`TP`)** | Неекранований апостроф у `"O'Brien"` ламає синтаксис SQL (`OperationalError` у `t1-m3.log`); після повернення `?` (`m3-fix.diff`) реальне попередження зникає в `bandit-m3-fixed.json` (залишається лише `1` базовий `FP` на рядку `196`, як і в `bandit-r0.json`). |
| 3 | AI-асистент | `R0` (`5a26c01`) | Набір `T0` не покриває `app/main.py:24`, `app/services.py:132, 158`, `app/database.py:182, 186, 200, 223` та спецсимволи `'` у `title` | **Підтверджено (`TP`)** | Поля `missing_lines` у `reports/lr3/coverage-t0.json` та виживання мутанта `M3` на наборі `T0` (`t0-m3.log`: `135 passed`). |
| 4 | AI-асистент | `R0` → `T1` (`3a40ed8`) | Згенеровані 8 тестів у `t-ai-draft.txt` коректні за контрактом ЛР1 і закривають усі цільові рядки `services.py` та `database.py` | **Підтверджено (`TP`)** | Усі 8 тестів прийнято без правок і пройдено з першого запуску; у `coverage-t1.json` покриття рядків `services.py` і `database.py` становить `100.0%`. |
| 5 | AI + `Skill tracker-slice v1` | `M1` (`16fa4c7`) | Падіння `T08` та реопен-тесту спричинене `IssueStatus.OPEN` у `ALLOWED_STATUS_TRANSITIONS[CLOSED]`, що суперечить `AC-05-02` і §2.7 | **Підтверджено (`TP`)** | Патч `m1-fix.diff` (`-1` рядок, коміт `4a08626`) відновив код `409 Conflict` і дав `145 passed` у `t1-m1-fixed.log`. |
| 6 | AI-асистент (прямий промпт) | `M3` (`dd9989a`) | Повернення плейсхолдера `?` і кортежу `(title, ...)` у `insert_issue` усуває падіння на `"O'Brien"` та `B608` у цій функції | **Підтверджено (`TP`)** | Патч `m3-fix.diff` (`5ccd73d`), `145 passed` у `t1-m3-fixed.log` та усунення `B608` на рядку `105` у `bandit-m3-fixed.json`. |

**Розрахунок точності висновків (`Precision`)**:
* Для статичного сканера `Bandit` (за унікальними локаціями `B608`): $TP = 1$, $FP = 1 \implies \text{Precision}_{\text{Bandit}} = \frac{1}{1 + 1} = 50.0\%$.
* Для тверджень AI-асистента: $TP = 4$, $FP = 0 \implies \text{Precision}_{\text{AI}} = \frac{4}{4 + 0} = 100.0\%$.
* **Сумарна точність за реєстром**:
  $$\text{Precision} = \frac{TP}{TP + FP} = \frac{5}{5 + 1} = \frac{5}{6} \approx 83.3\%$$

---

## 8. AI-бюджет та обмеження експерименту

* **AI-бюджет (кількість звернень у межах ЛР3)**: загалом виконано **8 цільових взаємодій** в агентному середовищі Google Antigravity IDE (`Gemini 4 Carbon (High)`): `1` запит на аудит `T0` і генерацію `t-ai-draft.txt` (`0` повторних спроб/правок), `3` ізольовані запити для підготовки контрольованих мутацій `M1–M3`, `2` репліки для усунення `M1` через `Skill tracker-slice v1` (перша — аналіз і план до гейту підтвердження на кроці 4, друга — застосування патча після підтвердження), `1` прямий запит на виправлення `M3` та `1` запит на зведення звітної документації.
* **Обмеження та загрози внутрішній/зовнішній валідності**:
  1. *Відкритий режим експерименту*: один виконавець формував розширення `T1` та проєктував контрольовані мутації `M1–M3`, знаючи структуру тестів і коду, тому показник `Mutation Score = 100%` відображає цільову перевірку трьох класів дефектів, а не сліпий автоматизований мутаційний скринінг усього AST.
  2. *Один виконавець і мала вибірка мутацій ($N=3$)*: синтетичні мутації охоплюють ключові бізнес-інваріанти контракту (матрицю станів, атомарність `PATCH`, SQL-параметризацію), проте не покривають усіх можливих комбінаторних дефектів.
  3. *Масштаб кодової бази*: сервіс має компактний обсяг (`319` виконуваних інструкцій у `app/`), що полегшує досягнення `100%` рядкового покриття та `100%` точності AI за наявності формалізованого контракту ЛР1 (`docs/requirements.md`, `docs/api-contract.md`).
