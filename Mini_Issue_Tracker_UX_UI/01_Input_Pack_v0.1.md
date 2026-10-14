UX/UI Design Input Pack: Mini Issue Tracker
Підтвердження прочитаного файлу та структури
Назва прочитаного файлу: SD_Spec..

Доступні розділи файлу:

Customer Request

Discovery / Problem Analysis (Problem Statement, Product Business goal, Stakeholders, Primary Users, Constraints, Assumptions, Open Questions та відповіді)

Product Vision + Initial Product Scope (Product Vision, Initial Product Scope, Out of Scope на поточному етапі, Initial Product Capabilities)

Stakeholder Needs & Stakeholder Requirements (SR-01 – SR-11, Business Rules BR-01 – BR-12)

Prioritization of Needs + Candidate MVP (Prioritized Stakeholder Requirements, Candidate MVP, Future / Deferred Requirements)

Detailed Functional Requirements Specification / User Stories + Acceptance Criteria (Epic 1, US-01 – US-09 з критеріями приймання та Gherkin-сценаріями, Dependencies)

Quality Attributes + Security Requirements (Приклади NFR: NFR-01 – NFR-04)

Feasibility, Estimation & Risk Assessment (Попередня оцінка, Основні ризики R-01 – R-03, Technical feasibility, Recommended scope adjustment)

MVP / Release Scope (Release MVP, Deferred, Future, Updated NFRs)

UX/UI & Interaction Design (розділ лише заявлений як заголовок; зміст відсутній).

Статус повноти: Матеріал специфікації містить повний аналітичний цикл до етапу проектування інтерфейсу. Останній розділ «UX/UI & Interaction Design» є порожнім заголовком без тексту, тому вхідні дані сформовано виключно на основі аналітичних розділів 1–9.

1. Product Purpose, Actors та межі першого релізу
Product Purpose: Внутрішня вебсистема для невеликої команди розробників, призначена для централізованої реєстрації, перегляду, відстеження життєвого циклу та координації вирішення проблем програмного продукту з можливістю швидкого виявлення важливих невирішених заявок, спрямована на скорочення часу від виявлення дефекту до його призначення й закриття.

Primary Actors:

Team Member: Член команди розробників, який створює заявки, переглядає їхній список та деталі, бере участь в обговоренні через коментарі, переглядає важливі заявки та керує статусом призначеної йому заявки.

Team Lead: Керівник команди, який володіє всіма можливостями Team Member, а також має виключні права на призначення відповідального виконавця та встановлення/зміну пріоритету заявки.

Secondary Stakeholders (поза основними сценаріями MVP): Product Owner / замовник, System Administrator.

Межі першого релізу (Release MVP Boundaries):

Включає виключно функції реєстрації дефектів, перегляду списку та деталей, призначення одного виконавця, встановлення пріоритету лідом, фіксації та перегляду статусів, додавання коментарів та перегляду списку важливих відкритих заявок (US-01 – US-08).

Обмежено середовищем Web Application для єдиної внутрішньої команди з 3 заздалегідь визначеними користувачами (2 Team Member, 1 Team Lead).

2. Класифікація обсягу (Scope Classification)
Included in Release MVP:

US-01 — Create Issue.

US-02 — View Issues.

US-03 — Assign Issue to the responsible team member.

US-04 — Set Issue Priority.

US-05 — Track Issue Progress.

US-06 — Add Comment.

US-07 — Update Issue Status.

US-08 — View Important Open Issues.

Deferred (відкладено з Candidate MVP на наступні релізи):

US-09 (SR-09) — Attach files to an issue (перенесено через високу технічну складність: сховище файлів, ліміти розміру, антивірусне сканування, бекап).

Future Requirements (за межами найближчих релізів):

SR-10 — Automatic issue categorization (AI-класифікація).

SR-11 — Automatic priority recommendation (AI-рекомендація пріоритету).

Explicitly Out of Scope (прямо виключено зі специфікації):

Customer support portal.

Billing.

Source-code hosting.

Continuous Integration / Continuous Delivery.

Time tracking.

Full project management.

Mobile application.

Інтеграція з зовнішніми системами (GitHub, GitLab, Jira чи іншими трекерами).

Видалення заявок.

Окрема користувацька історія змін issue.

Доступ зовнішніх клієнтів.

3. Деталізовані включені User Stories та Acceptance Criteria
Story US-01 — Create Issue
ID: US-01

Actor: Team Member (будь-який автентифікований член команди).

Мета: I want to create an issue with a title and description So that a problem is recorded and can be tracked.

Критерії приймання:

AC-01.1: Користувач може ввести: Title, Description.

AC-01.2: Title є обов'язковим.

AC-01.3: Description є обов'язковим.

AC-01.4: Після створення заявка отримує: ID, status = Open, created_at, author.

AC-01.5: Після створення issue його priority не встановлено.

Пов'язані сценарії BDD з вихідного тексту:

Сценарій для AC-01: Given the user is authenticated And the user is on the "New Issue" page When the user enters the title "Login fails" And enters the description "Application crashes after login" And clicks "Create" Then a new issue should be created And the issue status should be "Open" And the issue should have a unique ID And the issue should contain the current user as its author.

Сценарій для AC-02 (валідація обов'язковості): Given the user is creating a new issue When the user leaves the title empty And clicks "Create" Then the issue should not be created And the system should display "Title is required".

Story US-02 — View Issues
ID: US-02

Actor: Team Member.

Мета: I want to view registered issues, so that I can see which problems have been reported and inspect their current details.

Критерії приймання:

AC-02.1 — View issue list: Авторизований член команди може переглянути список зареєстрованих issues.

AC-02.2 — Issue information in the list: Для кожного issue у списку відображаються щонайменше: ID; Title; Status; Priority; Assignee, якщо він призначений.

AC-02.3 — View issue details: Користувач може вибрати issue зі списку та відкрити сторінку його деталей.

AC-02.4 — Issue details: На сторінці issue відображаються: ID; Title; Description; Status; Priority; Assignee, якщо він призначений; Author; Created at.

AC-02.5 — Empty list: Якщо зареєстрованих issues немає, система відображає порожній список або повідомлення про відсутність issues.

Story US-03 — Assign Issue to the responsible team member
ID: US-03

Actor: Team Lead.

Мета: Я хочу призначити заявку члену команди, щоб було зрозуміло, хто відповідає за її виконання.

Критерії приймання (у вихідному тексті подані списком без окремих літерно-цифрових індексів):

Можна вибрати одного assignee.

Assignee повинен бути членом команди.

Призначати заявку може лише Team Lead.

Поточний assignee відображається у заявці.

Story US-04 — Set Issue Priority
ID: US-04

Actor: Team Lead.

Мета: Я хочу встановлювати пріоритет заявки, щоб команда могла визначити порядок роботи.

Критерії приймання:

AC-04.1: Допустимі значення встановленого Priority: Low, Normal, High, Critical.

AC-04.2: Встановлювати та змінювати priority може лише Team Lead.

Story US-05 — Track Issue Progress
ID: US-05

Actor: Team Member.

Мета: As a team member, I want to see the current status of an issue, so that I can understand the current progress of work on the issue.

Критерії приймання:

AC-05.1: Поточний status відображається для кожного issue.

AC-05.2: Status відображається на сторінці issue.

AC-05.3: Status відображається у списку issues.

Story US-06 — Add Comment
ID: US-06

Actor: Team Member (член команди).

Мета: Я хочу додавати коментарі до заявки, щоб обговорювати проблему.

Критерії приймання:

AC-06.1: Comment text cannot be empty.

AC-06.2: Added comment is stored and shown for the issue.

AC-06.3: Comment author is stored and displayed.

AC-06.4: Creation date/time is stored and displayed.

AC-06.5: Failed save does not create a comment and produces an error.

Story US-07 — Update Issue Status
ID: US-07

Actor: Член команди, відповідальний за заявку (Assignee).

Мета: Я хочу змінювати статус заявки, щоб команда бачила поточний стан роботи над проблемою.

Критерії приймання:

AC-07.1: Нова заявка створюється зі статусом Open.

AC-07.2: Допустимі статуси: Open, In Progress, Resolved, Closed.

AC-07.3: Після зміни статусу система зберігає нове значення та відображає його при наступному перегляді заявки.

AC-07.4: Користувач, який не є виконавцем заявки, не може змінити її статус.

AC-07.5: Система не дозволяє встановити значення статусу, якого немає у визначеному переліку.

Story US-08 — View Important Open Issues
ID: US-08

Actor: Team Member (член команди).

Мета: Я хочу швидко бачити важливі відкриті заявки, щоб зосередитися на проблемах, які потребують першочергової уваги.

Критерії приймання:

AC-08.1: Заявка з priority = High і статусом, відмінним від Closed, відображається у списку Important Issues.

AC-08.2: Заявка з priority = Critical і статусом, відмінним від Closed, відображається у списку Important Issues.

AC-08.3: Заявки з priority = Low або Normal не відображаються у списку Important Issues.

AC-08.4: Заявки зі status = Closed не відображаються незалежно від priority.

4. UI-релевантні бізнес-правила (Business Rules)
Автентифікація та доступність дій за ролями (Permissions):

Системою можуть користуватися виключно автентифіковані члени команди.

Створювати issue може будь-який автентифікований член команди.

Призначати виконавця (Assignee) може тільки Team Lead. Користувач Team Member не повинен мати активного елемента керування призначенням.  [TYPE: DERIVED: Базується на прямому обмеженні прав у BR-06 та US-03]

Встановлювати та змінювати priority може виключно Team Lead.

Змінювати статус заявки має право виключно призначений виконавець (Assignee) цієї заявки.

Будь-який користувач, який не є поточним Assignee (включно з Team Lead, якщо він не призначений виконавцем), не має права змінювати статус. Елемент переходу статусу повинен бути заблокований або прихований для не-виконавців.  [TYPE: DERIVED: Прямий наслідок заборони в AC-07.4]

Початкові значення під час створення заявки (Initial Values):

Початковий статус завжди автоматично встановлюється у Open.

Початковий пріоритет обов'язково є не встановленим: Not Set (порожній стан). Поле не повинно містити дефолтного значення на зразок Low чи Normal.

Системні атрибути при генерації: автоматичне присвоєння унікального ID, фіксація автора (author = поточний автентифікований користувач) та часу створення (created_at).

Словники значень та правила переходів (State Transitions):

Priority: Дозволені встановлені значення — Low, Normal, High, Critical. Стан Not Set є відсутністю встановленого значення, а не одним із рівнів пріоритету.

Status: Дозволені значення — Open, In Progress, Resolved, Closed. Встановлення будь-яких інших статусів суворо заборонено.

Дозволені переходи статусів (State Machine):

Open → In Progress

In Progress → Resolved

Resolved → Closed

Resolved → In Progress (повторне відкриття роботи).

Недопустимі переходи статусів (Заборонені дії): Будь-які переходи, крім чотирьох перелічених вище, заборонені (наприклад, заборонено Open → Resolved, Open → Closed, In Progress → Closed, In Progress → Open, Closed → будь-який інший статус). Інтерфейс вибору статусу повинен пропонувати лише валідні цільові статуси згідно з поточним станом.  [TYPE: DERIVED: Пряме обмеження матриці переходів]

Правила відображення Important Issues:

У списку Important Issues відображаються заявки, які одночасно відповідають двом критеріям:

Пріоритет: High або Critical.

Статус: будь-який активний статус, відмінний від Closed.

Статус Resolved: Заявка зі статусом Resolved вважається вирішеною, але НЕ закритою. До переходу в Closed вона вважається активною і обов'язково відображається серед Important Issues, якщо має пріоритет High або Critical. Інтерфейс у жодному разі не повинен ототожнювати Resolved із Closed.

Виключення з Important Issues:

Заявки зі статусом Closed — виключаються завжди, незалежно від призначеного пріоритету.

Заявки з пріоритетом Low або Normal — ніколи не потрапляють до Important Issues.

Заявки з пріоритетом Not Set — не потрапляють до Important Issues, оскільки не відповідають умові High/Critical.  [TYPE: DERIVED: Наслідок визначення важливих заявок]

Правила для коментарів (Comments):

Текст коментаря не може бути порожнім. Кнопка відправки повинна блокуватися при порожньому вводі або валідуватися з помилкою.

Кожен збережений коментар повинен відображати: текст коментаря, автора (author), дату та час створення (created at).

Помилка збереження (Failed save): якщо збереження не вдалося, коментар не створюється, а інтерфейс обов'язково повинен відобразити повідомлення про помилку користувачеві.

Абсолютні заборони системи (Forbidden Actions):

Видалення заявок повністю заборонено (відсутність кнопок "Видалити", "Delete" в UI).

Окрема користувацька історія змін (Audit Log / Activity History) для issue у першій версії не передбачена і не проектується в інтерфейсі.

Завантаження та прикріплення файлів (Attachments) виключено з першого релізу (в інтерфейсі відсутні зони drag-and-drop та кнопки прикріплення файлів).

Автоматична зміна статусу, категорії або пріоритету через AI заборонена (AI-функціонал взагалі відсутній у MVP).

5. Нефункціональні вимоги (NFRs)
UI-релевантні NFR (перевіряються макетом / впливають на інтерфейс)
NFR-01: Час відповіді системи (Response time) < 1 s.

Вплив на UI: Необхідність проектування візуальних станів завантаження (skeleton screens, спінери або індикатори виконання) для дій створення заявки, збереження коментаря та оновлення статусів/пріоритетів, щоб інтерфейс сигналізував про виконання операції без затримок сприйняття.  [TYPE: DERIVED: Стандартне UX-відображення для часових рамок відгуку]

NFR-02: Обов'язкова автентифікація (Authentication required).

Вплив на UI: Необхідність наявності інтерфейсу входу/перемикання користувачів або відображення поточного активного профілю в шапці (header) системи.  [TYPE: DERIVED: Вимога відображення контексту автентифікованого користувача]

Валідація та обробка помилок (Error States):

Відображення тексту помилки валідації "Title is required", якщо поле назви порожнє.

Відображення стану порожнього списку (Empty state) або тексту про відсутність заявок, якщо в системі немає даних.

Відображення візуального повідомлення про помилку при невдалій спробі збереження коментаря.

NFR, які НЕ перевіряються макетом (System & Infrastructure NFRs)
NFR-03: HTTPS only — шифрування трафіку на рівні транспортного протоколу (інфраструктурне налаштування сервера та сертифікатів).

NFR-04: Резервне копіювання всіх даних (Backup of all data) — автоматичні бекапи бази даних на рівні інфраструктури зберігання.

6. Відкриті питання, конфлікти та прогалини (Q-ID)
Q-ID	Категорія	Опис проблеми / конфлікту	Джерело специфікації	Необхідне рішення людини
Q-01	Конфлікт бізнес-правил (Status Transition deadlock)
BR-08 та US-07 стверджують: змінювати статус може тільки призначений виконавець (assignee). Заявка створюється зі статусом Open та без виконавця (Assignee = Not Set). Перехід Open → In Progress згідно з BR-08.1 є першим кроком. Якщо виконавець не призначений, ніхто не має права перевести задачу в In Progress. Якщо ж виконавець призначений, але робота ще не почалася, чи може Team Lead змінити статус, або чи повинен статус змінюватися автоматично при призначенні?

BR-03, BR-08, BR-08.1, US-03, US-07 (AC-07.4)

UNRESOLVED: Потрібно вирішити: чи дозволено Team Lead переводити нерозподілену заявку в роботу, чи статус змінюється суворо після обов'язкового призначення Assignee самим цим Assignee?
Q-02	Прогалина прав (Призначення на нерозподілену заявку)
Згідно з US-03, призначати заявку може лише Team Lead. Чи може Team Member взяти нерозподілену заявку на себе самостійно ("Assign to me"), чи призначення відбувається виключно директивно через ліда?

SR-03, US-03 Acceptance Criteria 03, Open Questions

UNRESOLVED: Уточнити, чи допустимий сценарій самопризначення для Team Member, чи діє сувора монополія Team Lead.
Q-03	Прогалина логіки (Зняття або зміна Assignee)
US-03 вказує "можна вибрати одного assignee". Не описано, чи має право Team Lead зняти призначення взагалі (Unassign), повернувши заявку у стан без виконавця, і чи можна перепризначити іншого виконавця на статусах In Progress або Resolved.

US-03

UNRESOLVED: Визначити поведінку: чи підтримується очищення поля Assignee та ре-асайн під час виконання робіт.
Q-04	Прогалина логіки (Скидання пріоритету)
BR-05 зазначає: "До встановлення priority допускається стан Не встановлено (пусте значення)". US-04 описує лише встановлення значень Low, Normal, High, Critical. Не вказано, чи може Team Lead після встановлення пріоритету скинути його назад у Not Set.

BR-04, BR-05, US-04 (AC-04.1)

UNRESOLVED: Визначити, чи є вибір пріоритету незворотним (можна лише змінювати між 4 значеннями), чи можливе повернення до Not Set.
Q-05	Прогалина UX (Спосіб автентифікації 3 користувачів)
BR-01 та Open Questions фіксують 3 користувачів (2 Team Member, 1 Team Lead), а ризик R-01 прямо вказує: "спосіб реалізації authentication потребує уточнення". Не визначено, як саме відбувається вхід у MVP (форма логін/пароль чи спрощений UI-перемикач ролей/акаунтів для тестування прототипу).

Open Questions, BR-01, R-01

UNRESOLVED: Необхідно зафіксувати механіку входу/ідентифікації користувача для відображення на макетах.
Q-06	Прогалина UI (Формат представлення списку Important Issues)
US-08 формулює потребу: "швидко бачити важливі відкриті заявки". Критерії визначають правила фільтрації (High/Critical та не Closed), але не специфікують, чи це окрема сторінка/вкладка, чи збережений фільтр/віджет на головному дашборді списку заявок.

SR-08, US-02, US-08

UNRESOLVED: Дизайнеру потрібне узгодження: окремий це екран (View) чи швидкий фільтр на загальному списку.
Q-07	Прогалина валідації (Обмеження полів вводу)
US-01 вимагає обов'язковості Title та Description, US-06 вимагає непорожнього тексту коментаря. Проте максимальна довжина заголовка, ліміти символів або підтримка форматування тексту (Plain text vs Markdown) у специфікації відсутні.

US-01 (AC-01.2, AC-01.3), US-06 (AC-06.1)

UNRESOLVED: Задати максимальні ліміти довжини символів для Title, Description та Comment.
7. Source Check
Included US → Усі їхні AC → Місце у цьому Pack
US-01 (Create Issue):

AC-01.1 (Введення Title, Description) → Розділ 3 (US-01)

AC-01.2 (Title є обов'язковим) → Розділ 3 (US-01) та Розділ 5 (NFR/Validation)

AC-01.3 (Description є обов'язковим) → Розділ 3 (US-01)

AC-01.4 (Присвоєння ID, Open, created_at, author) → Розділ 3 (US-01) та Розділ 4 (Initial Values)

AC-01.5 (Priority не встановлено) → Розділ 3 (US-01) та Розділ 4 (Initial Values)

BDD AC-01, BDD AC-02 → Розділ 3 (US-01) та Розділ 5 (NFR/Validation)

US-02 (Vew Issues):

AC-02.1 (Перегляд списку) → Розділ 3 (US-02)

AC-02.2 (Поля списку: ID, Title, Status, Priority, Assignee) → Розділ 3 (US-02)

AC-02.3 (Перехід на сторінку деталей) → Розділ 3 (US-02)

AC-02.4 (Поля деталей: ID, Title, Description, Status, Priority, Assignee, Author, Created at) → Розділ 3 (US-02)

AC-02.5 (Empty list state) → Розділ 3 (US-02) та Розділ 5 (NFR/Validation)

US-03 (Assign Issue to the responsible team member):

Критерій 1 (Один assignee) → Розділ 3 (US-03)

Критерій 2 (Assignee є членом команди) → Розділ 3 (US-03)

Критерій 3 (Призначати може лише Team Lead) → Розділ 3 (US-03) та Розділ 4 (Permissions)

Критерій 4 (Поточний assignee відображається у заявці) → Розділ 3 (US-03)

US-04 (Set Issue Priority):

AC-04.1 (Допустимі значення: Low, Normal, High, Critical) → Розділ 3 (US-04) та Розділ 4 (State Transitions)

AC-04.2 (Встановлювати/змінювати може лише Team Lead) → Розділ 3 (US-04) та Розділ 4 (Permissions)

US-05 (Track Issue Progress):

AC-05.1 (Status відображається для кожного issue) → Розділ 3 (US-05)

AC-05.2 (Status на сторінці issue) → Розділ 3 (US-05)

AC-05.3 (Status у списку issues) → Розділ 3 (US-05)

US-06 (Add Comment):

AC-06.1 (Comment не може бути порожнім) → Розділ 3 (US-06) та Розділ 4 (Comments)

AC-06.2 (Збереження та відображення коментаря) → Розділ 3 (US-06) та Розділ 4 (Comments)

AC-06.3 (Author зберігається і відображається) → Розділ 3 (US-06) та Розділ 4 (Comments)

AC-06.4 (Created date/time зберігається і відображається) → Розділ 3 (US-06) та Розділ 4 (Comments)

AC-06.5 (Failed save не створює запис і дає помилку) → Розділ 3 (US-06), Розділ 4 (Comments), Розділ 5 (NFR/Validation)

US-07 (Update Issue Status):

AC-07.1 (Нова заявка зі статусом Open) → Розділ 3 (US-07) та Розділ 4 (Initial Values)

AC-07.2 (Допустимі статуси: Open, In Progress, Resolved, Closed) → Розділ 3 (US-07) та Розділ 4 (State Transitions)

AC-07.3 (Збереження та відображення нового статусу) → Розділ 3 (US-07)

AC-07.4 (Лише виконавець змінює статус; заборона не-виконавцям) → Розділ 3 (US-07) та Розділ 4 (Permissions)

AC-07.5 (Заборона недопустимих значень статусу) → Розділ 3 (US-07) та Розділ 4 (State Transitions)

US-08 (View Important Open Issues):

AC-08.1 (High + статус не Closed → у списку Important) → Розділ 3 (US-08) та Розділ 4 (Important Issues)

AC-08.2 (Critical + статус не Closed → у списку Important) → Розділ 3 (US-08) та Розділ 4 (Important Issues)

AC-08.3 (Low / Normal → не відображаються у Important) → Розділ 3 (US-08) та Розділ 4 (Important Issues)

AC-08.4 (Closed → не відображаються у Important ніколи) → Розділ 3 (US-08) та Розділ 4 (Important Issues)

Перелік Excluded вимог із причиною виключення
US-09 / SR-09 (Attach files to an issue): Включає критерії AC-09.1 – AC-09.6. Причина виключення: Перенесено у Deferred згідно з розділом MVP / Release Scope через надмірну технічну складність та ризик R-03 (вимагає окремого сховища файлів, обмеження розміру, інтеграції malware-сканування та бекапу файлів).

SR-10 (Automatic issue categorization): Причина виключення: Віднесено до категорії Future / Out of MVP згідно з розділом MVP / Release Scope та пріоритезацією "Won't for now" (висока невизначеність та брак тренувальних даних).

SR-11 (Automatic priority recommendation): Причина виключення: Віднесено до категорії Future / Out of MVP згідно з розділом MVP / Release Scope та обмеженням KC-06.

Видалення заявки (Delete Issue): Причина виключення: Прямо заборонено бізнес-правилом BR-10 та відповідями Open Questions.

Історія змін заявки (Change History / Audit Trail): Причина виключення: Прямо виключено для першої версії системи згідно з BR-11 та відповідями Open Questions.

Мобільний застосунок (Mobile App): Причина виключення: Прямо виключено згідно з Out of Scope та припущенням A-07.

Зовнішні інтеграції (Jira, GitHub, GitLab): Причина виключення: Прямо обмежено обмеженням KC-05.

Список нерозв'язаних питань (Unresolved Questions)
Q-01: Конфлікт між зміною статусу тільки виконавцем (Assignee) та відсутністю виконавця на старті для переходу Open → In Progress.

Q-02: Відсутність визначення можливості самопризначення ("Take to work" / "Assign to me") для Team Member.

Q-03: Відсутність правил щодо скидання призначення (Unassign) та перепризначення під час виконання робіт.

Q-04: Відсутність правила щодо можливості скидання пріоритету назад у стан Not Set.

Q-05: Відсутність затвердженого технічного/інтерфейсного механізму автентифікації 3 фіксованих користувачів (Ризик R-01).

Q-06: Відсутність конкретизації UI-формату списку Important Issues (окремий екран чи фільтр у таблиці).

Q-07: Відсутність граничних лімітів довжини та дозволеного формату для полів Title, Description, Comment.

Документ сформовано як аналітичний вхідний пакет (UX/UI Design Input Pack). Пакет не оголошується погодженим до моменту офіційного вирішення питань Q-01 – Q-07 зацікавленими сторонами.