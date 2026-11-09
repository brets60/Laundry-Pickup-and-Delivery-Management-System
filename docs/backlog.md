# Laundry Pickup and Delivery Management System

## Product Backlog & Deliverable 2 Module Ownership

This document contains the CRUD user stories and module assignments for the Laundry Pickup and Delivery Management System.

## Team Members & Deliverable 2 Ownership

| Module | Owner | Controller & Routes | Validation Function | Automated Tests |
|---|---|---|---|---|
| **Customer** | John Michael D. Bretaña | `/customers`, `/customers/:id` (`controllers/customer_routes.py`) | `validate_customer_payload` | `test_customers_full_crud_happy_path`, `test_customers_validation_and_edge_cases` |
| **Orders** | Tristan Dave M. Plaza | `/laundry-orders`, `/laundry-orders/:id` (`controllers/order_routes.py`) | `validate_laundry_order_payload` | `test_laundry_orders_full_crud_happy_path`, `test_laundry_orders_validation_and_edge_cases` |
| **Pickup** | Mark Ephraim Nicor | `/pickup-schedules`, `/pickup-schedules/:id` (`controllers/pickup_routes.py`) | `validate_pickup_schedule_payload` | `test_pickup_schedules_full_crud_happy_path`, `test_pickup_schedules_validation_and_edge_cases` |
| **Delivery** | Marvin Oclarino | `/delivery-records`, `/delivery-records/:id` (`controllers/delivery_routes.py`) | `validate_delivery_record_payload` | `test_delivery_records_full_crud_happy_path`, `test_delivery_records_validation_and_edge_cases` |
| **Payment** | Hazil Enoc | `/payments`, `/payments/:id` (`controllers/payment_routes.py`) | `validate_payment_payload` | `test_payments_full_crud_happy_path`, `test_payments_validation_and_edge_cases` |

## Team Assignment

- Customer - John Michael D. Bretaña
- Orders - Tristan Dave M. Plaza
- Pickup - Mark Ephraim Nicor
- Delivery - Marvin Oclarino
- Payment - Hazil Enoc

---

# Customer Module

**Owner:** John Michael D. Bretaña

## User Stories

### 1. Create Customer
**User Story**
As a staff member, I want to add a new customer so that I can store their information for future laundry transactions.

**Acceptance Criteria**
- Customer name is required.
- Contact number is required.
- Customer is successfully saved and appears in the customer list.

---

### 2. Read Customer List
**User Story**
As a staff member, I want to view all customers so that I can easily manage customer records.

**Acceptance Criteria**
- Displays all registered customers.
- Shows customer name and contact number.
- Displays a message if there are no customers.

---

### 3. Read Customer Details
**User Story**
As a staff member, I want to view a customer's complete information so that I can verify their details.

**Acceptance Criteria**
- Displays the customer's complete information.
- Shows an error message if the customer record does not exist.

---

### 4. Update Customer
**User Story**
As a staff member, I want to edit customer information so that records remain accurate and up to date.

**Acceptance Criteria**
- Existing customer information can be edited.
- Required fields cannot be left blank.
- Updated information is saved successfully.

---

### 5. Delete Customer
**User Story**
As a staff member, I want to remove inactive or incorrect customer records so that the database remains organized.

**Acceptance Criteria**
- A confirmation message appears before deletion.
- Customer record is removed after confirmation.
- Deleted customer no longer appears in the customer list.

---

# Orders Module

**Owner:** Tristan Dave M. Plaza

## User Stories

### 1. Create Order
**User Story**
As a staff member, I want to create a new laundry order so that customer laundry can be processed.

**Acceptance Criteria**
- Customer must be selected.
- Laundry weight must be greater than zero.
- Order is saved successfully.

---

### 2. Read Order List
**User Story**
As a staff member, I want to view all laundry orders so that I can monitor them.

**Acceptance Criteria**
- Displays all orders.
- Shows customer name, status, and total amount.
- Displays a message if there are no orders.

---

### 3. Read Order Details
**User Story**
As a staff member, I want to view order details so that I can verify the information.

**Acceptance Criteria**
- Displays complete order information.
- Shows an error if the order is not found.

---

### 4. Update Order
**User Story**
As a staff member, I want to edit an existing order so that incorrect information can be corrected.

**Acceptance Criteria**
- Existing order can be edited.
- Changes are saved successfully.
- Invalid values are rejected.

---

### 5. Delete Order
**User Story**
As a staff member, I want to remove cancelled orders so that the order list remains organized.

**Acceptance Criteria**
- Confirmation message appears.
- Order is deleted after confirmation.

---

# Pickup Module

**Owner:** Mark Ephraim Nicor

## User Stories

### 1. Create Pickup
**User Story**
As a staff member, I want to schedule a pickup so that laundry can be collected from the customer.

**Acceptance Criteria**
- Pickup date is required.
- Customer must be selected.
- Pickup schedule is saved successfully.

---

### 2. Read Pickup List
**User Story**
As a staff member, I want to view all pickup schedules so that I can manage daily pickups.

**Acceptance Criteria**
- Displays all pickup schedules.
- Shows a message if there are no schedules.

---

### 3. Read Pickup Details
**User Story**
As a staff member, I want to view pickup details so that I can verify the schedule.

**Acceptance Criteria**
- Displays complete pickup information.
- Shows an error if the pickup schedule does not exist.

---

### 4. Update Pickup
**User Story**
As a staff member, I want to update pickup schedules so that changes are reflected.

**Acceptance Criteria**
- Pickup schedule can be edited.
- Required fields cannot be left blank.
- Updated information is saved.

---

### 5. Delete Pickup
**User Story**
As a staff member, I want to cancel a pickup schedule so that unnecessary schedules are removed.

**Acceptance Criteria**
- Confirmation message appears before deletion.
- Pickup schedule is removed after confirmation.

---

# Delivery Module

**Owner:** Marvin Oclarino

## User Stories

### 1. Create Delivery Record
**User Story**
As a staff member, I want to create a delivery record so that completed laundry orders can be dispatched to the customer.

**Acceptance Criteria**
- Customer must be selected.
- Delivery date is required.
- Delivery record is saved successfully.

---

### 2. Read Delivery List
**User Story**
As a staff member, I want to view all delivery records so that I can track ongoing and completed deliveries.

**Acceptance Criteria**
- Displays all delivery records.
- Shows customer name, delivery date, and status.
- Displays a message if there are no delivery records.

---

### 3. Read Delivery Details
**User Story**
As a staff member, I want to view a delivery record's details so that I can check the delivery schedule and status.

**Acceptance Criteria**
- Displays complete delivery information.
- Shows an error if the delivery record is not found.

---

### 4. Update Delivery Record
**User Story**
As a staff member, I want to update delivery information so that status and schedule changes are recorded accurately.

**Acceptance Criteria**
- Delivery record can be edited.
- Required fields cannot be left blank.
- Changes are saved successfully.

---

### 5. Delete Delivery Record
**User Story**
As a staff member, I want to delete cancelled or duplicate delivery records so that the delivery list stays clean.

**Acceptance Criteria**
- Confirmation message appears before deletion.
- Delivery record is removed after confirmation.

---

# Payment Module

**Owner:** Hazil Enoc

## User Stories

### 1. Create Payment
**User Story**
As a staff member, I want to record customer payments so that transactions are documented.

**Acceptance Criteria**
- Customer must be selected.
- Payment amount is required and must be greater than zero.
- Payment method is selected.
- Payment is saved successfully.

---

### 2. Read Payment List
**User Story**
As a staff member, I want to view all payments so that I can monitor transactions.

**Acceptance Criteria**
- Displays all payment records.
- Shows a message if there are no payments.

---

### 3. Read Payment Details
**User Story**
As a staff member, I want to view payment details so that I can verify transactions.

**Acceptance Criteria**
- Displays complete payment information.
- Shows an error if the payment record is not found.

---

### 4. Update Payment
**User Story**
As a staff member, I want to update payment records so that errors can be corrected.

**Acceptance Criteria**
- Payment information can be edited.
- Invalid values are rejected with validation errors.
- Changes are saved successfully.

---

### 5. Delete Payment
**User Story**
As a staff member, I want to remove incorrect payment records so that the payment history remains accurate.

**Acceptance Criteria**
- Confirmation message appears before deletion.
- Payment record is removed after confirmation.
