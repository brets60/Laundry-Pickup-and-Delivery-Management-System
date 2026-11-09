from datetime import datetime
from db import get_db_connection


def customer_exists(customer_name):
    conn = get_db_connection()
    customer = conn.execute(
        "SELECT id FROM customers WHERE name = ?",
        (customer_name,)
    ).fetchone()
    conn.close()
    return customer is not None


def _coerce_id(raw_id):
    try:
        return int(raw_id)
    except (TypeError, ValueError):
        return raw_id


# Customers

def create_customer_record(cleaned_data):
    conn = get_db_connection()
    cursor = conn.execute(
        "INSERT INTO customers (name, contact_number) VALUES (?, ?)",
        (cleaned_data["name"], cleaned_data["contact_number"])
    )
    customer_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return {
        "id": customer_id,
        "name": cleaned_data["name"],
        "contact_number": cleaned_data["contact_number"]
    }


def list_customer_records():
    conn = get_db_connection()
    customers = conn.execute(
        "SELECT id, name, contact_number FROM customers ORDER BY id"
    ).fetchall()
    conn.close()
    return [dict(c) for c in customers]


def get_customer_record(customer_id):
    conn = get_db_connection()
    customer = conn.execute(
        "SELECT id, name, contact_number FROM customers WHERE id = ?",
        (customer_id,)
    ).fetchone()
    conn.close()
    return dict(customer) if customer else None


def update_customer_record(customer_id, cleaned_data):
    conn = get_db_connection()
    existing = conn.execute(
        "SELECT id FROM customers WHERE id = ?",
        (customer_id,)
    ).fetchone()
    if existing is None:
        conn.close()
        return None

    conn.execute(
        "UPDATE customers SET name = ?, contact_number = ? WHERE id = ?",
        (cleaned_data["name"], cleaned_data["contact_number"], customer_id)
    )
    conn.commit()
    conn.close()
    return {
        "id": _coerce_id(customer_id),
        "name": cleaned_data["name"],
        "contact_number": cleaned_data["contact_number"]
    }


def delete_customer_record(customer_id):
    conn = get_db_connection()
    existing = conn.execute(
        "SELECT id FROM customers WHERE id = ?",
        (customer_id,)
    ).fetchone()
    if existing is None:
        conn.close()
        return None

    conn.execute("DELETE FROM customers WHERE id = ?", (customer_id,))
    conn.commit()
    conn.close()
    return {
        "message": "Customer deleted successfully.",
        "id": _coerce_id(customer_id)
    }


# Laundry Orders

def create_laundry_order_record(cleaned_data):
    conn = get_db_connection()
    cursor = conn.execute(
        "INSERT INTO laundry_orders (customer, laundry_weight) VALUES (?, ?)",
        (cleaned_data["customer"], cleaned_data["laundry_weight"])
    )
    order_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return {
        "id": order_id,
        "customer": cleaned_data["customer"],
        "laundry_weight": cleaned_data["laundry_weight"]
    }


def list_laundry_order_records():
    conn = get_db_connection()
    orders = conn.execute(
        "SELECT id, customer, laundry_weight FROM laundry_orders ORDER BY id"
    ).fetchall()
    conn.close()
    return [dict(o) for o in orders]


def get_laundry_order_record(order_id):
    conn = get_db_connection()
    order = conn.execute(
        "SELECT id, customer, laundry_weight FROM laundry_orders WHERE id = ?",
        (order_id,)
    ).fetchone()
    conn.close()
    return dict(order) if order else None


def update_laundry_order_record(order_id, cleaned_data):
    conn = get_db_connection()
    existing = conn.execute(
        "SELECT id FROM laundry_orders WHERE id = ?",
        (order_id,)
    ).fetchone()
    if existing is None:
        conn.close()
        return None

    conn.execute(
        "UPDATE laundry_orders SET customer = ?, laundry_weight = ? WHERE id = ?",
        (cleaned_data["customer"], cleaned_data["laundry_weight"], order_id)
    )
    conn.commit()
    conn.close()
    return {
        "id": _coerce_id(order_id),
        "customer": cleaned_data["customer"],
        "laundry_weight": cleaned_data["laundry_weight"]
    }


def delete_laundry_order_record(order_id):
    conn = get_db_connection()
    existing = conn.execute(
        "SELECT id FROM laundry_orders WHERE id = ?",
        (order_id,)
    ).fetchone()
    if existing is None:
        conn.close()
        return None

    conn.execute("DELETE FROM laundry_orders WHERE id = ?", (order_id,))
    conn.commit()
    conn.close()
    return {
        "message": "Laundry order deleted successfully.",
        "id": _coerce_id(order_id)
    }


# Pickup Schedules

def create_pickup_schedule_record(cleaned_data):
    conn = get_db_connection()
    cursor = conn.execute(
        "INSERT INTO pickup_schedules (customer, pickup_date) VALUES (?, ?)",
        (cleaned_data["customer"], cleaned_data["pickup_date"])
    )
    schedule_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return {
        "id": schedule_id,
        "customer": cleaned_data["customer"],
        "pickup_date": cleaned_data["pickup_date"]
    }


def list_pickup_schedule_records():
    conn = get_db_connection()
    schedules = conn.execute(
        "SELECT id, customer, pickup_date FROM pickup_schedules ORDER BY id"
    ).fetchall()
    conn.close()
    return [dict(s) for s in schedules]


def get_pickup_schedule_record(schedule_id):
    conn = get_db_connection()
    schedule = conn.execute(
        "SELECT id, customer, pickup_date FROM pickup_schedules WHERE id = ?",
        (schedule_id,)
    ).fetchone()
    conn.close()
    return dict(schedule) if schedule else None


def update_pickup_schedule_record(schedule_id, cleaned_data):
    conn = get_db_connection()
    existing = conn.execute(
        "SELECT id FROM pickup_schedules WHERE id = ?",
        (schedule_id,)
    ).fetchone()
    if existing is None:
        conn.close()
        return None

    conn.execute(
        "UPDATE pickup_schedules SET customer = ?, pickup_date = ? WHERE id = ?",
        (cleaned_data["customer"], cleaned_data["pickup_date"], schedule_id)
    )
    conn.commit()
    conn.close()
    return {
        "id": _coerce_id(schedule_id),
        "customer": cleaned_data["customer"],
        "pickup_date": cleaned_data["pickup_date"]
    }


def delete_pickup_schedule_record(schedule_id):
    conn = get_db_connection()
    existing = conn.execute(
        "SELECT id FROM pickup_schedules WHERE id = ?",
        (schedule_id,)
    ).fetchone()
    if existing is None:
        conn.close()
        return None

    conn.execute("DELETE FROM pickup_schedules WHERE id = ?", (schedule_id,))
    conn.commit()
    conn.close()
    return {
        "message": "Pickup schedule deleted successfully.",
        "id": _coerce_id(schedule_id)
    }


# Delivery Records

def create_delivery_record_entry(cleaned_data):
    conn = get_db_connection()
    cursor = conn.execute(
        "INSERT INTO delivery_records (customer, delivery_date) VALUES (?, ?)",
        (cleaned_data["customer"], cleaned_data["delivery_date"])
    )
    delivery_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return {
        "id": delivery_id,
        "customer": cleaned_data["customer"],
        "delivery_date": cleaned_data["delivery_date"]
    }


def list_delivery_record_entries():
    conn = get_db_connection()
    records = conn.execute(
        "SELECT id, customer, delivery_date FROM delivery_records ORDER BY id"
    ).fetchall()
    conn.close()
    return [dict(r) for r in records]


def get_delivery_record_entry(delivery_id):
    conn = get_db_connection()
    record = conn.execute(
        "SELECT id, customer, delivery_date FROM delivery_records WHERE id = ?",
        (delivery_id,)
    ).fetchone()
    conn.close()
    return dict(record) if record else None


def update_delivery_record_entry(delivery_id, cleaned_data):
    conn = get_db_connection()
    existing = conn.execute(
        "SELECT id FROM delivery_records WHERE id = ?",
        (delivery_id,)
    ).fetchone()
    if existing is None:
        conn.close()
        return None

    conn.execute(
        "UPDATE delivery_records SET customer = ?, delivery_date = ? WHERE id = ?",
        (cleaned_data["customer"], cleaned_data["delivery_date"], delivery_id)
    )
    conn.commit()
    conn.close()
    return {
        "id": _coerce_id(delivery_id),
        "customer": cleaned_data["customer"],
        "delivery_date": cleaned_data["delivery_date"]
    }


def delete_delivery_record_entry(delivery_id):
    conn = get_db_connection()
    existing = conn.execute(
        "SELECT id FROM delivery_records WHERE id = ?",
        (delivery_id,)
    ).fetchone()
    if existing is None:
        conn.close()
        return None

    conn.execute("DELETE FROM delivery_records WHERE id = ?", (delivery_id,))
    conn.commit()
    conn.close()
    return {
        "message": "Delivery record deleted successfully.",
        "id": _coerce_id(delivery_id)
    }


# Payments

def create_payment_record(cleaned_data):
    conn = get_db_connection()
    transaction_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor = conn.execute(
        """
        INSERT INTO payments (customer, payment_amount, payment_method, transaction_time)
        VALUES (?, ?, ?, ?)
        """,
        (
            cleaned_data["customer"],
            cleaned_data["payment_amount"],
            cleaned_data["payment_method"],
            transaction_time
        )
    )
    payment_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return {
        "id": payment_id,
        "customer": cleaned_data["customer"],
        "payment_amount": cleaned_data["payment_amount"],
        "payment_method": cleaned_data["payment_method"],
        "transaction_time": transaction_time
    }


def list_payment_records():
    conn = get_db_connection()
    payments = conn.execute(
        """
        SELECT id, customer, payment_amount, payment_method, transaction_time
        FROM payments
        ORDER BY id
        """
    ).fetchall()
    conn.close()
    return [dict(p) for p in payments]


def get_payment_record(payment_id):
    conn = get_db_connection()
    payment = conn.execute(
        """
        SELECT id, customer, payment_amount, payment_method, transaction_time
        FROM payments
        WHERE id = ?
        """,
        (payment_id,)
    ).fetchone()
    conn.close()
    return dict(payment) if payment else None


def update_payment_record(payment_id, cleaned_data):
    conn = get_db_connection()
    existing = conn.execute(
        "SELECT id FROM payments WHERE id = ?",
        (payment_id,)
    ).fetchone()
    if existing is None:
        conn.close()
        return None

    conn.execute(
        """
        UPDATE payments
        SET customer = ?, payment_amount = ?, payment_method = ?
        WHERE id = ?
        """,
        (
            cleaned_data["customer"],
            cleaned_data["payment_amount"],
            cleaned_data["payment_method"],
            payment_id
        )
    )
    conn.commit()
    conn.close()
    return {
        "id": _coerce_id(payment_id),
        "customer": cleaned_data["customer"],
        "payment_amount": cleaned_data["payment_amount"],
        "payment_method": cleaned_data["payment_method"]
    }


def delete_payment_record(payment_id):
    conn = get_db_connection()
    existing = conn.execute(
        "SELECT id FROM payments WHERE id = ?",
        (payment_id,)
    ).fetchone()
    if existing is None:
        conn.close()
        return None

    conn.execute("DELETE FROM payments WHERE id = ?", (payment_id,))
    conn.commit()
    conn.close()
    return {
        "message": "Payment deleted successfully.",
        "id": _coerce_id(payment_id)
    }
