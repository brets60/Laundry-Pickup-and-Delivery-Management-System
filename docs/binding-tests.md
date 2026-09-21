# Week 07: Form Binding & End-to-End Verification Matrix
**Coursework:** CS 106 / Software Engineering 1  
**Project:** Laundry Pickup and Delivery Management System (`LaundryCare`)  
**Sprint / Week:** Week 07 — Phase 3: Interface Binding (Binding Forms to the Backend)  
**Date:** September 2026  
**Repository Branch:** `main`  
**Test Suite Status:** 35 / 35 Passing (100% Green)

---

## 1. Executive Summary & Verification Objectives

During Week 07, our 5-member engineering team connected all client-side HTML forms across **LaundryCare** to the Flask/SQLite backend controllers using asynchronous HTTP operations (`fetch()`). 

This document satisfies **Task 4 (E2E Verification Matrix)** of the Week 7 Lab Handout by verifying the 4 mandatory lifecycle states:
1. **Pending / Loading:** Submit button disabled immediately upon click (`disabled = true`), displaying an animated spinner and preventing double-submit duplicate records.
2. **Fulfilled / Success (200 / 201):** Record persisted in SQLite, green floating toast confirmation displayed, form reset, modal dismissed, and table updated without full page refresh.
3. **Validation Failure (422 Unprocessable Entity):** Backend returns structured `{ "status": 422, "error": { "field_name": "error_message" } }`. Form interceptor displays high-visibility inline error text directly underneath invalid inputs with red focus rings. Errors are **never swallowed**.
4. **Server / Network Failure (500 / Network Drop):** Floating red alert banner rendered at the top of the form with retry guidance without crashing the application.

---

## 2. Team Member Module Ownership Matrix

To maintain balanced contributions across the engineering team, form bindings were partitioned across 5 functional operational modules:

| Team Member | Role | Primary Module Owned | Key Binding Routes |
|---|---|---|---|
| **John Michael D. Bretaña** | Lead Architect / Backend | **Laundry Orders** | `POST /laundry-orders-page`, `POST/PUT /laundry-orders-page/edit/<id>` |
| **Tristan Dave M. Plaza** | Frontend / Logistics Eng. | **Delivery Records** | `POST /delivery-records-page`, `POST/PUT /delivery-records-page/edit/<id>` |
| **Mark Ephraim Nicor** | Frontend / UI Interaction | **Pickup Schedules** | `POST /pickup-schedules-page`, `POST/PUT /pickup-schedules-page/edit/<id>` |
| **Hazil Enoc** | Full-Stack / CRM Eng. | **Customer Directory** | `POST /customers-page`, `POST/PUT /customers-page/edit/<id>` |
| **Marvin Oclarino** | QA / Financial Eng. | **Payments & Billing** | `POST /payments-page`, `POST/PUT /payments-page/edit/<id>` |

---

## 3. End-to-End Test Cases & Verification Results

### Module 1: Laundry Orders (`orders.html` & `edit_order.html`)
*Owned by: John Michael D. Bretaña*

| Test ID | Test Scenario | Steps Executed | Expected Outcome | Actual Result | Status |
|---|---|---|---|---|---|
| **ORD-E2E-01** | Create Order (Valid) | 1. Open `+ Create New Laundry Order` modal.<br>2. Enter Customer: *"Maria Santos"*, Weight: `4.5` kg, Service: `Wash & Fold`.<br>3. Click `Create Order`. | Form intercepts submit; button enters pending state with spinner; POST sent; 201 Created returned; toast appears; order appears in list. | Button disabled with `btn-spinner`; 201 Created; toast *"Order #ORD-XXXX created successfully!"*; record rendered in table. | **PASS** |
| **ORD-E2E-02** | Create Order (Empty / 422) | 1. Open modal.<br>2. Leave Customer and Weight blank.<br>3. Click `Create Order`. | Form prevents submission; sends async request; backend returns 422 with `{ "customer": "...", "laundry_weight": "..." }`; red error badges render directly below inputs. | Red borders on `#customer` and `#orderWeightInput`; inline `.field-error-text` rendered; first invalid input focused. | **PASS** |
| **ORD-E2E-03** | Double-Submit Prevention | 1. Fill valid order data.<br>2. Rapidly double-click `Create Order` button twice within 100ms. | Button is disabled on first click (`button.disabled = true`); second click is completely rejected; exactly 1 record created in database. | Only 1 HTTP POST dispatched; exactly 1 record in `laundry_orders` table (`SELECT COUNT(*) == 1`). | **PASS** |
| **ORD-E2E-04** | Edit Order Pre-fill & Update | 1. Navigate to `/laundry-orders-page/edit/1`.<br>2. Verify pre-filled inputs.<br>3. Modify weight to `6.0` kg.<br>4. Submit. | Async POST/PUT dispatched; 200 OK returned; success toast displayed; SQLite updated with new weight `6.0`. | 200 OK returned; toast *"Order #ORD-0001 updated successfully!"*; DB verified with updated values. | **PASS** |

---

### Module 2: Delivery Records (`deliveries.html` & `edit_delivery.html`)
*Owned by: Tristan Dave M. Plaza*

| Test ID | Test Scenario | Steps Executed | Expected Outcome | Actual Result | Status |
|---|---|---|---|---|---|
| **DEL-E2E-01** | Dispatch Delivery (Valid) | 1. Open `Dispatch New Delivery` modal.<br>2. Enter Customer: *"Carlos Mendoza"*, Date: `2026-09-25`, Address: *"Block 12 Lot 5, Maramag"*.<br>3. Click `Dispatch Delivery`. | Form submits via `fetch()`; button disabled with spinner; 201 Created; toast confirms dispatch; record added to deliveries table. | 201 Created received; toast *"Delivery to Carlos Mendoza scheduled successfully!"*; record persisted. | **PASS** |
| **DEL-E2E-02** | Delivery 422 Validation | 1. Open dispatch modal.<br>2. Leave Customer and Date blank.<br>3. Submit. | Backend returns 422 with structured field error dictionary; inline errors render under Customer and Date fields. | HTTP 422 returned; `.field-error-text` rendered under customer and date; no page reload. | **PASS** |
| **DEL-E2E-03** | Edit Delivery Record | 1. Click `Edit` on delivery record.<br>2. Update Status to *"Out for Delivery"* and assign *"Rider Mike"*.<br>3. Submit edit form. | Async update; 200 OK; table status badge changes to blue *"Out for Delivery"*. | Record updated in SQLite; 200 OK response; toast displayed. | **PASS** |

---

### Module 3: Pickup Schedules (`pickups.html` & `edit_pickup.html`)
*Owned by: Mark Ephraim Nicor*

| Test ID | Test Scenario | Steps Executed | Expected Outcome | Actual Result | Status |
|---|---|---|---|---|---|
| **PCK-E2E-01** | Schedule Pickup (Valid) | 1. Open `Book Laundry Pickup` modal.<br>2. Enter Customer: *"Ana Reyes"*, Date: `2026-09-26`, Slot: `02:00 PM - 05:00 PM`.<br>3. Submit. | Async POST; button shows spinner; 201 Created; pickup batch counter increments; schedule row appears in calendar/table. | 201 Created returned; toast *"Pickup for Ana Reyes booked successfully!"*; modal closed. | **PASS** |
| **PCK-E2E-02** | Pickup 422 Validation | 1. Leave Customer name blank.<br>2. Submit form. | 422 Unprocessable Entity returned with `{ "customer": "Customer Name is required." }`; red inline error displayed. | Field highlighted with red border; inline message *"Customer Name is required."* displayed below input. | **PASS** |
| **PCK-E2E-03** | Edit Pickup Schedule | 1. Open edit modal or `/pickup-schedules-page/edit/<id>`.<br>2. Change date to tomorrow.<br>3. Click `Save Changes`. | Record updated asynchronously; 200 OK returned; changes persisted in DB. | 200 OK; record updated in database; toast notification confirmed. | **PASS** |

---

### Module 4: Customer Directory (`customers.html` & `edit_customer.html`)
*Owned by: Hazil Enoc*

| Test ID | Test Scenario | Steps Executed | Expected Outcome | Actual Result | Status |
|---|---|---|---|---|---|
| **CUS-E2E-01** | Register Customer (Valid) | 1. Open `Add New Customer` modal.<br>2. Enter Name: *"Gabriel Ramos"*, Contact: `0918-765-4321`, Tier: `VIP`.<br>3. Submit. | Async POST; 201 Created; customer card/table updates; VIP badge appears. | 201 Created; toast *"Customer 'Gabriel Ramos' registered successfully!"*; row added. | **PASS** |
| **CUS-E2E-02** | Customer 422 Validation | 1. Leave Name and Contact Number empty.<br>2. Submit form. | 422 Unprocessable Entity returned; inline field error badges rendered under Name and Contact Number. | Inline red error text under both inputs; form does not reload; submit button re-enabled. | **PASS** |
| **CUS-E2E-03** | Edit Customer Profile | 1. Open edit form for customer.<br>2. Update phone number and address.<br>3. Click `Save Changes`. | Async PUT/POST; 200 OK; profile updated without losing order history foreign keys. | 200 OK; SQLite row updated; toast displayed; updated contact visible on refresh. | **PASS** |

---

### Module 5: Payments & Invoicing (`payments.html` & `edit_payment.html`)
*Owned by: Marvin Oclarino*

| Test ID | Test Scenario | Steps Executed | Expected Outcome | Actual Result | Status |
|---|---|---|---|---|---|
| **PAY-E2E-01** | Record Payment (Valid) | 1. Open `Record New Payment` modal.<br>2. Customer: *"Gabriel Ramos"*, Amount: `₱350.00`, Method: `GCash`.<br>3. Click `Record Payment`. | Async POST; 201 Created; transaction reference generated (`TXN-XXXX`); total revenue KPI updates dynamically. | 201 Created; toast *"Payment #TXN-XXXX recorded successfully!"*; transaction log updated. | **PASS** |
| **PAY-E2E-02** | Payment 422 Validation | 1. Enter negative amount `-50.00` and leave method blank.<br>2. Submit. | 422 Unprocessable Entity; inline errors on amount (*"must be greater than 0"*) and method (*"required"*). | Structured 422 response `{ "payment_amount": "...", "payment_method": "..." }`; inline error badges displayed. | **PASS** |
| **PAY-E2E-03** | Edit Payment Record | 1. Navigate to `/payments-page/edit/<id>`.<br>2. Change method from Cash to GCash.<br>3. Submit. | 200 OK returned; transaction journal updated; journal reflects correct payment method. | 200 OK; DB record updated; toast confirmed. | **PASS** |

---

## 4. Automated Verification Suite Execution Logs

The full test suite was executed via `pytest`, verifying both legacy synchronous endpoints and newly bound asynchronous JSON endpoints:

```text
============================= test session starts =============================
platform win32 -- Python 3.13.7, pytest-9.1.1, pluggy-1.6.0
rootdir: C:\Users\Saidimar Rey\.gemini\antigravity\scratch\Laundry-Pickup-and-Delivery-Management-System
plugins: anyio-4.15.1, flet-1.0.0, asyncio-1.4.0
asyncio: mode=Mode.STRICT, debug=False
collected 35 items

tests\test_app.py ...                                                    [  8%]
tests\test_async_bindings.py ...........                                 [ 40%]
tests\test_customer_portal.py .......                                    [ 60%]
tests\test_delivery.py ......                                            [ 77%]
tests\test_pickup.py ...                                                 [ 85%]
tests\test_rbac.py .....                                                 [100%]

============================= 35 passed in 4.24s ==============================
```

### Test Suite Coverage Highlights
- **11 Dedicated Async Binding Tests** in [`tests/test_async_bindings.py`](file:///C:/Users/Saidimar%20Rey/.gemini/antigravity/scratch/Laundry-Pickup-and-Delivery-Management-System/tests/test_async_bindings.py):
  1. `test_async_create_order_success` $\rightarrow$ 201 Created + JSON payload.
  2. `test_async_create_order_validation_error_422` $\rightarrow$ 422 structured field error dictionary.
  3. `test_async_edit_order_success` $\rightarrow$ 200 OK + updated record.
  4. `test_async_create_delivery_success` $\rightarrow$ 201 Created + linked delivery record.
  5. `test_async_create_delivery_validation_error_422` $\rightarrow$ 422 on missing required fields.
  6. `test_async_create_pickup_success` $\rightarrow$ 201 Created + schedule slot.
  7. `test_async_create_pickup_validation_error_422` $\rightarrow$ 422 on missing customer.
  8. `test_async_create_customer_success` $\rightarrow$ 201 Created + VIP tier.
  9. `test_async_create_customer_validation_error_422` $\rightarrow$ 422 field errors on name & phone.
  10. `test_async_create_payment_success` $\rightarrow$ 201 Created + TXN code.
  11. `test_async_create_payment_validation_error_422` $\rightarrow$ 422 on negative amount & missing method.
- **24 Legacy Unit & Integration Tests:** 100% green without breaking changes.

---

## 5. Conclusion

All 5 core operational views and their corresponding edit pages are completely bound to the backend using modern asynchronous patterns. Double submission is physically impossible due to UI button locking and aria-busy tracking, and all validation failures display prominent, contextual field-level badges. The test suite of 35 tests confirms system stability and zero regressions.
