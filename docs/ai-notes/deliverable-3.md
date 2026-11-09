# Deliverable 3 — AI Disclosure, Prompt Log & Attribution Matrix
**Coursework:** CS 106 / Software Engineering 1  
**Project:** Laundry Pickup and Delivery Management System (`LaundryCare`)  
**Milestone:** Deliverable 3 — Interface & View Binding (Weeks 6–8 · Phase 3: AI ON)  
**Weight:** 30% · Due: End of Week 8  
**Repository Branch:** `main`

---

## 1. Purpose of AI Use in Phase 3 (Weeks 6–8)

In Phase 3 (AI ON), our 5-member engineering team used AI assistants (ChatGPT / Claude / Antigravity) to accelerate component decomposition, asynchronous `fetch()` form binding, and comprehensive failure-state handling across all 5 core CRUD modules (`Laundry Orders`, `Delivery Records`, `Pickup Schedules`, `Customers`, and `Payments`). Every AI-assisted artifact was reviewed, customized for LaundryCare's domain, tested with `pytest`, and verified by its student owner.

---

## 2. Consolidated Prompt Log (Weeks 6–8)

### Week 6 Prompts — Component Architecture & Reachable Screen States

#### Prompt 6.1: Reusable Component Decomposition (`docs/components.md`)
- **Prompt:**
  > *"Analyze our 24 views in LaundryCare (Orders, Deliveries, Pickups, Customers, Payments, Auth, Tracking) and propose a formal component catalog with 12 reusable UI components, defining their inputs, outputs, semantic HTML structure, and parent/child hierarchy."*
- **AI Output:**
  Proposed 12 atomic and molecular components (`SidebarNav`, `TopHeader`, `StatCard`, `FilterToolbar`, `DataTable`, `StatusBadge`, `EmptyState`, `LoadingSkeleton`, `ErrorAlert`, `ModalDialog`, `ReceiptCard`, `ProgressStepper`).
- **Human Review & Refinement:**
  Accepted the 12-component structure, mapped every screen (`list`, `detail`, `create`, `edit`) across all 5 modules to its constituent components in [`docs/components.md`](../components.md), and partitioned ownership across all 5 team members.

#### Prompt 6.2: Reachable Empty, Loading, and Error States on Every List View
- **Prompt:**
  > *"How can we make wireframe states (Empty, Loading skeleton, and Error retry alert) directly reachable on live routes for grading and usability testing without wiping the local SQLite database?"*
- **AI Output:**
  Suggested inspecting `request.args.get('state')` (`?state=empty`, `?state=loading`, `?state=error`) in Jinja2 templates alongside natural zero-record empty state checks (`orders|length == 0`), plus a `.state-preview-bar` switcher.
- **Human Review & Refinement:**
  Implemented across `orders.html`, `deliveries.html`, `pickups.html`, `customers.html`, and `payments.html`, ensuring natural empty-state rendering when the database table has 0 rows and skeleton shimmer placeholders (`static/css/animations.css`) during loading.

---

### Week 7 Prompts — Asynchronous Form Binding & Double-Submit Prevention

#### Prompt 7.1: Dual-Mode Backend Controllers (`200` / `201` / `422` JSON Envelopes)
- **Prompt:**
  > *"How do we update our Flask controller routes (`/laundry-orders-page`, `/delivery-records-page`, `/pickup-schedules-page`, `/customers-page`, `/payments-page` and their `/edit/<id>` routes) so they accept asynchronous `fetch()` JSON requests and return structured field-level 422 validation errors while preserving synchronous form fallbacks?"*
- **AI Output:**
  Provided the `is_async_request()` helper (`controllers/utils.py`) checking `request.is_json`, `X-Requested-With: XMLHttpRequest`, or `Accept: application/json`, returning `jsonify({"status": 422, "error": errors}), 422` on validation failure and `201`/`200` with the persisted record on success.
- **Human Review & Refinement:**
  Integrated into all 5 module controllers (`order_routes.py`, `delivery_routes.py`, `pickup_routes.py`, `customer_routes.py`, `payment_routes.py`) and aligned field keys with exact HTML input `name` attributes.

#### Prompt 7.2: Client-Side Async Form Interceptor (`static/js/form_bindings.js`)
- **Prompt:**
  > *"Write a reusable vanilla JavaScript form binding module (`form_bindings.js`) that intercepts `form[data-async-form]` submissions, disables the submit button with an animated loading spinner (`Saving...`) to prevent double-submits, maps HTTP 422 field errors inline beneath each input without reloading the page, and shows a confirmation toast on 200/201."*
- **AI Output:**
  Generated `bindAsyncForm()`, `displayFieldErrors()`, `clearFormErrors()`, and `showToast()`.
- **Human Review & Refinement:**
  Extended `displayFieldErrors()` to support both Phase 2 (`error.fields`) and Phase 3 (`error`) 422 envelopes, added automatic focus on the first invalid field, and bound all Create modals and Edit pages across all 5 modules.

---

### Week 8 Prompts — Complete Failure Handling (`422` / `404` / `500` / Network) & Human Micro-Copy

#### Prompt 8.1: Dual-Mode Global 404 & 500 Error Handlers (`app.py`, `404.html`, `500.html`)
- **Prompt:**
  > *"Implement Flask `@app.errorhandler(404)` and `@app.errorhandler(500)` handlers that return branded dark-glass HTML pages (`404.html`, `500.html`) for browser navigation and clean JSON envelopes for async `fetch()` calls, ensuring zero stack traces or raw status codes ever reach the user."*
- **AI Output:**
  Provided dual-mode handlers in `app.py` and dark-glass recovery templates in `templates/404.html` and `templates/500.html`.
- **Human Review & Refinement:**
  Added contextual entity-missing messages (e.g., *"Order #ORD-9999 was not found or has been removed"*) and recovery action buttons (*"Return to Dashboard"*, *"Try Again"*).

#### Prompt 8.2: Accessible Destructive Confirmation Modal & Async Row Removal
- **Prompt:**
  > *"Create an accessible confirmation modal (`confirmDestructiveAction` and `handleAsyncDelete` in `form_bindings.js`) so clicking Delete on any record asks for explicit confirmation, shows a `Deleting...` spinner on confirm, handles 200/404/500/network states, and smoothly fades out the deleted table row without a page reload."*
- **AI Output:**
  Generated `confirmDestructiveAction()` and `handleAsyncDelete()` with `.row-fade-out` CSS transition.
- **Human Review & Refinement:**
  Wired `data-delete-url` and `data-item-name` across all 5 module list tables and all 5 edit screens (`edit_order.html`, `edit_delivery.html`, `edit_pickup.html`, `edit_customer.html`, `edit_payment.html`).

---

## 3. Component, View & Binding Attribution Matrix (`AI-generated` / `AI-modified` / `Hand-written`)

Every component, view template, controller binding, and test file produced in Phase 3 is explicitly labeled below:

| Artifact / Component / Binding | File Path | AI Attribution Label | Student Owner | Work Performed & Human Refinement |
|---|---|:---:|---|---|
| **COMP-01: SidebarNav & Layout** | `static/css/sidebar.css`, `templates/*.html` | `AI-modified` | **John Michael D. Bretaña** | AI scaffolded base flex sidebar; Bretaña hand-wired RBAC visibility rules, notification badges, and active route states. |
| **COMP-02: TopHeader & Quick Switcher** | `templates/dashboard.html`, `app.py` | `AI-modified` | **John Michael D. Bretaña** | AI assisted with header layout; Bretaña wrote context processor and session role switcher. |
| **COMP-03 & COMP-04: StatCard & FilterToolbar** | `templates/orders.html`, `deliveries.html`, `pickups.html` | `AI-modified` | **Tristan Dave M. Plaza** | AI generated KPI card grid CSS; Plaza hand-wrote Barangay zone filter logic and status pill counters. |
| **COMP-05 & COMP-06: DataTable & StatusBadge** | `static/css/theme.css`, `templates/*.html` | `AI-modified` | **Mark Ephraim Nicor** | AI suggested badge color tokens; Nicor hand-wrote table row action bindings and live status indicators. |
| **COMP-07, COMP-08, COMP-09: EmptyState, LoadingSkeleton, ErrorAlert** | `static/css/animations.css`, `templates/*.html` | `AI-generated` | **Hazil Enoc** | AI generated `@keyframes shimmer` and SVG empty/error cards; Enoc wired `?state=empty|loading|error` conditionals across all 5 list views. |
| **COMP-10: ModalDialog & Destructive Confirm** | `static/js/form_bindings.js` | `AI-modified` | **Mark Ephraim Nicor** | AI scaffolded modal DOM template; Nicor added keyboard focus safety (`cancelBtn.focus()`), `aria-busy` locking, and `.row-fade-out` unmounting. |
| **COMP-11 & COMP-12: ReceiptCard & ProgressStepper** | `templates/order_details.html`, `payment_details.html`, `delivery_details.html` | `AI-modified` | **Marvin Oclarino** | AI assisted with thermal print CSS; Oclarino hand-wrote itemized pricing breakdown and 4-stage progress stepper logic. |
| **Async Form Binding Engine** | `static/js/form_bindings.js` | `AI-modified` | **Mark Ephraim Nicor** | AI generated initial `fetch()` wrapper; Nicor & Bretaña added Phase 2/Phase 3 `422` field-error normalization, `404`/`500`/network banners, and double-submit locking. |
| **Orders Views & Async Bindings** | `templates/orders.html`, `edit_order.html`, `order_details.html`, `controllers/order_routes.py` | `Hand-written` | **John Michael D. Bretaña** | Hand-wrote order weight bounds (`0 < weight <= 150`), auto-pricing calculation, async JSON responses, and edit/delete bindings. |
| **Deliveries Views & Async Bindings** | `templates/deliveries.html`, `edit_delivery.html`, `delivery_details.html`, `controllers/delivery_routes.py` | `Hand-written` | **Tristan Dave M. Plaza** | Hand-wrote delivery dispatch controller, order status cascading (`Out for Delivery`), and async form/delete bindings. |
| **Pickups Views & Async Bindings** | `templates/pickups.html`, `edit_pickup.html`, `pickup_details.html`, `controllers/pickup_routes.py` | `Hand-written` | **Mark Ephraim Nicor** | Hand-wrote pickup slot conflict density checker (`check_pickup_slot_conflict`), batch calculators, and async form/delete bindings. |
| **Customers Views & Async Bindings** | `templates/customers.html`, `edit_customer.html`, `customer_details.html`, `controllers/customer_routes.py` | `Hand-written` | **Hazil Enoc** | Hand-wrote phone normalization (`clean_phone_number`), VIP/Gold loyalty multiplier, and async customer create/edit/delete bindings. |
| **Payments Views & Async Bindings** | `templates/payments.html`, `edit_payment.html`, `payment_details.html`, `controllers/payment_routes.py` | `Hand-written` | **Marvin Oclarino** | Hand-wrote payment channel revenue breakdown (Cash/GCash/Bank), `TXN-XXXX` generator, and async payment create/edit/delete bindings. |
| **Branded 404 & 500 Error Views** | `templates/404.html`, `templates/500.html`, `app.py` | `AI-modified` | **Tristan Dave M. Plaza** | AI generated dark-glass card layout; Plaza & Bretaña wired dual-mode HTML/JSON handlers with zero stack trace leakage. |
| **Phase 3 Automated Test Suites** | `tests/test_async_bindings.py`, `tests/test_error_handling.py` | `Hand-written` | **All 5 Team Members** | Hand-wrote automated `pytest` suites verifying 201/200 async persistence, 422 inline field dictionaries, 404 missing records, and 500 safety across all 5 modules. |

---

## 4. Deliverable 3 Definition of Done Checklist

| Definition of Done Requirement | Status | Verification Evidence |
|---|:---:|---|
| **Create, read, update, and delete all work end to end in the running app** | **PASS ✅** | Verified across all 5 modules (`Orders`, `Deliveries`, `Pickups`, `Customers`, `Payments`); documented in [`docs/binding-tests.md`](../binding-tests.md). |
| **Every screen and state exists (list, detail, create, edit, empty, loading, error)** | **PASS ✅** | 12 reusable components and all screen states documented in [`docs/components.md`](../components.md) and reachable via `?state=empty`, `?state=loading`, `?state=error`. |
| **Create/Update forms bound async to controllers; records persist** | **PASS ✅** | Bound via `static/js/form_bindings.js` (`data-async-form`); tested in [`tests/test_async_bindings.py`](../../tests/test_async_bindings.py). |
| **Loading shown on every async action; controls disabled while pending** | **PASS ✅** | Submit and Delete buttons set `disabled = true`, `aria-busy="true"`, and render `.btn-spinner` (`Saving...` / `Deleting...`). |
| **422 (inline), 404, and 500/network failures all handled and visible** | **PASS ✅** | Documented in [`docs/feedback-matrix.md`](../feedback-matrix.md) and [`docs/feedback-tests.md`](../feedback-tests.md); verified in [`tests/test_error_handling.py`](../../tests/test_error_handling.py). |
| **Messages are specific, human, consistent; no leaked internals** | **PASS ✅** | Humanized micro-copy audited in [`docs/feedback-matrix.md`](../feedback-matrix.md); zero raw status codes or Python stack traces ever shown. |
| **Prompt log present with AI/hand-written labels** | **PASS ✅** | Documented in Section 2 & Section 3 of this file (`docs/ai-notes/deliverable-3.md`) as well as [`week-06.md`](week-06.md), [`week-07.md`](week-07.md), and [`week-08.md`](week-08.md). |
