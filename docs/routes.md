# Routing Table

## Laundry Pickup and Delivery Management System

This document contains the routing table for the Laundry Pickup and Delivery Management System. Each CRUD operation has a corresponding RESTful route and handler.

---

## Customer Module

| Method | Path             | Handler          | Story it serves              |
| ------ | ---------------- | ---------------- | ---------------------------- |
| POST   | `/customers`     | `createCustomer` | Add new customer information |
| GET    | `/customers`     | `listCustomers`  | View all customer records    |
| GET    | `/customers/:id` | `showCustomer`   | View customer details        |
| PUT    | `/customers/:id` | `updateCustomer` | Edit customer information    |
| DELETE | `/customers/:id` | `deleteCustomer` | Remove customer records      |

### Example Requests and Responses

**POST `/customers`**

Request:

```http
POST /customers
Content-Type: application/json

{
  "name": "John Doe",
  "contact_number": "09123456789"
}
```

Response:

```json
{
  "status": 201,
  "data": {
    "id": 1,
    "name": "John Doe",
    "contact_number": "09123456789"
  },
  "error": null
}
```

**GET `/customers`**

Request:

```http
GET /customers
```

Response:

```json
{
  "status": 200,
  "data": [
    {
      "id": 1,
      "name": "John Doe",
      "contact_number": "09123456789"
    }
  ],
  "error": null
}
```

**GET `/customers/1`**

Request:

```http
GET /customers/1
```

Response:

```json
{
  "status": 200,
  "data": {
    "id": 1,
    "name": "John Doe",
    "contact_number": "09123456789"
  },
  "error": null
}
```

**PUT `/customers/1`**

Request:

```http
PUT /customers/1
Content-Type: application/json

{
  "name": "John Doe",
  "contact_number": "09198765432"
}
```

Response:

```json
{
  "status": 200,
  "data": {
    "id": 1,
    "name": "John Doe",
    "contact_number": "09198765432"
  },
  "error": null
}
```

**DELETE `/customers/1`**

Request:

```http
DELETE /customers/1
```

Response:

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

## Laundry Orders Module

| Method | Path                  | Handler              | Story it serves                    |
| ------ | --------------------- | -------------------- | ---------------------------------- |
| POST   | `/laundry-orders`     | `createLaundryOrder` | Create a new laundry order         |
| GET    | `/laundry-orders`     | `listLaundryOrders`  | View all laundry orders and status |
| GET    | `/laundry-orders/:id` | `showLaundryOrder`   | View order details and status      |
| PUT    | `/laundry-orders/:id` | `updateLaundryOrder` | Update order status                |
| DELETE | `/laundry-orders/:id` | `deleteLaundryOrder` | Cancel or delete orders            |

### Example Requests and Responses

**POST `/laundry-orders`**

Request:

```http
POST /laundry-orders
Content-Type: application/json

{
  "customer": "John Doe",
  "laundry_weight": 5.0
}
```

Response:

```json
{
  "status": 201,
  "data": {
    "id": 1,
    "customer": "John Doe",
    "laundry_weight": 5.0
  },
  "error": null
}
```

**GET `/laundry-orders`**

Request:

```http
GET /laundry-orders
```

Response:

```json
{
  "status": 200,
  "data": [
    {
      "id": 1,
      "customer": "John Doe",
      "laundry_weight": 5.0
    }
  ],
  "error": null
}
```

**GET `/laundry-orders/1`**

Request:

```http
GET /laundry-orders/1
```

Response:

```json
{
  "status": 200,
  "data": {
    "id": 1,
    "customer": "John Doe",
    "laundry_weight": 5.0
  },
  "error": null
}
```

**PUT `/laundry-orders/1`**

Request:

```http
PUT /laundry-orders/1
Content-Type: application/json

{
  "customer": "John Doe",
  "laundry_weight": 6.5
}
```

Response:

```json
{
  "status": 200,
  "data": {
    "id": 1,
    "customer": "John Doe",
    "laundry_weight": 6.5
  },
  "error": null
}
```

**DELETE `/laundry-orders/1`**

Request:

```http
DELETE /laundry-orders/1
```

Response:

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

## Pickup Schedules Module

| Method | Path                    | Handler                | Story it serves             |
| ------ | ----------------------- | ---------------------- | --------------------------- |
| POST   | `/pickup-schedules`     | `createPickupSchedule` | Schedule a pickup request   |
| GET    | `/pickup-schedules`     | `listPickupSchedules`  | View pickup schedules       |
| GET    | `/pickup-schedules/:id` | `showPickupSchedule`   | View a pickup schedule      |
| PUT    | `/pickup-schedules/:id` | `updatePickupSchedule` | Modify pickup date and time |
| DELETE | `/pickup-schedules/:id` | `deletePickupSchedule` | Cancel pickup requests      |

### Example Requests and Responses

**POST `/pickup-schedules`**

Request:

```http
POST /pickup-schedules
Content-Type: application/json

{
  "customer": "John Doe",
  "pickup_date": "2026-08-26"
}
```

Response:

```json
{
  "status": 201,
  "data": {
    "id": 1,
    "customer": "John Doe",
    "pickup_date": "2026-08-26"
  },
  "error": null
}
```

**GET `/pickup-schedules`**

Request:

```http
GET /pickup-schedules
```

Response:

```json
{
  "status": 200,
  "data": [
    {
      "id": 1,
      "customer": "John Doe",
      "pickup_date": "2026-08-26"
    }
  ],
  "error": null
}
```

**GET `/pickup-schedules/1`**

Request:

```http
GET /pickup-schedules/1
```

Response:

```json
{
  "status": 200,
  "data": {
    "id": 1,
    "customer": "John Doe",
    "pickup_date": "2026-08-26"
  },
  "error": null
}
```

**PUT `/pickup-schedules/1`**

Request:

```http
PUT /pickup-schedules/1
Content-Type: application/json

{
  "customer": "John Doe",
  "pickup_date": "2026-08-27"
}
```

Response:

```json
{
  "status": 200,
  "data": {
    "id": 1,
    "customer": "John Doe",
    "pickup_date": "2026-08-27"
  },
  "error": null
}
```

**DELETE `/pickup-schedules/1`**

Request:

```http
DELETE /pickup-schedules/1
```

Response:

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

## Delivery Records Module

| Method | Path                    | Handler                | Story it serves             |
| ------ | ----------------------- | ---------------------- | --------------------------- |
| POST   | `/delivery-records`     | `createDeliveryRecord` | Create delivery records     |
| GET    | `/delivery-records`     | `listDeliveryRecords`  | View delivery status        |
| GET    | `/delivery-records/:id` | `showDeliveryRecord`   | View a delivery record      |
| PUT    | `/delivery-records/:id` | `updateDeliveryRecord` | Update delivery information |
| DELETE | `/delivery-records/:id` | `deleteDeliveryRecord` | Delete delivery records     |

### Example Requests and Responses

**POST `/delivery-records`**

Request:

```http
POST /delivery-records
Content-Type: application/json

{
  "customer": "John Doe",
  "delivery_date": "2026-08-28"
}
```

Response:

```json
{
  "status": 201,
  "data": {
    "id": 1,
    "customer": "John Doe",
    "delivery_date": "2026-08-28"
  },
  "error": null
}
```

**GET `/delivery-records`**

Request:

```http
GET /delivery-records
```

Response:

```json
{
  "status": 200,
  "data": [
    {
      "id": 1,
      "customer": "John Doe",
      "delivery_date": "2026-08-28"
    }
  ],
  "error": null
}
```

**GET `/delivery-records/1`**

Request:

```http
GET /delivery-records/1
```

Response:

```json
{
  "status": 200,
  "data": {
    "id": 1,
    "customer": "John Doe",
    "delivery_date": "2026-08-28"
  },
  "error": null
}
```

**PUT `/delivery-records/1`**

Request:

```http
PUT /delivery-records/1
Content-Type: application/json

{
  "customer": "John Doe",
  "delivery_date": "2026-08-29"
}
```

Response:

```json
{
  "status": 200,
  "data": {
    "id": 1,
    "customer": "John Doe",
    "delivery_date": "2026-08-29"
  },
  "error": null
}
```

**DELETE `/delivery-records/1`**

Request:

```http
DELETE /delivery-records/1
```

Response:

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

## Payment Module

| Method | Path            | Handler         | Story it serves          |
| ------ | --------------- | --------------- | ------------------------ |
| POST   | `/payments`     | `createPayment` | Add payment transactions |
| GET    | `/payments`     | `listPayments`  | View payment history     |
| GET    | `/payments/:id` | `showPayment`   | View a payment record    |
| PUT    | `/payments/:id` | `updatePayment` | Update payment status    |
| DELETE | `/payments/:id` | `deletePayment` | Delete payment records   |

### Example Requests and Responses

**POST `/payments`**

Request:

```http
POST /payments
Content-Type: application/json

{
  "customer": "John Doe",
  "payment_amount": 100.0,
  "payment_method": "Cash"
}
```

Response:

```json
{
  "status": 201,
  "data": {
    "id": 1,
    "customer": "John Doe",
    "payment_amount": 100.0,
    "payment_method": "Cash",
    "transaction_time": "2026-08-26 14:30:00"
  },
  "error": null
}
```

**GET `/payments`**

Request:

```http
GET /payments
```

Response:

```json
{
  "status": 200,
  "data": [
    {
      "id": 1,
      "customer": "John Doe",
      "payment_amount": 100.0,
      "payment_method": "Cash",
      "transaction_time": "2026-08-26 14:30:00"
    }
  ],
  "error": null
}
```

**GET `/payments/1`**

Request:

```http
GET /payments/1
```

Response:

```json
{
  "status": 200,
  "data": {
    "id": 1,
    "customer": "John Doe",
    "payment_amount": 100.0,
    "payment_method": "Cash",
    "transaction_time": "2026-08-26 14:30:00"
  },
  "error": null
}
```

**PUT `/payments/1`**

Request:

```http
PUT /payments/1
Content-Type: application/json

{
  "customer": "John Doe",
  "payment_amount": 150.0,
  "payment_method": "GCash"
}
```

Response:

```json
{
  "status": 200,
  "data": {
    "id": 1,
    "customer": "John Doe",
    "payment_amount": 150.0,
    "payment_method": "GCash"
  },
  "error": null
}
```

**DELETE `/payments/1`**

Request:

```http
DELETE /payments/1
```

Response:

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

## Response Format

All CRUD handlers use the same standardized response structure:

```json
{
  "status": 200,
  "data": {},
  "error": null
}
```

Create operations use HTTP status **201**. Read, update, and delete operations use **200** for successful responses.

---

## Route Testing Summary

All 25 routes were tested against the running Flask application at `http://127.0.0.1:5000`.

### Customer Module

| Method | Route | Actual Status | Result |
|---|---|---:|---|
| POST | `/customers` | 201 | PASS |
| GET | `/customers` | 200 | PASS |
| GET | `/customers/1` | 200 | PASS |
| PUT | `/customers/1` | 200 | PASS |
| DELETE | `/customers/1` | 200 | PASS |

### Laundry Orders Module

| Method | Route | Actual Status | Result |
|---|---|---:|---|
| POST | `/laundry-orders` | 201 | PASS |
| GET | `/laundry-orders` | 200 | PASS |
| GET | `/laundry-orders/1` | 200 | PASS |
| PUT | `/laundry-orders/1` | 200 | PASS |
| DELETE | `/laundry-orders/1` | 200 | PASS |

### Pickup Schedules Module

| Method | Route | Actual Status | Result |
|---|---|---:|---|
| POST | `/pickup-schedules` | 201 | PASS |
| GET | `/pickup-schedules` | 200 | PASS |
| GET | `/pickup-schedules/1` | 200 | PASS |
| PUT | `/pickup-schedules/1` | 200 | PASS |
| DELETE | `/pickup-schedules/1` | 200 | PASS |

### Delivery Records Module

| Method | Route | Actual Status | Result |
|---|---|---:|---|
| POST | `/delivery-records` | 201 | PASS |
| GET | `/delivery-records` | 200 | PASS |
| GET | `/delivery-records/1` | 200 | PASS |
| PUT | `/delivery-records/1` | 200 | PASS |
| DELETE | `/delivery-records/1` | 200 | PASS |

### Payment Module

| Method | Route | Actual Status | Result |
|---|---|---:|---|
| POST | `/payments` | 201 | PASS |
| GET | `/payments` | 200 | PASS |
| GET | `/payments/1` | 200 | PASS |
| PUT | `/payments/1` | 200 | PASS |
| DELETE | `/payments/1` | 200 | PASS |

### Wrong-Method Test

**Request:**

```http
DELETE /customers
```

**Response:**

```text
405 Method Not Allowed
```
