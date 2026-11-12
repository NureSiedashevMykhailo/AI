# Зрізи Mini Issue Tracker

Посилання вказують на фактичні розділи `docs/api-contract.md` і `docs/requirements.md` та пласку структуру `app/`.

## A. Створення й читання
- Код (app/): schemas.py, services.py, routes.py, database.py
- Тести (tests/): conftest.py, test_issues.py, test_users.py
- Читати: docs/api-contract.md — GET /users (2.2), POST /issues (2.3), GET /issues (2.4), GET /issues/{id} (2.5)
- Критерії: docs/requirements.md — US-01 (AC-01-01, AC-01-02, AC-01-03), US-03 (AC-03-01, AC-03-02); довідник User (FR-05, Розділ 4.1)
- Сценарії: T01, T02, T03, T13


## B. Зміни й стани
- Код (app/): schemas.py, services.py, routes.py, database.py
- Тести (tests/): test_issues.py
- Читати: docs/api-contract.md — правила PATCH (2.6); переходи статусів (2.7)
- Критерії: docs/requirements.md — US-04 (AC-04-01, AC-04-02, AC-04-03, AC-04-04), US-05 (AC-05-01, AC-05-02), US-06 (AC-06-01, AC-06-02)
- Сценарії: T07, T08, T09, T10, T14


## C. Коментарі
- Код (app/): schemas.py, services.py, routes.py, database.py
- Тести (tests/): test_comments.py
- Читати: docs/api-contract.md — POST /issues/{id}/comments (2.8), GET /issues/{id}/comments (2.9)
- Критерії: docs/requirements.md — US-07 (AC-07-01, AC-07-02, AC-07-03), US-01 (AC-01-03)
- Сценарії: T11, T12


## D. Фільтри
- Код (app/): schemas.py, services.py, routes.py
- Тести (tests/): test_issues.py
- Читати: docs/api-contract.md — GET /issues (2.4), параметри status і priority
- Критерії: docs/requirements.md — US-02 (AC-02-01, AC-02-02)
- Сценарії: T04, T05, T06
