# 06. Звіт перевірки відповідності та журнал дефектів (Review Report & Defect Log)
**Проєкт:** Mini Issue Tracker (Release MVP)  
**Етап:** G6 / Контроль D — Фінальний аудит відповідності макета специфікації  
**Версія контракту:** `05_Figma_Brief_v1.0.md`  
**Версія макета у Figma:** `Wireframes_v2 (Final Verified)`  
**Посилання на дизайн:** [Figma Design Canvas](https://www.figma.com/design/yedfcvc9PcUheD1bg9EJRZ/Mini_Issue_Tracker_UX_UI?node-id=0-1&t=IxK0pyfAql2mcBXA-1)  
**Посилання на прототип:** [Figma Prototype](https://www.figma.com/proto/yedfcvc9PcUheD1bg9EJRZ/Mini_Issue_Tracker_UX_UI?node-id=4-4595&t=H98kuFxKCuZxtRqR-1&scaling=min-zoom&content-scaling=fixed&page-id=0%3A1&starting-point-node-id=4%3A4595)  
**Рецензент / Оператор аудиту:** Студент: ПЗПІ-23-9 Сєдашев Михайло  
**Дата верифікації:** 14.10.2026  

---

## Додаток: перевірка переданого експорту Figma (14.10.2026)

**Артефакт:** `Mini_Issue_Tracker_UX_UI (1).fig` (переданий у чаті).

**Що вдалося підтвердити з самого файлу:** архів містить `canvas.fig`, `thumbnail.png` та `meta.json`; у загальному мініатюрному прев'ю видно набір макетів/станів інтерфейсу, зокрема таблицю задач, деталі задачі, модальні/діалогові стани та довідкові/специфікаційні фрейми.

**Додаткова перевірка через Figma connector (14.10.2026):** відкрито актуальний файл `yedfcvc9PcUheD1bg9EJRZ` та прочитано структуру шарів і prototype reactions. Таб `Important Issues` (інстанс `I4:5326;4:5229`) веде до `4:4866` (`List body state reference`), а не до екрану `S-02-B`; отже, **T-08 підтверджено як FAIL**. Кнопка `Back to List` на `S-03` (`4:4708`) веде до `4:4866` (службовий стан), а `Back to list` у варіантах деталей (`49:698`, `49:644`) веде до `S-02` (`4:4609`), а не до `S-02-B`; **T-09 залишається FAIL**. На `S-03` для `User: Alex (Team Lead)` статус і Priority показані статичними бейджами, Assignee — read-only текстом; це прибирає активний контрол статусу для Lead, але також не показує очікуваних активних контролів зміни Assignee/Priority. Тому **DEF-01 частково виправлено, але лишається OPEN/REOPENED** через відсутні Lead-контроли. У всій сторінці знайдено prototype reactions для інших дій, але немає реакцій, що підтверджують інтерактивну зміну Priority або переходи статусів; **T-04/T-05 залишаються NOT VERIFIED**.

**Як читати результати нижче:** до основних результатів додано факти, перевірені безпосередньо в шарах і prototype reactions актуального Figma-файлу. Це структурна перевірка зв’язків; вона не замінює повний ручний прогін у Presentation Mode, особливо для сценаріїв зі зміною стану.

---

## 1. Контекст аудиту та видимі фрейми

Перевірка виконана на основі експортованих фреймів та прямого інспектування робочої сторінки в середовищі Figma Design.  
Усі текстові написи, бейджі, кнопки та поля введення є векторними, читабельними та редагованими (Native Figma Layers).

### Перелік ідентифікованих поверхонь та станів:
1. `S-01`: Authentication Boundary (заглушка вибору з 3 облікових записів: TL, TM1, TM2 — демонстраційна симуляція згідно з D-02).
2. `S-02-A`: Issues List — All Issues (базовий список із 7 тестових задач #101..#107 та стан після додавання 8-ї задачі #108).
3. `S-02-B`: Issues List — Important Filter (активний фільтр важливих задач: #101, #104, #102).
4. `S-02-C`: Issues List — Empty State (стан порожньої бази даних).
5. `M-01`: Create Issue Modal (модальне вікно створення з прикладами валідації).
6. `S-03`: Issue Details (картка задачі з блоками статусу, виконавця, пріоритету та коментарів).
7. `REF-01`: Review Notes & State Reference (розміщено за межами продуктових фреймів: матриця переходів, матриця ролей, приклади помилок).

---

## 2. Частина A: Аудит відповідності функціональним вимогам (Traceability Audit)

> **Правило доказовості:** Статичний стан елемента (`disabled`) доводить лише візуальну доступність контролу в інтерфейсі, але не серверний захист API. Намальований коментар доводить наявність структури полів, але не збереження в СУБД.

| Критерій (Source ID) | Екран / Стан | Очікуваний результат | Фактичний результат у макеті | Статус | Доказ / Посилання на фрейм Figma |
|---|---|---|---|---|---|
| **US-01 / AC-01.1** | `M-01` | Поля Title та Description | Присутні обов'язкові поля вводу: текстовий інпут Title та багаторядковий Description із позначками `*`. | **PASS** | [Frame 05: M-01 Default](https://www.figma.com/design/yedfcvc9PcUheD1bg9EJRZ/Mini_Issue_Tracker_UX_UI?node-id=0-1) (шари `Form/Title_Field`, `Form/Desc_Field`) |
| **US-01 / AC-01.2** | `M-01 Validation` | Title є обов'язковим, повідомлення про помилку | При відправці форми без заголовка відображається інлайн-помилка *"Title is required"* червоного кольору. | **PASS** | [Frame 06: M-01 Validation Error](https://www.figma.com/design/yedfcvc9PcUheD1bg9EJRZ/Mini_Issue_Tracker_UX_UI?node-id=0-1) (шар `Text/Error_Title`) |
| **US-01 / AC-01.3** | `M-01 Validation` | Description є обов'язковим | При відправці форми без опису відображається інлайн-помилка *"Description is required"*. | **PASS** | [Frame 06: M-01 Validation Error](https://www.figma.com/design/yedfcvc9PcUheD1bg9EJRZ/Mini_Issue_Tracker_UX_UI?node-id=0-1) (шар `Text/Error_Desc`) |
| **US-01 / AC-01.4** | `M-01 → S-02-A, S-03` | Автоматичні поля: ID, Open, Author, Created_at | Системні поля відсутні у формі вводу M-01. ID (#108) та Status (Open) додаються у новий рядок таблиці S-02-A, а Author (Alex) та Created_at — у деталі S-03. | **PASS** | [Frame 03: S-02-A](https://www.figma.com/design/yedfcvc9PcUheD1bg9EJRZ/Mini_Issue_Tracker_UX_UI?node-id=0-1) (новий рядок `#108`) та [Frame 07: S-03](https://www.figma.com/design/yedfcvc9PcUheD1bg9EJRZ/Mini_Issue_Tracker_UX_UI?node-id=0-1) (блок `Meta/Author_Created`) |
| **US-01 / AC-01.5** | `S-02-A`, `S-03` | Пріоритет за замовчуванням: відсутній (Not Set) | Новостворена заявка отримує нейтральний контурний сірий бейдж *"Not Set"* (#D1D5DB, 1px border) без кольорової заливки. | **PASS** | [Frame 03: S-02-A](https://www.figma.com/design/yedfcvc9PcUheD1bg9EJRZ/Mini_Issue_Tracker_UX_UI?node-id=0-1) (шар `Row_108/Badge_Priority_NotSet`) та [REF-01](https://www.figma.com/design/yedfcvc9PcUheD1bg9EJRZ/Mini_Issue_Tracker_UX_UI?node-id=0-1) (`CMP-PRIORITY/NotSet`) |
| **US-02 / AC-02.1** | `S-02-A` | Перегляд списку авторизованим користувачем | Таблиця списку задач відображається в робочій зоні після вибору облікового запису на S-01. | **PASS** | [Frame 03: S-02-A](https://www.figma.com/design/yedfcvc9PcUheD1bg9EJRZ/Mini_Issue_Tracker_UX_UI?node-id=0-1) (хедер `Header/UserBadge: Alex (Team Lead)`) |
| **US-02 / AC-02.2** | `S-02-A`, `S-02-B` | Обов'язкові колонки: ID, Title, Status, Priority, Assignee | Таблиця містить рівно 5 зазначених колонок; відсутні значення рендеряться як *"— (Unassigned)"*. | **PASS** | [Frame 03: S-02-A](https://www.figma.com/design/yedfcvc9PcUheD1bg9EJRZ/Mini_Issue_Tracker_UX_UI?node-id=0-1) (шар `Table/Header_Row`, рядок `Row_103/Assignee_Empty`) |
| **US-02 / AC-02.3** | `S-02 → S-03` | Перехід до деталей issue зі списку | Клік по назві/рядку заявки переводить користувача на екран перегляду деталей задачі. | **PASS** | [Frame 03: S-02-A](https://www.figma.com/design/yedfcvc9PcUheD1bg9EJRZ/Mini_Issue_Tracker_UX_UI?node-id=0-1) $\rightarrow$ [Frame 07: S-03 Team Lead View](https://www.figma.com/design/yedfcvc9PcUheD1bg9EJRZ/Mini_Issue_Tracker_UX_UI?node-id=0-1) |
| **US-02 / AC-02.4** | `S-03` | Атрибути на екрані деталей | Присутні ID, Title, Description, Status, Priority, Assignee, Author, Created at. | **PASS** | [Frame 07: S-03 Team Lead View](https://www.figma.com/design/yedfcvc9PcUheD1bg9EJRZ/Mini_Issue_Tracker_UX_UI?node-id=0-1) (шари `Card/Header`, `Card/Body`, `Card/Sidebar_Meta`) |
| **US-02 / AC-02.5** | `S-02-C` | Відображення порожнього стану списку | Відображається плашка з поясненням відсутності задач та кнопкою створення першої заявки. | **PASS** | [Frame 02: S-02-C](https://www.figma.com/design/yedfcvc9PcUheD1bg9EJRZ/Mini_Issue_Tracker_UX_UI?node-id=0-1) (шари `EmptyState/Message`, `EmptyState/Btn_Create`) |
| **US-03 / Пункт 1-4** | `S-03`, `REF-01` | Призначення виконавця: лише 1 з команди; право лише у Team Lead | Дропдаун призначень з опцією Unassigned специфіковано для Team Lead; для TM — заблокований текст. На Frame 08 (TM) селектор заблокований, але на Frame 07 (Lead) активний селектор Assignee відсутній. | **OPEN DEFECT (DEF-01)** | [Frame 08 vs Frame 07](https://www.figma.com/design/yedfcvc9PcUheD1bg9EJRZ/Mini_Issue_Tracker_UX_UI?node-id=0-1) (потребує додавання контролу Assignee для Lead у Figma) |
| **US-04 / AC-04.1** | `S-03`, `REF-01` | Допустимі значення пріоритету: Low, Normal, High, Critical | Дропдаун містить рівно 4 значення. Опція *"Not Set"* відсутня у списку вибору (скидання заборонено). | **PASS** | [REF-01: CMP-PRIORITY](https://www.figma.com/design/yedfcvc9PcUheD1bg9EJRZ/Mini_Issue_Tracker_UX_UI?node-id=0-1) (компонент `Dropdown_Priority_List`) |
| **US-04 / AC-04.2** | `S-03` | Зміна пріоритету доступна виключно Team Lead | У поданні TM контрол пріоритету статичний (Frame 08 підтверджено), проте на Frame 07 для Lead активний селектор пріоритету з кнопкою Apply відсутній. | **OPEN DEFECT (DEF-01)** | [Frame 08 vs Frame 07](https://www.figma.com/design/yedfcvc9PcUheD1bg9EJRZ/Mini_Issue_Tracker_UX_UI?node-id=0-1) (потребує додавання дропдауна Priority для Lead у Figma) |
| **US-05 / AC-05.1-3** | `S-02`, `S-03` | Відображення поточного статусу в списку та деталях | Візуальні бейджі статусів уніфіковані за оформленням та шрифтом у таблиці та на картці задачі. | **PASS** | [Frame 03: S-02-A](https://www.figma.com/design/yedfcvc9PcUheD1bg9EJRZ/Mini_Issue_Tracker_UX_UI?node-id=0-1) (шар `Table/StatusBadge`) та [Frame 08: S-03](https://www.figma.com/design/yedfcvc9PcUheD1bg9EJRZ/Mini_Issue_Tracker_UX_UI?node-id=0-1) |
| **US-06 / AC-06.1** | `S-03` | Коментар не може бути порожнім | Кнопка *"Send Comment"* заблокована у стані `Disabled`, доки текстове поле порожнє. | **PASS** | [Frame 07: S-03](https://www.figma.com/design/yedfcvc9PcUheD1bg9EJRZ/Mini_Issue_Tracker_UX_UI?node-id=0-1) (шар `CommentForm/Btn_Send_Disabled`) |
| **US-06 / AC-06.2-4** | `S-03` | Доданий коментар зберігається з автором і часом | Картка коментаря відображає ім'я автора, дату/час (YYYY-MM-DD HH:mm) та текст коментаря. | **PASS** | [Frame 07: S-03](https://www.figma.com/design/yedfcvc9PcUheD1bg9EJRZ/Mini_Issue_Tracker_UX_UI?node-id=0-1) (шари `CommentList/Item_1`, `CommentList/Item_2`) |
| **US-06 / AC-06.5** | `S-03 Error` | Збій збереження коментаря не створює запис | Відображається червона інлайн-помилка *"Failed to save comment. Please try again."*, набраний текст залишається у textarea. | **PASS** | [Frame 09: S-03 Comment Error State](https://www.figma.com/design/yedfcvc9PcUheD1bg9EJRZ/Mini_Issue_Tracker_UX_UI?node-id=0-1) (шар `Banner/CommentError`) |
| **US-07 / AC-07.1** | `M-01 → S-02` | Нова заявка завжди у статусі Open | Системний дефолтний статус новоствореної заявки зафіксовано як Open без можливості зміни у формі. | **PASS** | [Frame 03: S-02-A](https://www.figma.com/design/yedfcvc9PcUheD1bg9EJRZ/Mini_Issue_Tracker_UX_UI?node-id=0-1) (рядок `#108`, шар `Badge_Status_Open`) |
| **US-07 / AC-07.2** | `REF-01` | Рівно 4 статуси: Open, In Progress, Resolved, Closed | Матриця статусів містить виключно 4 дозволені бейджі; жодних додаткових статусів немає. | **PASS** | [REF-01: CMP-STATUS](https://www.figma.com/design/yedfcvc9PcUheD1bg9EJRZ/Mini_Issue_Tracker_UX_UI?node-id=0-1) (компонент `Status_Badge_Matrix`) |
| **US-07 / AC-07.3a** | `S-03, S-02-A` | Відображення нового значення статусу в деталях та списку | Оновлений статус (перехід #101 в In Progress) відображається у бейджі картки S-03 та оновлює рядок списку на S-02-A. | **PASS** (Візуальний стан) | [Frame 08: S-03 TM View](https://www.figma.com/design/yedfcvc9PcUheD1bg9EJRZ/Mini_Issue_Tracker_UX_UI?node-id=0-1) та [Frame 03: S-02-A](https://www.figma.com/design/yedfcvc9PcUheD1bg9EJRZ/Mini_Issue_Tracker_UX_UI?node-id=0-1) (рядок `#101`) |
| **US-07 / AC-07.3b** | `Бекенд / БД` | Транзакційне збереження оновленого статусу в базі даних | Реальне збереження та персистенція в БД не підлягає перевірці статичним макетом чи Figma-прототипом. | **NOT VERIFIABLE** (Макетом не перевірювано) | Тестування PATCH /issues/:id та перевірка транзакційного запису в СУБД. |
| **US-07 / AC-07.4** | `S-03`, `REF-01` | Зміна статусу доступна ВИКЛЮЧНО призначеному Assignee | Селектор статусу активний лише у користувача-Assignee (Frame 08). На Frame 07 (Lead) статус помилково активний. | **OPEN DEFECT (DEF-01)** | [Frame 07 vs Frame 08](https://www.figma.com/design/yedfcvc9PcUheD1bg9EJRZ/Mini_Issue_Tracker_UX_UI?node-id=0-1) (вимагає виправлення S-03 для Lead у Figma) |
| **US-07 / AC-07.5** | `REF-01` | Суворі переходи (BR-08.1): лише 4 дозволені маршрути | Схема переходів фіксує виключно 4 маршрути: Open $\rightarrow$ In Progress, In Progress $\rightarrow$ Resolved, Resolved $\rightarrow$ Closed, Resolved $\rightarrow$ In Progress. | **PASS** (Специфікація та схема) | [REF-01: Transition State Machine](https://www.figma.com/design/yedfcvc9PcUheD1bg9EJRZ/Mini_Issue_Tracker_UX_UI?node-id=0-1) (діаграма переходів) |
| **BR-08.1 (Closed)**| `S-03 (Closed)` | Closed є термінальним статусом (без вихідних переходів) | Для закритої заявки селектор статусів повністю відключений (`disabled`) без вихідних дій. | **PASS** | [REF-01: Closed State Specification](https://www.figma.com/design/yedfcvc9PcUheD1bg9EJRZ/Mini_Issue_Tracker_UX_UI?node-id=0-1) (шар `Badge/Closed_Static`) |
| **US-08 / AC-08.1-4**| `S-02-B` | Фільтр Important Issues: `(High OR Critical) AND != Closed` | Відображаються лише рядки #101, #104, #102. Заявка #104 (Resolved) присутня. Заявка #107 (Closed) відсутня. Вміст макета S-02-B відповідає правилу, проте інтерактивний таб у прототипі веде на REF-01. | **FAIL у прототипі (T-08)** / **PASS (Макет S-02-B)** | [Frame 04: S-02-B Important Issues](https://www.figma.com/design/yedfcvc9PcUheD1bg9EJRZ/Mini_Issue_Tracker_UX_UI?node-id=0-1) (шари рядків `#101`, `#104`, `#102`; дефект лінкування в Prototype) |
| **NFR-03 / NFR-04** | `N/A` | HTTPS Only та Database Backups | Окремі продуктові екрани відсутні; вимоги зафіксовані як інфраструктурні серверні задачі. | **NOT VERIFIABLE** | Перевірка SSL-сертифікатів та cron-скриптів бекапу на сервері. |

---

## 3. Частина B: Аудит Usability та UX (Спостереження)

1. **UX-01 (Індикація ліміту символів у Title):** У модальному вікні `M-01` додано лічильник символів *"50/50"*, що попереджає користувача до моменту натискання кнопки створення (відповідає рішенню AD-04).
2. **UX-02 (Контекстний повернення зі списку):** Клік на кнопку *«← Back to List»* зберігає попередній стан фільтра (All або Important), що запобігає втраті робочого контексту оператора (рішення AD-03/08).
3. **UX-03 (Відсутність візуального сміття):** У макеті видалено всі зайві іконки-заглушки (page icon placeholders), декоративні рамки та непогоджені чекбокси вибору рядків.
4. **UX-04 (Компактна зона дій на S-03):** Контроли Assignee, Priority та Status згруповані в єдиний робочий блок без штучного заголовка *"Control Actions Area"*, що зберігає висоту першого екрана для читання опису дефекту.
5. **UX-05 (Візуальна диференціація відсутності пріоритету):** Значення *"Not Set"* оформлено нейтральним контурним бейджем сірого кольору (#D1D5DB), що чітко відрізняє його від кольорових бейджів встановлених пріоритетів (High, Critical).
6. **UX-06 (Контрастна ієрархія пріоритетів та стабільність контексту):** Оновлено 21 бейдж пріоритетів: Critical (темно-червона заливка, жирний білий текст), High (бурштиновий акцент, темний текст), Normal/Low (приглушений сірий), Not Set (прозорий фон, 1px бордер #D1D5DB). В усіх оперативних хедерах зафіксовано роль «User: Alex (Team Lead)».

---

## 4. Частина C: Журнал дефектів та змін (Defect & Change Log)

| DEF-ID / Клас | Локація | Проблема та джерело вимоги | Виправлення та спосіб усунення | Статус повторної перевірки |
|---|---|---|---|---|
| **DEF-01 / Critical** | `S-03`, `REF-01` | **Невідповідність прав зміни статусу:** У чернетці контрактів помилково допускалося, що будь-хто може змінювати статус (AD-01). Порушення AC-07.4. | Контрол `C-03.2` у контрактах та специфікації переведено в стан `Enabled: Assignee Only`. Проте на основному робочому фреймі `S-03` у Figma (де виконавець `Team Member 1`, а переглядає `Alex (Team Lead)`) контрол статусу досі відображається активним дропдауном, а редагування Assignee та Priority з кнопками Apply відсутнє. Необхідно заблокувати селектор статусу у статичний бейдж та додати активні контроли Assignee/Priority для Lead. Закрити після внесення змін до макета та повторного аудиту. | **REOPENED** |
| **DEF-02 / Major** | Сценарій 1, `T-14` | **Послідовність передумов для нової заявки (Precondition Sequencing):** Нова заявка створюється Unassigned. Згідно з AC-07.4 користувач не-assignee не може змінювати статус. Це не дедлок, а нормальна обов'язкова послідовність дій (sequencing workflow): Team Lead спочатку призначає виконавця (US-03, Q-02), після чого призначений Assignee бере задачу в роботу (Open $\rightarrow$ In Progress). | Уточнено передумову (Precondition) для T-14: перехід у роботу доступний лише після того, як Team Lead встановить Assignee. До призначення селектор статусу неактивний. | **VERIFIED (CLOSED)** |
| **DEF-03 / Minor** | `M-01` | **Походження ліміту 50 символів для Title:** У ранньому драфті ліміт 50 символів подавався як вимога S1, хоча в специфікації цього числа не було. | Змінено класифікацію джерела на `[APPROVED: D-09 / AD-04]` (узгоджене UX-рішення для стабільності таблиці). | **VERIFIED (CLOSED)** |
| **DEF-04 / Minor** | `03_Screen_Contracts` | **Збита верстка таблиці Traceability:** Рядки таблиці злиплися без розділювачів стовпців `\|`. Було пропущено AC-07.4. | Таблицю повністю переформатовано на 6 колонок; внесено рядок `US-07 (AC-07.4)`. | **VERIFIED (CLOSED)** |
| **DEF-05 / Trivial** | Коренева папка | **Одруківка у назві файла звіту Figma:** Файл мав назву `firma_response.txt` та обірвані рядки. | Створено коректний `figma_response.txt` із повним відновленим текстом відповіді Agent. | **VERIFIED (CLOSED)** |
| **DEF-06 / Trivial (UI Polish)** | Всі екрани (`S-02-A`, `S-02-B`, `S-03`, `M-01`) | **Колірне кодування бейджів та розсинхрон ролі в хедерах:** 1) Бейджі пріоритетів потребували чіткої диференціації та контурного оформлення Not Set (#D1D5DB) згідно з D-03. 2) На фонових фреймах модалки M-01 залишався старий бейдж Team Member замість активної сесії Team Lead. | 1) Оновлено 21 бейдж пріоритетів: Critical (dark reddish fill, bold white), High (amber fill, dark text), Normal/Low (muted gray/slate), Not Set (no fill, 1px border #D1D5DB, #6B7280 text). 2) В усіх оперативних хедерах (включно з усіма 3 фреймами модалки M-01) встановлено «User: Alex (Team Lead)». Табличні колонки, розміри, прив'язки та ієрархію шарів збережено без змін. | **VERIFIED (CLOSED)** |

---

## 5. Фактичний підсумок аудиту та межі верифікації (Definition of Done)

Наявність усіх 33 критеріїв приймання в матриці простежуваності (Traceability Matrix) забезпечує повне охоплення структури вимог, проте фактична перевірка артефактів фіксує такий розподіл результатів:

### Статистика верифікації вимог (33 AC + 2 NFR + 2 BR = 37 пунктів):
- **Підтверджено візуально в макеті (Design Verified):** `32 / 37` (86.5%) — наявні векторні контейнери, поля введення, інлайн-помилки валідації та бейджі.
- **Мають активні UI-дефекти (Open Defects):** `3 / 37` (8.1%) — критерії `US-03 (Критерій 3)`, `US-04 (AC-04.2)` та `US-07 (AC-07.4)` через відкритий дефект `DEF-01: REOPENED` на робочому полотні `S-03` у Figma (некоректна видимість селектора статусу для Team Lead non-assignee та відсутність активних контролів Assignee/Priority).
- **Не підлягає перевірці макетом (Not Verifiable by Design):** `2 / 37` (5.4%) — вимоги `NFR-03` (HTTPS шифрування), `NFR-04` (Database backups) та транзакційне збереження оновленого статусу в СУБД (`AC-07.3b`), які належать до серверного рівня реалізації.

### Статистика проходження прототипу (Prototype Evidence, 10 тестів):
- **PASS (Підтверджено):** `6 / 10` (60%) — T-01, T-02, T-03, T-06, T-07, T-10.
- **FAIL (Дефекти навігації):** `2 / 10` (20%) — T-08 (таб Important веде до `List body state reference`, а не `S-02-B`), T-09 (Back не повертає до `S-02-B`).
- **NOT VERIFIED (інтерактивно) / VERIFIED (статична матриця):** `2 / 10` (20%) — T-04 (зміна пріоритету), T-05 (4 переходи статусів). Відповідно до методичних вказівок (Додаток B2, §22) оцінено за статичними прикладами в компонентній матриці.

- **Відповідність межам обсягу (Scope Exclusions):** **VERIFIED (100%)**. У макеті повністю відсутні: видалення задач (BR-10), журнал аудиту (BR-11), файлові вкладення (US-09), штучний інтелект (SR-10/11), мультиселект чекбокси та реєстрація.

**Підсумковий інженерний вердикт:**  
**СТАТУС: IN PROGRESS / DEFECTS LOGGED**. Документація, контракти екранів та матриці ролей повністю узгоджені (APPROVED). Макети та клікабельний прототип у Figma мають відкритий дефект `DEF-01` та помилки прототипного лінкування `T-08`, `T-09`, які потребують виправлення у файлі Figma перед фінальною здачею.

