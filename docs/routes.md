# Routing Structure & API Specification (`docs/routes.md`)

**Project:** Laundry Pickup and Delivery Management System (`LaundryCare`)  
**Milestone:** Deliverable 2 — Routing, Logic & Tests (Weeks 3–5 · Phase 2)

This document defines the complete RESTful routing structure across all 5 core domain modules of the Laundry Pickup and Delivery Management System. Every route uses the appropriate HTTP verb, delegates input defense to isolated guard-clause validators (`controllers/validators.py`), executes business logic via thin controllers (`controllers/crud_service.py`), and returns a standardized JSON envelope.

---

## Standardized Response Envelope

All 25 CRUD routes return a consistent top-level JSON structure:

```json
{
  "status": 200,
  "data": {},
  "error": null
}
```

- **Create (`POST`)**: Returns HTTP `201 Created` with the newly created record in `data`.
- **Read / Update / Delete (`GET`, `PUT`, `DELETE`)**: Returns HTTP `200 OK` with the requested or updated resource in `data`.
- **Validation Error (`POST`, `PUT`)**: Returns HTTP `422 Unprocessable Entity` with `data: null` and field-level error messages in `error.fields`.
- **Missing Record (`GET`, `PUT`, `DELETE`)**: Returns HTTP `404 Not Found` with `data: null` and `error.code: "NOT_FOUND"`.

---

## 1. Customer Module (Owner: Hazil Enoc)

| Method | Path             | Handler          | Validator                    | Story it serves              |
| ------ | ---------------- | ---------------- | ---------------------------- | ---------------------------- |
| POST   | `/customers`     | `createCustomer` | `validate_customer_payload`  | Add new customer information |
| GET    | `/customers`     | `listCustomers`  | —                            | View all customer records    |
| GET    | `/customers/:id` | `showCustomer`   | —                            | View customer details        |
| PUT    | `/customers/:id` | `updateCustomer` | `validate_customer_payload`  | Edit customer information    |
| DELETE | `/customers/:id` | `deleteCustomer` | —                            | Remove customer records      |

### Example Requests and Responses

#### `POST /customers`

**Request:**

```http
POST /customers HTTP/1.1
Content-Type: application/json

{
  "name": "Juan Dela Cruz",
  "contact_number": "09171234567"
}
```

**Response (`201 Created`):**

```json
{
  "status": 201,
  "data": {
    "id": 1,
    "name": "Juan Dela Cruz",
    "contact_number": "09171234567"
  },
  "error": null
}
```

#### `GET /customers`

**Request:**

```http
GET /customers HTTP/1.1
```

**Response (`200 OK`):**

```json
{
  "status": 200,
  "data": [
    {
      "id": 1,
      "name": "Juan Dela Cruz",
      "contact_number": "09171234567"
    }
  ],
  "error": null
}
```

#### `GET /customers/1`

**Request:**

```http
GET /customers/1 HTTP/1.1
```

**Response (`200 OK`):**

```json
{
  "status": 200,
  "data": {
    "id": 1,
    "name": "Juan Dela Cruz",
    "contact_number": "09171234567"
  },
  "error": null
}
```

#### `PUT /customers/1`

**Request:**

```http
PUT /customers/1 HTTP/1.1
Content-Type: application/json

{
  "name": "Juan Dela Cruz Jr.",
  "contact_number": "09189876543"
}
```

**Response (`200 OK`):**

```json
{
  "status": 200,
  "data": {
    "id": 1,
    "name": "Juan Dela Cruz Jr.",
    "contact_number": "09189876543"
  },
  "error": null
}
```

#### `DELETE /customers/1`

**Request:**

```http
DELETE /customers/1 HTTP/1.1
```

**Response (`200 OK`):**

```json
{
  "status": 200,
  "data": {
    "id": 1,
    "message": "Customer deleted successfully."
  },
  "error": null
}
```

---

## 2. Laundry Orders Module (Owner: John Michael D. Bretaña)

| Method | Path                  | Handler              | Validator                         | Story it serves                    |
| ------ | --------------------- | -------------------- | --------------------------------- | ---------------------------------- |
| POST   | `/laundry-orders`     | `createLaundryOrder` | `validate_laundry_order_payload`  | Create a new laundry order         |
| GET    | `/laundry-orders`     | `listLaundryOrders`  | —                                 | View all laundry orders and status |
| GET    | `/laundry-orders/:id` | `showLaundryOrder`   | —                                 | View order details and status      |
| PUT    | `/laundry-orders/:id` | `updateLaundryOrder` | `validate_laundry_order_payload`  | Update order details and weight    |
| DELETE | `/laundry-orders/:id` | `deleteLaundryOrder` | —                                 | Cancel or delete orders            |

### Example Requests and Responses

#### `POST /laundry-orders`

**Request:**

```http
POST /laundry-orders HTTP/1.1
Content-Type: application/json

{
  "customer": "Juan Dela Cruz",
  "laundry_weight": 5.5
}
```

**Response (`201 Created`):**

```json
{
  "status": 201,
  "data": {
    "id": 1,
    "customer": "Juan Dela Cruz",
    "laundry_weight": 5.5
  },
  "error": null
}
```

#### `GET /laundry-orders`

**Request:**

```http
GET /laundry-orders HTTP/1.1
```

**Response (`200 OK`):**

```json
{
  "status": 200,
  "data": [
    {
      "id": 1,
      "customer": "Juan Dela Cruz",
      "laundry_weight": 5.5
    }
  ],
  "error": null
}
```

#### `GET /laundry-orders/1`

**Request:**

```http
GET /laundry-orders/1 HTTP/1.1
```

**Response (`200 OK`):**

```json
{
  "status": 200,
  "data": {
    "id": 1,
    "customer": "Juan Dela Cruz",
    "laundry_weight": 5.5
  },
  "error": null
}
```

#### `PUT /laundry-orders/1`

**Request:**

```http
PUT /laundry-orders/1 HTTP/1.1
Content-Type: application/json

{
  "customer": "Juan Dela Cruz",
  "laundry_weight": 7.0
}
```

**Response (`200 OK`):**

```json
{
  "status": 200,
  "data": {
    "id": 1,
    "customer": "Juan Dela Cruz",
    "laundry_weight": 7.0
  },
  "error": null
}
```

#### `DELETE /laundry-orders/1`

**Request:**

```http
DELETE /laundry-orders/1 HTTP/1.1
```

**Response (`200 OK`):**

```json
{
  "status": 200,
  "data": {
    "id": 1,
    "message": "Laundry order deleted successfully."
  },
  "error": null
}
```

---

## 3. Pickup Schedules Module (Owner: Mark Ephraim Nicor)

| Method | Path                    | Handler                | Validator                           | Story it serves             |
| ------ | ----------------------- | ---------------------- | ----------------------------------- | --------------------------- |
| POST   | `/pickup-schedules`     | `createPickupSchedule` | `validate_pickup_schedule_payload`  | Schedule a pickup request   |
| GET    | `/pickup-schedules`     | `listPickupSchedules`  | —                                   | View pickup schedules       |
| GET    | `/pickup-schedules/:id` | `showPickupSchedule`   | —                                   | View a pickup schedule      |
| PUT    | `/pickup-schedules/:id` | `updatePickupSchedule` | `validate_pickup_schedule_payload`  | Modify pickup date and time |
| DELETE | `/pickup-schedules/:id` | `deletePickupSchedule` | —                                   | Cancel pickup requests      |

### Example Requests and Responses

#### `POST /pickup-schedules`

**Request:**

```http
POST /pickup-schedules HTTP/1.1
Content-Type: application/json

{
  "customer": "Juan Dela Cruz",
  "pickup_date": "2026-08-26"
}
```

**Response (`201 Created`):**

```json
{
  "status": 201,
  "data": {
    "id": 1,
    "customer": "Juan Dela Cruz",
    "pickup_date": "2026-08-26"
  },
  "error": null
}
```

#### `GET /pickup-schedules`

**Request:**

```http
GET /pickup-schedules HTTP/1.1
```

**Response (`200 OK`):**

```json
{
  "status": 200,
  "data": [
    {
      "id": 1,
      "customer": "Juan Dela Cruz",
      "pickup_date": "2026-08-26"
    }
  ],
  "error": null
}
```

#### `GET /pickup-schedules/1`

**Request:**

```http
GET /pickup-schedules/1 HTTP/1.1
```

**Response (`200 OK`):**

```json
{
  "status": 200,
  "data": {
    "id": 1,
    "customer": "Juan Dela Cruz",
    "pickup_date": "2026-08-26"
  },
  "error": null
}
```

#### `PUT /pickup-schedules/1`

**Request:**

```http
PUT /pickup-schedules/1 HTTP/1.1
Content-Type: application/json

{
  "customer": "Juan Dela Cruz",
  "pickup_date": "2026-08-27"
}
```

**Response (`200 OK`):**

```json
{
  "status": 200,
  "data": {
    "id": 1,
    "customer": "Juan Dela Cruz",
    "pickup_date": "2026-08-27"
  },
  "error": null
}
```

#### `DELETE /pickup-schedules/1`

**Request:**

```http
DELETE /pickup-schedules/1 HTTP/1.1
```

**Response (`200 OK`):**

```json
{
  "status": 200,
  "data": {
    "id": 1,
    "message": "Pickup schedule deleted successfully."
  },
  "error": null
}
```

---

## 4. Delivery Records Module (Owner: Tristan Dave M. Plaza)

| Method | Path                    | Handler                | Validator                           | Story it serves             |
| ------ | ----------------------- | ---------------------- | ----------------------------------- | --------------------------- |
| POST   | `/delivery-records`     | `createDeliveryRecord` | `validate_delivery_record_payload`  | Create delivery records     |
| GET    | `/delivery-records`     | `listDeliveryRecords`  | —                                   | View delivery status        |
| GET    | `/delivery-records/:id` | `showDeliveryRecord`   | —                                   | View a delivery record      |
| PUT    | `/delivery-records/:id` | `updateDeliveryRecord` | `validate_delivery_record_payload`  | Update delivery information |
| DELETE | `/delivery-records/:id` | `deleteDeliveryRecord` | —                                   | Delete delivery records     |

### Example Requests and Responses

#### `POST /delivery-records`

**Request:**

```http
POST /delivery-records HTTP/1.1
Content-Type: application/json

{
  "customer": "Juan Dela Cruz",
  "delivery_date": "2026-08-28"
}
```

**Response (`201 Created`):**

```json
{
  "status": 201,
  "data": {
    "id": 1,
    "customer": "Juan Dela Cruz",
    "delivery_date": "2026-08-28"
  },
  "error": null
}
```

#### `GET /delivery-records`

**Request:**

```http
GET /delivery-records HTTP/1.1
```

**Response (`200 OK`):**

```json
{
  "status": 200,
  "data": [
    {
      "id": 1,
      "customer": "Juan Dela Cruz",
      "delivery_date": "2026-08-28"
    }
  ],
  "error": null
}
```

#### `GET /delivery-records/1`

**Request:**

```http
GET /delivery-records/1 HTTP/1.1
```

**Response (`200 OK`):**

```json
{
  "status": 200,
  "data": {
    "id": 1,
    "customer": "Juan Dela Cruz",
    "delivery_date": "2026-08-28"
  },
  "error": null
}
```

#### `PUT /delivery-records/1`

**Request:**

```http
PUT /delivery-records/1 HTTP/1.1
Content-Type: application/json

{
  "customer": "Juan Dela Cruz",
  "delivery_date": "2026-08-29"
}
```

**Response (`200 OK`):**

```json
{
  "status": 200,
  "data": {
    "id": 1,
    "customer": "Juan Dela Cruz",
    "delivery_date": "2026-08-29"
  },
  "error": null
}
```

#### `DELETE /delivery-records/1`

**Request:**

```http
DELETE /delivery-records/1 HTTP/1.1
```

**Response (`200 OK`):**

```json
{
  "status": 200,
  "data": {
    "id": 1,
    "message": "Delivery record deleted successfully."
  },
  "error": null
}
```

---

## 5. Payment Module (Owner: Marvin Oclarino)

| Method | Path            | Handler         | Validator                  | Story it serves          |
| ------ | --------------- | --------------- | -------------------------- | ------------------------ |
| POST   | `/payments`     | `createPayment` | `validate_payment_payload` | Add payment transactions |
| GET    | `/payments`     | `listPayments`  | —                          | View payment history     |
| GET    | `/payments/:id` | `showPayment`   | —                          | View a payment record    |
| PUT    | `/payments/:id` | `updatePayment` | `validate_payment_payload` | Update payment status    |
| DELETE | `/payments/:id` | `deletePayment` | —                          | Delete payment records   |

### Example Requests and Responses

#### `POST /payments`

**Request:**

```http
POST /payments HTTP/1.1
Content-Type: application/json

{
  "customer": "Juan Dela Cruz",
  "payment_amount": 275.0,
  "payment_method": "Cash"
}
```

**Response (`201 Created`):**

```json
{
  "status": 201,
  "data": {
    "id": 1,
    "customer": "Juan Dela Cruz",
    "payment_amount": 275.0,
    "payment_method": "Cash",
    "transaction_time": "2026-08-26 14:30:00"
  },
  "error": null
}
```

#### `GET /payments`

**Request:**

```http
GET /payments HTTP/1.1
```

**Response (`200 OK`):**

```json
{
  "status": 200,
  "data": [
    {
      "id": 1,
      "customer": "Juan Dela Cruz",
      "payment_amount": 275.0,
      "payment_method": "Cash",
      "transaction_time": "2026-08-26 14:30:00"
    }
  ],
  "error": null
}
```

#### `GET /payments/1`

**Request:**

```http
GET /payments/1 HTTP/1.1
```

**Response (`200 OK`):**

```json
{
  "status": 200,
  "data": {
    "id": 1,
    "customer": "Juan Dela Cruz",
    "payment_amount": 275.0,
    "payment_method": "Cash",
    "transaction_time": "2026-08-26 14:30:00"
  },
  "error": null
}
```

#### `PUT /payments/1`

**Request:**

```http
PUT /payments/1 HTTP/1.1
Content-Type: application/json

{
  "customer": "Juan Dela Cruz",
  "payment_amount": 350.0,
  "payment_method": "GCash"
}
```

**Response (`200 OK`):**

```json
{
  "status": 200,
  "data": {
    "id": 1,
    "customer": "Juan Dela Cruz",
    "payment_amount": 350.0,
    "payment_method": "GCash"
  },
  "error": null
}
```

#### `DELETE /payments/1`

**Request:**

```http
DELETE /payments/1 HTTP/1.1
```

**Response (`200 OK`):**

```json
{
  "status": 200,
  "data": {
    "id": 1,
    "message": "Payment deleted successfully."
  },
  "error": null
}
```

---

## Route Verification Matrix (25/25 CRUD Endpoints)

All 25 CRUD routes are verified both manually and in the automated test suite (`tests/test_deliverable_2_crud.py`).

| # | Module | Method | Route | Expected Status | Actual Status | Result |
|---:|---|---|---|---:|---:|:---:|
| 1 | Customer | `POST` | `/customers` | 201 | 201 | PASS |
| 2 | Customer | `GET` | `/customers` | 200 | 200 | PASS |
| 3 | Customer | `GET` | `/customers/1` | 200 | 200 | PASS |
| 4 | Customer | `PUT` | `/customers/1` | 200 | 200 | PASS |
| 5 | Customer | `DELETE` | `/customers/1` | 200 | 200 | PASS |
| 6 | Laundry Orders | `POST` | `/laundry-orders` | 201 | 201 | PASS |
| 7 | Laundry Orders | `GET` | `/laundry-orders` | 200 | 200 | PASS |
| 8 | Laundry Orders | `GET` | `/laundry-orders/1` | 200 | 200 | PASS |
| 9 | Laundry Orders | `PUT` | `/laundry-orders/1` | 200 | 200 | PASS |
| 10 | Laundry Orders | `DELETE` | `/laundry-orders/1` | 200 | 200 | PASS |
| 11 | Pickup Schedules | `POST` | `/pickup-schedules` | 201 | 201 | PASS |
| 12 | Pickup Schedules | `GET` | `/pickup-schedules` | 200 | 200 | PASS |
| 13 | Pickup Schedules | `GET` | `/pickup-schedules/1` | 200 | 200 | PASS |
| 14 | Pickup Schedules | `PUT` | `/pickup-schedules/1` | 200 | 200 | PASS |
| 15 | Pickup Schedules | `DELETE` | `/pickup-schedules/1` | 200 | 200 | PASS |
| 16 | Delivery Records | `POST` | `/delivery-records` | 201 | 201 | PASS |
| 17 | Delivery Records | `GET` | `/delivery-records` | 200 | 200 | PASS |
| 18 | Delivery Records | `GET` | `/delivery-records/1` | 200 | 200 | PASS |
| 19 | Delivery Records | `PUT` | `/delivery-records/1` | 200 | 200 | PASS |
| 20 | Delivery Records | `DELETE` | `/delivery-records/1` | 200 | 200 | PASS |
| 21 | Payments | `POST` | `/payments` | 201 | 201 | PASS |
| 22 | Payments | `GET` | `/payments` | 200 | 200 | PASS |
| 23 | Payments | `GET` | `/payments/1` | 200 | 200 | PASS |
| 24 | Payments | `PUT` | `/payments/1` | 200 | 200 | PASS |
| 25 | Payments | `DELETE` | `/payments/1` | 200 | 200 | PASS |

### Wrong-Method Defense (`405 Method Not Allowed`)

Collection endpoints reject destructive `DELETE` or `PUT` calls that omit a resource `:id`:

```http
DELETE /customers HTTP/1.1
DELETE /laundry-orders HTTP/1.1
DELETE /pickup-schedules HTTP/1.1
DELETE /delivery-records HTTP/1.1
DELETE /payments HTTP/1.1
```

**Response:** `405 Method Not Allowed`
