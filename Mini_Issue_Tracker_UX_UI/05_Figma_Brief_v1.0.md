# Figma Design Implementation Brief: Mini Issue Tracker (Release MVP)

## 1. Purpose and Scope

- **Product Purpose:**  Internal web-based issue tracking system for a small development team to register, view, track lifecycle progress, and coordinate resolution of software defects with focus on critical open items [S1: Vision, Customer Request].
- **Release Scope:**  Core tracking workflow covering User Stories US-01 through US-08 [S1: Release Scope].
- **User Base:**  Exactly three predefined team members: one Team Lead (TL), two Team Members (TM1, TM2) [S1: BR-01, Open Questions]. No external users, registration, or self-sign-up [S1: KC-04].

## 2. Design Constraints & Figma Requirements

- **Deliverable Format:**  A single Figma page containing editable native vector layers, semantic text layers, and local components [Instruction].
- **Fidelity & Styling:**  Grayscale low-fidelity wireframe. Use system/neutral fonts (Inter or Roboto), structured grayscale palette (white, grays, black), consistent spacing (8px grid), and functional borders. No decorative illustrations, unstyled square placeholders, or brand colors [Instruction].
- **Layout Structure:**  Use native Figma Auto Layout across all containers, lists, rows, headers, and modal overlays [Instruction].
- **Layer Hygiene:**  Clear semantic layer naming (e.g., Row/IssueItem, Badge/Status/InProgress, Btn/Primary/Default). Group components logically; do not leave default names like Frame 412 or Rectangle 12 [Instruction].
- **Prototyping Level:**  Static wireframe canonical frames with explicit textual transition sticky callouts/annotations placed strictly outside the product artboards. Do not implement complex Figma conditional prototyping logic or variables [Instruction].
- **Control Cleanliness:**  No row checkboxes, no multi-select bulk action bars, and no arbitrary icon placeholders [Instruction].

## 3. Canonical Screens, Modals & States (Exact IDs)

### Canonical Frames for Canvas

- **S-01:** Authentication Boundary (Placeholder)
- **S-02-A:** Issues List — All Issues (Default View)
- **S-02-B:** Issues List — Important Issues Filter (Active Filter View)
- **S-02-C:** Issues List — Empty State (Zero Data View)
- **M-01:** Create Issue Modal (Overlay over S-02)
- **S-03:** Issue Details Screen (Canonical Work Surface)
### State Reference Components (Compact Matrix placed outside main frames)

- **CMP-STATUS:** Status Badge in all 4 permitted values (Open, In Progress, Resolved, Closed) [S1: BR-07].
- **CMP-PRIORITY:** Priority Badge in all 5 visual states (Not Set, Low, Normal, High, Critical) [S1: BR-04, BR-05].
- **CMP-ROLES:** 4 distinct authorization state examples for S-03 action header:
  - Lead assignee
  - Lead non-assignee
  - Member assignee
  - Member non-assignee

## 4. Required Labels, Visible Data & Missing Values

### Data Rules per View

#### Header / Global Context (S-02, S-03)
- **App Title:** "Mini Issue Tracker" [S1: Vision]
- **Current User Badge:** Displays active user and role, e.g., "User: Alex (Team Lead)" [S1: NFR-02; D-ID: AD-02].

#### Issue List Table Columns (S-02)
- **ID:** Monospace/bold text (e.g., #101) [S1: AC-02.2].
- **Title:** Truncated single-line text [S1: AC-02.2; D-ID: AD-04].
- **Status:** Visual badge [S1: AC-02.2, AC-05.3].
- **Priority:** Visual badge. Missing value: "Not Set" (plain neutral gray tag) [S1: BR-04, AC-01.5].
- **Assignee:** Name text. Missing value: "—" (dash) or "Unassigned" [S1: AC-02.2].

#### Create Modal Inputs (M-01)
- **Title:** Text input, label "Title *", placeholder "Enter issue title (max 50 chars)" [S1: AC-01.1, AC-01.2; D-ID: AD-04].
- **Description:** Textarea input, label "Description *", placeholder "Enter issue description" [S1: AC-01.1, AC-01.3].
- **System-generated on submit (hidden from form inputs):** ID, Status = Open, Priority = Not Set, Author = Current User, Created_at = Current Time [S1: AC-01.4, AC-01.5, BR-03, BR-04].

#### Issue Details Surface (S-03)
- **Header Meta:** ID, Title, Author, Created at (format: YYYY-MM-DD HH:mm) [S1: AC-02.4].
- **Body:** Description (multiline text box) [S1: AC-02.4].
- **Control Panel:** Explicit sections for Status, Assignee, and Priority [S1: AC-02.4].
- **Comments Thread:** Chronological stream. Each comment card contains Author, Created at, and Comment Body [S1: AC-06.2, AC-06.3, AC-06.4]. Empty state label: "No comments yet" [D-ID: D-03].
- **Comment Input:** Multiline textarea with placeholder "Write a comment..." and action button "Send Comment" [S1: AC-06.1].

## 5. Controls, Actions & Permission Matrix

### Control Definitions

- **C-01.1 [S-01]:** User account picker (TL, TM1, TM2) [S1: BR-01; D-ID: D-01].
- **C-01.2 [S-01]:** Button "Continue / Login" [D-ID: AD-02].
- **C-02.1 [S-02]:** Segmented button "All Issues" [S1: US-02; D-ID: AD-03].
- **C-02.2 [S-02]:** Segmented button "Important Issues" [S1: US-08; D-ID: AD-03].
- **C-02.3 [S-02]:** Primary button "+ Create Issue" [S1: US-01].
- **C-02.4 [S-02]:** Clickable row item leading to S-03 [S1: AC-02.3].
- **C-03.1 [S-03]:** Navigation link "← Back to List" [S1: US-02].
- **C-03.2 [S-03]:** Dropdown Status Selector [S1: US-07].
- **C-03.3 [S-03]:** Button "Apply Status" [D-ID: AD-06].
- **C-03.4 [S-03]:** Dropdown Assignee Selector (Options: TM1, TM2, TL, Unassigned) [S1: US-03; D-ID: AD-05].
- **C-03.5 [S-03]:** Button "Apply Assignee" [D-ID: AD-06].
- **C-03.6 [S-03]:** Dropdown Priority Selector (Options: strictly Low, Normal, High, Critical; no "Not Set" in dropdown) [S1: US-04, AC-04.1; D-ID: AD-07].
- **C-03.7 [S-03]:** Button "Apply Priority" [D-ID: AD-06].
- **C-03.8 [S-03]:** Textarea Comment Input [S1: US-06].
- **C-03.9 [S-03]:** Button "Send Comment" [S1: US-06].

### Canonical Permission Matrix [S1: BR-02, BR-06, US-02, US-03, US-06, AC-07.4]

| Action / Capability | Member non-assignee | Member assignee | Lead non-assignee | Lead assignee | UI Enforcement Rule |
|---|---|---|---|---|---|
| View issues list & details | YES | YES | YES | YES | Renders across all views. |
| Create new issue | YES | YES | YES | YES | + Create Issue button visible and active. |
| Add comment | YES | YES | YES | YES | Textarea and Send Comment button active. |
| Assign / Re-assign / Unassign | NO | NO | YES | YES | For Members: Read-only text. Apply Assignee button is hidden. |
| Change Priority | NO | NO | YES | YES | For Members: Read-only badge. Apply Priority button is hidden. |
| Change Status (per BR-08.1) | NO | YES | NO | YES | For Non-assignees: Status is static badge. Selector and Apply Status button are disabled/hidden [S1: AC-07.4]. |

## 6. Strict Status Transition Rules [S1: BR-07, BR-08, BR-08.1]

- Only the assigned user (Assignee) can execute status changes [S1: AC-07.4].
- A new issue starts at Open [S1: BR-03].
- Transition to In Progress requires that Assignee is already assigned (Assignee != Not Set). If unassigned, status change is blocked [Defect Fix: DEF-02].
- Closed is a terminal status. Once closed, all transition controls are permanently disabled [S1: BR-08.1].
- Transition options in dropdown C-03.2 are strictly restricted by current state:

| From Status | Permitted Next Options in C-03.2 | Forbidden Transitions |
|---|---|---|
| Open | In Progress | Resolved, Closed |
| In Progress | Resolved | Open, Closed |
| Resolved | Closed, In Progress (Reopen) | Open |
| Closed | None (Dropdown disabled) | Open, In Progress, Resolved |

## 7. Important Issues Predicate & Logic [S1: US-08, BR-09, BR-09.1]

### Predicate Formula
$$\text{IsImportant} = (\text{Priority} \in \{\text{High}, \text{Critical}\}) \land (\text{Status} \neq \text{Closed})$$
### Behavior Rules
- **Resolved State Rule:** Resolved indicates resolved but not closed (Resolved != Closed). A High or Critical issue with status Resolved MUST be displayed in the Important Issues view [S1: BR-09.1].- **Exclusion 1:** Any issue with status Closed is never shown in Important Issues, even if Critical [S1: AC-08.4].- **Exclusion 2:** Issues with priority Low, Normal, or Not Set are never shown in Important Issues [S1: AC-08.3].

## 8. Required Empty, Validation & Error States

- **Empty List State (S-02-C):**  Center-aligned card displaying text "No issues found. Create the first issue to get started." and primary button "+ Create Issue" [S1: AC-02.5].
- **Empty Important Filter State (S-02-B Sub-state):**  Table is replaced by banner: "No important open issues matching criteria." [S1: US-08].
- **Modal Required Validation (M-01):**  Red inline error label "Title is required" below Title input when submitted empty [S1: BDD AC-02]. Red outline and "Description is required" when Description is empty.
- **Modal Title Max Length Validation (M-01):**  Input field enforces 50-character limit with counter "50/50" or error message "Title cannot exceed 50 characters" [D-ID: AD-04].
- **Empty Comment State (S-03):**  "Send Comment" button is Disabled as long as comment input is empty or contains only whitespace [S1: AC-06.1].
- **Comment Failed Save Error (S-03):**  Prominent inline error container above input: "Failed to save comment. Please try again." Entered comment text is preserved inside the textarea; no entry is added to thread [S1: AC-06.5].
- **Non-assignee Status Lock (S-03):**  Informational tooltip or disabled state indicator: "Only the assigned team member can update the status." [S1: AC-07.4].

## 9. Navigation Intent & Transitions (Annotation Notes)

- **T-01:** S-01 $\rightarrow$ Click Login $\rightarrow$ Route to S-02-A (or S-02-C if database empty) [D-ID: AD-02].

- **T-02:** S-02 (any state) $\rightarrow$ Click + Create Issue $\rightarrow$ Open M-01 overlay [S1: US-01].

- **T-03:** M-01 $\rightarrow$ Click Cancel or backdrop $\rightarrow$ Close modal, return to underlying S-02 state [S1: US-01].

- **T-04:** M-01 $\rightarrow$ Click Create with invalid fields $\rightarrow$ Retain M-01, show inline error messages [S1: US-01].

- **T-05:** M-01 $\rightarrow$ Click Create with valid fields $\rightarrow$ Close modal, append issue, show S-02-A [S1: AC-01.4].

- **T-06:** S-02-A / S-02-B $\rightarrow$ Click issue row $\rightarrow$ Route to S-03 [S1: AC-02.3].

- **T-07:** S-03 $\rightarrow$ Click ← Back to List $\rightarrow$ Return to S-02 preserving previous filter tab selection (All or Important) [D-ID: AD-03, AD-08].

- **T-08:** S-02-A $\rightarrow$ Click Important Issues tab $\rightarrow$ Switch view to S-02-B [D-ID: AD-03].

- **T-09:** S-02-B $\rightarrow$ Click All Issues tab $\rightarrow$ Switch view to S-02-A [D-ID: AD-03].

- **T-10..T-17:** S-03 $\rightarrow$ Click Apply / Send $\rightarrow$ Update local section state on S-03; stay on S-03 [D-ID: AD-06].

## 10. Sample Data for Mockups

### Issues List Data Set (Demonstrating Priority Sort: Critical → High → Normal → Low → Not Set; Default View is Triage Inbox Sorted by Created_at DESC) [D-ID: D-12 / AD-09]

> **Note on Sorting Models (D-12):** The table below illustrates the explicit **Priority Sort** order (Critical → High → Normal → Low → Not Set). In the system's **Default View** (`S-02-A`), rows are ordered by `Created_at DESC` (Triage Inbox model), ensuring newly registered issues (such as newly created #108 with Not Set priority) immediately surface at the very top of the list for initial triage and verification under test TC-01.

| ID | Title (max 50 chars) | Priority | Status | Assignee | Display in Important Filter? |
|---|---|---|---|---|---|
| #101 | Production database connection timeout | Critical | In Progress | Team Member 1 | YES (Critical + In Progress) |
| #104 | API gateway memory leak on heavy load | Critical | Resolved | Team Lead | YES (Critical + Resolved) |
| #102 | Export to CSV crashes on special characters | High | Open | Team Member 2 | YES (High + Open) |
| #105 | UI button alignment distorted in Safari | Normal | Open | Team Member 1 | NO (Normal Priority) |
| #106 | Minor typo in navigation drawer settings | Low | Resolved | Team Member 2 | NO (Low Priority) |
| #107 | Payment webhook intermittent failure | Critical | Closed | Team Member 1 | NO (Closed Status) |
| #103 | User avatar fails to refresh on profile | Not Set | Open | — (Unassigned) | NO (Not Set Priority) |

### Sample Comments for Issue #101 (S-03)

- **Team Member 1 (2026-10-07 09:15):** "Investigated logs. The pool size is exhausted during peak spikes."
- **Team Lead (2026-10-07 09:30):** "Approved pool size increase to 50 connections. Monitoring performance."

## 11. Absolute Exclusions (Do NOT Design)

The following capabilities are explicitly barred from this release. Any presence in wireframes constitutes an immediate design defect [S1: Out of Scope, KC-05, BR-10, BR-11; Release Scope]:
- **No Delete Controls:**  No delete buttons, archive actions, or trash icons anywhere [S1: BR-10].
- **No Change History / Audit Log:**  No system activity feed showing past field modifications [S1: BR-11].
- **No File Attachments:**  No upload buttons, drag-and-drop file zones, paperclip icons, or file preview widgets (US-09 is Deferred) [S1: Feasibility R-03, Release Scope].
- **No AI Elements:**  No AI triage badges, automatic categorization prompts, or recommendation widgets (SR-10, SR-11 are Future) [S1: KC-06, Release Scope].
- **No Infrastructure Screens:**  No screens or UI controls for HTTPS configuration, server backup schedules, or database dumps (NFR-03, NFR-04 are backend-only) [S1: Quality Attributes].
- **No External Integrations:**  No Jira, GitHub, or GitLab import/export controls [S1: KC-05].
- **No Complex Multi-Tenancy:**  No workspace switchers, organization selectors, or invitation modals [S1: KC-01, BR-01].

## 12. Acceptance Checklist for Design Review

Before handing off the Figma frame canvas, verify that:
- [ ] Exactly 3 full canonical screen frames (S-01, S-02, S-03), 1 modal overlay (M-01), and 3 state representations (S-02-A, S-02-B, S-02-C) exist on the page.
- [ ] S-01 is structured strictly as an account-selection boundary placeholder for the 3 predefined users (TL, TM1, TM2), not a generic public sign-up screen.
- [ ] The list table in S-02 exhibits the 5 required columns: ID, Title, Status, Priority, Assignee.
- [ ] Important Issues view (S-02-B) includes #104 (Critical + Resolved) and excludes #107 (Critical + Closed).
- [ ] In M-01, user input fields are strictly limited to Title and Description. No inputs exist for status, priority, or assignee.
- [ ] In M-01, the title input visibly denotes a 50-character limit and shows required asterisk indicators.
- [ ] In S-03, Assignee and Priority dropdown controls with their Apply buttons are visible/active only for Team Lead. For Team Member, they render as static read-only text.
- [ ] In S-03, status change controls are enabled only if the logged-in user is the current Assignee. Non-assignees see a static status badge.
- [ ] For an issue in Closed status, all status transition controls are visibly disabled.
- [ ] The failed comment save error state is documented with inline error text and preserved textarea input.
- [ ] No delete buttons, attachment zones, audit logs, or AI widgets are present on any surface.
