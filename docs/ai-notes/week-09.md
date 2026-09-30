# Week 09 AI Disclosure & Peer Code Review Log
**Coursework:** CS 106 / Software Engineering 1  
**Project:** Laundry Pickup and Delivery Management System (`LaundryCare`)  
**Sprint / Week:** Week 09 — Reviewing Code (Especially the AI's)  
**Date:** October 2026  
**Repository Branch:** `main` (Branch Protection & Peer-Review Gate Enforced)  

---

## 1. Executive Summary & Team Roster
During Week 09, our team shifted focus from code generation to **rigorous peer code review**, auditing AI-generated pull requests against an objective five-point checklist, hunting planted vulnerabilities, and enforcing the cardinal merge rule: **No PR merges without 100% passing tests and an approved peer review.**

### Engineering Team & Operational System Roles:
- **John Michael Bretaña** (`Manager / Lead Architect`): System architecture, RBAC enforcement, and PR sign-off gating.
- **Hazil Enoc** (`Store Cashier`): Front counter CRM, customer directory, and customer loyalty rewards.
- **Marvin Oclarino** (`Delivery Driver — Van 1`): Commercial transport, payment channel distribution, and cash reconciliation.
- **Tristan Dave M. Plaza** (`Delivery Driver — Motorcycle 1`): Express CMU route logistics, mobile signature capture, and delivery tracking.
- **Mark Ephraim Nicor** (`Laundry Operator`): Wash hub plant management, machine load balancing, and pickup schedule intake.

---

## 2. Task 1: AI-Assisted Pull Requests & Prompt Logs

Each team member authored an AI-assisted pull request for their respective domain, logging initial prompts and human refinements:

### PR #101: `feat(crm): customer loyalty tier calculation and CSV directory export`
- **Author:** Hazil Enoc (`Store Cashier`)
- **Prompt:**
  > *"Generate a customer loyalty calculation function for our LaundryCare Flask backend that computes total spent, completed orders, and awards loyalty points with a multiplier for VIP and Gold tiers. Also add an endpoint to export the customer directory to CSV."*
- **AI Output:**
  Generated loyalty scoring and CSV streaming.
- **Human Refinement (Hazil Enoc):**
  Added tier discount text formatting (`15% Off Services`), fallback handling for null order totals, clean title-casing for client names, and phone number sanitization (`clean_phone_number()`).
- **Automated Tests:** Covered in `tests/test_customers_crm.py` (5 passing tests).

---

### PR #102: `feat(billing): payment channels and POS thermal receipt generator`
- **Author:** Marvin Oclarino (`Delivery Driver — Van 1`)
- **Prompt:**
  > *"Create an official thermal receipt modal in HTML/CSS with an SVG barcode and a cash change calculator for couriers receiving COD cash payments in the field. Also calculate dynamic channel breakdown percentages (Cash, GCash, Bank) in Flask."*
- **AI Output:**
  Generated modal markup and Python aggregations.
- **Human Refinement (Marvin Oclarino):**
  Fixed the `@media print` CSS bug where `.modal-overlay` was hiding the printable slip in Chromium browsers. Added courier/driver audit sign-off lines and real-time change calculation with green/red feedback for over/under-tendered bills.
- **Automated Tests:** Covered in `tests/test_payments_billing.py` (4 passing tests).

---

### PR #103: `feat(logistics): courier route sequencing and mobile signature pad`
- **Author:** Tristan Dave M. Plaza (`Delivery Driver — Motorcycle 1`)
- **Prompt:**
  > *"Implement an interactive fleet route switcher in JavaScript allowing dispatchers to toggle between Van 1 (Marvin) and Motorcycle 1 (Tristan), and add touch support to our HTML5 signature canvas so customers can sign on mobile devices."*
- **AI Output:**
  Provided canvas event listeners and route dataset swap logic.
- **Human Refinement (Tristan Dave M. Plaza):**
  Added `e.preventDefault()` to touch event listeners (`touchstart`, `touchmove`) to eliminate mobile screen scrolling during customer signatures. Updated courier telemetry to reflect Bukidnon delivery sectors (CMU Musuan, Poblacion, Dologon).
- **Automated Tests:** Covered in `tests/test_delivery_logistics.py` (4 passing tests).

---

### PR #104: `feat(wash-hub): pickup conflict detection and machine load monitor`
- **Author:** Mark Ephraim Nicor (`Laundry Operator`)
- **Prompt:**
  > *"Write a helper function to detect pickup booking slot conflicts in SQLite when more than 4 orders are scheduled for the same time window, and create a wash hub machine status monitor widget for the pickups dashboard."*
- **AI Output:**
  Drafted SQL query and dashboard banner.
- **Human Refinement (Mark Ephraim Nicor):**
  Added parameter exclusions for cancelled bookings (`status != 'Cancelled'`) and integrated machine load metrics (active washers, dryer tumblers, sanitization cycle) into `templates/pickups.html`.
- **Automated Tests:** Covered in `tests/test_pickup_hub.py` (4 passing tests).

---

### PR #105: `feat(core): role alignment and branch protection merge gate`
- **Author:** John Michael Bretaña (`Manager / Lead Architect`)
- **Prompt:**
  > *"Review our RBAC access guards and ensure team member operational roles are synchronized across the database, employee roster, sidebar navigation badges, and automated test fixtures."*
- **AI Output:**
  Suggested database migration scripts and session role checks.
- **Human Refinement (John Michael Bretaña):**
  Synchronized roles (`admin`, `staff`, `rider`) and author identities across all views and tests, confirming 67/67 tests passing.

---

## 3. Tasks 2 & 4: Peer Code Review Transcripts (Checklist & Feedback Practice)

Every PR was audited against the mandatory 5-point checklist:
1. **Correctness:** Right behavior, edge cases, safe error paths?
2. **Readability:** Clear variable naming, sensible modular structure?
3. **Consistency:** Conforms to team design patterns, error shapes, and glassmorphism styling?
4. **Security:** Input validation present, no raw string interpolation, zero exposed secrets?
5. **Tests:** Meaningful unit/integration assertions present and green?

All comments follow our team feedback standard: **Specific, kind, actionable, labeled `[BLOCKING]` or `[NIT]`, and noting at least one thing the code did well.**

---

### Review 1: PR #101 (Hazil Enoc's Customer Loyalty Feature)
**Reviewer:** Tristan Dave M. Plaza (`Delivery Driver`)  
**Verdict:** Approved with revisions

> **Checklist Assessment:**
> - [x] **Correctness:** Loyalty math works accurately across all customer tiers.
> - [x] **Readability:** Variable names (`tier_multiplier`, `loyalty_points`) are descriptive and self-documenting.
> - [x] **Consistency:** Matches the dual-mode JSON/HTML pattern used in other controllers.
> - [x] **Security:** CSV export uses `csv.writer` to prevent injection and escapes strings.
> - [x] **Tests:** 5 tests asserting status codes, headers, and calculation logic.

**Substantive Comments:**
1. **What the code did well:**  
   *"The loyalty card sidebar widget in `templates/customer_details.html` looks amazing! The gradient border and VIP pill badges integrate seamlessly with our dark theme, and the CSV export is super fast."*
2. `[BLOCKING]` **Handled Edge Case:**  
   *"In `controllers/customer_routes.py`, when a customer has never made an order, `sum(o['total_price'] for o in orders)` could receive `None` values if the database total is null. Please use `(o['total_price'] or 0.0)` so we never trigger a `TypeError` during float arithmetic."*  
   *(Resolved by Hazil in commit `9ca878e`)*
3. `[NIT]` **Debounce Optimization:**  
   *"The live search in `templates/customers.html` binds directly to `onkeyup`. On slower devices, typing quickly could lag the table. Consider wrapping it in a 200ms `setTimeout` debounce."*  
   *(Resolved by Hazil in commit `edb0756`)*

---

### Review 2: PR #102 (Marvin Oclarino's Financial Settlement & Thermal Barcode)
**Reviewer:** Hazil Enoc (`Store Cashier`)  
**Verdict:** Approved with revisions

> **Checklist Assessment:**
> - [x] **Correctness:** Change calculation correctly computes difference between tendered cash and amount due.
> - [x] **Readability:** Clear separation between payment methods and transaction log rows.
> - [x] **Consistency:** Follows table styling and button conventions from Deliverable 3.
> - [x] **Security:** Financial routes strictly require `admin` role authorization.
> - [x] **Tests:** Pytest asserts 200 OK, Content-Disposition headers, and unauthenticated redirects.

**Substantive Comments:**
1. **What the code did well:**  
   *"The Code128 SVG barcode rendered on the printable receipt gives our receipt modal an ultra-professional, authentic POS look that front-desk cashiers will love."*
2. `[BLOCKING]` **Print Bug Resolution:**  
   *"When clicking 'Print Receipt' in Chrome, the receipt paper disappeared because `.modal-overlay` had `display: none !important;` in `@media print`. Please ensure `.modal-overlay#receiptModal` is set to `display: block !important; visibility: visible !important;` so physical POS thermal printers can output the slip."*  
   *(Resolved by Marvin in commit `6a0572a`)*
3. `[NIT]` **Dynamic Total Binding:**  
   *"In `templates/payments.html`, the settlement breakdown bar previously had hardcoded numbers. Great job replacing them with dynamic variables `stats.cash_total` and `stats.gcash_total`."*

---

### Review 3: PR #103 (Tristan Dave M. Plaza's Courier Logistics & Signature Pad)
**Reviewer:** Mark Ephraim Nicor (`Laundry Operator`)  
**Verdict:** Approved with revisions

> **Checklist Assessment:**
> - [x] **Correctness:** Route switching correctly updates stop count and vehicle labels.
> - [x] **Readability:** Clean JS functions with clear DOM element IDs.
> - [x] **Consistency:** Reuses existing modal layout and color scheme.
> - [x] **Security:** Delivery updates require authenticated rider or admin session.
> - [x] **Tests:** Integration tests verify route dispatching and status transitions.

**Substantive Comments:**
1. **What the code did well:**  
   *"The digital signature canvas is an outstanding touch for proof-of-delivery. Letting customers sign with their finger directly on the delivery driver's phone eliminates paperwork completely."*
2. `[BLOCKING]` **Touch Scrolling Fix:**  
   *"On mobile touchscreens, dragging a finger on the signature pad causes the entire webpage to scroll. Please add `e.preventDefault()` inside the `touchstart` and `touchmove` listeners so the customer can draw their signature smoothly without viewport bouncing."*  
   *(Resolved by Tristan in commit `6c85633`)*
3. `[NIT]` **Express Route Metadata:**  
   *"Motorcycle 1 should highlight CMU Campus stops since dormitory students frequently request express 24-hour turnaround."*  
   *(Resolved by Tristan in commit `1b8d508`)*

---

### Review 4: PR #104 (Mark Ephraim Nicor's Wash Hub Scheduling & Machine Capacity)
**Reviewer:** Marvin Oclarino (`Delivery Driver`)  
**Verdict:** Approved with revisions

> **Checklist Assessment:**
> - [x] **Correctness:** Slot conflict helper accurately flags time windows with >= 4 bookings.
> - [x] **Readability:** Clean SQL query with parameter binding.
> - [x] **Consistency:** Matches the styling of the delivery timeline cards.
> - [x] **Security:** Queries use parameterized `?` placeholders; zero SQL injection.
> - [x] **Tests:** Unit test validates helper output dictionary structure.

**Substantive Comments:**
1. **What the code did well:**  
   *"The Wash Hub Intake & Machine Status monitor provides incredible operational visibility. Seeing active washers and dryers in real time helps couriers know exactly when to bring in newly collected bags."*
2. `[BLOCKING]` **Cancelled Booking Filter:**  
   *"In `check_pickup_slot_conflict()`, make sure you add `AND status != 'Cancelled'`. Otherwise, cancelled pickups will falsely trigger high-density warning alerts."*  
   *(Resolved by Mark in commit `6096b4f`)*
3. `[NIT]` **Zone Pill Consistency:**  
   *"Let's update the zone sector buttons in `templates/pickups.html` to display the actual assigned couriers (Van 1 & Moto 1) rather than placeholder names."*  
   *(Resolved by Mark in commit `ce1c859`)*

---

### Review 5: PR #105 (John Michael Bretaña's Role Architecture & Test Suite Expansion)
**Reviewers:** Hazil Enoc & Tristan Dave M. Plaza  
**Verdict:** Approved

> **Checklist Assessment:**
> - [x] **Correctness:** All 67 automated test cases pass with 100% green status.
> - [x] **Readability:** Clear modular blueprints (`order_bp`, `customer_bp`, `delivery_bp`, `pickup_bp`, `payment_bp`).
> - [x] **Consistency:** Standardized error response shapes `{ "status": ..., "error": ... }`.
> - [x] **Security:** CSRF safeguards, session validation, and strict RBAC decorators.
> - [x] **Tests:** Comprehensive coverage across failure paths, edge cases, and CRUD operations.

**Substantive Comments:**
1. **What the code did well:**  
   *"The comprehensive role separation between Manager, Cashier, Drivers, and Laundry Operator guarantees that team members have access to the exact tools they need for their daily duties without clutter."*
2. `[NIT]` **Lint & Formatting:**  
   *"All route controllers are formatted cleanly according to PEP 8 standards with zero leftover console logs."*

---

## 4. Task 3: Find the Flaw Summary
As detailed in our dedicated bug dossier [`docs/find-the-flaw.md`](file:///C:/Users/Saidimar%20Rey/.gemini/antigravity/scratch/Laundry-Pickup-and-Delivery-Management-System/docs/find-the-flaw.md), the team investigated five critical flaws commonly generated by AI coding models:
1. **Missing Input Validation & Type Coercion** in order intake (CWE-20).
2. **Wrong HTTP Status Codes & Failure Masking** (returning 200 OK on invalid data).
3. **Unhandled 404/500 & Silent Failure** in customer order tracking.
4. **Hallucinated Database Methods** (cross-framework syntax mixing).
5. **Floating-Point Rounding & Negative Discount Exploitation** in payment totals.

Every flaw was documented with the root cause in LLMs, the production-grade fix, and the prevention rule for code reviews.

---

## 5. Task 5: Merge Rule Enforcement

### The Cardinal Rule:
> **"No pull request merges to `main` without a 100% passing test suite and at least one approving peer review."**

### Verification Protocol:
1. **Automated Continuous Testing:** Every pull request triggers `pytest tests/`. Merging is strictly blocked if even a single test fails.
2. **Two-Person Integrity:** Branch protection on GitHub blocks direct pushes to `main` by single contributors. All changes must be submitted via PR with peer sign-off.
3. **Audit Trail:** Review comments must be addressed, commits pushed, and re-reviewed before squashing or merging.

### Current Test Suite Health:
```
============================= test session starts =============================
collected 67 items

tests/test_app.py ...                                                    [  4%]
tests/test_async_bindings.py ...........                                 [ 20%]
tests/test_customer_portal.py .......                                    [ 31%]
tests/test_customers_crm.py .....                                        [ 38%]
tests/test_delivery.py ......                                            [ 50%]
tests/test_delivery_logistics.py ....                                    [ 57%]
tests/test_error_handling.py ...............                             [ 80%]
tests/test_payments_billing.py ....                                      [ 87%]
tests/test_pickup.py ...                                                 [ 92%]
tests/test_pickup_hub.py ....                                            [ 95%]
tests/test_rbac.py .....                                                 [100%]

============================= 67 passed in 3.41s ==============================
```

---

## 6. End-of-Lab Checklist

- [x] **Each member opened at least one reviewed PR with a prompt log:**
  - Hazil Enoc (PR #101)
  - Marvin Oclarino (PR #102)
  - Tristan Dave M. Plaza (PR #103)
  - Mark Ephraim Nicor (PR #104)
  - John Michael Bretaña (PR #105)
- [x] **Each member gave at least one substantive review with a blocking/nit label:** All 5 reviews documented in Section 3.
- [x] **`/docs/find-the-flaw.md` created:** Comprehensive bug dossier analyzing 5 AI code snippets with planted flaws.
- [x] **No un-reviewed, red-suite merges this week:** All 67 automated test cases passing (100% green).
- [x] **Prompt logs current in `/docs/ai-notes/week-09.md`:** Complete disclosure of AI prompts, human refinements, and attribution.

---

## 7. Looking Ahead to Week 10
In Week 10, LaundryCare enters **Feature Freeze**. New feature development stops, and the team will execute:
1. **Full Manual QA Pass:** Testing every user journey across all user roles (Admin, Cashier, Driver, Operator).
2. **Cross-Browser & Device Test Matrix:** Validating responsiveness on desktop, tablet, and mobile.
3. **Adversarial Testing:** Attempting SQL injection, XSS, negative values, and concurrent state race conditions.
4. **Triaged Bug List:** Categorizing and resolving all outstanding edge cases before production shipment.
