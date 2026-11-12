# Звіт з лабораторної роботи №02
**Тема**: Реалізація сервісу з AI-асистентом та проєктування Agent Skill  
**Проєкт**: Mini Issue Tracker  
**Виконавець**: Студент гр. ПЗПІ-23-9 Сєдашев Михайло (`Siedashev Mykhailo`)  
**Репозиторій**: [NureSiedashevMykhailo/AI](https://github.com/NureSiedashevMykhailo/AI)  
**Базова специфікація**: Tag: `lab01-spec`  

---

## 1. Крок 0 — Підготовка середовища та Skill `tracker-slice` (v0)

* **База специфікації**: використано затверджені артефакти ЛР1 ([docs/requirements.md](requirements.md), [docs/architecture.md](architecture.md), [docs/api-contract.md](api-contract.md), [docs/traceability.csv](traceability.csv)).
* **Робоче середовище (Windows)**: підготовлено інструкцію розгортання ізольованого Python-середовища `.venv` у PowerShell (`python -m venv .venv`, `.\.venv\Scripts\Activate.ps1`).
* **Створено Skill `tracker-slice` (v0)**: [.agents/skills/tracker-slice/SKILL.md](../.agents/skills/tracker-slice/SKILL.md). Skill обмежує агента реалізацією одного вертикального зрізу за `docs/api-contract.md`, вимагає планування перед редагуванням коду та забороняє запуск на задачах налаштування середовища чи загальних теоретичних питаннях.

---

## 2. Хід реалізації та тестування активації Skill

### 2.1. Тестування точності активації Skill `tracker-slice`
Проведено серію контрольних запитів для перевірки тригера `tracker-slice` (позитивні та негативні кейси). Детальний протокол зафіксовано в [docs/ai-log.md](ai-log.md) (Записи 6–10).

| № у `ai-log.md` | Запит | Очікування Skill | Фактична поведінка | Результат |
| :--- | :--- | :--- | :--- | :--- |
| **Запис 6** | «Додай `PATCH /issues/{id}/status` за таблицею станів» | Активація `tracker-slice` | Активовано; визначено Зріз B, прочитано потрібні розділи `docs/`, перелічено перевірки `AC-05-01`, `AC-05-02`, `T07–T10`, `T14`, подано план із 4 пунктів | **Пройдено** |
| **Запис 7** | «Реалізуй додавання коментаря до заявки» | Активація `tracker-slice` | Активовано; виявлено відсутність `references/slices.md`, використано `docs/` напряму, перелічено перевірки `AC-07-01`, `AC-07-02`, `404`/`422`, подано план із 5 пунктів | **Пройдено із зауваженням** |
| **Запис 8** | «Поясни, чим 409 відрізняється від 422» | Не активувати | Не активовано; надано чітке розмежування конфлікту стану (`409`) та невалідного payload (`422`) | **Пройдено** |
| **Запис 9** | «Як створити віртуальне середовище у Windows?» | Не активувати | Не активовано; надано команди `venv` для PowerShell і CMD | **Пройдено** |
| **Запис 10** | Реалізація мінімального каркасу застосунку (Крок 1) | Не активувати | Не активовано; реалізовано базовий каркас без бізнес-маршрутів зрізів A–D | **Пройдено** |
| **Запис 11** | Реалізація Зрізу A (`POST /issues`, `GET /issues`, `GET /issues/{id}`) | Активація `tracker-slice` | Активовано; повний цикл (план → підтвердження → мінімальний diff → `pytest` `26 passed`, `ruff` `All checks passed!`) | **Пройдено** |
| **Запис 12** | Реалізація Зрізу B (`PATCH /issues/{id}`, `PATCH /issues/{id}/status`) | Активація `tracker-slice` | Активовано; виявлено й узгоджено суперечність `{}` із `docs/`, виконано план → `pytest` `66 passed`, `ruff` `All checks passed!` | **Пройдено** |

### 2.2. Крок 1 — Мінімальний каркас застосунку
* **База даних (`app/database.py`)**: реалізовано `get_connection(db_path)` із `sqlite3.Row` та обов'язковим `PRAGMA foreign_keys = ON;` на кожному з'єднанні; `init_db(db_path)` створює таблиці `users`, `issues`, `comments` згідно з ER-моделлю ЛР1 (`CHECK`-обмеження для `status` і `priority`, зовнішні ключі) та ідемпотентно додає користувачів `(1, "Agent A")` і `(2, "Agent B")` через `INSERT OR IGNORE`.
* **Точка входу (`app/main.py`)**: реалізовано фабрику `create_app(db_path: str = "data/app.db")` з викликом `init_db(db_path)`, підключенням роутера та маршрутом `GET /health` (`200 OK`, `{"status": "ok"}`); створено екземпляр `app = create_app()` для `uvicorn`.
* **Базові модулі**: створено `app/__init__.py`, `app/schemas.py`, `app/services.py`, `app/routes.py` (`APIRouter`) без зайвих абстракцій і без бізнес-маршрутів зрізів A–D.
* **Перевірки Кроку 1**:
  * `.\.venv\Scripts\ruff.exe check app` (та `--select E4,E7,E9,F,I`) — `All checks passed!`.
  * Smoke-перевірка через FastAPI `TestClient` на тимчасовій БД (`tempfile.TemporaryDirectory`) та на `app`: підтверджено `GET /health` → `200 OK`, `PRAGMA foreign_keys == 1`, наявність таблиць `users`, `issues`, `comments`, спрацювання `sqlite3.IntegrityError` при невалідному `assignee_id` та ідемпотентність повторного `init_db` без дублювання користувачів і втрати рядків у `issues`.

### 2.3. Реалізація Зрізу A — Створення й читання заявок
* **Схеми (`app/schemas.py`)**: `IssueStatus`, `IssuePriority`, `IssueCreate` (`extra="forbid"`, `strip_whitespace=True` і довжина `3..120` для `title`, `description` `0..2000` із дефолтом `""`, `priority="medium"`, `assignee_id` лише `1 | 2 | None` із відхиленням `bool`) та `IssueRead`.
* **БД і сервіс (`app/database.py`, `app/services.py`)**: параметризовані функції `insert_issue`, `list_issues` (`ORDER BY created_at ASC, id ASC`), `get_issue_by_id`; у сервісі — `IssueNotFoundError`, `create_issue` (`status="OPEN"`, UTC `YYYY-MM-DDTHH:MM:SSZ`), `get_issues` і `get_issue`.
* **Маршрути (`app/routes.py`)**: `POST /issues` (`201 Created`), `GET /issues` (`200 OK`, без фільтрів зрізу D), `GET /issues/{id}` (`id > 0` → `200 OK` або `404 Not Found`).
* **Тести (`tests/conftest.py`, `tests/test_issues.py`)**: фікстура `TestClient` на `tmp_path / "test.db"` і тести для `T01, T02, T03, T13` (`AC-01-01..03`, `AC-03-01..02`), включно з персистентністю між перезапусками `create_app`.
* **Перевірки Зрізу A**:
  * `.\.venv\Scripts\python.exe -m pytest -q` — `26 passed` (`app.db` не змінювався).
  * `.\.venv\Scripts\python.exe -m ruff check app tests --select E4,E7,E9,F,I` — `All checks passed!`.

### 2.4. Реалізація Зрізу B — Оновлення, матриця станів $3 \times 3$ та захист `CLOSED`
* **Схеми (`app/schemas.py`)**: винесено спільний тип `AssigneeId` (`[1, 2] | None`, відхилення `bool`), додано `IssueUpdate` (`extra="forbid"`, валідатор `reject_null_for_non_nullable_fields` для `title`/`description`/`priority`) та `IssueStatusUpdate`.
* **БД і сервіс (`app/database.py`, `app/services.py`)**: додано `UPDATABLE_ISSUE_COLUMNS`, параметризовані `update_issue` і `update_issue_status` у транзакції `with conn:`; у сервісі — `IssueConflictError` (`409`), матрицю переходів $3 \times 3$ (`ALLOWED_STATUS_TRANSITIONS`), `update_issue` (`exclude_unset=True`, `{}` як `no-op` для відкритих заявок) та `update_issue_status`.
* **Маршрути (`app/routes.py`)**: `PATCH /issues/{id}` та `PATCH /issues/{id}/status` (`id > 0`, мапінг `404`/`409`).
* **Тести (`tests/test_issues.py`)**: +40 тест-кейсів для `T07, T08, T09, T10, T14` (`{}`, заборона `status` у загальному `PATCH`, атомарність, порядок `422 → 404 → 409`).
* **Перевірки Зрізу B**:
  * `.\.venv\Scripts\python.exe -m pytest -q` — `66 passed`.
  * `.\.venv\Scripts\python.exe -m ruff check app tests --select E4,E7,E9,F,I` — `All checks passed!`.

---

## 3. Рев'ю планів та diff (Крок 1, Зрізи A та B)

1. **Захист специфікації `docs/` як Single Source of Truth**: під час планування Зрізу B агент виявив суперечність між формулюванням у промпті («заборона порожнього PATCH») і контрактом у `docs/requirements.md` та `docs/api-contract.md` (`{}` → `200 OK` як `no-op` для відкритої заявки, `409 Conflict` для `CLOSED`). Роботу було зупинено до підтвердження оператора, що запобігло поломці контракту.
2. **Дотримання меж і безпеки**: у Кроці 1, Зрізі A та Зрізі B збережено скоуп (зрізи C, D і `GET /users` не чіпалися), параметризовані запити з allowlist колонок, `PRAGMA foreign_keys = ON`, `extra="forbid"`, відхилення `bool` для `assignee_id` та ізоляцію тестів у `tmp_path`.
3. **Узгодження структури модулів**: зафіксовану в Кроці 1 пласку структуру (`app/database.py`, `app/main.py`, `app/schemas.py`, `app/services.py`, `app/routes.py`) без конфліктів використано у Зрізах A та B.

---

## 4. Зміни Skill `tracker-slice` (`v0 → v1`)

За результатами тестування `v0` та виконання Кроку 1:

1. **Виконано — додано `references/slices.md`**: довідник перенесено всередину теки скіла ([.agents/skills/tracker-slice/references/slices.md](../.agents/skills/tracker-slice/references/slices.md)), де зафіксовано зрізи `A–D` і єдину пласку структуру файлів `app/`.
2. **Залишилося уточнити в `v1`**: замінити шаблонні плейсхолдери `<US-xx, AC-xx-yy>` у `references/slices.md` на фактичні ідентифікатори з [docs/requirements.md](requirements.md), додати `database.py` до переліку дозволених файлів Зрізу B (оскільки `UPDATE`-функції не існували на старті зрізу) та уточнити поведінку при порожньому каркасі `app/`.

---

## 5. Пов'язані артефакти

* [docs/ai-log.md](ai-log.md) — Журнал взаємодії з AI-асистентом (Записи 6–12 для ЛР-02)
* [.agents/skills/tracker-slice/SKILL.md](../.agents/skills/tracker-slice/SKILL.md) — Специфікація Skill `tracker-slice`
* [.agents/skills/tracker-slice/references/slices.md](../.agents/skills/tracker-slice/references/slices.md) — Довідник зрізів `A–D`
* [tests/test_issues.py](../tests/test_issues.py) — Автотести Зрізів A і B (`T01–T03, T07–T10, T13, T14`)
* [docs/api-contract.md](api-contract.md) — Контракт REST API (Single Source of Truth)
* [docs/requirements.md](requirements.md) — Вимоги та критерії приймання
