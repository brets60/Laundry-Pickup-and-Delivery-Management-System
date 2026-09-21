# Week 08: Failure-Path & UI Feedback Verification Test Log
**Coursework:** CS 106 / Software Engineering 1  
**Project:** Laundry Pickup and Delivery Management System (`LaundryCare`)  
**Sprint / Week:** Week 08 — Phase 3: Error Handling & Feedback  
**Milestone:** Deliverable 3: Interface & View Binding (30%)  
**Date:** September 2026  
**Repository Branch:** `main`  
**Automated Test Suite:** 45+ Passing Tests

---

## 1. Scope & Verification Strategy

As mandated by **Task 6 (Failure-Path Verification & Ship)** and the **Deliverable 3 Rubric**, all software applications must prove resilience against invalid inputs, broken routes, unexpected server exceptions, and destructive accidents. 

This test log documents the systematic verification of four primary failure categories across all five operational modules of **LaundryCare**:
1. **Category 1: 422 Validation Failures** (Field-level inline errors, red focus rings, auto-focus on first invalid input, no page reloads).
2. **Category 2: 404 Not Found Handling** (Custom dark-glass error page with recovery links, dual-mode JSON 404s for API requests, non-existent entity IDs).
3. **Category 3: 500 Server Error Safety** (Custom dark-glass 500 error page with retry button, zero stack trace leakage to clients).
4. **Category 4: Destructive Action Safety** (Confirmation modal dialog preventing accidental one-click deletions, cancellation tests, and row removal animation).

---

## 2. Test Execution Log by Failure Category

### Category 1: 422 Validation Failures (Inline Field-Level Badges)

| Test ID | Module | Scenario / Trigger | Input Data | Expected Behavior | Observed Result | Status |
|---|---|---|---|---|---|---|
| **ERR-422-01** | Orders | Create order with empty customer & zero weight | `customer = ""` , `laundry_weight = 0` | 422 returned; red borders on `#customer` & `#orderWeightInput`; inline text *"Customer name is required"* & *"Laundry weight must be greater than 0 kg."* | Red borders and inline `.field-error-text` rendered; first invalid field focused. | **PASS** |
| **ERR-422-02** | Orders | Edit order with negative weight | `laundry_weight = -3.5` | 422 returned; inline error below weight input; previous valid customer name preserved in form | Red border and message *"Laundry weight must be greater than 0 kg."* displayed. | **PASS** |
| **ERR-422-03** | Deliveries | Dispatch delivery without customer name | `customer = ""`, `delivery_date = "2026-09-25"` | 422 returned; field error under Customer input; submit button re-enabled | Red focus ring and *"Customer Name is required."* displayed; submit button re-enabled. | **PASS** |
| **ERR-422-04** | Deliveries | Dispatch delivery without delivery date | `customer = "John Doe"`, `delivery_date = ""` | 422 returned; field error under Date input | Red focus ring and *"Delivery Date is required."* displayed. | **PASS** |
| **ERR-422-05** | Pickups | Book pickup without customer name | `customer = ""` | 422 returned; red border on customer input; *"Customer Name is required."* | Red focus ring and inline message displayed; modal remains open for correction. | **PASS** |
| **ERR-422-06** | Pickups | Book pickup without pickup date | `customer = "Jane Smith"`, `pickup_date = ""` | 422 returned; inline message under pickup date input | Red outline and *"Pickup Date is required."* displayed. | **PASS** |
| **ERR-422-07** | Customers | Register customer with empty name | `name = ""`, `contact_number = "0917-111-2222"` | 422 returned; red focus ring on `#new_name`; *"Customer Name is required."* | Field highlighted in red; inline error badge displayed; submit button re-enabled. | **PASS** |
| **ERR-422-08** | Customers | Register customer with empty contact number | `name = "Mario Lopez"`, `contact_number = ""` | 422 returned; inline message under `#new_contact_number` | Red ring and *"Contact Number is required."* rendered. | **PASS** |
| **ERR-422-09** | Payments | Record payment with empty customer | `customer = ""`, `payment_amount = 500` | 422 returned; inline error under Customer input | Highlighted red with *"Customer Name is required."* | **PASS** |
| **ERR-422-10** | Payments | Record payment with zero or negative amount | `customer = "Rita Gomez"`, `payment_amount = -100` | 422 returned; inline message *"Payment amount must be greater than ₱0.00"* | Red ring and inline warning displayed. | **PASS** |

---

### Category 2: 404 Not Found Handling (Missing Records & Non-Existent Routes)

| Test ID | View / Route | Scenario / Trigger | Request Type | Expected Behavior | Observed Result | Status |
|---|---|---|---|---|---|---|
| **ERR-404-01** | Global Route | Access `/non-existent-page-url` | Synchronous GET | Branded dark-glass 404 error page rendered (`templates/404.html`) with "Return to Dashboard" link | Dark-glass 404 template rendered; HTTP 404 status; no raw server text. | **PASS** |
| **ERR-404-02** | Orders | Access `/laundry-orders-page/details/99999` (ID does not exist) | Synchronous GET | Branded 404 error page displayed with order recovery links | Branded 404 template displayed; 404 status confirmed. | **PASS** |
| **ERR-404-03** | Orders | Edit non-existent order `/laundry-orders-page/edit/99999` | Synchronous GET | Custom 404 template rendered; graceful navigation back to Orders directory | 404 page rendered with clear navigation buttons. | **PASS** |
| **ERR-404-04** | Deliveries | Access `/delivery-records-page/details/99999` | Synchronous GET | Custom 404 error page rendered | Dark-glass 404 error template rendered. | **PASS** |
| **ERR-404-05** | Pickups | Access `/pickup-schedules-page/details/99999` | Synchronous GET | Custom 404 error page rendered | Dark-glass 404 error template rendered. | **PASS** |
| **ERR-404-06** | Customers | Access `/customers-page/details/99999` | Synchronous GET | Custom 404 error page rendered | Dark-glass 404 error template rendered. | **PASS** |
| **ERR-404-07** | Payments | Access `/payments-page/details/99999` | Synchronous GET | Custom 404 error page rendered | Dark-glass 404 error template rendered. | **PASS** |
| **ERR-404-08** | API / Async | Async `DELETE` on `/laundry-orders-page/delete/99999` | Async JSON (`X-Requested-With`) | HTTP 404 JSON returned `{ "status": 404, "error": "Order not found or has already been deleted." }` | JSON 404 response received; toast notification *"Record was not found or has already been deleted."* displayed. | **PASS** |
| **ERR-404-09** | API / Async | Async `DELETE` on `/customers-page/delete/99999` | Async JSON (`Accept: application/json`) | HTTP 404 JSON returned `{ "status": 404, "error": "Customer not found or has already been deleted." }` | JSON 404 returned; error toast displayed. | **PASS** |

---

### Category 3: 500 Server Error Safety (No Stack Trace Leakage)

| Test ID | Trigger / Scenario | Request Type | Expected Behavior | Observed Result | Status |
|---|---|---|---|---|---|
| **ERR-500-01** | Simulated internal server exception | Synchronous GET | Custom dark-glass 500 error page (`templates/500.html`) rendered with "Try Again" reload button and support email; zero Python stack traces or traceback lines visible to user | Rendered branded dark-glass 500 page; no traceback or internal code visible in DOM or source. | **PASS** |
| **ERR-500-02** | Simulated backend failure on async form submission | Async POST (`X-Requested-With: XMLHttpRequest`) | JSON 500 returned `{ "status": 500, "error": "An internal server error occurred. Please try again later." }`; client re-enables submit button and shows error toast | HTTP 500 JSON received; submit button re-enabled; red toast displayed; no application crash. | **PASS** |
| **ERR-500-03** | Server timeout simulation on list query (`?state=error`) | Wireframe State GET | Dedicated error table state rendered with retry button (`↺ Retry Fetching Orders`) | Table error state displayed with ⚠️ icon and retry link. | **PASS** |

---

### Category 4: Destructive Action Safety (Confirmation Modals)

| Test ID | Module | Scenario / Trigger | Action Taken | Expected Outcome | Observed Result | Status |
|---|---|---|---|---|---|---|
| **ERR-DEL-01** | Orders | Click `Delete` button on Order #ORD-0001 | Click `Cancel` in confirmation modal | Modal closes immediately; record remains intact in SQLite; table row is NOT deleted | Deletion aborted; modal unmounted; row remains untouched in DOM. | **PASS** |
| **ERR-DEL-02** | Orders | Click `Delete` button on Order #ORD-0001 | Click `Yes, Delete` in confirmation modal | Confirm button enters loading state with spinner; async POST dispatched; 200 OK received; green toast appears; row animates out (`.row-fade-out`) and unmounts | Row smoothly faded out and removed; toast *"Order #ORD-0001 deleted successfully."* displayed; DB confirmed deleted. | **PASS** |
| **ERR-DEL-03** | Deliveries | Click `Delete` on Delivery #DEL-0001 | Click `Cancel` | Action cancelled; no network request dispatched | No request dispatched; record remains unchanged. | **PASS** |
| **ERR-DEL-04** | Deliveries | Click `Delete` on Delivery #DEL-0001 | Click `Yes, Delete` | Async delete dispatched; 200 OK; toast displayed; row faded out | Record removed from SQLite and DOM without page reload. | **PASS** |
| **ERR-DEL-05** | Pickups | Click `Delete` on Pickup #PCK-0001 | Click `Yes, Delete` | Modal confirms; async delete; 200 OK; toast confirmation; row removed | Record deleted; green toast confirmed; row removed. | **PASS** |
| **ERR-DEL-06** | Customers | Click `Delete Client` in customer edit modal | Click `Yes, Delete` | Edit modal dismissed; confirm dialog confirms; async delete sent; 200 OK; toast confirms | Client record deleted; row fades out in table; toast confirmed. | **PASS** |
| **ERR-DEL-07** | Payments | Click `Delete` on Transaction #TXN-0001 | Click `Yes, Delete` | Confirmation dialog verifies financial audit warning; async delete; 200 OK; row removed | Record deleted; green toast displayed; ledger row unmounted. | **PASS** |

---

## 3. Humanized Error Micro-Copy Audit

All micro-copy across the application was audited against the rubric standards:

| Context | Legacy / Technical Error (Before) | Humanized Micro-Copy (After) | Audit Result |
|---|---|---|---|
| Order Weight | *"Weight is invalid or null"* | *"Laundry weight must be greater than 0 kg."* | ✅ Approved |
| Customer Name | *"IntegrityError: customer NOT NULL"* | *"Customer Name is required."* | ✅ Approved |
| Contact Number | *"Invalid format regex"* | *"Please provide a contact phone number."* | ✅ Approved |
| Payment Amount | *"Amount <= 0 invalid"* | *"Payment amount must be greater than ₱0.00"* | ✅ Approved |
| Delivery Date | *"delivery_date missing"* | *"Delivery Date is required."* | ✅ Approved |
| Pickup Date | *"pickup_date missing"* | *"Pickup Date is required."* | ✅ Approved |
| 404 Route | *"404 Not Found - nginx"* | *"Page or record not found. The item you requested may have been moved or deleted."* | ✅ Approved |
| 500 Exception | *Python Traceback (line 142 in ...)* | *"Something went wrong on our end. Our engineering team has been notified. Please try again."* | ✅ Approved |
