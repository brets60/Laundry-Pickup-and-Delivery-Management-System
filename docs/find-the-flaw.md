# Find the Flaw: Code Review & Bug Hunting in AI-Generated Code
**Coursework:** CS 106 / Software Engineering 1  
**Sprint / Week:** Week 09 — Reviewing Code (Especially the AI's)  
**Project:** Laundry Pickup and Delivery Management System (`LaundryCare`)  
**Team Members:**  
1. John Michael Bretaña (Manager / Lead Architect)  
2. Hazil Enoc (Store Cashier / CRM Specialist)  
3. Marvin Oclarino (Delivery Driver / Financial Settlement)  
4. Tristan Dave M. Plaza (Delivery Driver / Courier Logistics)  
5. Mark Ephraim Nicor (Laundry Operator / Wash Hub Lead)  

---

## Executive Summary
Generative AI models accelerate software development, but blindly trusting AI output introduces severe vulnerabilities, logic flaws, wrong status codes, and silent failures. For Week 9 Task 3, our engineering team analyzed five AI-generated backend snippets with planted flaws typical of large language models. Below is the comprehensive bug dossier detailing **what is wrong**, **why the AI generated it**, the **production-grade fix**, and the **prevention checklist item**.

---

## Snippet 1: Missing Validation & Type Coercion in Order Creation
**Severity:** Critical (`[BLOCKING]`)  
**CWE:** CWE-20 (Improper Input Validation)  
**Location:** Order Intake Controller  

### Flawed AI-Generated Code:
```python
@order_bp.route('/api/orders/create', methods=['POST'])
def create_order():
    data = request.get_json()
    # Flaw: No null checks, no type safety, string concatenated directly
    customer = data['customer']
    weight = data['weight']
    service = data['service']

    total_price = float(weight) * 45.0
    conn = get_db_connection()
    conn.execute(
        "INSERT INTO laundry_orders (customer, laundry_weight, service_type, total_price, status) VALUES (?, ?, ?, ?, 'Pending')",
        (customer, weight, service, total_price)
    )
    conn.commit()
    conn.close()
    return jsonify({"message": "Order created!"})
```

### What's Wrong:
1. **Unchecked Dictionary Access:** Accessing `data['customer']` without checking raises a `KeyError` (500 Internal Server Error) if the payload is missing a key.
2. **Missing Boundary & Zero Validation:** If `weight <= 0` or negative (e.g., `-5.0`), the system creates an order with a negative charge or zero price.
3. **No String Trimming / Empty Field Guard:** An empty string (`""`) for `customer` or `service` passes through directly into the database.
4. **Missing Status Code:** Defaults to `200 OK` on resource creation instead of `201 Created`.

### Why AI Generated It:
LLMs optimize for the "happy path" unless prompted with adversarial edge cases. The model hallucinates that input data is always well-formed and sanitized by an upstream middleware.

### Production Fix:
```python
@order_bp.route('/api/orders/create', methods=['POST'])
def create_order():
    data = request.get_json(silent=True) or {}
    customer = str(data.get('customer') or '').strip()
    service = str(data.get('service') or '').strip()
    weight_raw = data.get('weight')

    errors = {}
    if not customer:
        errors['customer'] = "Customer name is required."
    if not service:
        errors['service'] = "Service type is required."

    try:
        weight = float(weight_raw)
        if weight <= 0:
            errors['weight'] = "Laundry weight must be greater than 0 kg."
        elif weight > 100:
            errors['weight'] = "Single batch order cannot exceed 100 kg. Please schedule a commercial bulk intake."
    except (ValueError, TypeError):
        errors['weight'] = "Weight must be a valid numeric quantity in kilograms."

    if errors:
        return jsonify({"status": 422, "error": errors}), 422

    total_price = round(weight * 45.0, 2)
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO laundry_orders (customer, laundry_weight, service_type, total_price, status) VALUES (?, ?, ?, ?, 'Pending')",
        (customer, weight, service, total_price)
    )
    new_id = cursor.lastrowid
    conn.commit()
    conn.close()

    return jsonify({
        "status": 201,
        "message": f"Order #ORD-{new_id:04d} created successfully!",
        "order_id": new_id
    }), 201
```

---

## Snippet 2: Wrong HTTP Status Codes & Failure Masking
**Severity:** High (`[BLOCKING]`)  
**RFC Violation:** RFC 9110 (HTTP Semantics)  
**Location:** Delivery Dispatch Controller  

### Flawed AI-Generated Code:
```python
@delivery_bp.route('/deliveries/dispatch', methods=['POST'])
def dispatch_delivery():
    data = request.form
    order_id = data.get('order_id')
    rider = data.get('rider')

    if not order_id or not rider:
        # Flaw: Returning 200 OK for a client validation error!
        return jsonify({"success": False, "msg": "Missing fields"}), 200

    conn = get_db_connection()
    order = conn.execute("SELECT * FROM laundry_orders WHERE id = ?", (order_id,)).fetchone()
    if not order:
        # Flaw: Returning 500 Server Error for a missing client resource!
        return jsonify({"error": "Order not found"}), 500

    conn.execute("UPDATE laundry_orders SET status = 'Out for Delivery' WHERE id = ?", (order_id,))
    conn.commit()
    conn.close()
    return jsonify({"success": True})
```

### What's Wrong:
1. **HTTP 200 on Validation Failure:** Returning `200 OK` with `{"success": false}` fools frontend `fetch()` checks (since `response.ok` is `true` for 200-299), masking failures from error interceptors.
2. **HTTP 500 on Non-Existent Client ID:** If an order does not exist, that is a client mistake (`404 Not Found`), not a server crash (`500`). This artificially inflates server error monitoring alerts.
3. **Missing Resource Mutation Verification:** Fails to check if the update query affected any rows.

### Why AI Generated It:
Older web tutorials frequently dumped JSON with status `200` and a custom `success` boolean. LLM training corpora are filled with this anti-pattern.

### Production Fix:
```python
@delivery_bp.route('/deliveries/dispatch', methods=['POST'])
def dispatch_delivery():
    data = request.get_json(silent=True) if request.is_json else request.form
    order_id = data.get('order_id')
    rider = str(data.get('rider') or '').strip()

    if not order_id or not rider:
        return jsonify({
            "status": 422,
            "error": "Both order_id and assigned courier rider are required."
        }), 422

    conn = get_db_connection()
    order = conn.execute("SELECT id, status FROM laundry_orders WHERE id = ?", (order_id,)).fetchone()
    if order is None:
        conn.close()
        return jsonify({
            "status": 404,
            "error": f"Order #{order_id} does not exist in dispatch registry."
        }), 404

    conn.execute("UPDATE laundry_orders SET status = 'Out for Delivery' WHERE id = ?", (order_id,))
    conn.commit()
    conn.close()

    return jsonify({
        "status": 200,
        "message": f"Order #{order_id} assigned to courier {rider}."
    }), 200
```

---

## Snippet 3: Unhandled 404 / 500 & Silent Failure in Tracking Route
**Severity:** High (`[BLOCKING]`)  
**Impact:** Client application crash & untracked laundry inquiries  
**Location:** Customer Tracking Route  

### Flawed AI-Generated Code:
```python
@app.route('/track/<tracking_code>')
def track_laundry(tracking_code):
    # Flaw: No database exception handling, blind splitting, crash on bad format
    parts = tracking_code.split('-')
    order_id = int(parts[1])

    conn = get_db_connection()
    order = conn.execute("SELECT * FROM laundry_orders WHERE id = " + str(order_id)).fetchone()
    customer = conn.execute("SELECT * FROM customers WHERE name = '" + order['customer'] + "'").fetchone()

    return render_template('track_status.html', order=order, customer=customer)
```

### What's Wrong:
1. **SQL Injection Vulnerability (CWE-89):** Concatenating `order['customer']` and `str(order_id)` into raw SQL strings without parameterization.
2. **Unhandled `IndexError` & `ValueError`:** If a user navigates to `/track/INVALID`, `parts[1]` throws `IndexError` and `int()` throws `ValueError`, causing an unhandled 500 server crash.
3. **Unhandled `NoneType` Exception:** If `order` is `None`, evaluating `order['customer']` crashes with `TypeError: 'NoneType' object is not subscriptable`.
4. **Database Connection Leak:** If an error occurs midway, `conn.close()` is never executed.

### Why AI Generated It:
LLMs often produce concise snippets for tutorial demonstrations, omitting defensive try-except blocks and parameterized SQL queries unless prompted with security requirements.

### Production Fix:
```python
@app.route('/track/<tracking_code>')
def track_laundry(tracking_code):
    clean_code = (tracking_code or '').strip().upper()
    if not clean_code.startswith("ORD-") and not clean_code.startswith("PCK-") and not clean_code.startswith("DEL-"):
        return render_template('404.html', message=f"Invalid tracking format '{tracking_code}'. Tracking codes start with ORD-, PCK-, or DEL-."), 404

    parts = clean_code.split('-')
    if len(parts) < 2 or not parts[1].isdigit():
        return render_template('404.html', message="Invalid tracking reference number."), 404

    target_id = int(parts[1])
    conn = get_db_connection()
    try:
        order = conn.execute("SELECT * FROM laundry_orders WHERE id = ?", (target_id,)).fetchone()
        if not order:
            conn.close()
            return render_template('404.html', message=f"Tracking order #{target_id:04d} was not found."), 404

        customer = conn.execute("SELECT * FROM customers WHERE name = ?", (order['customer'],)).fetchone()
        deliveries = conn.execute("SELECT * FROM delivery_records WHERE order_id = ?", (target_id,)).fetchall()
        conn.close()
        return render_template('track_status.html', order=order, customer=customer, deliveries=deliveries)
    except Exception as e:
        conn.close()
        return render_template('500.html', error_id=f"TRK-{target_id}"), 500
```

---

## Snippet 4: Hallucinated ORM & Database Methods
**Severity:** Medium (`[BLOCKING]`)  
**Impact:** `AttributeError` at runtime during customer record edits  
**Location:** Customer Repository Helper  

### Flawed AI-Generated Code:
```python
def update_customer_balance(customer_id, additional_charge):
    conn = get_db_connection()
    # Flaw: Hallucinated method names from other frameworks!
    conn.begin_transaction()  # Hallucinated! sqlite3 uses conn.isolation_level or context managers
    customer = conn.find_one({"id": customer_id})  # Hallucinated! MongoDB syntax in SQLite
    customer.save_and_commit()  # Hallucinated! Django/Spring syntax in raw SQLite
    conn.close()
```

### What's Wrong:
1. **Cross-Framework Syntax Hallucination:** The model mixed raw Python `sqlite3`, MongoDB (`find_one`), and ActiveRecord (`save_and_commit`).
2. **Immediate Runtime Explosion:** Invoking this function immediately raises `AttributeError: 'sqlite3.Connection' object has no attribute 'begin_transaction'`.

### Why AI Generated It:
LLMs synthesize statistical token associations across hundreds of web frameworks (Mongoose, Django ORM, SQLAlchemy, raw SQLite). When context is under-specified, the model blends paradigms into nonexistent APIs.

### Production Fix:
```python
def update_customer_balance(customer_id, additional_charge):
    conn = get_db_connection()
    try:
        with conn:
            # Native SQLite parameterization
            row = conn.execute("SELECT pending_balance FROM customers WHERE id = ?", (customer_id,)).fetchone()
            if not row:
                return False, "Customer not found"
            
            new_balance = max(0.0, float(row['pending_balance'] or 0.0) + float(additional_charge))
            conn.execute(
                "UPDATE customers SET pending_balance = ? WHERE id = ?",
                (new_balance, customer_id)
            )
        return True, f"Balance updated to ₱{new_balance:.2f}"
    except sqlite3.Error as e:
        return False, str(e)
    finally:
        conn.close()
```

---

## Snippet 5: Floating-Point Rounding & Negative Discount Vulnerability
**Severity:** Medium (`[NIT] / Must Address before Shipping`)  
**Impact:** Financial ledger drift & revenue leakage  
**Location:** Cashier Payment Calculation  

### Flawed AI-Generated Code:
```python
def apply_tier_discount(subtotal, tier, discount_code=None):
    # Flaw: IEEE-754 precision inaccuracies and unbounded negative math
    if tier == 'VIP':
        discount = subtotal * 0.15
    elif tier == 'Gold':
        discount = subtotal * 0.10
    else:
        discount = 0.0

    if discount_code:
        discount += 50.0  # Flaw: If subtotal is 40.0, final total becomes -10.0!

    final_total = subtotal - discount
    return final_total  # Returns floating point: e.g. 42.49999999999999
```

### What's Wrong:
1. **Negative Payment Exploitation:** If a customer orders a ₱40 service with a ₱50 coupon, `final_total` is negative (`-₱10.00`), causing the system to owe money to the customer.
2. **IEEE 754 Floating Point Drift:** Multiplying floats directly produces artifacts like `84.99999999999999` instead of `85.00`.

### Why AI Generated It:
AI models treat mathematical calculations as generic arithmetic without domain knowledge of commercial cash drawers and accounting invariants.

### Production Fix:
```python
from decimal import Decimal, ROUND_HALF_UP

def apply_tier_discount(subtotal_amount, tier, discount_php=0.0):
    subtotal = Decimal(str(subtotal_amount))
    tier_lower = (tier or '').lower()

    if tier_lower == 'vip':
        discount_rate = Decimal('0.15')
    elif tier_lower == 'gold':
        discount_rate = Decimal('0.10')
    else:
        discount_rate = Decimal('0.00')

    tier_discount = subtotal * discount_rate
    promo_discount = Decimal(str(max(0.0, float(discount_php or 0.0))))
    total_discount = tier_discount + promo_discount

    # Enforce non-negative floor
    final_total = max(Decimal('0.00'), subtotal - total_discount)

    # Quantize to exact 2-decimal centavos
    return float(final_total.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP))
```

---

## Team Bug-Hunting Summary & Prevention Matrix

| Flaw Category | Detected By | Root Cause in LLM | Peer Review Prevention Rule |
|---|---|---|---|
| **Missing Validation** | Hazil Enoc | LLM assumes clean inputs | All POST/PUT routes must validate presence, type, and min/max bounds |
| **Wrong Status Codes** | Tristan Dave M. Plaza | Old web tutorial training data | RFC 9110 compliance: 201 on create, 404 on missing, 422 on validation |
| **Silent 500 Crashes** | Marvin Oclarino | Omitting try/except blocks | Every external parameter parsing must be guarded with safe fallbacks |
| **Hallucinated ORM** | Mark Ephraim Nicor | Mixed framework associations | Strictly verify that method calls match `sqlite3` and Flask documentation |
| **Float Precision & Negatives** | John Michael Bretaña | Untyped mathematical arithmetic | Use decimal rounding and non-negative clamping on all monetary computations |
