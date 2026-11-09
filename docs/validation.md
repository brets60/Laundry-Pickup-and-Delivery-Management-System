# Week 4 Validation Matrix

This document defines the validation rules for the create and update routes of the Laundry Pickup and Delivery Management System.

## Customer Module

### POST /customers

| Field | Required | Validation Rule |
|---|---|---|
| name | Yes | Must not be blank |
| contact_number | Yes | Must not be blank |

### PUT /customers/:id

| Field | Required | Validation Rule |
|---|---|---|
| name | Yes | Must not be blank |
| contact_number | Yes | Must not be blank |

## Laundry Orders Module

### POST /laundry-orders

| Field | Required | Validation Rule |
|---|---|---|
| customer | Yes | Customer must be selected |
| laundry_weight | Yes | Must be a number greater than zero |

### PUT /laundry-orders/:id

| Field | Required | Validation Rule |
|---|---|---|
| customer | Yes | Customer must be selected |
| laundry_weight | Yes | Must be a number greater than zero |

## Pickup Module

### POST /pickup-schedules

| Field | Required | Validation Rule |
|---|---|---|
| pickup_date | Yes | Must not be blank |
| customer | Yes | Customer must be selected |

### PUT /pickup-schedules/:id

| Field | Required | Validation Rule |
|---|---|---|
| pickup_date | Yes | Must not be blank |
| customer | Yes | Customer must be selected |

## Delivery Module

### POST /delivery-records

| Field | Required | Validation Rule |
|---|---|---|
| delivery_date | Yes | Must not be blank |
| customer | Yes | Customer must be selected |

### PUT /delivery-records/:id

| Field | Required | Validation Rule |
|---|---|---|
| delivery_date | Yes | Must not be blank |
| customer | Yes | Customer must be selected |

## Payment Module

### POST /payments

| Field | Required | Validation Rule |
|---|---|---|
| customer | Yes | Customer must be selected |
| payment_amount | Yes | Must be a number greater than zero |
| payment_method | Yes | Must be selected |

### PUT /payments/:id

| Field | Required | Validation Rule |
|---|---|---|
| customer | Yes | Customer must be selected |
| payment_amount | Yes | Must be a number greater than zero |
| payment_method | Yes | Must be selected |

## Standard Validation Response

Invalid input returns HTTP 422 with the following structure:

```json
{
  "status": 422,
  "data": null,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Validation failed.",
    "fields": {}
  }
}
```

## Customer Validation Test Evidence

### POST /customers — Missing Fields

Request:

```json
{}
```

Response (`422`):

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

### POST /customers — Missing Contact Number

Request:

```json
{
  "name": "John Doe"
}
```

Response (`422`):

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

### POST /customers — Missing Name

Request:

```json
{
  "contact_number": "09123456789"
}
```

Response (`422`):

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

### POST /customers — Valid Data

Request:

```json
{
  "name": "John Doe",
  "contact_number": "09123456789"
}
```

Response (`201`):

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

### PUT /customers/1 — Missing Fields

Request:

```json
{}
```

Response (`422`):

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

### PUT /customers/1 — Valid Data

Request:

```json
{
  "name": "John Doe",
  "contact_number": "09123456789"
}
```

Response (`200`):

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

## Laundry Orders Validation Test Evidence

### POST /laundry-orders — Missing Fields

Request:

```json
{}
```

Response (`422`):

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

### POST /laundry-orders — Zero Laundry Weight

Request:

```json
{
  "customer": "John Doe",
  "laundry_weight": 0
}
```

Response (`422`):

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

### POST /laundry-orders — Invalid Laundry Weight Type

Request:

```json
{
  "customer": "John Doe",
  "laundry_weight": "abc"
}
```

Response (`422`):

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

### POST /laundry-orders — Valid Data

Request:

```json
{
  "customer": "John Doe",
  "laundry_weight": 5
}
```

Response (`201`):

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

### PUT /laundry-orders/1 — Missing Fields

Request:

```json
{}
```

Response (`422`):

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

## Pickup Validation Test Evidence

### POST /pickup-schedules — Missing Fields

Request:

```json
{}
```

Response (`422`):

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

### POST /pickup-schedules — Valid Data

Request:

```json
{
  "pickup_date": "2026-08-26",
  "customer": "John Doe"
}
```

Response (`201`):

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

### PUT /pickup-schedules/1 — Missing Fields

Request:

```json
{}
```

Response (`422`):

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

## Delivery Validation Test Evidence

### POST /delivery-records — Missing Fields

Request:

```json
{}
```

Response (`422`):

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

### POST /delivery-records — Valid Data

Request:

```json
{
  "delivery_date": "2026-08-26",
  "customer": "John Doe"
}
```

Response (`201`):

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

### PUT /delivery-records/1 — Missing Fields

Request:

```json
{}
```

Response (`422`):

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

## Payment Validation Test Evidence

### POST /payments — Missing Fields

Request:

```json
{}
```

Response (`422`):

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

### POST /payments — Zero or Invalid Payment Amount

Request:

```json
{
  "customer": "John Doe",
  "payment_amount": 0,
  "payment_method": "Cash"
}
```

Response (`422`):

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

### POST /payments — Valid Data

Request:

```json
{
  "customer": "John Doe",
  "payment_amount": 100,
  "payment_method": "Cash"
}
```

Response (`201`):

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

### PUT /payments/1 — Missing Fields

Request:

```json
{}
```

Response (`422`):

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

## Week 5 CRUD Route Test Evidence

### DELETE Route Tests

- `DELETE /customers/1` -> `200 OK` (Passed)
- `DELETE /laundry-orders/1` -> `200 OK` (Passed)
- `DELETE /pickup-schedules/1` -> `200 OK` (Passed)
- `DELETE /delivery-records/1` -> `200 OK` (Passed)
- `DELETE /payments/1` -> `200 OK` (Passed)

### GET Route Tests

| Module | GET List | GET Details |
|---|---|---|
| Customer | Passed (`200`) | Passed (`200`) |
| Laundry Orders | Passed (`200`) | Passed (`200`) |
| Pickup | Passed (`200`) | Passed (`200`) |
| Delivery | Passed (`200`) | Passed (`200`) |
| Payment | Passed (`200`) | Passed (`200`) |

### Invalid GET ID Tests (`404`)

The following nonexistent record IDs were tested using ID `99999`:

- `GET /customers/99999` -> `404 Not Found` (Passed)
- `GET /laundry-orders/99999` -> `404 Not Found` (Passed)
- `GET /pickup-schedules/99999` -> `404 Not Found` (Passed)
- `GET /delivery-records/99999` -> `404 Not Found` (Passed)
- `GET /payments/99999` -> `404 Not Found` (Passed)

## Week 5 Wrong HTTP Method Test Evidence (`405`)

```http
DELETE /customers
DELETE /laundry-orders
DELETE /pickup-schedules
DELETE /delivery-records
DELETE /payments
```

Expected Result: `405 Method Not Allowed` — Passed.
