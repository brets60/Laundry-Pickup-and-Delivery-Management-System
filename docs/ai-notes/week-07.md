# Week 07 AI Disclosure & Technical Defense Log
**Coursework:** CS 106 / Software Engineering 1  
**Project:** Laundry Pickup and Delivery Management System (`LaundryCare`)  
**Sprint / Week:** Week 07 — Phase 3: Interface Binding (Binding Forms to the Backend)  
**Date:** September 2026  
**Repository Branch:** `main`

---

## 1. Purpose of AI Use

During Week 07, our 5-member engineering team utilized AI tooling (Claude / ChatGPT / Antigravity) to assist with:
1. **Dual-Mode Controller Architecture:** Designing backwards-compatible Flask endpoints that seamlessly detect asynchronous requests (`request.is_json` or `X-Requested-With: XMLHttpRequest`) and return standardized JSON responses (`201 Created`, `200 OK`, `422 Unprocessable Entity`), while continuing to serve synchronous HTTP redirects for legacy form submissions.
2. **Client-Side Form Interceptor Engine (`static/js/form_bindings.js`):** Scaffolding a reusable vanilla JavaScript engine that intercepts form submit events, prevents duplicate submissions via button locking, renders animated loading indicators, and injects contextual field-level error messages directly beneath invalid inputs.
3. **Automated Async Testing (`tests/test_async_bindings.py`):** Drafting integration tests to verify JSON contracts, 422 validation structures, and double-submit prevention across all 5 core modules.

---

## 2. Prompts Used & Interaction Log

### Task 1: Dual-Mode Controller Design & Structured 422 Contract
- **Prompt:**
  > *"How do we update existing Flask controller routes (`/laundry-orders-page`, `/delivery-records-page`, etc.) to support async JSON requests with structured field-level 422 validation errors without breaking existing pytest test suites that submit standard form data?"*
- **AI Output:**
  Suggested introducing a helper function `is_async_request()` checking `request.is_json`, `request.headers.get('X-Requested-With') == 'XMLHttpRequest'`, or `'application/json' in request.headers.get('Accept')`. If `is_async`, parse JSON body and return `jsonify({"status": 422, "error": errors_dict}), 422`. If synchronous, preserve the existing `redirect(...)` or flash message.
- **Human Verification & Refinement:**
  Adopted across all 5 route controllers (`order_routes.py`, `delivery_routes.py`, `pickup_routes.py`, `customer_routes.py`, `payment_routes.py`). Refined error dictionaries to match exact HTML input `name` and `id` attributes.

---

### Task 2: Double-Submit Prevention & Loading Lifecycle
- **Prompt:**
  > *"Write a robust vanilla JavaScript form interceptor that prevents double-submit bugs by disabling the submit button and showing a spinner during the pending fetch request, and re-enables the button in a finally block."*
- **AI Output:**
  Provided an event listener for `submit` that sets `button.disabled = true; button.setAttribute('aria-busy', 'true')`, caches the original button HTML, and restores it inside a `finally` clause.
- **Human Verification & Refinement:**
  Implemented in `static/js/form_bindings.js`. Added CSS animations (`@keyframes spin`, `.btn-loading`, `.btn-spinner`) in `static/css/animations.css`. Verified that rapid repeated clicks on the submit button only fire a single network request.

---

### Task 3: Visible Field-Level 422 Error Display
- **Prompt:**
  > *"When the backend returns HTTP 422 with `{ error: { field_name: message } }`, how can we dynamically inject accessible red error badges under each input and scroll the first invalid field into view?"*
- **AI Output:**
  Suggested iterating over the error dictionary, querying `form.querySelector('[name="' + field + '"]')`, appending `<div class="field-error-text">`, adding `.input-invalid` class with red border and shake animation, and calling `.focus()` on the first invalid field.
- **Human Verification & Refinement:**
  Engineered in `static/js/form_bindings.js`. Created accompanying SVG icons and CSS in `animations.css` with WCAG AA compliant red contrast (`#dc2626`).

---

### Task 4: Automated Async Test Suite
- **Prompt:**
  > *"Generate pytest test cases using Flask's test client to test our 5 async form endpoints for both 201 success and 422 validation failure using JSON payloads and XMLHttpRequest headers."*
- **AI Output:**
  Generated baseline test structure for `tests/test_async_bindings.py`.
- **Human Verification & Refinement:**
  Refined assertions to verify exact database state insertions and structured error dictionaries. Scaled test suite from 24 to 35 tests, running with 100% pass rate.

---

## 3. Component & Code Attribution Matrix

| File / Artifact | Attribution Tag | Author / Maintainer | Description & Human Refinement |
|---|---|---|---|
| [`static/js/form_bindings.js`](file:///C:/Users/Saidimar%20Rey/.gemini/antigravity/scratch/Laundry-Pickup-and-Delivery-Management-System/static/js/form_bindings.js) | `AI-modified` | Mark Ephraim Nicor | AI provided core fetch wrapper; Nicor integrated modal dismissal, toast container lifecycle, and accessible ARIA attributes. |
| [`static/css/animations.css`](file:///C:/Users/Saidimar%20Rey/.gemini/antigravity/scratch/Laundry-Pickup-and-Delivery-Management-System/static/css/animations.css) | `AI-modified` | Tristan Dave M. Plaza | Plaza designed `.field-error-text`, `.input-invalid`, `.btn-loading`, and `.lc-toast` styles and animations. |
| [`controllers/order_routes.py`](file:///C:/Users/Saidimar%20Rey/.gemini/antigravity/scratch/Laundry-Pickup-and-Delivery-Management-System/controllers/order_routes.py) | `AI-modified` | John Michael D. Bretaña | Bretaña implemented dual-mode async endpoints, weight calculations, and structured 422 error dictionaries. |
| [`controllers/delivery_routes.py`](file:///C:/Users/Saidimar%20Rey/.gemini/antigravity/scratch/Laundry-Pickup-and-Delivery-Management-System/controllers/delivery_routes.py) | `AI-modified` | Tristan Dave M. Plaza | Plaza bound dispatch and edit delivery routes to async contracts with rider and zone validations. |
| [`controllers/pickup_routes.py`](file:///C:/Users/Saidimar%20Rey/.gemini/antigravity/scratch/Laundry-Pickup-and-Delivery-Management-System/controllers/pickup_routes.py) | `AI-modified` | Mark Ephraim Nicor | Nicor wired schedule pickup create and edit endpoints with time slot and customer validations. |
| [`controllers/customer_routes.py`](file:///C:/Users/Saidimar%20Rey/.gemini/antigravity/scratch/Laundry-Pickup-and-Delivery-Management-System/controllers/customer_routes.py) | `AI-modified` | Hazil Enoc | Enoc implemented customer registration and update async routes with contact number validations. |
| [`controllers/payment_routes.py`](file:///C:/Users/Saidimar%20Rey/.gemini/antigravity/scratch/Laundry-Pickup-and-Delivery-Management-System/controllers/payment_routes.py) | `AI-modified` | Marvin Oclarino | Oclarino connected financial payment recording, transaction ID generation, and positive amount validation. |
| [`tests/test_async_bindings.py`](file:///C:/Users/Saidimar%20Rey/.gemini/antigravity/scratch/Laundry-Pickup-and-Delivery-Management-System/tests/test_async_bindings.py) | `AI-modified` | Team (Bretaña, Plaza, Nicor, Enoc, Oclarino) | 11 comprehensive automated tests verifying async CRUD contracts and 422 validations (all 35 project tests passing). |
| [`docs/binding-tests.md`](file:///C:/Users/Saidimar%20Rey/.gemini/antigravity/scratch/Laundry-Pickup-and-Delivery-Management-System/docs/binding-tests.md) | `Hand-written` | John Michael D. Bretaña | End-to-end verification matrix documenting manual tests, double-submit tests, and execution logs. |
| [`docs/ai-notes/week-07.md`](file:///C:/Users/Saidimar%20Rey/.gemini/antigravity/scratch/Laundry-Pickup-and-Delivery-Management-System/docs/ai-notes/week-07.md) | `Hand-written` | John Michael D. Bretaña | Week 7 AI usage log, attribution tags, review decisions, and individual defense cheat-sheets. |

---

## 4. Technical Defense Preparation Cheat-Sheet

During lab defense and oral evaluation, each team member can defend their respective module implementation using the technical answers below:

### 1. John Michael D. Bretaña (Lead Architect — Orders Module & Dual-Mode Contract)
- **Question:** *"Why did you use a dual-mode pattern in the backend controllers instead of building separate API endpoints?"*
- **Defense:**
  > *"A dual-mode pattern (`is_async_request()`) allows our application to serve both modern asynchronous client-side `fetch()` requests and standard synchronous form submissions from the exact same URL endpoint. This design decision guaranteed 100% backwards compatibility with our existing 24 unit/integration tests without code duplication. When the request header contains `Accept: application/json` or `X-Requested-With: XMLHttpRequest`, the controller parses JSON and responds with standardized HTTP `201` or `422` JSON payloads. Otherwise, it redirects or flashes messages as usual."*

---

### 2. Mark Ephraim Nicor (Frontend Engine — Form Interceptor & Double-Submit Protection)
- **Question:** *"How does your client-side binding prevent double-submit bugs, and what happens if the network connection fails?"*
- **Defense:**
  > *"In `static/js/form_bindings.js`, we intercept the form submit event using `e.preventDefault()`. Immediately upon execution, we query the submit button, set `button.disabled = true`, add `aria-busy='true'`, and inject an animated SVG spinner (`.btn-spinner`) with the text 'Saving...'. This physically prevents rapid repeated clicks from creating duplicate database records. Furthermore, the button restoration is encapsulated within a `finally` block, ensuring that even if a network timeout or 500 error occurs, the button is safely re-enabled and the user can retry without reloading."*

---

### 3. Tristan Dave M. Plaza (Logistics & Delivery Bindings)
- **Question:** *"How does the system display validation errors without reloading the entire page?"*
- **Defense:**
  > *"When an operator submits a delivery without a customer name or delivery date, the backend rejects the request with HTTP `422 Unprocessable Entity` and returns `{ 'status': 422, 'error': { 'customer': 'Customer Name is required.', 'delivery_date': 'Delivery Date is required.' } }`. The JavaScript interceptor reads this dictionary, locates the corresponding `<input name='customer'>`, adds the `.input-invalid` CSS class (which triggers a red border and subtle shake animation), and injects a `<div class='field-error-text'>` directly beneath the input with an exclamation badge. Finally, it calls `.focus()` on the first invalid field for immediate keyboard accessibility."*

---

### 4. Hazil Enoc (CRM & Customer Directory Bindings)
- **Question:** *"What is the difference between HTTP 400 and HTTP 422 in your form validation architecture?"*
- **Defense:**
  > *"We specifically utilized HTTP `422 Unprocessable Entity` rather than HTTP `400 Bad Request`. According to RFC 4918 and REST best practices, HTTP 400 represents malformed request syntax (such as corrupted JSON formatting), whereas HTTP 422 indicates that the server understood the content-type and syntax of the request, but was unable to process the contained instructions due to semantic validation failures (such as empty required fields or non-numeric inputs). This semantic distinction allows our client engine to differentiate between fatal communication errors and user-correctable form inputs."*

---

### 5. Marvin Oclarino (Payments & Financial Integrity)
- **Question:** *"How do the payment form bindings ensure financial data integrity before records are persisted?"*
- **Defense:**
  > *"In `controllers/payment_routes.py`, we enforce strict server-side validation on both Create and Edit routes. Payment amounts are parsed and checked to ensure `payment_amount > 0.0`. If a negative or non-numeric value is submitted, the controller immediately returns a 422 error with `'payment_amount': 'Payment Amount must be greater than 0.'`. Furthermore, each successful async transaction automatically generates a unique reference number (`TXN-XXXX`) and commits the transaction time using SQLite's datetime function, ensuring an immutable audit trail."*
