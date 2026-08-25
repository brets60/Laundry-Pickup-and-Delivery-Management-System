from flask import Flask, jsonify, request

app = Flask(__name__)


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

    return jsonify({
        "status": 201,
        "data": {
            "message": "createCustomer stub"
        },
        "error": None
    }), 201

@app.route("/customers", methods=["GET"])
def listCustomers():
    return jsonify({
        "status": 200,
        "data": {
            "message": "listCustomers stub"
        },
        "error": None
    }), 200


@app.route("/customers/<id>", methods=["GET"])
def showCustomer(id):
    return jsonify({
        "status": 200,
        "data": {
            "message": "showCustomer stub",
            "id": id
        },
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

    return jsonify({
        "status": 200,
        "data": {
            "message": "updateCustomer stub",
            "id": id
        },
        "error": None
    }), 200


@app.route("/customers/<id>", methods=["DELETE"])
def deleteCustomer(id):
    return jsonify({
        "status": 200,
        "data": {
            "message": "deleteCustomer stub",
            "id": id
        },
        "error": None
    }), 200

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
                errors["laundry_weight"] = "Laundry weight must be greater than zero."

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
                errors["laundry_weight"] = "Laundry weight must be greater than zero."

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
                errors["payment_amount"] = "Payment amount must be greater than zero."

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
                errors["payment_amount"] = "Payment amount must be greater than zero."

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

if __name__ == "__main__":
    app.run(debug=True)