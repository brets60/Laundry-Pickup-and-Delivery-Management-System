# Laundry Pickup and Delivery Management System

## Product Backlog

This document contains the CRUD user stories for the Laundry Pickup and Delivery Management System.

## Team Members

| Module | Owner |
|---------|-------|
| Customer | Bretaña |
| Orders | Plaza |
| Pickup | Nicor |
| Delivery | Oclarino |
| Payment | Enoc |
   
## Team Assignment

Customer - John Michael D. Bretaña
Orders - Tristan Dave M. Plaza
Pickup - Mark Ephraim Nicor
Delivery - Marvin Oclarino
Payment - Hazil Enoc

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

**Owner:** Member 2

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

**Owner:** Member 3

## User Stories

### 1. Create Pickup
As a staff member, I want to schedule a pickup so that laundry can be collected from the customer.

**Acceptance Criteria**
- Pickup date is required.
- Customer must be selected.
- Pickup schedule is saved successfully.

---

### 2. Read Pickup List
As a staff member, I want to view all pickup schedules so that I can manage daily pickups.

**Acceptance Criteria**
- Displays all pickup schedules.
- Shows a message if there are no schedules.

---

### 3. Read Pickup Details
As a staff member, I want to view pickup details so that I can verify the schedule.

**Acceptance Criteria**
- Displays complete pickup information.

---

### 4. Update Pickup
As a staff member, I want to update pickup schedules so that changes are reflected.

**Acceptance Criteria**
- Pickup schedule can be edited.
- Updated information is saved.

---

### 5. Delete Pickup
As a staff member, I want to cancel a pickup schedule so that unnecessary schedules are removed.

**Acceptance Criteria**
- Confirmation message appears before deletion.
