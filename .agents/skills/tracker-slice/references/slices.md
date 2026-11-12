# Зрізи Mini Issue Tracker


Назви розділів docs/ замініть на фактичні назви у ваших документах.
Якщо маршрути розміщено в main.py, замініть routes.py на main.py.


## A. Створення й читання
- Код (app/): schemas.py, services.py, routes.py, database.py
- Тести (tests/): conftest.py, test_issues.py
- Читати: docs/api-contract.md — POST /issues, GET /issues, GET /issues/{id}
- Критерії: docs/requirements.md — <US-xx, AC-xx-yy>
- Сценарії: T01, T02, T03, T13


## B. Зміни й стани
- Код (app/): schemas.py, services.py, routes.py, database.py
- Тести (tests/): test_issues.py
- Читати: docs/api-contract.md — правила PATCH; переходи статусів
- Критерії: docs/requirements.md — <US-xx, AC-xx-yy>
- Сценарії: T07, T08, T09, T10, T14


## C. Коментарі
- Код (app/): schemas.py, services.py, routes.py, database.py
- Тести (tests/): test_comments.py
- Читати: docs/api-contract.md — POST і GET /issues/{id}/comments
- Критерії: docs/requirements.md — <US-xx, AC-xx-yy>
- Сценарії: T11, T12


## D. Фільтри
- Код (app/): schemas.py, services.py, routes.py
- Тести (tests/): test_issues.py
- Читати: docs/api-contract.md — GET /issues, параметри status і priority
- Критерії: docs/requirements.md — <US-xx, AC-xx-yy>
- Сценарії: T04, T05, T06
