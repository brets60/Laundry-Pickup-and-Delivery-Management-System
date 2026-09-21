# Week 08: Error Handling & Feedback Matrix
**Coursework:** CS 106 / Software Engineering 1  
**Project:** Laundry Pickup and Delivery Management System (`LaundryCare`)  
**Sprint / Week:** Week 08 — Phase 3: Error Handling, UI Feedback & Micro-Copy  
**Milestone:** Deliverable 3: Interface & View Binding (30%)  
**Date:** September 2026  
**Repository Branch:** `main`

---

## 1. Feedback Architecture Overview

In accordance with **Week 08 Lab Objectives (Interface & View Binding)**, every user action across **LaundryCare** is mapped to deterministic, predictable visual states. The system guarantees that users are never left wondering whether an action was processed, whether it succeeded, or what went wrong.

### The Core Feedback Principles:
1. **Always-On Loading State:** Every asynchronous operation (form submission, table loading, record deletion) immediately disables interactive controls (`disabled = true`, `aria-busy="true"`) and presents clear loading cues (`.btn-spinner`, skeleton shimmer rows) to eliminate double-submits and uncertainty.
2. **Deterministic Success Feedback:** Operations that complete successfully (HTTP 200/201) provide immediate confirmation through floating toasts (`.lc-toast-success`), form resets, modal dismissals, and DOM updates without requiring full-page reloads.
3. **Structured & Humanized Error Handling:**
   - **422 Validation Failures:** Field-level inline error badges (`.field-error-text`) render directly underneath the problematic inputs with high-contrast red focus rings (`.input-invalid`), accompanied by automatic keyboard focus on the first offending field.
   - **404 Not Found:** Dedicated, branded dark-glass error page (`templates/404.html`) and structured JSON error objects for missing entity lookups.
   - **500 Server Failures:** Dedicated error page (`templates/500.html`) and structured JSON payloads with zero stack trace leakage and a "Try Again" recovery path.
   - **Network Drops:** Resilient retry guidance in floating alert banners (`.lc-toast-error`).
4. **Destructive Action Confirmation:** Deletions are never executed on a single accidental click. A custom accessible modal dialog (`.lc-confirm-overlay`) requires explicit confirmation with red destructive cues before dispatching an asynchronous delete.

---

## 2. Team Member Module Ownership Matrix

To ensure clear accountability across the 5-member engineering team for Deliverable 3, module ownership is partitioned as follows:

| Team Member | Operational & System Role | Module Owned | Primary Views & Handlers |
|---|---|---|---|
| **John Michael D. Bretaña** | Manager (Admin / Lead Architect) | **Laundry Orders & System Admin** | `orders.html`, `edit_order.html`, `order_details.html`, Global `app.py` Error Handlers |
| **Hazil Enoc** | Store Cashier (Full-Stack / CRM) | **Customer Directory & POS Counter** | `customers.html`, `customer_details.html`, `animations.css` Feedback Styles |
| **Marvin Oclarino** | Delivery Driver (Logistics / Financial QA) | **Payments, Ledger & Route Van 1** | `payments.html`, `payment_details.html`, `test_error_handling.py` Test Suite |
| **Tristan Dave M. Plaza** | Delivery Driver (Logistics / Dispatch) | **Delivery Records & Courier Dispatch** | `deliveries.html`, `edit_delivery.html`, `delivery_details.html`, `404.html`, `500.html` |
| **Mark Ephraim Nicor** | Laundry Operator (Washing / UI Engine) | **Pickup Schedules & Wash Hub** | `pickups.html`, `edit_pickup.html`, `pickup_details.html`, `form_bindings.js` Engine |

---

## 3. Comprehensive Feedback State Matrix

The following matrix documents the exact visual, structural, and behavioral feedback provided for each action across all 5 operational modules:

### Module 1: Laundry Orders (Owner: John Michael D. Bretaña)

| Action | Trigger | Loading State | Success State (200 / 201) | Error State (422 / 404 / 500 / Net) | Destructive Confirmation |
|---|---|---|---|---|---|
| **Load Orders Table** | Page navigation to `/laundry-orders-page` | Skeleton shimmer rows (`.skeleton-shimmer`) with pulsing blue radar indicator | Fully populated table rows with status badges and mini-progress timeline | Error state card (`.error-table-state`) with "Failed to Load Laundry Orders" and retry button | N/A |
| **Create Order** | Click `+ Create Order` button in modal | Submit button disabled; spinner spins (`.btn-spinner`); text changes to *"Saving..."* | Toast *"Order #ORD-XXXX created successfully!"*; modal auto-closes; form resets; row prepended | 422: Red border on Customer and Weight inputs; inline text *"Customer name is required"* or *"Weight must be > 0"*<br>500: Red banner *"Failed to save order. Please try again."* | N/A |
| **View Order Details** | Click `View` button on row | Modal overlay appears immediately with populated order attributes | Complete summary loaded with itemized weight, pricing, and timeline | 404: Branded 404 dark-glass page *"Order Not Found"* with navigation links | N/A |
| **Edit Order** | Submit form on `/laundry-orders-page/edit/<id>` | Button disabled; spinner active; `aria-busy="true"` | Toast *"Order #ORD-XXXX updated successfully!"*; values reflected | 422: Inline field errors on invalid inputs<br>404: Branded 404 error page if ID does not exist | N/A |
| **Delete Order** | Click `Delete` button on table row or edit page | Confirm button in modal turns into spinner *"Deleting..."* | Toast *"Order #ORD-XXXX deleted successfully."*; table row smoothly fades out (`.row-fade-out`) and is removed | 404: Toast *"Record was not found or has already been deleted."*<br>Net: Toast *"Network error while deleting record."* | **Required:** Dark-glass modal: *"Delete Order #ORD-XXXX? This action cannot be undone."* [Cancel] [Yes, Delete] |

---

### Module 2: Delivery Records (Owner: Tristan Dave M. Plaza)

| Action | Trigger | Loading State | Success State (200 / 201) | Error State (422 / 404 / 500 / Net) | Destructive Confirmation |
|---|---|---|---|---|---|
| **Load Deliveries Table** | Page navigation to `/delivery-records-page` | Shimmering placeholder table rows with live zone indicator | Populated deliveries list with courier tags, zone pills, and timeline nodes | Error state banner with ⚠️ icon and *"Retry Delivery Query"* recovery action | N/A |
| **Dispatch Delivery** | Submit `Dispatch New Delivery` form | Submit button disabled with spinner and *"Saving..."* micro-copy | Toast *"Delivery to [Name] scheduled successfully!"*; modal closes | 422: Red border on Customer and Date; inline messages *"Customer Name is required."*<br>500: Toast *"Failed to dispatch delivery."* | N/A |
| **View Delivery Slip** | Click `Print Slip` on row | Slip modal renders instant preview with barcode tracking ID | Formatted printable thermal delivery slip ready for `window.print()` | 404: Toast *"Delivery record not found."* | N/A |
| **Edit Delivery** | Submit `/delivery-records-page/edit/<id>` | Button locked (`disabled = true`); spinner active | Toast *"Delivery record updated successfully!"*; status badge updated | 422: Inline error badges under empty fields<br>404: Branded 404 page | N/A |
| **Delete Delivery** | Click `Delete` on table row or edit page | Modal button shows animated spinner *"Deleting..."* | Toast *"Delivery #DEL-XXXX deleted successfully."*; row fades out and unmounts from DOM | 404: Toast *"Delivery record not found or already deleted."*<br>Net: Toast *"Network error while deleting record."* | **Required:** Dark-glass modal: *"Delete Delivery #DEL-XXXX? Are you sure you want to permanently delete this delivery?"* |

---

### Module 3: Pickup Schedules (Owner: Mark Ephraim Nicor)

| Action | Trigger | Loading State | Success State (200 / 201) | Error State (422 / 404 / 500 / Net) | Destructive Confirmation |
|---|---|---|---|---|---|
| **Load Pickup Table** | Navigate to `/pickup-schedules-page` | Pulse beacon with blue radar text *"Loading pickup schedules..."* + 4 shimmer rows | Active schedule table with zone categorization, time slots, and status badges | Error table state with *"Failed to Load Pickup Schedules"* and retry button | N/A |
| **Book Pickup** | Submit `Schedule New Pickup` modal form | Submit button disabled; spinner activated; prevents double-booking | Toast *"Pickup for [Name] booked successfully!"*; batch count increments | 422: Red outline on Customer, Date, Time Slot; inline message *"Please select a valid time slot"* | N/A |
| **View Pickup Details** | Click `View` on pickup schedule | Modal opens with driver assignment, address, and notes | All pickup parameters displayed with quick action buttons | 404: Branded 404 page if schedule does not exist | N/A |
| **Edit Pickup** | Submit `/pickup-schedules-page/edit/<id>` | Button locks with spinner; `aria-busy="true"` | Toast *"Pickup schedule updated successfully!"*; table row refreshed | 422: Inline field errors under invalid inputs<br>404: Branded 404 page | N/A |
| **Delete Pickup** | Click `Delete` on row or edit modal | Button disabled with spinner *"Deleting..."* | Toast *"Pickup #PCK-XXXX deleted successfully."*; row removed with CSS slide-fade | 404: Toast *"Pickup schedule not found."*<br>500: Toast *"Failed to delete schedule."* | **Required:** Dark-glass modal: *"Delete Pickup #PCK-XXXX? This action cannot be undone."* [Cancel] [Yes, Delete] |

---

### Module 4: Customer Directory (Owner: Hazil Enoc)

| Action | Trigger | Loading State | Success State (200 / 201) | Error State (422 / 404 / 500 / Net) | Destructive Confirmation |
|---|---|---|---|---|---|
| **Load Customer List** | Navigate to `/customers-page` | Blue pulse beacon with 3 shimmer skeleton bars | Table populated with CRM cards, order activity sparklines, and membership badges | Error table state with *"CRM database timeout. (HTTP 500)"* and retry button | N/A |
| **Register Customer** | Submit `Add New Customer` modal | Button disabled; spinner spins; prevents duplicate client entry | Toast *"Customer [Name] registered successfully!"*; modal dismissed; client added | 422: Red borders on Name and Contact Number; inline text *"Contact number is required."*<br>Net: Form-level alert banner | N/A |
| **View Customer Profile** | Click `View` on customer row | Customer profile modal renders with WhatsApp link and contact info | Instant profile display with order metrics and VIP tier badge | 404: Branded 404 page if customer ID does not exist | N/A |
| **Edit Customer Profile** | Submit `/customers-page/edit/<id>` | Submit button locked; spinner active | Toast *"Customer profile updated successfully!"*; details updated in table | 422: Inline badges on invalid inputs<br>404: Branded 404 page | N/A |
| **Delete Customer** | Click `Delete` on row or edit modal | Spinner active on modal button *"Deleting..."* | Toast *"Customer [Name] deleted successfully."*; table row smoothly unmounts | 404: Toast *"Customer not found or already deleted."*<br>Net: Toast *"Network error while deleting record."* | **Required:** Dark-glass modal: *"Delete Customer [Name]? Are you sure you want to permanently delete this customer profile?"* |

---

### Module 5: Payments & Billing (Owner: Marvin Oclarino)

| Action | Trigger | Loading State | Success State (200 / 201) | Error State (422 / 404 / 500 / Net) | Destructive Confirmation |
|---|---|---|---|---|---|
| **Load Payment Ledger** | Navigate to `/payments-page` | Skeleton shimmer rows with financial pulse beacon | Populated transaction ledger with reference codes, channel badges, and timestamps | Error state card with *"Financial ledger database error (HTTP 500)"* and retry button | N/A |
| **Record Payment** | Submit `Record New Payment` modal | Submit button disabled; spinner spins; prevents double-billing | Toast *"Payment #TXN-XXXX recorded successfully!"*; ledger updated | 422: Red border on Customer and Amount; inline message *"Payment amount must be greater than ₱0.00"* | N/A |
| **Print Receipt Slip** | Click `Print Slip` on row | Electronic thermal receipt modal opens with breakdown and totals | Formatted customer receipt ready for printing via `window.print()` | 404: Toast *"Transaction record not found."* | N/A |
| **Edit Payment** | Submit `/payments-page/edit/<id>` | Button disabled; spinner active | Toast *"Transaction #TXN-XXXX updated successfully!"*; status badge updated | 422: Inline field errors on negative amounts<br>404: Branded 404 page | N/A |
| **Delete Transaction** | Click `Delete` on row or edit modal | Spinner active on modal button *"Deleting..."* | Toast *"Transaction #TXN-XXXX deleted successfully."*; row fades out and unmounts | 404: Toast *"Transaction not found or already deleted."*<br>Net: Toast *"Network error."* | **Required:** Dark-glass modal: *"Delete Transaction #TXN-XXXX? Financial audit trail will be modified."* |

---

## 4. Humanized Micro-Copy Standards

To uphold the humanized feedback guidelines required by the rubric, our error messages obey strict linguistic criteria:
1. **Never Blame the User:** Instead of *"You entered an invalid weight"*, we use *"Laundry weight must be greater than 0 kg."*
2. **Plain English (No Technical Jargon):** Never display raw database errors, SQL syntax errors, or status codes like *"SQLITE_CONSTRAINT_NOTNULL"*. Use *"Please provide a customer name."*
3. **Actionable Recovery Guidance:** Every error explains how to correct it (e.g. *"Please enter a valid Philippine mobile number (e.g. 0917-123-4567)"*).
4. **Sentence Case & Calm Tone:** Messages avoid harsh ALL CAPS and exclamation marks, using clean, sentence-case phrasing.
