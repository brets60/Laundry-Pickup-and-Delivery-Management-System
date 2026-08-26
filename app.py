from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)

DATABASE = "laundry.db"


# =========================
# DATABASE
# =========================

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_database():
    conn = get_db_connection()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            contact_number TEXT NOT NULL
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS laundry_orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer TEXT NOT NULL,
            laundry_weight REAL NOT NULL
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS pickup_schedules (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer TEXT NOT NULL,
            pickup_date TEXT NOT NULL
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS delivery_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer TEXT NOT NULL,
            delivery_date TEXT NOT NULL
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS payments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            payment_amount REAL NOT NULL,
            payment_method TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


init_database()


# =========================
# CUSTOMERS
# =========================

@app.route("/customers", methods=["POST"])
def createCustomer():
    data = request.get_json(silent=True) or {}

    errors = {}

    if not data.get("name"):
        errors["name"] = "Name is required."

    if not data.get("contact_number"):
        errors["contact_number"] = "Contact number is required."

    if errors:
        return jsonify({
            "status": 422,
            "data": None,
            "error": {
                "code": "VALIDATION_ERROR",
                "message": "Validation failed.",
                "fields": errors
            }
        }), 422

    conn = get_db_connection()

    cursor = conn.execute(
        """
        INSERT INTO customers (name, contact_number)
        VALUES (?, ?)
        """,
        (
            data["name"],
            data["contact_number"]
        )
    )

    customer_id = cursor.lastrowid

    conn.commit()
    conn.close()

    return jsonify({
        "status": 201,
        "data": {
            "id": customer_id,
            "name": data["name"],
            "contact_number": data["contact_number"]
        },
        "error": None
    }), 201


@app.route("/customers", methods=["GET"])
def listCustomers():
    conn = get_db_connection()

    customers = conn.execute(
        """
        SELECT id, name, contact_number
        FROM customers
        ORDER BY id
        """
    ).fetchall()

    conn.close()

    return jsonify({
        "status": 200,
        "data": [dict(customer) for customer in customers],
        "error": None
    }), 200


@app.route("/customers/<id>", methods=["GET"])
def showCustomer(id):
    conn = get_db_connection()

    customer = conn.execute(
        """
        SELECT id, name, contact_number
        FROM customers
        WHERE id = ?
        """,
        (id,)
    ).fetchone()

    conn.close()

    if customer is None:
        return jsonify({
            "status": 404,
            "data": None,
            "error": {
                "code": "NOT_FOUND",
                "message": "Customer not found."
            }
        }), 404

    return jsonify({
        "status": 200,
        "data": dict(customer),
        "error": None
    }), 200


@app.route("/customers/<id>", methods=["PUT"])
def updateCustomer(id):
    data = request.get_json(silent=True) or {}

    errors = {}

    if not data.get("name"):
        errors["name"] = "Name is required."

    if not data.get("contact_number"):
        errors["contact_number"] = "Contact number is required."

    if errors:
        return jsonify({
            "status": 422,
            "data": None,
            "error": {
                "code": "VALIDATION_ERROR",
                "message": "Validation failed.",
                "fields": errors
            }
        }), 422

    conn = get_db_connection()

    customer = conn.execute(
        """
        SELECT id
        FROM customers
        WHERE id = ?
        """,
        (id,)
    ).fetchone()

    if customer is None:
        conn.close()

        return jsonify({
            "status": 404,
            "data": None,
            "error": {
                "code": "NOT_FOUND",
                "message": "Customer not found."
            }
        }), 404

    conn.execute(
        """
        UPDATE customers
        SET name = ?, contact_number = ?
        WHERE id = ?
        """,
        (
            data["name"],
            data["contact_number"],
            id
        )
    )

    conn.commit()
    conn.close()

    return jsonify({
        "status": 200,
        "data": {
            "id": int(id),
            "name": data["name"],
            "contact_number": data["contact_number"]
        },
        "error": None
    }), 200


@app.route("/customers/<id>", methods=["DELETE"])
def deleteCustomer(id):
    conn = get_db_connection()

    customer = conn.execute(
        """
        SELECT id
        FROM customers
        WHERE id = ?
        """,
        (id,)
    ).fetchone()

    if customer is None:
        conn.close()

        return jsonify({
            "status": 404,
            "data": None,
            "error": {
                "code": "NOT_FOUND",
                "message": "Customer not found."
            }
        }), 404

    conn.execute(
        """
        DELETE FROM customers
        WHERE id = ?
        """,
        (id,)
    )

    conn.commit()
    conn.close()

    return jsonify({
        "status": 200,
        "data": {
            "message": "Customer deleted successfully.",
            "id": int(id)
        },
        "error": None
    }), 200


# =========================
# LAUNDRY ORDERS
# =========================

@app.route("/laundry-orders", methods=["POST"])
def createLaundryOrder():
    data = request.get_json(silent=True) or {}

    errors = {}

    if not data.get("customer"):
        errors["customer"] = "Customer is required."

    if "laundry_weight" not in data:
        errors["laundry_weight"] = "Laundry weight is required."
    else:
        try:
            laundry_weight = float(data["laundry_weight"])

            if laundry_weight <= 0:
                errors["laundry_weight"] = (
                    "Laundry weight must be greater than zero."
                )

        except (TypeError, ValueError):
            errors["laundry_weight"] = "Laundry weight must be a number."

    if errors:
        return jsonify({
            "status": 422,
            "data": None,
            "error": {
                "code": "VALIDATION_ERROR",
                "message": "Validation failed.",
                "fields": errors
            }
        }), 422

    conn = get_db_connection()

    cursor = conn.execute(
        """
        INSERT INTO laundry_orders (customer, laundry_weight)
        VALUES (?, ?)
        """,
        (
            data["customer"],
            laundry_weight
        )
    )

    order_id = cursor.lastrowid

    conn.commit()
    conn.close()

    return jsonify({
        "status": 201,
        "data": {
            "id": order_id,
            "customer": data["customer"],
            "laundry_weight": laundry_weight
        },
        "error": None
    }), 201


@app.route("/laundry-orders", methods=["GET"])
def listLaundryOrders():
    conn = get_db_connection()

    orders = conn.execute(
        """
        SELECT id, customer, laundry_weight
        FROM laundry_orders
        ORDER BY id
        """
    ).fetchall()

    conn.close()

    return jsonify({
        "status": 200,
        "data": [dict(order) for order in orders],
        "error": None
    }), 200


@app.route("/laundry-orders/<id>", methods=["GET"])
def showLaundryOrder(id):
    conn = get_db_connection()

    order = conn.execute(
        """
        SELECT id, customer, laundry_weight
        FROM laundry_orders
        WHERE id = ?
        """,
        (id,)
    ).fetchone()

    conn.close()

    if order is None:
        return jsonify({
            "status": 404,
            "data": None,
            "error": {
                "code": "NOT_FOUND",
                "message": "Laundry order not found."
            }
        }), 404

    return jsonify({
        "status": 200,
        "data": dict(order),
        "error": None
    }), 200


@app.route("/laundry-orders/<id>", methods=["PUT"])
def updateLaundryOrder(id):
    data = request.get_json(silent=True) or {}

    errors = {}

    if not data.get("customer"):
        errors["customer"] = "Customer is required."

    if "laundry_weight" not in data:
        errors["laundry_weight"] = "Laundry weight is required."
    else:
        try:
            laundry_weight = float(data["laundry_weight"])

            if laundry_weight <= 0:
                errors["laundry_weight"] = (
                    "Laundry weight must be greater than zero."
                )

        except (TypeError, ValueError):
            errors["laundry_weight"] = "Laundry weight must be a number."

    if errors:
        return jsonify({
            "status": 422,
            "data": None,
            "error": {
                "code": "VALIDATION_ERROR",
                "message": "Validation failed.",
                "fields": errors
            }
        }), 422

    conn = get_db_connection()

    order = conn.execute(
        """
        SELECT id
        FROM laundry_orders
        WHERE id = ?
        """,
        (id,)
    ).fetchone()

    if order is None:
        conn.close()

        return jsonify({
            "status": 404,
            "data": None,
            "error": {
                "code": "NOT_FOUND",
                "message": "Laundry order not found."
            }
        }), 404

    conn.execute(
        """
        UPDATE laundry_orders
        SET customer = ?, laundry_weight = ?
        WHERE id = ?
        """,
        (
            data["customer"],
            laundry_weight,
            id
        )
    )

    conn.commit()
    conn.close()

    return jsonify({
        "status": 200,
        "data": {
            "id": int(id),
            "customer": data["customer"],
            "laundry_weight": laundry_weight
        },
        "error": None
    }), 200


@app.route("/laundry-orders/<id>", methods=["DELETE"])
def deleteLaundryOrder(id):
    conn = get_db_connection()

    order = conn.execute(
        """
        SELECT id
        FROM laundry_orders
        WHERE id = ?
        """,
        (id,)
    ).fetchone()

    if order is None:
        conn.close()

        return jsonify({
            "status": 404,
            "data": None,
            "error": {
                "code": "NOT_FOUND",
                "message": "Laundry order not found."
            }
        }), 404

    conn.execute(
        """
        DELETE FROM laundry_orders
        WHERE id = ?
        """,
        (id,)
    )

    conn.commit()
    conn.close()

    return jsonify({
        "status": 200,
        "data": {
            "message": "Laundry order deleted successfully.",
            "id": int(id)
        },
        "error": None
    }), 200


# =========================
# PICKUP SCHEDULES
# =========================

@app.route("/pickup-schedules", methods=["GET"])
def listPickupSchedules():
    conn = get_db_connection()

    schedules = conn.execute(
        """
        SELECT id, customer, pickup_date
        FROM pickup_schedules
        ORDER BY id
        """
    ).fetchall()

    conn.close()

    return jsonify({
        "status": 200,
        "data": [dict(schedule) for schedule in schedules],
        "error": None
    }), 200


@app.route("/pickup-schedules/<id>", methods=["GET"])
def showPickupSchedule(id):
    conn = get_db_connection()

    schedule = conn.execute(
        """
        SELECT id, customer, pickup_date
        FROM pickup_schedules
        WHERE id = ?
        """,
        (id,)
    ).fetchone()

    conn.close()

    if schedule is None:
        return jsonify({
            "status": 404,
            "data": None,
            "error": {
                "code": "NOT_FOUND",
                "message": "Pickup schedule not found."
            }
        }), 404

    return jsonify({
        "status": 200,
        "data": dict(schedule),
        "error": None
    }), 200


@app.route("/pickup-schedules/<id>", methods=["PUT"])
def updatePickupSchedule(id):
    data = request.get_json(silent=True) or {}

    errors = {}

    if not data.get("pickup_date"):
        errors["pickup_date"] = "Pickup date is required."

    if not data.get("customer"):
        errors["customer"] = "Customer is required."

    if errors:
        return jsonify({
            "status": 422,
            "data": None,
            "error": {
                "code": "VALIDATION_ERROR",
                "message": "Validation failed.",
                "fields": errors
            }
        }), 422

    conn = get_db_connection()

    schedule = conn.execute(
        """
        SELECT id
        FROM pickup_schedules
        WHERE id = ?
        """,
        (id,)
    ).fetchone()

    if schedule is None:
        conn.close()

        return jsonify({
            "status": 404,
            "data": None,
            "error": {
                "code": "NOT_FOUND",
                "message": "Pickup schedule not found."
            }
        }), 404

    conn.execute(
        """
        UPDATE pickup_schedules
        SET customer = ?, pickup_date = ?
        WHERE id = ?
        """,
        (
            data["customer"],
            data["pickup_date"],
            id
        )
    )

    conn.commit()
    conn.close()

    return jsonify({
        "status": 200,
        "data": {
            "id": int(id),
            "customer": data["customer"],
            "pickup_date": data["pickup_date"]
        },
        "error": None
    }), 200


@app.route("/pickup-schedules", methods=["POST"])
def createPickupSchedule():
    data = request.get_json(silent=True) or {}

    errors = {}

    if not data.get("pickup_date"):
        errors["pickup_date"] = "Pickup date is required."

    if not data.get("customer"):
        errors["customer"] = "Customer is required."

    if errors:
        return jsonify({
            "status": 422,
            "data": None,
            "error": {
                "code": "VALIDATION_ERROR",
                "message": "Validation failed.",
                "fields": errors
            }
        }), 422

    conn = get_db_connection()

    cursor = conn.execute(
        """
        INSERT INTO pickup_schedules (customer, pickup_date)
        VALUES (?, ?)
        """,
        (
            data["customer"],
            data["pickup_date"]
        )
    )

    schedule_id = cursor.lastrowid

    conn.commit()
    conn.close()

    return jsonify({
        "status": 201,
        "data": {
            "id": schedule_id,
            "customer": data["customer"],
            "pickup_date": data["pickup_date"]
        },
        "error": None
    }), 201


@app.route("/pickup-schedules/<id>", methods=["DELETE"])
def deletePickupSchedule(id):
    conn = get_db_connection()

    schedule = conn.execute(
        """
        SELECT id
        FROM pickup_schedules
        WHERE id = ?
        """,
        (id,)
    ).fetchone()

    if schedule is None:
        conn.close()

        return jsonify({
            "status": 404,
            "data": None,
            "error": {
                "code": "NOT_FOUND",
                "message": "Pickup schedule not found."
            }
        }), 404

    conn.execute(
        """
        DELETE FROM pickup_schedules
        WHERE id = ?
        """,
        (id,)
    )

    conn.commit()
    conn.close()

    return jsonify({
        "status": 200,
        "data": {
            "message": "Pickup schedule deleted successfully.",
            "id": int(id)
        },
        "error": None
    }), 200


# =========================
# DELIVERY RECORDS
# =========================

@app.route("/delivery-records", methods=["POST"])
def createDeliveryRecord():
    data = request.get_json(silent=True) or {}

    errors = {}

    if not data.get("delivery_date"):
        errors["delivery_date"] = "Delivery date is required."

    if not data.get("customer"):
        errors["customer"] = "Customer is required."

    if errors:
        return jsonify({
            "status": 422,
            "data": None,
            "error": {
                "code": "VALIDATION_ERROR",
                "message": "Validation failed.",
                "fields": errors
            }
        }), 422

    conn = get_db_connection()

    cursor = conn.execute(
        """
        INSERT INTO delivery_records (customer, delivery_date)
        VALUES (?, ?)
        """,
        (
            data["customer"],
            data["delivery_date"]
        )
    )

    delivery_id = cursor.lastrowid

    conn.commit()
    conn.close()

    return jsonify({
        "status": 201,
        "data": {
            "id": delivery_id,
            "customer": data["customer"],
            "delivery_date": data["delivery_date"]
        },
        "error": None
    }), 201


@app.route("/delivery-records", methods=["GET"])
def listDeliveryRecords():
    conn = get_db_connection()

    records = conn.execute(
        """
        SELECT id, customer, delivery_date
        FROM delivery_records
        ORDER BY id
        """
    ).fetchall()

    conn.close()

    return jsonify({
        "status": 200,
        "data": [dict(record) for record in records],
        "error": None
    }), 200


@app.route("/delivery-records/<id>", methods=["GET"])
def showDeliveryRecord(id):
    conn = get_db_connection()

    record = conn.execute(
        """
        SELECT id, customer, delivery_date
        FROM delivery_records
        WHERE id = ?
        """,
        (id,)
    ).fetchone()

    conn.close()

    if record is None:
        return jsonify({
            "status": 404,
            "data": None,
            "error": {
                "code": "NOT_FOUND",
                "message": "Delivery record not found."
            }
        }), 404

    return jsonify({
        "status": 200,
        "data": dict(record),
        "error": None
    }), 200


@app.route("/delivery-records/<id>", methods=["PUT"])
def updateDeliveryRecord(id):
    data = request.get_json(silent=True) or {}

    errors = {}

    if not data.get("delivery_date"):
        errors["delivery_date"] = "Delivery date is required."

    if not data.get("customer"):
        errors["customer"] = "Customer is required."

    if errors:
        return jsonify({
            "status": 422,
            "data": None,
            "error": {
                "code": "VALIDATION_ERROR",
                "message": "Validation failed.",
                "fields": errors
            }
        }), 422

    conn = get_db_connection()

    record = conn.execute(
        """
        SELECT id
        FROM delivery_records
        WHERE id = ?
        """,
        (id,)
    ).fetchone()

    if record is None:
        conn.close()

        return jsonify({
            "status": 404,
            "data": None,
            "error": {
                "code": "NOT_FOUND",
                "message": "Delivery record not found."
            }
        }), 404

    conn.execute(
        """
        UPDATE delivery_records
        SET customer = ?, delivery_date = ?
        WHERE id = ?
        """,
        (
            data["customer"],
            data["delivery_date"],
            id
        )
    )

    conn.commit()
    conn.close()

    return jsonify({
        "status": 200,
        "data": {
            "id": int(id),
            "customer": data["customer"],
            "delivery_date": data["delivery_date"]
        },
        "error": None
    }), 200


@app.route("/delivery-records/<id>", methods=["DELETE"])
def deleteDeliveryRecord(id):
    conn = get_db_connection()

    record = conn.execute(
        """
        SELECT id
        FROM delivery_records
        WHERE id = ?
        """,
        (id,)
    ).fetchone()

    if record is None:
        conn.close()

        return jsonify({
            "status": 404,
            "data": None,
            "error": {
                "code": "NOT_FOUND",
                "message": "Delivery record not found."
            }
        }), 404

    conn.execute(
        """
        DELETE FROM delivery_records
        WHERE id = ?
        """,
        (id,)
    )

    conn.commit()
    conn.close()

    return jsonify({
        "status": 200,
        "data": {
            "message": "Delivery record deleted successfully.",
            "id": int(id)
        },
        "error": None
    }), 200


# =========================
# PAYMENTS
# =========================

@app.route("/payments", methods=["POST"])
def createPayment():
    data = request.get_json(silent=True) or {}

    errors = {}

    if "payment_amount" not in data:
        errors["payment_amount"] = "Payment amount is required."
    else:
        try:
            payment_amount = float(data["payment_amount"])

            if payment_amount <= 0:
                errors["payment_amount"] = (
                    "Payment amount must be greater than zero."
                )

        except (TypeError, ValueError):
            errors["payment_amount"] = "Payment amount must be a number."

    if not data.get("payment_method"):
        errors["payment_method"] = "Payment method is required."

    if errors:
        return jsonify({
            "status": 422,
            "data": None,
            "error": {
                "code": "VALIDATION_ERROR",
                "message": "Validation failed.",
                "fields": errors
            }
        }), 422

    conn = get_db_connection()

    cursor = conn.execute(
        """
        INSERT INTO payments (payment_amount, payment_method)
        VALUES (?, ?)
        """,
        (
            payment_amount,
            data["payment_method"]
        )
    )

    payment_id = cursor.lastrowid

    conn.commit()
    conn.close()

    return jsonify({
        "status": 201,
        "data": {
            "id": payment_id,
            "payment_amount": payment_amount,
            "payment_method": data["payment_method"]
        },
        "error": None
    }), 201


@app.route("/payments", methods=["GET"])
def listPayments():
    conn = get_db_connection()

    payments = conn.execute(
        """
        SELECT id, payment_amount, payment_method
        FROM payments
        ORDER BY id
        """
    ).fetchall()

    conn.close()

    return jsonify({
        "status": 200,
        "data": [dict(payment) for payment in payments],
        "error": None
    }), 200


@app.route("/payments/<id>", methods=["GET"])
def showPayment(id):
    conn = get_db_connection()

    payment = conn.execute(
        """
        SELECT id, payment_amount, payment_method
        FROM payments
        WHERE id = ?
        """,
        (id,)
    ).fetchone()

    conn.close()

    if payment is None:
        return jsonify({
            "status": 404,
            "data": None,
            "error": {
                "code": "NOT_FOUND",
                "message": "Payment not found."
            }
        }), 404

    return jsonify({
        "status": 200,
        "data": dict(payment),
        "error": None
    }), 200


@app.route("/payments/<id>", methods=["PUT"])
def updatePayment(id):
    data = request.get_json(silent=True) or {}

    errors = {}

    if "payment_amount" not in data:
        errors["payment_amount"] = "Payment amount is required."
    else:
        try:
            payment_amount = float(data["payment_amount"])

            if payment_amount <= 0:
                errors["payment_amount"] = (
                    "Payment amount must be greater than zero."
                )

        except (TypeError, ValueError):
            errors["payment_amount"] = "Payment amount must be a number."

    if not data.get("payment_method"):
        errors["payment_method"] = "Payment method is required."

    if errors:
        return jsonify({
            "status": 422,
            "data": None,
            "error": {
                "code": "VALIDATION_ERROR",
                "message": "Validation failed.",
                "fields": errors
            }
        }), 422

    conn = get_db_connection()

    payment = conn.execute(
        """
        SELECT id
        FROM payments
        WHERE id = ?
        """,
        (id,)
    ).fetchone()

    if payment is None:
        conn.close()

        return jsonify({
            "status": 404,
            "data": None,
            "error": {
                "code": "NOT_FOUND",
                "message": "Payment not found."
            }
        }), 404

    conn.execute(
        """
        UPDATE payments
        SET payment_amount = ?, payment_method = ?
        WHERE id = ?
        """,
        (
            payment_amount,
            data["payment_method"],
            id
        )
    )

    conn.commit()
    conn.close()

    return jsonify({
        "status": 200,
        "data": {
            "id": int(id),
            "payment_amount": payment_amount,
            "payment_method": data["payment_method"]
        },
        "error": None
    }), 200


@app.route("/payments/<id>", methods=["DELETE"])
def deletePayment(id):
    conn = get_db_connection()

    payment = conn.execute(
        """
        SELECT id
        FROM payments
        WHERE id = ?
        """,
        (id,)
    ).fetchone()

    if payment is None:
        conn.close()

        return jsonify({
            "status": 404,
            "data": None,
            "error": {
                "code": "NOT_FOUND",
                "message": "Payment not found."
            }
        }), 404

    conn.execute(
        """
        DELETE FROM payments
        WHERE id = ?
        """,
        (id,)
    )

    conn.commit()
    conn.close()

    return jsonify({
        "status": 200,
        "data": {
            "message": "Payment deleted successfully.",
            "id": int(id)
        },
        "error": None
    }), 200


# =========================
# RUN APPLICATION
# =========================

if __name__ == "__main__":
    app.run(debug=True)