# Deliverable 2 — Live AI-Off Checkpoint Guide & Solo Route-Building Playbook

> **Why This Matters (18/50 Individual Points — Mandatory Pass Gate):**  
> During the **Deliverable 2 Live AI-Off Checkpoint**, the instructor observes each team member **solo** (with AI turned off) as they either **build a CRUD route from scratch**, **fix a broken route/validator**, or **write a passing `pytest` test**. A student cannot pass the individual half of Deliverable 2 on Git commits alone without completing this live checkpoint.

---

## 1. The Universal 4-Step Pattern to Memorize

Every route in `LaundryCare` follows the exact same 4-step pipeline:
1. **Read Request JSON:** `data = request.get_json(silent=True) or {}`
2. **Guard-Clause Validation:** Validate required fields and numeric ranges first; if invalid, immediately return `422 Unprocessable Entity`.
3. **Database & `404` Check:** Query SQLite via `get_db_connection()`; if `:id` does not exist, close the connection and return `404 Not Found`.
4. **Return Standardized Success Envelope:** Return `201 Created` on `POST` or `200 OK` on `GET`, `PUT`, and `DELETE`.

### Memorize These 3 Standard JSON Envelopes

#### A. Success Envelope (`201 Created` for `POST`, `200 OK` for `GET` / `PUT` / `DELETE`)
```python
return jsonify({
    "status": 201,          # Use 201 for POST, 200 for GET / PUT / DELETE
    "data": { ... },        # Dictionary (or list of dicts) of the record
    "error": None
}), 201
```

#### B. Validation Error Envelope (`422 Unprocessable Entity` — Guard Clause)
```python
return jsonify({
    "status": 422,
    "data": None,
    "error": {
        "code": "VALIDATION_ERROR",
        "message": "Validation failed.",
        "fields": errors    # e.g. {"name": "Name is required."}
    }
}), 422
```

#### C. Not Found Envelope (`404 Not Found` — Missing `:id` or Missing Customer)
```python
return jsonify({
    "status": 404,
    "data": None,
    "error": {
        "code": "NOT_FOUND",
        "message": "Record not found."
    }
}), 404
```

---

## 2. Common Live Checkpoint Challenges & Solutions

### Scenario 1: "Fix a route that crashes with a `500` on bad input instead of returning `422`"

```python
data = request.get_json(silent=True) or {}
errors = {}

# 1. String guard clause (catches None, "", and "   ")
name = str(data.get("name") or "").strip()
if not name:
    errors["name"] = "Name is required."

# 2. Numeric guard clause (catches missing, "abc", True/False, 0, and negative)
raw_val = data.get("laundry_weight")
if raw_val is None or (isinstance(raw_val, str) and not raw_val.strip()):
    errors["laundry_weight"] = "Laundry weight is required."
elif isinstance(raw_val, bool):
    errors["laundry_weight"] = "Laundry weight must be a number."
else:
    try:
        weight = float(raw_val)
        if weight <= 0:
            errors["laundry_weight"] = "Laundry weight must be greater than zero."
    except (TypeError, ValueError):
        errors["laundry_weight"] = "Laundry weight must be a number."

if errors:
    return jsonify({
        "status": 422,
        "data": None,
        "error": {"code": "VALIDATION_ERROR", "message": "Validation failed.", "fields": errors}
    }), 422
```

### Scenario 2: "Build a `PUT /<resource>/<id>` route solo"

On `PUT /<resource>/<id>`, **always run 422 validation first**, then check if the `:id` exists in the database (`404`), then `UPDATE` and return `200`:

```python
@app.route("/customers/<id>", methods=["PUT"])
def updateCustomer(id):
    # Step 1: Validate input FIRST (422)
    data = request.get_json(silent=True) or {}
    cleaned, errors = validate_customer_payload(data)
    if errors:
        return validation_error_response(errors)

    # Step 2: Check if record exists (404)
    conn = get_db_connection()
    existing = conn.execute("SELECT id FROM customers WHERE id = ?", (id,)).fetchone()
    if existing is None:
        conn.close()
        return not_found_response("Customer not found.")

    # Step 3: Update & Commit (200)
    conn.execute(
        "UPDATE customers SET name = ?, contact_number = ? WHERE id = ?",
        (cleaned["name"], cleaned["contact_number"], id)
    )
    conn.commit()
    conn.close()

    return success_response({
        "id": int(id),
        "name": cleaned["name"],
        "contact_number": cleaned["contact_number"]
    }, 200)
```

### Scenario 3: "Write a meaningful `pytest` test for your route (Happy Path + 422 + 404)"

```python
def test_customer_crud_and_validation(api_client):
    # 1. Happy Path (201 Created)
    res = api_client.post("/customers", json={
        "name": "Maria Santos",
        "contact_number": "09171234567"
    })
    assert res.status_code == 201
    body = res.get_json()
    assert body["data"]["name"] == "Maria Santos"
    cust_id = body["data"]["id"]

    # 2. Validation Failure (422 Unprocessable Entity)
    bad_res = api_client.post("/customers", json={"name": "", "contact_number": ""})
    assert bad_res.status_code == 422
    bad_body = bad_res.get_json()
    assert bad_body["error"]["code"] == "VALIDATION_ERROR"
    assert "name" in bad_body["error"]["fields"]

    # 3. Edge Case — Missing ID (404 Not Found)
    missing_res = api_client.get("/customers/999999")
    assert missing_res.status_code == 404
    assert missing_res.get_json()["error"]["code"] == "NOT_FOUND"
```

---

## 3. Individual Member Cheat-Sheets (By Assigned Module)

### 1. John Michael D. Bretaña — Laundry Orders (`/laundry-orders`)
- **Files Owned:** `controllers/order_routes.py`, `controllers/validators.py` (`validate_laundry_order_payload`), `controllers/crud_service.py`
- **Table:** `laundry_orders (id, customer, laundry_weight, service_type, total_price, status, created_at)`
- **5 CRUD Routes:** `POST /laundry-orders` (`201`), `GET /laundry-orders` (`200`), `GET /laundry-orders/<id>` (`200`/`404`), `PUT /laundry-orders/<id>` (`200`/`422`/`404`), `DELETE /laundry-orders/<id>` (`200`/`404`)
- **Validation Rules:** `customer` required non-blank (`"Customer is required."`); `laundry_weight` required numeric `> 0` (`"Laundry weight is required."`, `"Laundry weight must be a number."`, `"Laundry weight must be greater than zero."`).

### 2. Hazil Enoc — Customers (`/customers`)
- **Files Owned:** `controllers/customer_routes.py`, `controllers/validators.py` (`validate_customer_payload`), `controllers/crud_service.py`
- **Table:** `customers (id, name, contact_number, email, address, membership)`
- **5 CRUD Routes:** `POST /customers` (`201`), `GET /customers` (`200`), `GET /customers/<id>` (`200`/`404`), `PUT /customers/<id>` (`200`/`422`/`404`), `DELETE /customers/<id>` (`200`/`404`)
- **Validation Rules:** `name` required non-blank (`"Name is required."`); `contact_number` required non-blank (`"Contact number is required."`).

### 3. Mark Ephraim Nicor — Pickup Schedules (`/pickup-schedules`)
- **Files Owned:** `controllers/pickup_routes.py`, `controllers/validators.py` (`validate_pickup_schedule_payload`), `controllers/crud_service.py`
- **Table:** `pickup_schedules (id, customer, pickup_date, pickup_time, pickup_address, status, assigned_driver, notes)`
- **5 CRUD Routes:** `POST /pickup-schedules` (`201`), `GET /pickup-schedules` (`200`), `GET /pickup-schedules/<id>` (`200`/`404`), `PUT /pickup-schedules/<id>` (`200`/`422`/`404`), `DELETE /pickup-schedules/<id>` (`200`/`404`)
- **Validation Rules:** `pickup_date` required non-blank (`"Pickup date is required."`); `customer` required non-blank (`"Customer is required."`).

### 4. Tristan Dave M. Plaza — Delivery Records (`/delivery-records`)
- **Files Owned:** `controllers/delivery_routes.py`, `controllers/validators.py` (`validate_delivery_record_payload`), `controllers/crud_service.py`
- **Table:** `delivery_records (id, customer, order_id, delivery_date, delivery_address, status, assigned_rider, delivery_notes)`
- **5 CRUD Routes:** `POST /delivery-records` (`201`), `GET /delivery-records` (`200`), `GET /delivery-records/<id>` (`200`/`404`), `PUT /delivery-records/<id>` (`200`/`422`/`404`), `DELETE /delivery-records/<id>` (`200`/`404`)
- **Validation Rules:** `delivery_date` required non-blank (`"Delivery date is required."`); `customer` required non-blank (`"Customer is required."`).

### 5. Marvin Oclarino — Payments (`/payments`)
- **Files Owned:** `controllers/payment_routes.py`, `controllers/validators.py` (`validate_payment_payload`), `controllers/crud_service.py`
- **Table:** `payments (id, customer, payment_amount, payment_method, transaction_time, order_id, status, reference_no, notes)`
- **5 CRUD Routes:** `POST /payments` (`201`), `GET /payments` (`200`), `GET /payments/<id>` (`200`/`404`), `PUT /payments/<id>` (`200`/`422`/`404`), `DELETE /payments/<id>` (`200`/`404`)
- **Validation Rules:** `customer` required non-blank (`"Customer is required."`); `payment_amount` required numeric `> 0` (`"Payment amount is required."`, `"Payment amount must be a number."`, `"Payment amount must be greater than zero."`); `payment_method` required non-blank (`"Payment method is required."`).
