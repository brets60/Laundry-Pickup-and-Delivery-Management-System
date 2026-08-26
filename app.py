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

    return jsonify({
        "status": 201,
        "data": {
            "message": "createLaundryOrder stub"
        },
        "error": None
    }), 201


@app.route("/laundry-orders", methods=["GET"])
def listLaundryOrders():
    return jsonify({
        "status": 200,
        "data": {
            "message": "listLaundryOrders stub"
        },
        "error": None
    }), 200


@app.route("/laundry-orders/<id>", methods=["GET"])
def showLaundryOrder(id):
    return jsonify({
        "status": 200,
        "data": {
            "message": "showLaundryOrder stub",
            "id": id
        },
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

    return jsonify({
        "status": 200,
        "data": {
            "message": "updateLaundryOrder stub",
            "id": id
        },
        "error": None
    }), 200


@app.route("/laundry-orders/<id>", methods=["DELETE"])
def deleteLaundryOrder(id):
    return jsonify({
        "status": 200,
        "data": {
            "message": "deleteLaundryOrder stub",
            "id": id
        },
        "error": None
    }), 200


# =========================
# PICKUP SCHEDULES
# =========================

@app.route("/pickup-schedules", methods=["GET"])
def listPickupSchedules():
    return jsonify({
        "status": 200,
        "data": {
            "message": "listPickupSchedules stub"
        },
        "error": None
    }), 200


@app.route("/pickup-schedules/<id>", methods=["GET"])
def showPickupSchedule(id):
    return jsonify({
        "status": 200,
        "data": {
            "message": "showPickupSchedule stub",
            "id": id
        },
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

    return jsonify({
        "status": 200,
        "data": {
            "message": "updatePickupSchedule stub",
            "id": id
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

    return jsonify({
        "status": 201,
        "data": {
            "message": "createPickupSchedule stub"
        },
        "error": None
    }), 201


@app.route("/pickup-schedules/<id>", methods=["DELETE"])
def deletePickupSchedule(id):
    return jsonify({
        "status": 200,
        "data": {
            "message": "deletePickupSchedule stub",
            "id": id
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

    return jsonify({
        "status": 201,
        "data": {
            "message": "createDeliveryRecord stub"
        },
        "error": None
    }), 201


@app.route("/delivery-records", methods=["GET"])
def listDeliveryRecords():
    return jsonify({
        "status": 200,
        "data": {
            "message": "listDeliveryRecords stub"
        },
        "error": None
    }), 200


@app.route("/delivery-records/<id>", methods=["GET"])
def showDeliveryRecord(id):
    return jsonify({
        "status": 200,
        "data": {
            "message": "showDeliveryRecord stub",
            "id": id
        },
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

    return jsonify({
        "status": 200,
        "data": {
            "message": "updateDeliveryRecord stub",
            "id": id
        },
        "error": None
    }), 200


@app.route("/delivery-records/<id>", methods=["DELETE"])
def deleteDeliveryRecord(id):
    return jsonify({
        "status": 200,
        "data": {
            "message": "deleteDeliveryRecord stub",
            "id": id
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

    return jsonify({
        "status": 201,
        "data": {
            "message": "createPayment stub"
        },
        "error": None
    }), 201


@app.route("/payments", methods=["GET"])
def listPayments():
    return jsonify({
        "status": 200,
        "data": {
            "message": "listPayments stub"
        },
        "error": None
    }), 200


@app.route("/payments/<id>", methods=["GET"])
def showPayment(id):
    return jsonify({
        "status": 200,
        "data": {
            "message": "showPayment stub",
            "id": id
        },
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

    return jsonify({
        "status": 200,
        "data": {
            "message": "updatePayment stub",
            "id": id
        },
        "error": None
    }), 200


@app.route("/payments/<id>", methods=["DELETE"])
def deletePayment(id):
    return jsonify({
        "status": 200,
        "data": {
            "message": "deletePayment stub",
            "id": id
        },
        "error": None
    }), 200


# =========================
# RUN APPLICATION
# =========================

if __name__ == "__main__":
    app.run(debug=True)