# Mini Issue Tracker — REST API Контракт
**Версія**: 1.0 (APPROVED)  
**Єдине джерело бізнес-правил**: [docs/requirements.md](requirements.md)  
**Архітектурна основа**: [docs/architecture.md](architecture.md)  
**Формат обміну даними**: `application/json; charset=utf-8`  
**Часовий пояс та формат дат**: UTC, ISO 8601 (`YYYY-MM-DDTHH:MM:SSZ`)  

---

## 1. Загальні конвенції контракту

1. **Єдине джерело істини**: Усі правила нормалізації рядків (`trim`), допустимі межі довжин, матриця переходів статусів `3 × 3` (Розділ 5), семантика часткового оновлення `PATCH` (Розділ 6) та пріоритет перевірок помилок `422 → 404 → 409` (Розділ 7) визначені у [docs/requirements.md](requirements.md).
2. **Сувора схема вхідних даних**: Усі вхідні JSON-тіла перевіряються з правилом `extra = "forbid"`. Передача будь-якого невідомого або системного поля (`id`, `created_at`, `issue_id`) негайно повертає `422 Unprocessable Entity`.
3. **Формат помилок**:
   * Помилки валідації схеми (`422 Unprocessable Entity`) повертаються у стандартному форматі FastAPI / Pydantic (`{"detail": [{"loc": [...], "msg": "...", "type": "..."}]}`).
   * Доменні помилки (`404 Not Found`, `409 Conflict`) повертаються у форматі `{"detail": "Опис причини відхилення"}`.

---

## 2. Специфікація маршрутів (Endpoints)

### 2.1. `GET /health` — Технічна перевірка працездатності сервісу

* **HTTP Method та Path**: `GET /health`
* **Path / Query Parameters**: Відсутні.
* **Request Body Schema**: Відсутнє.
* **Response Codes**:
  * `200 OK` — Сервіс запущений та готовий обробляти запити.

#### Приклад успішного запиту та відповіді (`200 OK`)
**Запит:**
```http
GET /health HTTP/1.1
```
**Відповідь (`200 OK`):**
```json
{
  "status": "ok"
}
```

---

### 2.2. `GET /users` — Отримання тестового довідника користувачів

* **HTTP Method та Path**: `GET /users`
* **Path / Query Parameters**: Відсутні.
* **Request Body Schema**: Відсутнє.
* **Response Codes**:
  * `200 OK` — Повертає фіксований список із двох синтетичних користувачів (`1 — Agent A`, `2 — Agent B`), впорядкований за `id ASC`.

#### Приклад успішного запиту та відповіді (`200 OK`)
**Запит:**
```http
GET /users HTTP/1.1
```
**Відповідь (`200 OK`):**
```json
[
  {
    "id": 1,
    "name": "Agent A"
  },
  {
    "id": 2,
    "name": "Agent B"
  }
]
```

---

### 2.3. `POST /issues` — Створення нової заявки

* **HTTP Method та Path**: `POST /issues`
* **Path / Query Parameters**: Відсутні.
* **Request Body Schema (`application/json`)**:
  | Поле | Тип | Обов'язковість | Дефолт | Правила валідації ([docs/requirements.md](requirements.md#41-специфікація-сутностей-і-полів)) |
  | :--- | :--- | :--- | :--- | :--- |
  | `title` | `string` | **Так** | — | Не `null`; після `trim` довжина від `3` до `120` символів включно. |
  | `description` | `string` | Ні | `""` | Не `null`; довжина від `0` до `2000` символів включно. |
  | `priority` | `string` | Ні | `"medium"` | Строгий `enum`: `"low"`, `"medium"`, `"high"` (регістрозалежний). Не `null`. |
  | `assignee_id` | `integer \| null` | Ні | `null` | Допустимі значення: `1`, `2` або `null`. |
  *(Поля `id`, `status`, `created_at` клієнтом не передаються; початковий `status` завжди встановлюється сервером у `"OPEN"`).*
* **Response Codes**:
  * `201 Created` — Заявку успішно створено та збережено в SQLite. Повертає створений об'єкт.
  * `422 Unprocessable Entity` — Відсутнє поле `title`, порушено обмеження довжини після `trim`, передано невірний `priority`, неіснуючий `assignee_id` (поза `[1, 2]`), `null` у недозволеному полі або невідоме поле.

#### Приклад успішного запиту та відповіді (`201 Created`)
**Запит:**
```http
POST /issues HTTP/1.1
Content-Type: application/json

{
  "title": "  Fix payment gateway timeout  ",
  "description": "Requests to payment provider fail after 30s under load.",
  "priority": "high",
  "assignee_id": 1
}
```
**Відповідь (`201 Created`):**
```json
{
  "id": 1,
  "title": "Fix payment gateway timeout",
  "description": "Requests to payment provider fail after 30s under load.",
  "status": "OPEN",
  "priority": "high",
  "assignee_id": 1,
  "created_at": "2026-11-01T12:00:00Z"
}
```

#### Приклад відповіді з помилкою (`422 Unprocessable Entity`)
**Запит (назва після `trim` містить лише 2 символи):**
```http
POST /issues HTTP/1.1
Content-Type: application/json

{
  "title": "  ab  ",
  "priority": "medium"
}
```
**Відповідь (`422 Unprocessable Entity`):**
```json
{
  "detail": [
    {
      "loc": ["body", "title"],
      "msg": "String should have at least 3 characters after trimming",
      "type": "string_too_short"
    }
  ]
}
```

---

### 2.4. `GET /issues` — Перегляд та фільтрація списку заявок

* **HTTP Method та Path**: `GET /issues`
* **Path Parameters**: Відсутні.
* **Query Parameters**:
  | Параметр | Тип | Обов'язковість | Правила та поведінка |
  | :--- | :--- | :--- | :--- |
  | `status` | `string` | Ні | Строгий `enum`: `"OPEN"`, `"IN_PROGRESS"`, `"CLOSED"` (регістрозалежний). |
  | `priority` | `string` | Ні | Строгий `enum`: `"low"`, `"medium"`, `"high"` (регістрозалежний). |
  *(При одночасній передачі `status` та `priority` застосовується логічне **`AND`**. Вибірка завжди сортується за `created_at ASC, id ASC`).*
* **Request Body Schema**: Відсутнє.
* **Response Codes**:
  * `200 OK` — Повертає масив заявок (або порожній масив `[]`, якщо збігів немає).
  * `422 Unprocessable Entity` — У query-параметрах `status` або `priority` передано значення поза допустимим `enum`.

#### Приклад успішного запиту та відповіді (`200 OK`)
**Запит:**
```http
GET /issues?status=OPEN&priority=high HTTP/1.1
```
**Відповідь (`200 OK`):**
```json
[
  {
    "id": 1,
    "title": "Fix payment gateway timeout",
    "description": "Requests to payment provider fail after 30s under load.",
    "status": "OPEN",
    "priority": "high",
    "assignee_id": 1,
    "created_at": "2026-11-01T12:00:00Z"
  }
]
```

---

### 2.5. `GET /issues/{id}` — Отримання детальної інформації про одну заявку

* **HTTP Method та Path**: `GET /issues/{id}`
* **Path Parameters**:
  * `id` (`integer`, обов'язковий, $> 0$) — Унікальний ідентифікатор заявки.
* **Query Parameters**: Відсутні.
* **Request Body Schema**: Відсутнє.
* **Response Codes**:
  * `200 OK` — Заявку знайдено (незалежно від її статусу, включаючи `CLOSED`).
  * `404 Not Found` — Заявки з вказаним `id` не існує в БД.
  * `422 Unprocessable Entity` — Параметр шляху `id` не є валідним додатним цілим числом.

#### Приклад успішного запиту та відповіді (`200 OK`)
**Запит:**
```http
GET /issues/1 HTTP/1.1
```
**Відповідь (`200 OK`):**
```json
{
  "id": 1,
  "title": "Fix payment gateway timeout",
  "description": "Requests to payment provider fail after 30s under load.",
  "status": "OPEN",
  "priority": "high",
  "assignee_id": 1,
  "created_at": "2026-11-01T12:00:00Z"
}
```

---

### 2.6. `PATCH /issues/{id}` — Часткове оновлення атрибутів заявки

* **HTTP Method та Path**: `PATCH /issues/{id}`
* **Path Parameters**:
  * `id` (`integer`, обов'язковий, $> 0$) — Ідентифікатор цільової заявки.
* **Query Parameters**: Відсутні.
* **Request Body Schema (`application/json`)**:  
  Виконується згідно з єдиними правилами часткового оновлення та транзакційної атомарності ([docs/requirements.md, Розділ 6](requirements.md#6-семантика-часткового-оновлення-patch)):
  | Поле | Тип | Обов'язковість | Семантика Missing vs `null` та валідація |
  | :--- | :--- | :--- | :--- |
  | `title` | `string` | Ні | Якщо ключ відсутній — не змінюється. Якщо передано `null` — `422`. Якщо рядок — `trim`, довжина `3..120`. |
  | `description` | `string` | Ні | Якщо ключ відсутній — не змінюється. Якщо передано `null` — `422`. Якщо рядок — довжина `0..2000`. |
  | `priority` | `string` | Ні | Якщо ключ відсутній — не змінюється. Якщо передано `null` — `422`. Строгий `enum`: `"low"`, `"medium"`, `"high"`. |
  | `assignee_id` | `integer \| null` | Ні | Якщо ключ відсутній — не змінюється. Якщо `1` або `2` — призначає виконавця. **Якщо `null` — знімає призначення виконавця**. Інші числа — `422`. |
  *(Порожній об'єкт `{}` для відкритої заявки є валідним `no-op` і повертає `200 OK`. Передача поля `status` або будь-яких невідомих полів відхиляється з кодом `422`).*
* **Response Codes**:
  * `200 OK` — Передані поля атомарно оновлено; повертається повний актуальний об'єкт заявки.
  * `404 Not Found` — Заявки з вказаним `id` не існує.
  * `409 Conflict` — Заявка перебуває в термінальному статусі `CLOSED` (редагування основних даних та виконавця заборонене).
  * `422 Unprocessable Entity` — Хоча б одне поле не пройшло валідацію (жодна зміна із запиту не зберігається).

#### Приклад успішного запиту та відповіді (`200 OK` — зняття виконавця та зміна пріоритету)
**Запит:**
```http
PATCH /issues/1 HTTP/1.1
Content-Type: application/json

{
  "priority": "medium",
  "assignee_id": null
}
```
**Відповідь (`200 OK`):**
```json
{
  "id": 1,
  "title": "Fix payment gateway timeout",
  "description": "Requests to payment provider fail after 30s under load.",
  "status": "OPEN",
  "priority": "medium",
  "assignee_id": null,
  "created_at": "2026-11-01T12:00:00Z"
}
```

---

### 2.7. `PATCH /issues/{id}/status` — Окрема операція зміни статусу заявки

* **HTTP Method та Path**: `PATCH /issues/{id}/status`
* **Path Parameters**:
  * `id` (`integer`, обов'язковий, $> 0$) — Ідентифікатор заявки.
* **Query Parameters**: Відсутні.
* **Request Body Schema (`application/json`)**:
  | Поле | Тип | Обов'язковість | Правила валідації та переходів ([docs/requirements.md, Розділ 5](requirements.md#5-життєвий-цикл-заявки-та-матриця-переходів)) |
  | :--- | :--- | :--- | :--- |
  | `status` | `string` | **Так** | Строгий `enum`: `"OPEN"`, `"IN_PROGRESS"`, `"CLOSED"` (регістрозалежний, не `null`). |
* **Response Codes**:
  * `200 OK` — Виконано дозволений перехід (`OPEN → IN_PROGRESS`, `OPEN → CLOSED`, `IN_PROGRESS → CLOSED`) або ідемпотентне встановлення вже поточного статусу (`OPEN → OPEN`, `IN_PROGRESS → IN_PROGRESS`, `CLOSED → CLOSED`).
  * `404 Not Found` — Заявки з вказаним `id` не існує.
  * `409 Conflict` — Спроба виконати заборонений матрицею перехід назад (`IN_PROGRESS → OPEN`, `CLOSED → OPEN`, `CLOSED → IN_PROGRESS`).
  * `422 Unprocessable Entity` — Поле `status` відсутнє, має значення `null`, не входить до `enum` або передано сторонні поля.

#### Приклад успішного запиту та відповіді (`200 OK`)
**Запит:**
```http
PATCH /issues/1/status HTTP/1.1
Content-Type: application/json

{
  "status": "IN_PROGRESS"
}
```
**Відповідь (`200 OK`):**
```json
{
  "id": 1,
  "title": "Fix payment gateway timeout",
  "description": "Requests to payment provider fail after 30s under load.",
  "status": "IN_PROGRESS",
  "priority": "medium",
  "assignee_id": null,
  "created_at": "2026-11-01T12:00:00Z"
}
```

#### Приклад відповіді з помилкою (`409 Conflict`)
**Запит (спроба повернути закриту заявку у статус `OPEN`):**
```http
PATCH /issues/1/status HTTP/1.1
Content-Type: application/json

{
  "status": "OPEN"
}
```
**Відповідь (`409 Conflict`):**
```json
{
  "detail": "Invalid status transition from CLOSED to OPEN"
}
```

---

### 2.8. `POST /issues/{id}/comments` — Додавання коментаря до заявки

* **HTTP Method та Path**: `POST /issues/{id}/comments`
* **Path Parameters**:
  * `id` (`integer`, обов'язковий, $> 0$) — Ідентифікатор заявки (дозволено для заявок у будь-якому статусі, включаючи `CLOSED`).
* **Query Parameters**: Відсутні.
* **Request Body Schema (`application/json`)**:
  | Поле | Тип | Обов'язковість | Правила валідації ([docs/requirements.md](requirements.md#сутність-comment-коментар)) |
  | :--- | :--- | :--- | :--- |
  | `author_id` | `integer` | **Так** | Не `null`; строго `1` (`Agent A`) або `2` (`Agent B`). |
  | `text` | `string` | **Так** | Не `null`; після `trim` довжина від `1` до `1000` символів включно. |
* **Response Codes**:
  * `201 Created` — Коментар успішно збережено та прив'язано до заявки.
  * `404 Not Found` — Заявки з вказаним `id` не існує.
  * `422 Unprocessable Entity` — Порожній після `trim` або занадто довгий `text` ($> 1000$), `author_id` поза довідником `[1, 2]`, відсутні обов'язкові поля або передані зайві ключі.

#### Приклад успішного запиту та відповіді (`201 Created`)
**Запит:**
```http
POST /issues/1/comments HTTP/1.1
Content-Type: application/json

{
  "author_id": 2,
  "text": "  Root cause identified: connection pool limit reached.  "
}
```
**Відповідь (`201 Created`):**
```json
{
  "id": 1,
  "issue_id": 1,
  "author_id": 2,
  "text": "Root cause identified: connection pool limit reached.",
  "created_at": "2026-11-01T12:15:00Z"
}
```

#### Приклад відповіді з помилкою (`422 Unprocessable Entity`)
**Запит (текст складається лише з пробілів та передано невідомого автора `author_id: 99`):**
```http
POST /issues/1/comments HTTP/1.1
Content-Type: application/json

{
  "author_id": 99,
  "text": "     "
}
```
**Відповідь (`422 Unprocessable Entity`):**
```json
{
  "detail": [
    {
      "loc": ["body", "author_id"],
      "msg": "author_id must be one of the predefined users: 1 or 2",
      "type": "value_error"
    },
    {
      "loc": ["body", "text"],
      "msg": "Comment text cannot be empty after trimming",
      "type": "string_too_short"
    }
  ]
}
```

---

### 2.9. `GET /issues/{id}/comments` — Отримання списку коментарів заявки

* **HTTP Method та Path**: `GET /issues/{id}/comments`
* **Path Parameters**:
  * `id` (`integer`, обов'язковий, $> 0$) — Ідентифікатор заявки.
* **Query Parameters**: Відсутні.
* **Request Body Schema**: Відсутнє.
* **Response Codes**:
  * `200 OK` — Повертає масив коментарів заявки у хронологічному порядку створення (`ORDER BY created_at ASC, id ASC`). Якщо до існуючої заявки ще немає коментарів, повертає порожній масив `[]`.
  * `404 Not Found` — Заявки з вказаним `id` не існує в БД.
  * `422 Unprocessable Entity` — Параметр шляху `id` не є валідним додатним цілим числом.

#### Приклад успішного запиту та відповіді (`200 OK`)
**Запит:**
```http
GET /issues/1/comments HTTP/1.1
```
**Відповідь (`200 OK`):**
```json
[
  {
    "id": 1,
    "issue_id": 1,
    "author_id": 2,
    "text": "Root cause identified: connection pool limit reached.",
    "created_at": "2026-11-01T12:15:00Z"
  }
]
```

