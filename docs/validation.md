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
| laundry_weight | Yes | Must be greater than zero |

### PUT /laundry-orders/:id

| Field | Required | Validation Rule |
|---|---|---|
| customer | Yes | Customer must be selected |
| laundry_weight | Yes | Must be greater than zero |

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

## Payment Module

### POST /payments

| Field | Required | Validation Rule |
|---|---|---|
| payment_amount | Yes | Must not be blank |
| payment_method | Yes | Must be selected |

### PUT /payments/:id

| Field | Required | Validation Rule |
|---|---|---|
| payment_amount | Yes | Must not be blank |
| payment_method | Yes | Must be selected |

## Delivery Module

Delivery validation rules will be added after the Delivery Module requirements are provided.

## Standard Validation Response

Invalid input must return HTTP 422 with the following structure:

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

## Customer Validation Test Evidence

### POST /customers — Missing Fields

**Request**

```json
{}

### POST /customers — Missing Contact Number

Request:

```json
{
  "name": "John Doe"
}

### POST /customers — Missing Name

Request:

```json
{
  "contact_number": "09123456789"
}

### POST /customers — Valid Data

Request:

```json
{
  "name": "John Doe",
  "contact_number": "09123456789"
}

### PUT /customers/1 — Missing Fields

Request:

```json
{}

### PUT /customers/1 — Valid Data

Request:

```json
{
  "name": "John Doe",
  "contact_number": "09123456789"
}

## Laundry Orders Validation Test Evidence

### POST /laundry-orders — Missing Fields

Request:

```json
{}

### POST /laundry-orders — Zero Laundry Weight

Request:

```json
{
  "customer": "1",
  "laundry_weight": 0
}

### POST /laundry-orders — Invalid Laundry Weight Type

Request:

```json
{
  "customer": "1",
  "laundry_weight": "abc"
}

### POST /laundry-orders — Valid Data

Request:

```json
{
  "customer": "1",
  "laundry_weight": 5
}

### PUT /laundry-orders/1 — Missing Fields

Request:

```json
{}

{
  "customer": "1",
  "laundry_weight": 0
}

{
  "customer": "1",
  "laundry_weight": "abc"
}
{
  "customer": "1",
  "laundry_weight": 5
}

## Pickup Validation Test Evidence

### POST /pickup-schedules — Missing Fields

Request:

```json
{}

{
  "pickup_date": "2026-08-26"
}

{
  "pickup_date": "2026-08-26",
  "customer": "1"
}

### PUT /pickup-schedules/1 — Missing Fields

Request:

```json
{}

{
  "pickup_date": "2026-08-26"
}

{
  "pickup_date": "2026-08-26",
  "customer": "1"
}

## Delivery Validation Test Evidence

### POST /delivery-records — Missing Fields

Request:

```json
{}

{
  "delivery_date": "2026-08-26"
}

{
  "delivery_date": "2026-08-26",
  "customer": "1"
}   

### PUT /delivery-records/1 — Missing Fields

Request:

```json
{}

{
  "delivery_date": "2026-08-26"
}

{
  "delivery_date": "2026-08-26",
  "customer": "1"
}

## Payment Validation Test Evidence

### POST /payments — Missing Fields

Request:

```json
{}

{
  "payment_amount": 0,
  "payment_method": "Cash"
}

{
  "payment_amount": "abc",
  "payment_method": "Cash"
}

{
  "payment_amount": 100
}

{
  "payment_amount": 100,
  "payment_method": "Cash"
}

### PUT /payments/1 — Missing Fields

Request:

```json
{}

{
  "payment_amount": 0,
  "payment_method": "Cash"
}

{
  "payment_amount": "abc",
  "payment_method": "Cash"
}

{
  "payment_amount": 100,
  "payment_method": "Cash"
}

## Week 5 CRUD Route Test Evidence

### DELETE Route Tests

#### DELETE /customers/1

Expected Result: `200`

Result: Passed. The Customer DELETE endpoint returned a successful response.

#### DELETE /laundry-orders/1

Expected Result: `200`

Result: Passed. The Laundry Order DELETE endpoint returned a successful response.

#### DELETE /pickup-schedules/1

Expected Result: `200`

Result: Passed. The Pickup DELETE endpoint returned a successful response.

#### DELETE /delivery-records/1

Expected Result: `200`

Result: Passed. The Delivery DELETE endpoint returned a successful response.

#### DELETE /payments/1

Expected Result: `200`

Result: Passed. The Payment DELETE endpoint returned a successful response.

---

### GET Route Tests

The GET list and GET details endpoints were tested for all five modules.

| Module | GET List | GET Details |
|---|---|---|
| Customer | Passed | Passed |
| Laundry Orders | Passed | Passed |
| Pickup | Passed | Passed |
| Delivery | Passed | Passed |
| Payment | Passed | Passed |

Expected Result: `200`

Result: Passed. All GET list and detail endpoints returned successful responses.

---

### Invalid GET ID Tests

The following nonexistent record IDs were tested using ID `99999`:

- `GET /customers/99999`
- `GET /laundry-orders/99999`
- `GET /pickup-schedules/99999`
- `GET /delivery-records/99999`
- `GET /payments/99999`

Expected Result: `404`

Result: Passed. All five endpoints correctly returned a not-found response for nonexistent records.

## Week 5 Wrong HTTP Method Test Evidence

### DELETE /customers

Request:

```http
DELETE /customers

DELETE /laundry-orders

DELETE /pickup-schedules

DELETE /delivery-records

DELETE /payments

