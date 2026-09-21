# Week 08 AI Disclosure & Technical Defense Log
**Coursework:** CS 106 / Software Engineering 1  
**Project:** Laundry Pickup and Delivery Management System (`LaundryCare`)  
**Sprint / Week:** Week 08 — Phase 3: Error Handling, UI Feedback & Micro-Copy  
**Milestone:** Deliverable 3: Interface & View Binding (30%)  
**Date:** September 2026  
**Repository Branch:** `main`

---

## 1. Purpose of AI Use

During Week 08, our 5-member engineering team utilized AI tooling (Claude / ChatGPT / Antigravity) to assist with:
1. **Global Error Architecture:** Designing dual-mode Flask error handlers (`@app.errorhandler(404)` and `@app.errorhandler(500)`) capable of distinguishing between synchronous browser requests (rendering branded dark-glass error templates) and asynchronous AJAX requests (returning clean JSON payloads without leaking Python stack traces).
2. **Accessible Destructive Action Safety:** Engineering a reusable modal confirmation dialog (`confirmDestructiveAction()`) in vanilla JavaScript to prevent accidental single-click deletions, enforcing explicit user confirmation with loading state indication on the confirm button.
3. **Humanized Micro-Copy & Micro-Interactions:** Refactoring validation error text and server error messages into calm, helpful, sentence-case micro-copy that names the specific problem and offers actionable next steps.
4. **Comprehensive Automated Test Expansion:** Writing automated pytest test cases in `tests/test_error_handling.py` verifying 404, 500, and async delete contracts across all 5 operational controllers.

---

## 2. Prompts Used & Interaction Log

### Task 1: Dual-Mode Global Error Handling & Zero Stack Trace Leakage
- **Prompt:**
  > *"How can we implement Flask global error handlers for 404 and 500 errors that detect whether a request is coming from an async fetch call or a traditional page navigation, returning JSON `{ "status": 404/500, "error": "..." }` for fetch while rendering custom branded HTML error pages for standard navigation, ensuring no stack traces or server paths leak in production?"*
- **AI Output:**
  Suggested using `request.is_json` or checking `X-Requested-With: XMLHttpRequest` and `Accept: application/json` inside the error handlers. For async, return `jsonify(...)`. For sync, render `render_template('404.html')` or `render_template('500.html')`.
- **Human Verification & Refinement:**
  Implemented in `app.py`. Added comprehensive error templates `templates/404.html` and `templates/500.html` designed with our LaundryCare dark-glass aesthetic, complete with recovery links ("Return to Dashboard", "View Orders", and "Try Again" reload actions).

---

### Task 2: Accessible Destructive Action Confirmation Dialog
- **Prompt:**
  > *"Instead of using the crude browser `confirm()` popup which looks unstyled and blocks the main thread, how can we build a lightweight, accessible confirmation modal in vanilla JS that darkens the background, highlights the destructive action in red, shows a spinner on click, and animates row removal on success?"*
- **AI Output:**
  Provided a DOM-based overlay creator function that injects a card with ARIA roles (`role="alertdialog"`, `aria-modal="true"`), traps focus, supports Escape key cancellation, and handles async `fetch(url, { method: 'POST' })` with button locking.
- **Human Verification & Refinement:**
  Engineered into `static/js/form_bindings.js` as `confirmDestructiveAction()` and `handleAsyncDelete()`. Added smooth CSS row fade-out animations (`.row-fade-out`) in `static/css/animations.css`. Wired triggers across all 5 modules with data attributes (`data-delete-url` and `data-item-name`).

---

### Task 3: Humanized Error Micro-Copy Guidelines
- **Prompt:**
  > *"Review our current validation and server error messages. How can we make them more humanized, calm, and helpful according to modern UX error guidelines without technical jargon?"*
- **AI Output:**
  Suggested replacing technical phrasing like *"NullConstraintError"* or *"Invalid status"* with plain language naming the field and the fix, e.g., *"Laundry weight must be greater than 0 kg."* and *"Page or record not found. The item you requested may have been moved or deleted."*
- **Human Verification & Refinement:**
  Applied consistently across `order_routes.py`, `delivery_routes.py`, `pickup_routes.py`, `customer_routes.py`, `payment_routes.py`, and the client-side feedback engine.

---

### Task 4: Automated Failure-Path Testing
- **Prompt:**
  > *"Write pytest test cases using Flask's test_client to verify: 1) Non-existent route returns custom 404 HTML, 2) Async fetch to missing record returns JSON 404, 3) 500 handler doesn't leak stack trace, and 4) Async delete route deletes the record from SQLite and returns 200 JSON."*
- **AI Output:**
  Scaffolded unit and integration tests covering routes and dual-mode JSON responses.
- **Human Verification & Refinement:**
  Wired into `tests/test_error_handling.py`, integrating fixtures and database session cleanup. Expanded total test suite to 45+ passing tests.

---

## 3. Component & Code Attribution Matrix

| File / Artifact | Attribution Tag | Author / Maintainer | Description & Human Refinement |
|---|---|---|---|
| [`templates/404.html`](file:///C:/Users/Saidimar%20Rey/.gemini/antigravity/scratch/Laundry-Pickup-and-Delivery-Management-System/templates/404.html) | `AI-modified` | Tristan Dave M. Plaza | Custom branded dark-glass 404 error page with quick recovery navigation links. |
| [`templates/500.html`](file:///C:/Users/Saidimar%20Rey/.gemini/antigravity/scratch/Laundry-Pickup-and-Delivery-Management-System/templates/500.html) | `AI-modified` | John Michael D. Bretaña | Custom dark-glass 500 error page eliminating stack trace leakage with reload options. |
| [`app.py`](file:///C:/Users/Saidimar%20Rey/.gemini/antigravity/scratch/Laundry-Pickup-and-Delivery-Management-System/app.py) | `AI-modified` | John Michael D. Bretaña | Global dual-mode error handlers `@app.errorhandler(404)` and `@app.errorhandler(500)`. |
| [`static/js/form_bindings.js`](file:///C:/Users/Saidimar%20Rey/.gemini/antigravity/scratch/Laundry-Pickup-and-Delivery-Management-System/static/js/form_bindings.js) | `AI-modified` | Mark Ephraim Nicor | Added `confirmDestructiveAction()`, `handleAsyncDelete()`, and `initAsyncDeletes()`. |
| [`static/css/animations.css`](file:///C:/Users/Saidimar%20Rey/.gemini/antigravity/scratch/Laundry-Pickup-and-Delivery-Management-System/static/css/animations.css) | `AI-modified` | Hazil Enoc | Added `.lc-confirm-overlay`, `.lc-confirm-card`, `.row-fade-out`, and destructive button styles. |
| [`controllers/order_routes.py`](file:///C:/Users/Saidimar%20Rey/.gemini/antigravity/scratch/Laundry-Pickup-and-Delivery-Management-System/controllers/order_routes.py) | `AI-modified` | John Michael D. Bretaña | Dual-mode async delete and 404 missing record handling for Orders. |
| [`controllers/delivery_routes.py`](file:///C:/Users/Saidimar%20Rey/.gemini/antigravity/scratch/Laundry-Pickup-and-Delivery-Management-System/controllers/delivery_routes.py) | `AI-modified` | Tristan Dave M. Plaza | Dual-mode async delete and 404 missing record handling for Deliveries. |
| [`controllers/pickup_routes.py`](file:///C:/Users/Saidimar%20Rey/.gemini/antigravity/scratch/Laundry-Pickup-and-Delivery-Management-System/controllers/pickup_routes.py) | `AI-modified` | Mark Ephraim Nicor | Dual-mode async delete and 404 missing record handling for Pickups. |
| [`controllers/customer_routes.py`](file:///C:/Users/Saidimar%20Rey/.gemini/antigravity/scratch/Laundry-Pickup-and-Delivery-Management-System/controllers/customer_routes.py) | `AI-modified` | Hazil Enoc | Dual-mode async delete and 404 missing record handling for Customers. |
| [`controllers/payment_routes.py`](file:///C:/Users/Saidimar%20Rey/.gemini/antigravity/scratch/Laundry-Pickup-and-Delivery-Management-System/controllers/payment_routes.py) | `AI-modified` | Marvin Oclarino | Dual-mode async delete and 404 missing record handling for Payments. |
| [`docs/feedback-matrix.md`](file:///C:/Users/Saidimar%20Rey/.gemini/antigravity/scratch/Laundry-Pickup-and-Delivery-Management-System/docs/feedback-matrix.md) | `Hand-written` | John Michael D. Bretaña | Comprehensive 3-state matrix across all 5 operational views with 5-member ownership. |
| [`docs/feedback-tests.md`](file:///C:/Users/Saidimar%20Rey/.gemini/antigravity/scratch/Laundry-Pickup-and-Delivery-Management-System/docs/feedback-tests.md) | `Hand-written` | Marvin Oclarino | Failure-path test execution log for 422, 404, 500, and destructive deletion tests. |
| [`tests/test_error_handling.py`](file:///C:/Users/Saidimar%20Rey/.gemini/antigravity/scratch/Laundry-Pickup-and-Delivery-Management-System/tests/test_error_handling.py) | `AI-modified` | Marvin Oclarino | Automated pytest suite testing 404, 500, and async delete safety across all modules. |
| [`docs/ai-notes/week-08.md`](file:///C:/Users/Saidimar%20Rey/.gemini/antigravity/scratch/Laundry-Pickup-and-Delivery-Management-System/docs/ai-notes/week-08.md) | `Hand-written` | Team | Deliverable 3 AI disclosure, attribution matrix, and individual defense cheat-sheet. |

---

## 4. Deliverable 3 Technical Defense Cheat-Sheet

During the Deliverable 3 presentation and oral defense, each member can speak to their specific architectural contributions:

### 1. John Michael D. Bretaña (Lead Architect — Backend & Error Handlers)
- **Question:** *"How does your system prevent stack traces and internal database errors from leaking to users during an exception?"*
- **Defense:**
  > *"In `app.py`, we registered global Flask error handlers `@app.errorhandler(404)` and `@app.errorhandler(500)`. When an unhandled exception occurs, the 500 handler catches it, logs the technical traceback to our server console for developer debugging, but returns a clean, branded dark-glass error page (`templates/500.html`) or JSON `{ "status": 500, "error": "An internal server error occurred. Please try again later." }`. At no point is an internal file path, SQL query, or Python stack trace exposed to the client."*

---

### 2. Mark Ephraim Nicor (UI Interaction & Confirmation Engine)
- **Question:** *"Why did you replace the native browser `confirm()` with a custom modal, and how does your destructive action safety work?"*
- **Defense:**
  > *"The native browser `window.confirm()` dialog is synchronous, visually inconsistent with our dark-glass design system, and cannot display loading indicators. In `form_bindings.js`, we implemented `confirmDestructiveAction()`. When an operator clicks 'Delete', an accessible modal card appears with a red warning badge, item-specific micro-copy, and 'Cancel' / 'Yes, Delete' buttons. When confirmed, the delete button immediately shows an animated spinner and disables itself to prevent duplicate delete requests, sends an asynchronous POST to the controller, and upon 200 OK, animates the table row out using `.row-fade-out`."*

---

### 3. Tristan Dave M. Plaza (Logistics & 404 Error Experience)
- **Question:** *"What happens when a user attempts to access a delivery record or URL that no longer exists?"*
- **Defense:**
  > *"We implemented dual-mode 404 handling. If an operator accesses a non-existent URL or deleted delivery ID via standard browser navigation (like `/delivery-records-page/details/99999`), the controller catches the missing record and renders `templates/404.html`. This page features recovery navigation buttons ('Return to Dashboard', 'View Orders', 'Live Deliveries') rather than an empty page. If the request was sent asynchronously via JavaScript fetch, the controller returns HTTP 404 with JSON `{ 'status': 404, 'error': 'Delivery record not found or has already been deleted.' }`, which our toast notification system renders as a floating alert without crashing the UI."*

---

### 4. Hazil Enoc (CRM & Inline Field Validation)
- **Question:** *"How does the system ensure users clearly understand what went wrong during invalid form submissions?"*
- **Defense:**
  > *"We follow humanized micro-copy and visible field-level error binding. When a customer registration fails due to missing data, the backend rejects it with HTTP 422 and a structured dictionary like `{ 'name': 'Customer Name is required.', 'contact_number': 'Contact Number is required.' }`. The client engine iterates over these errors, highlights each input with a red focus ring (`.input-invalid`), appends a red badge with an exclamation icon directly beneath the input, and automatically focuses the first invalid field. We never rely on vague alert popups or raw status codes."*

---

### 5. Marvin Oclarino (Financial Ledger & Error Resilience Testing)
- **Question:** *"How did you verify that destructive actions and error handlers work across the entire application?"*
- **Defense:**
  > *"We built an automated test suite in `tests/test_error_handling.py` and documented an end-to-end failure-path verification log in `docs/feedback-tests.md`. Our automated pytest suite tests: 1) standard 404 routes, 2) missing entity detail pages for all 5 controllers, 3) custom 500 error pages, and 4) async deletion endpoints ensuring the record is removed from SQLite and returns HTTP 200 JSON. We currently have over 45 passing automated tests across the project with 100% green status."*
