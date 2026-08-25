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
```

Response:

```json
{
  "status": 201,
  "data": {
    "message": "createCustomer stub"
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
  "data": {
    "message": "listCustomers stub"
  },
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
    "message": "showCustomer stub",
    "id": "1"
  },
  "error": null
}
```

**PUT `/customers/1`**

Request:

```http
PUT /customers/1
```

Response:

```json
{
  "status": 200,
  "data": {
    "message": "updateCustomer stub",
    "id": "1"
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
    "message": "deleteCustomer stub",
    "id": "1"
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

```json
{
  "status": 201,
  "data": {
    "message": "createLaundryOrder stub"
  },
  "error": null
}
```

**GET `/laundry-orders`**

```json
{
  "status": 200,
  "data": {
    "message": "listLaundryOrders stub"
  },
  "error": null
}
```

**GET `/laundry-orders/1`**

```json
{
  "status": 200,
  "data": {
    "message": "showLaundryOrder stub",
    "id": "1"
  },
  "error": null
}
```

**PUT `/laundry-orders/1`**

```json
{
  "status": 200,
  "data": {
    "message": "updateLaundryOrder stub",
    "id": "1"
  },
  "error": null
}
```

**DELETE `/laundry-orders/1`**

```json
{
  "status": 200,
  "data": {
    "message": "deleteLaundryOrder stub",
    "id": "1"
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

```json
{
  "status": 201,
  "data": {
    "message": "createPickupSchedule stub"
  },
  "error": null
}
```

**GET `/pickup-schedules`**

```json
{
  "status": 200,
  "data": {
    "message": "listPickupSchedules stub"
  },
  "error": null
}
```

**GET `/pickup-schedules/1`**

```json
{
  "status": 200,
  "data": {
    "message": "showPickupSchedule stub",
    "id": "1"
  },
  "error": null
}
```

**PUT `/pickup-schedules/1`**

```json
{
  "status": 200,
  "data": {
    "message": "updatePickupSchedule stub",
    "id": "1"
  },
  "error": null
}
```

**DELETE `/pickup-schedules/1`**

```json
{
  "status": 200,
  "data": {
    "message": "deletePickupSchedule stub",
    "id": "1"
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

```json
{
  "status": 201,
  "data": {
    "message": "createDeliveryRecord stub"
  },
  "error": null
}
```

**GET `/delivery-records`**

```json
{
  "status": 200,
  "data": {
    "message": "listDeliveryRecords stub"
  },
  "error": null
}
```

**GET `/delivery-records/1`**

```json
{
  "status": 200,
  "data": {
    "message": "showDeliveryRecord stub",
    "id": "1"
  },
  "error": null
}
```

**PUT `/delivery-records/1`**

```json
{
  "status": 200,
  "data": {
    "message": "updateDeliveryRecord stub",
    "id": "1"
  },
  "error": null
}
```

**DELETE `/delivery-records/1`**

```json
{
  "status": 200,
  "data": {
    "message": "deleteDeliveryRecord stub",
    "id": "1"
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

```json
{
  "status": 201,
  "data": {
    "message": "createPayment stub"
  },
  "error": null
}
```

**GET `/payments`**

```json
{
  "status": 200,
  "data": {
    "message": "listPayments stub"
  },
  "error": null
}
```

**GET `/payments/1`**

```json
{
  "status": 200,
  "data": {
    "message": "showPayment stub",
    "id": "1"
  },
  "error": null
}
```

**PUT `/payments/1`**

```json
{
  "status": 200,
  "data": {
    "message": "updatePayment stub",
    "id": "1"
  },
  "error": null
}
```

**DELETE `/payments/1`**

```json
{
  "status": 200,
  "data": {
    "message": "deletePayment stub",
    "id": "1"
  },
  "error": null
}
```

---

## Response Format

All stub handlers use the same response structure:

```json
{
  "status": 200,
  "data": {},
  "error": null
}
```

Create operations use HTTP status **201**. Read, update, and delete operations use **200** for the successful stub responses.

Route parameters such as `:id` are read and returned in the response.

---

## Week 3 Testing

Each route must be tested with a real request.

| Method | Example Path          | Expected Status |
| ------ | --------------------- | --------------- |
| POST   | `/customers`          | 201             |
| GET    | `/customers`          | 200             |
| GET    | `/customers/1`        | 200             |
| PUT    | `/customers/1`        | 200             |
| DELETE | `/customers/1`        | 200             |
| POST   | `/laundry-orders`     | 201             |
| GET    | `/laundry-orders`     | 200             |
| GET    | `/laundry-orders/1`   | 200             |
| PUT    | `/laundry-orders/1`   | 200             |
| DELETE | `/laundry-orders/1`   | 200             |
| POST   | `/pickup-schedules`   | 201             |
| GET    | `/pickup-schedules`   | 200             |
| GET    | `/pickup-schedules/1` | 200             |
| PUT    | `/pickup-schedules/1` | 200             |
| DELETE | `/pickup-schedules/1` | 200             |
| POST   | `/delivery-records`   | 201             |
| GET    | `/delivery-records`   | 200             |
| GET    | `/delivery-records/1` | 200             |
| PUT    | `/delivery-records/1` | 200             |
| DELETE | `/delivery-records/1` | 200             |
| POST   | `/payments`           | 201             |
| GET    | `/payments`           | 200             |
| GET    | `/payments/1`         | 200             |
| PUT    | `/payments/1`         | 200             |
| DELETE | `/payments/1`         | 200             |

The handout's required end result is a `routes.md` containing the **full routing table plus one example request/response per route**.

---

# Request / Response Examples
This document contains the routing table and example requests and responses for the Laundry Pickup and Delivery Management System.

The routes currently use stub handlers only. No database logic is implemented at this stage.

All routes were implemented as stub handlers for Week 3.
No database logic is included at this stage.

## Customer Module

### 1. Create Customer

**Request**

```http
POST /customers
{
  "status": 201,
  "data": {
    "message": "createCustomer stub"
  },
  "error": null
}

GET /customers

{
  "status": 200,
  "data": {
    "message": "listCustomers stub"
  },
  "error": null
}

GET /customers/1
{
  "status": 200,
  "data": {
    "message": "showCustomer stub",
    "id": "1"
  },
  "error": null
}

PUT /customers/1

{
  "status": 200,
  "data": {
    "message": "updateCustomer stub",
    "id": "1"
  },
  "error": null
}

DELETE /customers/1
{
  "status": 200,
  "data": {
    "message": "deleteCustomer stub",
    "id": "1"
  },
  "error": null
}


### Why we're doing this

Your routing table tells the instructor **what routes exist**. This section shows **what happens when those routes are called**.

The handout specifically requires the routes to be tested and the request/response examples to be documented in `docs/routes.md`. :contentReference[oaicite:0]{index=0}

**For now, only add the Customer section above.**

When you've pasted it into `routes.md`, tell me **`done`** and I'll give you the **Laundry Orders section next**, in the same specific format.

---

## Laundry Orders Module

### 1. Create Laundry Order

**Request**

```http
POST /laundry-orders

{
  "status": 201,
  "data": {
    "message": "createLaundryOrder stub"
  },
  "error": null
}

GET /laundry-orders
{
  "status": 200,
  "data": {
    "message": "listLaundryOrders stub"
  },
  "error": null
}
GET /laundry-orders/1
{
  "status": 200,
  "data": {
    "message": "showLaundryOrder stub",
    "id": "1"
  },
  "error": null
}
PUT /laundry-orders/1
{
  "status": 200,
  "data": {
    "message": "updateLaundryOrder stub",
    "id": "1"
  },
  "error": null
}
DELETE /laundry-orders/1
{
  "status": 200,
  "data": {
    "message": "deleteLaundryOrder stub",
    "id": "1"
  },
  "error": null
}


### Your `routes.md` should now contain

```text
Routing Table
     ↓
Customer Module
     ↓
Laundry Orders Module

---

## Pickup Schedules Module

### 1. Create Pickup Schedule

**Request**

```http
POST /pickup-schedules

{
  "status": 201,
  "data": {
    "message": "createPickupSchedule stub"
  },
  "error": null
}

GET /pickup-schedules

{
  "status": 200,
  "data": {
    "message": "listPickupSchedules stub"
  },
  "error": null
}

GET /pickup-schedules/1
{
  "status": 200,
  "data": {
    "message": "showPickupSchedule stub",
    "id": "1"
  },
  "error": null
}
PUT /pickup-schedules/1

{
  "status": 200,
  "data": {
    "message": "updatePickupSchedule stub",
    "id": "1"
  },
  "error": null
}
DELETE /pickup-schedules/1
{
  "status": 200,
  "data": {
    "message": "deletePickupSchedule stub",
    "id": "1"
  },
  "error": null
}


### Your `routes.md` progress

You should now have:

```text
routes.md
│
├── Routing Table
│
├── Customer Module
│   ├── Create
│   ├── Read List
│   ├── Read Details
│   ├── Update
│   └── Delete
│
├── Laundry Orders Module
│   ├── Create
│   ├── Read List
│   ├── Read Details
│   ├── Update
│   └── Delete
│
└── Pickup Schedules Module
    ├── Create
    ├── Read List
    ├── Read Details
    ├── Update
    └── Delete  

---

## Delivery Records Module

### 1. Create Delivery Record

**Request**

```http
POST /delivery-records

{
  "status": 201,
  "data": {
    "message": "createDeliveryRecord stub"
  },
  "error": null
}

GET /delivery-records

{
  "status": 200,
  "data": {
    "message": "listDeliveryRecords stub"
  },
  "error": null
}
GET /delivery-records/1
{
  "status": 200,
  "data": {
    "message": "showDeliveryRecord stub",
    "id": "1"
  },
  "error": null
}
PUT /delivery-records/1
{
  "status": 200,
  "data": {
    "message": "updateDeliveryRecord stub",
    "id": "1"
  },
  "error": null
}
DELETE /delivery-records/1
{
  "status": 200,
  "data": {
    "message": "deleteDeliveryRecord stub",
    "id": "1"
  },
  "error": null
}


### Your `routes.md` now has 4 modules

```text
Routing Table
    ↓
Customer Module
    ↓
Laundry Orders Module
    ↓
Pickup Schedules Module
    ↓
Delivery Records Module

---

## Payment Module

### 1. Create Payment

**Request**

```http
POST /payments
{
  "status": 201,
  "data": {
    "message": "createPayment stub"
  },
  "error": null
}

GET /payments
{
  "status": 200,
  "data": {
    "message": "listPayments stub"
  },
  "error": null
}
GET /payments/1
{
  "status": 200,
  "data": {
    "message": "showPayment stub",
    "id": "1"
  },
  "error": null
}
PUT /payments/1

{
  "status": 200,
  "data": {
    "message": "updatePayment stub",
    "id": "1"
  },
  "error": null
}

DELETE /payments/1

{
  "status": 200,
  "data": {
    "message": "deletePayment stub",
    "id": "1"
  },
  "error": null
}


### Your `routes.md` should now contain all 5 modules

```text
docs/
└── routes.md
    ├── Routing Table
    ├── Customer Module          5 routes
    ├── Laundry Orders Module    5 routes
    ├── Pickup Schedules Module  5 routes
    ├── Delivery Records Module  5 routes
    └── Payment Module           5 routes
                                  ─────
                                  25 routes
