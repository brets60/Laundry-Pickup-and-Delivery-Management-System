# Input Validation Rules & Guard-Clause Specification (`docs/validation.md`)

**Project:** Laundry Pickup and Delivery Management System (`LaundryCare`)  
**Milestone:** Deliverable 2 — Routing, Logic & Tests (Weeks 3–5 · Phase 2)

This document defines the guard-clause input validation rules defending every create (`POST`) and update (`PUT`) route in the Laundry Pickup and Delivery Management System. Validation logic is isolated in [`controllers/validators.py`](../controllers/validators.py) so that malformed, empty, or out-of-range payloads are rejected with a standardized `422 Unprocessable Entity` JSON envelope before reaching controller persistence logic—never resulting in a `500 Internal Server Error`.

---

## Standardized HTTP 422 Validation Error Envelope

Whenever one or more validation rules fail on a `POST` or `PUT` request, the validator halts execution and returns HTTP `422 Unprocessable Entity`:

```json
{
  "status": 422,
  "data": null,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Validation failed.",
    "fields": {
      "field_name": "Human-readable validation message."
    }
  }
}
```

---

## 1. Customer Module Validation Rules (`validate_customer_payload`)

### `POST /customers` & `PUT /customers/:id`

| Field | Type | Required | Guard-Clause Rule | Error Message (`422`) |
|---|---|:---:|---|---|
| `name` | `string` | Yes | Must be present and non-blank after `.strip()` | `"Name is required."` |
| `contact_number` | `string` | Yes | Must be present and non-blank after `.strip()` | `"Contact number is required."` |

### Customer Validation Test Evidence

#### `POST /customers` — Missing All Fields (`422`)

**Request:**

```json
{}
```

**Response (`422 Unprocessable Entity`):**

```json
{
  "status": 422,
  "data": null,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Validation failed.",
    "fields": {
      "name": "Name is required.",
      "contact_number": "Contact number is required."
    }
  }
}
```

#### `POST /customers` — Missing Contact Number (`422`)

**Request:**

```json
{
  "name": "John Doe"
}
```

**Response (`422 Unprocessable Entity`):**

```json
{
  "status": 422,
  "data": null,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Validation failed.",
    "fields": {
      "contact_number": "Contact number is required."
    }
  }
}
```

#### `POST /customers` — Missing Name (`422`)

**Request:**

```json
{
  "contact_number": "09123456789"
}
```

**Response (`422 Unprocessable Entity`):**

```json
{
  "status": 422,
  "data": null,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Validation failed.",
    "fields": {
      "name": "Name is required."
    }
  }
}
```

#### `POST /customers` & `PUT /customers/1` — Valid Data (`201` / `200`)

**Request:**

```json
{
  "name": "John Doe",
  "contact_number": "09123456789"
}
```

**Response (`201 Created` on `POST`, `200 OK` on `PUT`):**

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

---

## 2. Laundry Orders Module Validation Rules (`validate_laundry_order_payload`)

### `POST /laundry-orders` & `PUT /laundry-orders/:id`

| Field | Type | Required | Guard-Clause Rule | Error Message (`422`) |
|---|---|:---:|---|---|
| `customer` | `string` | Yes | Must be present and non-blank; on `POST`, customer must exist | `"Customer is required."` |
| `laundry_weight` | `number` | Yes | Must be present, numeric (not boolean/string), and `> 0` | `"Laundry weight is required."` / `"Laundry weight must be a number."` / `"Laundry weight must be greater than zero."` |

### Laundry Orders Validation Test Evidence

#### `POST /laundry-orders` — Missing Fields (`422`)

**Request:**

```json
{}
```

**Response (`422 Unprocessable Entity`):**

```json
{
  "status": 422,
  "data": null,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Validation failed.",
    "fields": {
      "customer": "Customer is required.",
      "laundry_weight": "Laundry weight is required."
    }
  }
}
```

#### `POST /laundry-orders` — Zero or Negative Laundry Weight (`422`)

**Request:**

```json
{
  "customer": "John Doe",
  "laundry_weight": 0
}
```

**Response (`422 Unprocessable Entity`):**

```json
{
  "status": 422,
  "data": null,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Validation failed.",
    "fields": {
      "laundry_weight": "Laundry weight must be greater than zero."
    }
  }
}
```

#### `POST /laundry-orders` — Non-Numeric Laundry Weight (`422`)

**Request:**

```json
{
  "customer": "John Doe",
  "laundry_weight": "abc"
}
```

**Response (`422 Unprocessable Entity`):**

```json
{
  "status": 422,
  "data": null,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Validation failed.",
    "fields": {
      "laundry_weight": "Laundry weight must be a number."
    }
  }
}
```

#### `POST /laundry-orders` & `PUT /laundry-orders/1` — Valid Data (`201` / `200`)

**Request:**

```json
{
  "customer": "John Doe",
  "laundry_weight": 5
}
```

**Response (`201 Created` on `POST`, `200 OK` on `PUT`):**

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

---

## 3. Pickup Schedules Module Validation Rules (`validate_pickup_schedule_payload`)

### `POST /pickup-schedules` & `PUT /pickup-schedules/:id`

| Field | Type | Required | Guard-Clause Rule | Error Message (`422`) |
|---|---|:---:|---|---|
| `pickup_date` | `string` | Yes | Must be present and non-blank after `.strip()` | `"Pickup date is required."` |
| `customer` | `string` | Yes | Must be present and non-blank; on `POST`, customer must exist | `"Customer is required."` |

### Pickup Validation Test Evidence

#### `POST /pickup-schedules` & `PUT /pickup-schedules/1` — Missing Fields (`422`)

**Request:**

```json
{}
```

**Response (`422 Unprocessable Entity`):**

```json
{
  "status": 422,
  "data": null,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Validation failed.",
    "fields": {
      "pickup_date": "Pickup date is required.",
      "customer": "Customer is required."
    }
  }
}
```

#### `POST /pickup-schedules` — Missing Customer (`422`)

**Request:**

```json
{
  "pickup_date": "2026-08-26"
}
```

**Response (`422 Unprocessable Entity`):**

```json
{
  "status": 422,
  "data": null,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Validation failed.",
    "fields": {
      "customer": "Customer is required."
    }
  }
}
```

#### `POST /pickup-schedules` & `PUT /pickup-schedules/1` — Valid Data (`201` / `200`)

**Request:**

```json
{
  "pickup_date": "2026-08-26",
  "customer": "John Doe"
}
```

**Response (`201 Created` on `POST`, `200 OK` on `PUT`):**

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

---

## 4. Delivery Records Module Validation Rules (`validate_delivery_record_payload`)

### `POST /delivery-records` & `PUT /delivery-records/:id`

| Field | Type | Required | Guard-Clause Rule | Error Message (`422`) |
|---|---|:---:|---|---|
| `delivery_date` | `string` | Yes | Must be present and non-blank after `.strip()` | `"Delivery date is required."` |
| `customer` | `string` | Yes | Must be present and non-blank; on `POST`, customer must exist | `"Customer is required."` |

### Delivery Validation Test Evidence

#### `POST /delivery-records` & `PUT /delivery-records/1` — Missing Fields (`422`)

**Request:**

```json
{}
```

**Response (`422 Unprocessable Entity`):**

```json
{
  "status": 422,
  "data": null,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Validation failed.",
    "fields": {
      "delivery_date": "Delivery date is required.",
      "customer": "Customer is required."
    }
  }
}
```

#### `POST /delivery-records` — Missing Customer (`422`)

**Request:**

```json
{
  "delivery_date": "2026-08-26"
}
```

**Response (`422 Unprocessable Entity`):**

```json
{
  "status": 422,
  "data": null,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Validation failed.",
    "fields": {
      "customer": "Customer is required."
    }
  }
}
```

#### `POST /delivery-records` & `PUT /delivery-records/1` — Valid Data (`201` / `200`)

**Request:**

```json
{
  "delivery_date": "2026-08-26",
  "customer": "John Doe"
}
```

**Response (`201 Created` on `POST`, `200 OK` on `PUT`):**

```json
{
  "status": 201,
  "data": {
    "id": 1,
    "customer": "John Doe",
    "delivery_date": "2026-08-26"
  },
  "error": null
}
```

---

## 5. Payment Module Validation Rules (`validate_payment_payload`)

### `POST /payments` & `PUT /payments/:id`

| Field | Type | Required | Guard-Clause Rule | Error Message (`422`) |
|---|---|:---:|---|---|
| `customer` | `string` | Yes | Must be present and non-blank after `.strip()` | `"Customer is required."` |
| `payment_amount` | `number` | Yes | Must be present, numeric (not boolean/string), and `> 0` | `"Payment amount is required."` / `"Payment amount must be a number."` / `"Payment amount must be greater than zero."` |
| `payment_method` | `string` | Yes | Must be present and non-blank after `.strip()` | `"Payment method is required."` |

### Payment Validation Test Evidence

#### `POST /payments` & `PUT /payments/1` — Missing All Fields (`422`)

**Request:**

```json
{}
```

**Response (`422 Unprocessable Entity`):**

```json
{
  "status": 422,
  "data": null,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Validation failed.",
    "fields": {
      "customer": "Customer is required.",
      "payment_amount": "Payment amount is required.",
      "payment_method": "Payment method is required."
    }
  }
}
```

#### `POST /payments` — Zero or Negative Payment Amount (`422`)

**Request:**

```json
{
  "customer": "John Doe",
  "payment_amount": 0,
  "payment_method": "Cash"
}
```

**Response (`422 Unprocessable Entity`):**

```json
{
  "status": 422,
  "data": null,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Validation failed.",
    "fields": {
      "payment_amount": "Payment amount must be greater than zero."
    }
  }
}
```

#### `POST /payments` — Invalid Payment Amount Type (`422`)

**Request:**

```json
{
  "customer": "John Doe",
  "payment_amount": "abc",
  "payment_method": "Cash"
}
```

**Response (`422 Unprocessable Entity`):**

```json
{
  "status": 422,
  "data": null,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Validation failed.",
    "fields": {
      "payment_amount": "Payment amount must be a number."
    }
  }
}
```

#### `POST /payments` & `PUT /payments/1` — Valid Data (`201` / `200`)

**Request:**

```json
{
  "customer": "John Doe",
  "payment_amount": 100,
  "payment_method": "Cash"
}
```

**Response (`201 Created` on `POST`, `200 OK` on `PUT`):**

```json
{
  "status": 201,
  "data": {
    "id": 1,
    "customer": "John Doe",
    "payment_amount": 100.0,
    "payment_method": "Cash",
    "transaction_time": "2026-08-26 15:00:00"
  },
  "error": null
}
```

---

## Week 5 CRUD & Edge-Case Verification Summary

| Test Category | Endpoints Covered | Expected HTTP Status | Result |
|---|---|:---:|:---:|
| **Create (`POST`) — Valid Payload** | `/customers`, `/laundry-orders`, `/pickup-schedules`, `/delivery-records`, `/payments` | `201 Created` | **PASS** |
| **Create/Update (`POST`/`PUT`) — Invalid/Missing/Blank Input** | All 10 Create & Update routes | `422 Unprocessable Entity` | **PASS** |
| **Read List & Details (`GET`) — Existing Records** | All 10 Read routes | `200 OK` | **PASS** |
| **Update (`PUT`) — Valid Payload on Existing ID** | All 5 Update routes | `200 OK` | **PASS** |
| **Delete (`DELETE`) — Existing ID** | All 5 Delete routes | `200 OK` | **PASS** |
| **Missing Record ID (`99999`) on `GET`, `PUT`, `DELETE`** | All 15 `:id` routes | `404 Not Found` | **PASS** |
| **Wrong HTTP Method on Collection (`DELETE /customers`, etc.)** | All 5 Collection routes | `405 Method Not Allowed` | **PASS** |
