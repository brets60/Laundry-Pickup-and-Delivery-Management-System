from flask import jsonify


def validation_error_response(fields_dict):
    return jsonify({
        "status": 422,
        "data": None,
        "error": {
            "code": "VALIDATION_ERROR",
            "message": "Validation failed.",
            "fields": fields_dict
        }
    }), 422


def not_found_response(message):
    return jsonify({
        "status": 404,
        "data": None,
        "error": {
            "code": "NOT_FOUND",
            "message": message
        }
    }), 404


def success_response(data, status_code=200):
    return jsonify({
        "status": status_code,
        "data": data,
        "error": None
    }), status_code


def _is_blank_string(val):
    if val is None:
        return True
    if isinstance(val, str) and not val.strip():
        return True
    return False


def _parse_positive_number(val, field_label):
    if isinstance(val, bool):
        return None, f"{field_label} must be a number."
    try:
        num = float(val)
        if num != num or num == float("inf") or num == float("-inf"):
            return None, f"{field_label} must be a number."
        if num <= 0:
            return None, f"{field_label} must be greater than zero."
        return num, None
    except (TypeError, ValueError):
        return None, f"{field_label} must be a number."


def validate_customer_payload(data):
    if not isinstance(data, dict):
        data = {}

    errors = {}
    name = data.get("name")
    contact_number = data.get("contact_number")

    if _is_blank_string(name):
        errors["name"] = "Name is required."

    if _is_blank_string(contact_number):
        errors["contact_number"] = "Contact number is required."

    if errors:
        return None, errors

    return {
        "name": str(name).strip(),
        "contact_number": str(contact_number).strip()
    }, {}


def validate_laundry_order_payload(data):
    if not isinstance(data, dict):
        data = {}

    errors = {}
    customer = data.get("customer")

    if _is_blank_string(customer):
        errors["customer"] = "Customer is required."

    if "laundry_weight" not in data or _is_blank_string(data.get("laundry_weight")):
        errors["laundry_weight"] = "Laundry weight is required."
        laundry_weight = None
    else:
        laundry_weight, weight_err = _parse_positive_number(
            data["laundry_weight"], "Laundry weight"
        )
        if weight_err:
            errors["laundry_weight"] = weight_err

    if errors:
        return None, errors

    return {
        "customer": str(customer).strip(),
        "laundry_weight": laundry_weight
    }, {}


def validate_pickup_schedule_payload(data):
    if not isinstance(data, dict):
        data = {}

    errors = {}
    pickup_date = data.get("pickup_date")
    customer = data.get("customer")

    if _is_blank_string(pickup_date):
        errors["pickup_date"] = "Pickup date is required."

    if _is_blank_string(customer):
        errors["customer"] = "Customer is required."

    if errors:
        return None, errors

    return {
        "customer": str(customer).strip(),
        "pickup_date": str(pickup_date).strip()
    }, {}


def validate_delivery_record_payload(data):
    if not isinstance(data, dict):
        data = {}

    errors = {}
    delivery_date = data.get("delivery_date")
    customer = data.get("customer")

    if _is_blank_string(delivery_date):
        errors["delivery_date"] = "Delivery date is required."

    if _is_blank_string(customer):
        errors["customer"] = "Customer is required."

    if errors:
        return None, errors

    return {
        "customer": str(customer).strip(),
        "delivery_date": str(delivery_date).strip()
    }, {}


def validate_payment_payload(data):
    if not isinstance(data, dict):
        data = {}

    errors = {}
    customer = data.get("customer")
    payment_method = data.get("payment_method")

    if _is_blank_string(customer):
        errors["customer"] = "Customer is required."

    if "payment_amount" not in data or _is_blank_string(data.get("payment_amount")):
        errors["payment_amount"] = "Payment amount is required."
        payment_amount = None
    else:
        payment_amount, amount_err = _parse_positive_number(
            data["payment_amount"], "Payment amount"
        )
        if amount_err:
            errors["payment_amount"] = amount_err

    if _is_blank_string(payment_method):
        errors["payment_method"] = "Payment method is required."

    if errors:
        return None, errors

    return {
        "customer": str(customer).strip(),
        "payment_amount": payment_amount,
        "payment_method": str(payment_method).strip()
    }, {}
