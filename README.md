# LaundryCare — Laundry Pickup and Delivery Management System

**Live Web Application:** [https://laundrycare-management.onrender.com](https://laundrycare-management.onrender.com)  
**GitHub Repository:** [https://github.com/brets60/Laundry-Pickup-and-Delivery-Management-System](https://github.com/brets60/Laundry-Pickup-and-Delivery-Management-System)  
**Cloud Database:** Supabase (PostgreSQL - Singapore Region) / Local SQLite Fallback  
**Application Hosting:** Render Cloud Platform (PaaS)

---

## Problem Statement

Many laundry shops still use manual methods to record customer information, laundry orders, pickup schedules, and delivery transactions. This often leads to lost records, delayed deliveries, and poor communication with customers. The proposed Laundry Pickup and Delivery Management System aims to automate these processes by allowing customers to schedule pickups and deliveries, monitor the status of their laundry, and help administrators efficiently manage orders and records.

---

## Team Roster

**Project Title:** Laundry Pickup and Delivery Management System

| Name | Coursework Role | System Operational Role | Owned Controller & Test Modules |
| :--- | :--- | :--- | :--- |
| **John Michael D. Bretaña** | Repo Lead | Manager (Admin) | Laundry Orders (`controllers/order_routes.py`, `/laundry-orders`), Core Architecture & Auth |
| **Hazil Enoc** | Builder | Store Cashier | Customers (`controllers/customer_routes.py`, `/customers`), CRM & Loyalty |
| **Marvin Oclarino** | Builder | Delivery Driver | Payments (`controllers/payment_routes.py`, `/payments`), POS Billing & Receipts |
| **Tristan Dave M. Plaza** | Board Lead | Delivery Driver | Delivery Records (`controllers/delivery_routes.py`, `/delivery-records`), Fleet Dispatch |
| **Mark Ephraim Nicor** | Scribe | Laundry Operator | Pickup Schedules (`controllers/pickup_routes.py`, `/pickup-schedules`), Wash Hub Operations |

---

## Objectives

### General Objective

The main objective of the study is to develop a Laundry Pickup and Delivery Management System that will automate and improve the management of laundry services, including customer records, order processing, pickup scheduling, and delivery tracking.

### Specific Objectives

1. To create a system that allows customers to schedule laundry pickup and delivery services conveniently.
2. To develop a centralized database for managing customer information and laundry orders.
3. To provide real-time updates on the status of laundry orders, from pickup to delivery.
4. To enable administrators to efficiently manage pickup schedules, deliveries, and payment transactions.
5. To evaluate the effectiveness of the system in terms of usability, reliability, efficiency, security, and user satisfaction.

---

## Record Types & CRUD Matrix

| Module / Record Type | Create (`POST`)              | Read (`GET`)                  | Update (`PUT`)              | Delete (`DELETE`)       |
| -------------------- | ---------------------------- | ----------------------------- | --------------------------- | ----------------------- |
| **Customers**        | Add new customer information | View customer details         | Edit customer information   | Remove customer records |
| **Laundry Orders**   | Create a new laundry order   | View order details and status | Update order status         | Cancel or delete orders |
| **Pickup Schedules** | Schedule a pickup request    | View pickup schedules         | Modify pickup date and time | Cancel pickup requests  |
| **Delivery Records** | Create delivery records      | View delivery status          | Update delivery information | Delete delivery records |
| **Payments**         | Add payment transactions     | View payment history          | Update payment status       | Delete payment records  |

---

## Project Architecture & Deliverable Documentation

- **Routing Specification (Deliverable 2):** [`docs/routes.md`](docs/routes.md) — Full 25-route CRUD routing table and standardized request/response examples.
- **Validation Rules (Deliverable 2):** [`docs/validation.md`](docs/validation.md) — Guard-clause input validation matrix and HTTP `422` test evidence.
- **Isolated Validators & Services (Deliverable 2):** [`controllers/validators.py`](controllers/validators.py) & [`controllers/crud_service.py`](controllers/crud_service.py).
- **AI Statements & Notes:**
  - Deliverable 1 (Planning & Wireframes): [`docs/ai-notes/deliverable-1.md`](docs/ai-notes/deliverable-1.md)
  - Deliverable 2 (Phase 2 — AI OFF Statement): [`docs/ai-notes/deliverable-2.md`](docs/ai-notes/deliverable-2.md)
  - Deliverable 3 (Weeks 6–8 Interface & View Binding): [`docs/ai-notes/week-06.md`](docs/ai-notes/week-06.md), [`docs/ai-notes/week-07.md`](docs/ai-notes/week-07.md), [`docs/ai-notes/week-08.md`](docs/ai-notes/week-08.md)
  - Deliverable 4 (QA, Deployment & Final Defense): [`docs/ai-notes/deliverable-4.md`](docs/ai-notes/deliverable-4.md)

---

## Running the Application & Automated Test Suite

### 1. Install Dependencies

```bash
python -m venv .venv
# Windows PowerShell:
.venv\Scripts\pip install -r requirements.txt
# macOS / Linux:
.venv/bin/pip install -r requirements.txt
```

### 2. Run the Web Application Locally

```bash
python app.py
```

The server starts at `http://127.0.0.1:5000`.

### 3. Run the Automated Test Suite

Run the full automated test suite (covering happy paths, HTTP `422` validation failures, and `404`/`405` edge cases across all 5 CRUD modules):

```bash
pytest -v
```

To run only the Deliverable 2 core CRUD routing, validation, and controller test suite:

```bash
pytest tests/test_deliverable_2_crud.py -v
```

---

## Target Users of the System

1. **Customers** — Schedule laundry pickups and deliveries, monitor the status of their orders, and view transaction history.
2. **Administrator** — Manages customer records, laundry orders, pickup schedules, deliveries, and payment transactions.
3. **Delivery Personnel** — Handles the pickup and delivery of laundry items and updates the status of each transaction.
4. **Laundry Staff** — Manages the washing, drying, folding, and packaging processes and updates the progress of customers' orders.
