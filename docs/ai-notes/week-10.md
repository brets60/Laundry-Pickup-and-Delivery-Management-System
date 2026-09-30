# Week 10 AI Disclosure & Manual QA Defense Log
**Coursework:** CS 106 / Software Engineering 1  
**Project:** Laundry Pickup and Delivery Management System (`LaundryCare`)  
**Sprint / Week:** Week 10 — Manual QA & Bug Hunting  
**Milestone:** Feature Freeze & Pre-Deployment Hardening  
**Date:** October 2026  
**Repository Branch:** `main`  

---

## 1. Executive Summary & Policy on Feature Freeze
During Week 10, the team officially entered **Feature Freeze**. In accordance with the course guidelines:
> *"Today you stop building and start breaking. A systematic QA pass now means no nasty surprises during the final defense. You'll test every feature against every scenario, try hard to break the app, and produce a clean, triaged bug list that next week's fixes will work through."*

No new functional features were merged into `main`. The team focused 100% on:
1. **Building the Comprehensive Test Matrix** ([`docs/test-matrix.md`](file:///C:/Users/Saidimar%20Rey/.gemini/antigravity/scratch/Laundry-Pickup-and-Delivery-Management-System/docs/test-matrix.md)) evaluating 15 features across 5 scenario dimensions (Happy Path, Boundary, Invalid Input, Empty State, Permissions/RBAC).
2. **Conducting Manual QA Testing** across all roles (Admin, Cashier, Van Courier, Moto Courier, Wash Operator).
3. **Adversarial Fuzzing Sessions** deliberately attempting to break system invariants with malformed data, concurrent clicks, and unexpected sequences.
4. **Expanding Automated Regression Suite** via [`tests/test_adversarial_qa.py`](file:///C:/Users/Saidimar%20Rey/.gemini/antigravity/scratch/Laundry-Pickup-and-Delivery-Management-System/tests/test_adversarial_qa.py), bringing total automated test coverage to **75 passing tests (100% green)**.
5. **Triaging Bugs into P0 / P1 / P2 Priorities** scheduled for resolution in Week 11.

---

## 2. Team Operational Roster & QA Assignments

| Member | Operational Role | QA Focus Area |
|---|---|---|
| **John Michael Bretaña** | Manager / Lead Architect | Global RBAC, session isolation, automated test suite architecture |
| **Hazil Enoc** | Store Cashier | CRM directory search, customer loyalty multiplier, boundary edge cases |
| **Marvin Oclarino** | Delivery Driver (Van 1) | Payment channel percentages, cash change calculator, thermal receipt printing |
| **Tristan Dave M. Plaza** | Delivery Driver (Motorcycle 1) | Mobile signature canvas touch interactions, route switcher, delivery dispatch |
| **Mark Ephraim Nicor** | Laundry Operator | Pickup slot conflict detection, wash hub machine capacity telemetry |

---

## 3. Prompts Used & Interaction Log (AI Disclosure)

In Week 10, AI was utilized **strictly for test scaffolding and boundary test generation**, while the team designed all test scenarios and executed manual validations:

### Task 1 & 2: Test Matrix Scaffolding
- **Prompt:**
  > *"Generate a comprehensive QA test matrix template in Markdown for a Flask/SQLite laundry delivery system covering 15 core features across 5 scenarios: Happy Path, Boundary Cases, Invalid Input, Empty State, and Permissions/RBAC."*
- **AI Output:**
  Provided a tabular matrix layout.
- **Human Refinement:**
  Populated every cell with LaundryCare-specific scenarios (e.g., dormitory addresses in CMU Musuan, 80mm thermal receipt constraints, dual-mode 404/500 error detection). Recorded in [`docs/test-matrix.md`](file:///C:/Users/Saidimar%20Rey/.gemini/antigravity/scratch/Laundry-Pickup-and-Delivery-Management-System/docs/test-matrix.md).

---

### Task 3: Automated Adversarial Test Scaffolding
- **Prompt:**
  > *"Write a pytest test file using Flask's test_client that adversarially attempts to break: 1) Negative laundry weight, 2) Negative payment amounts, 3) Accessing non-existent customer IDs, 4) Deleting stale records, 5) Malformed tracking codes, and 6) Role boundaries (riders blocked from financial exports)."*
- **AI Output:**
  Generated test cases in `tests/test_adversarial_qa.py`.
- **Human Refinement:**
  Adjusted response assertions to match LaundryCare's dual-mode error architecture (JSON 404/422 for AJAX requests and branded templates for in-page searches). Verified all 8 new tests pass cleanly.

---

### Task 4 & 5: Adversarial Bug Triage & Classification
- **Prompt:**
  > *"How should we triage and structure bug reports for: 1) Uncapped laundry weights (>100 kg), 2) Potential stored XSS in public booking notes, and 3) Selecting past dates in pickup datepickers into standard P0, P1, and P2 priority buckets?"*
- **AI Output:**
  Provided industry-standard bug report templates (Title, Severity, Steps to Reproduce, Expected vs. Actual, Triage Action).
- **Human Refinement:**
  Documented and triaged 4 specific bugs into the Bug Registry in [`docs/test-matrix.md`](file:///C:/Users/Saidimar%20Rey/.gemini/antigravity/scratch/Laundry-Pickup-and-Delivery-Management-System/docs/test-matrix.md).

---

## 4. Adversarial Session Findings Summary

| Adversarial Attack Vector | Behavior Observed | Evaluation |
|---|---|---|
| **Weird Input: Extreme Numbers** | Inputting `999999` kg generated an order total > ₱44M without a ceiling limit. | **BUG-002 (P1):** Uncapped weight ceiling needs upper bound limit (150 kg). |
| **Weird Input: Emojis** | Inputting `Juan Dela Cruz 🧺🧼` in name was stored and retrieved correctly. | **PASS ✅** SQLite UTF-8 encoding preserved characters cleanly. |
| **Weird Input: Stored XSS** | Inputting `<script>alert(1)</script>` in booking notes was escaped by Jinja2 in browser views, but stored raw in DB. | **BUG-001 (P1):** Tag-stripping middleware needed for complete defense-in-depth. |
| **Weird Input: Negative Money** | Submitting `-₱450.00` in payment amount was intercepted by structured validation (`HTTP 422`). | **PASS ✅** Core financial constraint holds. |
| **Out-of-Order: Double-Click** | Clicking "Record Payment" rapidly triggered `form_bindings.js` button disable lock; only 1 record created. | **PASS ✅** Zero duplicate billing. |
| **Out-of-Order: Back Button** | Clicking browser Back after deleting a client resulted in a graceful `404 Not Found` page. | **PASS ✅** Zero uncaught server crashes. |
| **Direct URL to Non-Existent ID** | Navigating to `/customers-page/details/99999` returned custom branded `404.html`. | **PASS ✅** Custom error handling active. |
| **Mobile Touchpad Signature** | Signing on phone canvas triggered `e.preventDefault()`, preventing screen scrolling during strokes. | **PASS ✅** Mobile driver ergonomics verified. |

---

## 5. Automated Test Suite Metrics

```bash
python -m pytest tests/
```
```
============================= test session starts =============================
platform win32 -- Python 3.13.7, pytest-9.1.1, pluggy-1.6.0
rootdir: C:\Users\Saidimar Rey\.gemini\antigravity\scratch\Laundry-Pickup-and-Delivery-Management-System
plugins: anyio-4.15.1, flet-1.0.0, asyncio-1.4.0
collected 75 items

tests\test_adversarial_qa.py ........                                    [ 10%]
tests\test_app.py ...                                                    [ 14%]
tests\test_async_bindings.py ...........                                 [ 29%]
tests\test_customer_portal.py .......                                    [ 38%]
tests\test_customers_crm.py .....                                        [ 45%]
tests\test_delivery.py ......                                            [ 53%]
tests\test_delivery_logistics.py ....                                    [ 58%]
tests\test_error_handling.py ...............                             [ 78%]
tests\test_payments_billing.py ....                                      [ 84%]
tests\test_pickup.py ...                                                 [ 88%]
tests\test_pickup_hub.py ....                                            [ 93%]
tests\test_rbac.py .....                                                 [100%]

============================= 75 passed in 3.48s ==============================
```

---

## 6. End-of-Lab Checklist

- [x] **`/docs/test-matrix.md` created:** 15 features × 5 scenarios, marked `PASS` / `FAIL`.
- [x] **Automated tests expanded on critical gaps:** Added [`tests/test_adversarial_qa.py`](file:///C:/Users/Saidimar%20Rey/.gemini/antigravity/scratch/Laundry-Pickup-and-Delivery-Management-System/tests/test_adversarial_qa.py); suite 100% green (75/75 passing).
- [x] **Adversarial testing session completed:** Fuzzing, XSS attempts, out-of-order actions, and network degradation evaluated.
- [x] **Every bug logged with reproduction steps + P0/P1/P2 labels:** BUG-001 through BUG-004 triaged in test matrix.
- [x] **Prompt logs current in `/docs/ai-notes/week-10.md`:** Complete AI disclosure and team attribution documented.

---

## 7. Looking Ahead to Week 11
In Week 11, the team will:
1. Work through the triaged bug list, resolving **P1 bugs first** (BUG-001 and BUG-002).
2. Pay down minor technical debt (BUG-003 date picker minimums and BUG-004 Escape key handler).
3. Prepare production configurations (`Gunicorn` / `Waitress`, environment variables, SQLite WAL mode).
4. Deploy `LaundryCare` to a live host (Render / Railway / PythonAnywhere) so it leaves `localhost`!
