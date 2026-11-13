# Mini Issue Tracker

Навчальний REST API-сервіс обліку заявок (`FR-01`–`FR-07`), реалізований на FastAPI, Pydantic v2 та SQLite у межах курсу «Штучний інтелект у програмній інженерії» (ЛР1–ЛР2).

---

## 1. Вимоги до середовища

- **Python**: `3.11+` (локальна збірка й перевірки підтверджені на `Python 3.13.1`).
- **Залежності**: зафіксовані у [`requirements-lock.txt`](requirements-lock.txt) (зокрема `fastapi==0.162.5`, `pydantic==2.14.3`, `uvicorn==0.54.0`, `pytest==9.2.0`, `ruff==0.17.5`).

---

## 2. Налаштування та встановлення (Windows: PowerShell / CMD / Git Bash)

Робоче середовище проєкту — **Windows** (`PowerShell`, `CMD` або `Git Bash`). З кореня репозиторію створіть віртуальне середовище `.venv`, активуйте його в потрібній оболонці (або використовуйте прямий виклик інтерпретатора `.venv\Scripts\python.exe`) та встановіть зафіксовані пакети:

```powershell
# 1. Створення .venv (однаково в PowerShell / CMD / Git Bash)
python -m venv .venv
```

Активація `.venv` залежно від оболонки Windows:
- **PowerShell**: `.\.venv\Scripts\Activate.ps1`  
  *(якщо PowerShell блокує запуск скриптів активації, виконайте одноразово: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`)*
- **CMD (Command Prompt)**: `.venv\Scripts\activate.bat`
- **Git Bash**: `source .venv/Scripts/activate`

Встановлення залежностей (з активованим `.venv` або прямим викликом `.venv\Scripts\python.exe`):

```powershell
# PowerShell / CMD (без активації .venv)
.venv\Scripts\python.exe -m pip install -r requirements-lock.txt

# Git Bash (без активації .venv)
./.venv/Scripts/python.exe -m pip install -r requirements-lock.txt

# Або в будь-якій оболонці після активації .venv
python -m pip install -r requirements-lock.txt
```

---

## 3. Запуск сервера

Запустіть локальний ASGI-сервер на `127.0.0.1:8000`:

```powershell
# PowerShell / CMD (прямий виклик без активації .venv; у Git Bash — ./.venv/Scripts/uvicorn.exe)
.venv\Scripts\uvicorn.exe app.main:app --host 127.0.0.1 --port 8000
```

Або при активованому `.venv` (`PowerShell` / `CMD` / `Git Bash`):

```powershell
uvicorn app.main:app --host 127.0.0.1 --port 8000
```

- Базова адреса API: `http://127.0.0.1:8000`
- Інтерактивна документація OpenAPI (Swagger UI): `http://127.0.0.1:8000/docs`
- Файл бази даних SQLite `data/app.db` створюється та ініціалізується автоматично при старті застосунку через `lifespan` у `create_app()` (`PRAGMA foreign_keys = ON`, початкові користувачі `1: Agent A`, `2: Agent B`).

---

## 4. Запуск тестів і лінтера

```powershell
# Повний прогін автотестів (PowerShell / CMD; у Git Bash — ./.venv/Scripts/python.exe)
.venv\Scripts\python.exe -m pytest -q

# Статичний аналіз коду й тестів через ruff
.venv\Scripts\python.exe -m ruff check app tests --select E4,E7,E9,F,I
```

*(За активованого `.venv` у `PowerShell`, `CMD` або `Git Bash` достатньо викликати `python -m pytest -q` та `python -m ruff check app tests --select E4,E7,E9,F,I`.)*

---

## 5. Приклади API-запитів (`curl`)

> У Windows PowerShell команда `curl` є псевдонімом `Invoke-WebRequest`, тому для прикладів нижче в PowerShell викликайте `curl.exe` (або виконуйте в Git Bash / Linux shell як `curl`).

### Перевірка стану сервісу (`GET /health`)
```bash
curl.exe -s http://127.0.0.1:8000/health
```

### Отримання довідника користувачів (`GET /users`)
```bash
curl.exe -s http://127.0.0.1:8000/users
```

### Створення заявки (`POST /issues`)
```bash
curl.exe -s -X POST http://127.0.0.1:8000/issues ^
  -H "Content-Type: application/json" ^
  -d "{\"title\": \"Fix payment gateway timeout\", \"description\": \"Timeout after 30s\", \"priority\": \"high\", \"assignee_id\": 1}"
```

### Перегляд і фільтрація списку заявок (`GET /issues`)
```bash
curl.exe -s "http://127.0.0.1:8000/issues"
curl.exe -s "http://127.0.0.1:8000/issues?status=OPEN&priority=high"
```

### Отримання заявки за ID (`GET /issues/{id}`)
```bash
curl.exe -s http://127.0.0.1:8000/issues/1
```

### Часткове оновлення заявки та зняття виконавця (`PATCH /issues/{id}`)
```bash
curl.exe -s -X PATCH http://127.0.0.1:8000/issues/1 ^
  -H "Content-Type: application/json" ^
  -d "{\"priority\": \"medium\", \"assignee_id\": null}"
```

### Зміна статусу за матрицею переходів (`PATCH /issues/{id}/status`)
```bash
curl.exe -s -X PATCH http://127.0.0.1:8000/issues/1/status ^
  -H "Content-Type: application/json" ^
  -d "{\"status\": \"IN_PROGRESS\"}"
```

### Додавання та перегляд коментарів (`POST/GET /issues/{id}/comments`)
```bash
curl.exe -s -X POST http://127.0.0.1:8000/issues/1/comments ^
  -H "Content-Type: application/json" ^
  -d "{\"author_id\": 2, \"text\": \"Root cause identified.\"}"

curl.exe -s http://127.0.0.1:8000/issues/1/comments
```

---

## 6. Навчальні обмеження проєкту

- **Без `FR-08`**: модуль дорадчої AI-класифікації (`ClassifierService`) зарезервовано на ЛР4 і в поточній версії не реалізовано.
- **Без автентифікації та RBAC**: відсутні реєстрація, паролі, токени (JWT/OAuth) і сесії; використовується фіксований довідник із двох користувачів (`1 — Agent A`, `2 — Agent B`).
- **Локальна SQLite**: дані зберігаються в одному локальному файлі `data/app.db` без окремого сервера БД, Docker чи хмарного розгортання.
- **Обмеження MVP**: реалізовано всі 9 маршрутів контракту ЛР1 (`GET /health`, `GET /users` та операції з заявками й коментарями); видалення заявок, пагінація, повнотекстовий пошук, вкладення файлів і email-сповіщення свідомо виключені.

---

## 7. Документація проєкту

- [`docs/requirements.md`](docs/requirements.md) — функціональні та нефункціональні вимоги (Single Source of Truth)
- [`docs/architecture.md`](docs/architecture.md) — компонентна архітектура, ER-діаграма та ADR
- [`docs/api-contract.md`](docs/api-contract.md) — REST API контракт
- [`docs/traceability.csv`](docs/traceability.csv) — матриця простежуваності вимог і тестів
- [`docs/experiment-lr2.csv`](docs/experiment-lr2.csv) — результати мікроексперименту (`no-AI` vs `AI + Skill`)
- [`docs/ai-log.md`](docs/ai-log.md) — журнал взаємодії з AI-асистентом
- [`docs/lab-01.md`](docs/lab-01.md), [`docs/lab-02.md`](docs/lab-02.md) — звіти з ЛР1 та ЛР2
