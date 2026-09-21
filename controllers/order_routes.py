from flask import Blueprint, render_template, request, redirect, flash, jsonify
import sqlite3

order_bp = Blueprint('order', __name__)
DATABASE = "laundry.db"


def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def is_async_request():
    return (
        request.is_json
        or request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        or 'application/json' in request.headers.get('Accept', '')
    )


# ==========================================
# 1. READ LIST & CREATE ORDER
# ==========================================
@order_bp.route('/laundry-orders-page', methods=['GET', 'POST'])
def manage_orders():
    conn = get_db_connection()

    if request.method == 'POST':
        is_async = is_async_request()
        data = request.get_json(silent=True) if request.is_json else request.form
        customer = str(data.get('customer') or '').strip()
        laundry_weight = str(data.get('laundry_weight') or '').strip()
        service_type = str(data.get('service_type') or 'Wash & Fold').strip()
        status = str(data.get('status') or 'Received').strip()
        price_input = str(data.get('total_price') or '').strip()

        # Structured Validation
        errors = {}
        if not customer:
            errors['customer'] = "Customer Name is required."
        if not laundry_weight:
            errors['laundry_weight'] = "Laundry Weight is required."
        else:
            try:
                weight_val = float(laundry_weight)
                if weight_val <= 0:
                    errors['laundry_weight'] = "Weight must be greater than 0 kg."
            except ValueError:
                errors['laundry_weight'] = "Weight must be a valid number."

        price_val = 0.0
        if price_input:
            try:
                price_val = float(price_input)
                if price_val < 0:
                    errors['total_price'] = "Total price cannot be negative."
            except ValueError:
                errors['total_price'] = "Total price must be a valid number."
        elif 'laundry_weight' not in errors:
            price_val = weight_val * 50.0

        if errors:
            conn.close()
            if is_async:
                return jsonify({"status": 422, "error": errors}), 422
            first_err = next(iter(errors.values()))
            return f"Validation Error: {first_err}", 422

        # Insert new order
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO laundry_orders (customer, laundry_weight, service_type, total_price, status, created_at)
            VALUES (?, ?, ?, ?, ?, datetime('now'))
            """,
            (customer, weight_val, service_type, price_val, status)
        )
        new_id = cursor.lastrowid
        conn.commit()
        conn.close()

        if is_async:
            return jsonify({
                "status": 201,
                "message": f"Order #ORD-{new_id:04d} created successfully!",
                "data": {
                    "id": new_id,
                    "order_code": f"ORD-{new_id:04d}",
                    "customer": customer,
                    "laundry_weight": weight_val,
                    "service_type": service_type,
                    "total_price": price_val,
                    "status": status,
                    "created_at": "Today"
                }
            }), 201

        return redirect('/laundry-orders-page')

    # KPI Statistics
    total_orders = conn.execute("SELECT COUNT(*) FROM laundry_orders").fetchone()[0]
    total_weight = conn.execute("SELECT COALESCE(SUM(laundry_weight), 0) FROM laundry_orders").fetchone()[0]
    in_wash_count = conn.execute("SELECT COUNT(*) FROM laundry_orders WHERE LOWER(COALESCE(status, '')) = 'in wash'").fetchone()[0]
    ready_count = conn.execute("SELECT COUNT(*) FROM laundry_orders WHERE LOWER(COALESCE(status, '')) = 'ready'").fetchone()[0]

    # Query all orders with customer phone
    orders = conn.execute(
        """
        SELECT o.*, c.contact_number
        FROM laundry_orders o
        LEFT JOIN customers c ON o.customer = c.name
        ORDER BY o.id DESC
        """
    ).fetchall()

    customers = conn.execute("SELECT * FROM customers ORDER BY name ASC").fetchall()
    conn.close()

    return render_template(
        'orders.html',
        orders=orders,
        customers=customers,
        total_orders=total_orders,
        total_weight=round(total_weight, 1),
        in_wash_count=in_wash_count,
        ready_count=ready_count
    )


# ==========================================
# 2. READ ORDER DETAILS / PRINT TAG
# ==========================================
@order_bp.route('/laundry-orders-page/details/<int:order_id>')
def order_details(order_id):
    conn = get_db_connection()
    order = conn.execute(
        """
        SELECT o.*, c.contact_number
        FROM laundry_orders o
        LEFT JOIN customers c ON o.customer = c.name
        WHERE o.id = ?
        """,
        (order_id,)
    ).fetchone()
    conn.close()

    if order is None:
        if is_async_request():
            return jsonify({"status": 404, "error": "Order not found or has been deleted."}), 404
        return render_template('404.html', message=f"Order #ORD-{order_id:04d} was not found or has been removed."), 404

    return render_template('order_details.html', order=order)


@order_bp.route('/laundry-orders-page/print/<int:order_id>')
def print_order_tag(order_id):
    conn = get_db_connection()
    order = conn.execute(
        """
        SELECT o.*, c.contact_number
        FROM laundry_orders o
        LEFT JOIN customers c ON o.customer = c.name
        WHERE o.id = ?
        """,
        (order_id,)
    ).fetchone()
    conn.close()

    if order is None:
        if is_async_request():
            return jsonify({"status": 404, "error": "Order not found."}), 404
        return render_template('404.html', message=f"Order tag for #ORD-{order_id:04d} cannot be printed because the record does not exist."), 404

    return render_template('order_details.html', order=order, print_mode=True)


# ==========================================
# 3. UPDATE ORDER
# ==========================================
@order_bp.route('/laundry-orders-page/edit/<int:order_id>', methods=['GET', 'POST', 'PUT'])
def edit_order(order_id):
    conn = get_db_connection()
    order = conn.execute("SELECT * FROM laundry_orders WHERE id = ?", (order_id,)).fetchone()

    if order is None:
        conn.close()
        if is_async_request():
            return jsonify({"status": 404, "error": "Order not found."}), 404
        return render_template('404.html', message=f"Cannot edit Order #ORD-{order_id:04d} because it does not exist."), 404

    if request.method in ['POST', 'PUT']:
        is_async = is_async_request()
        data = request.get_json(silent=True) if request.is_json else request.form
        customer = str(data.get('customer') or '').strip()
        laundry_weight = str(data.get('laundry_weight') or '').strip()
        service_type = str(data.get('service_type') or 'Wash & Fold').strip()
        status = str(data.get('status') or 'Received').strip()
        price_input = str(data.get('total_price') or '').strip()

        errors = {}
        if not customer:
            errors['customer'] = "Customer Name is required."
        if not laundry_weight:
            errors['laundry_weight'] = "Laundry Weight is required."
        else:
            try:
                weight_val = float(laundry_weight)
                if weight_val <= 0:
                    errors['laundry_weight'] = "Weight must be greater than 0 kg."
            except ValueError:
                errors['laundry_weight'] = "Weight must be a valid number."

        price_val = 0.0
        if price_input:
            try:
                price_val = float(price_input)
                if price_val < 0:
                    errors['total_price'] = "Total price cannot be negative."
            except ValueError:
                errors['total_price'] = "Total price must be a valid number."
        elif 'laundry_weight' not in errors:
            price_val = weight_val * 50.0

        if errors:
            conn.close()
            if is_async:
                return jsonify({"status": 422, "error": errors}), 422
            first_err = next(iter(errors.values()))
            return f"Validation Error: {first_err}", 422

        conn.execute(
            """
            UPDATE laundry_orders
            SET customer = ?, laundry_weight = ?, service_type = ?, total_price = ?, status = ?
            WHERE id = ?
            """,
            (customer, weight_val, service_type, price_val, status, order_id)
        )
        conn.commit()
        conn.close()

        if is_async:
            return jsonify({
                "status": 200,
                "message": f"Order #ORD-{order_id:04d} updated successfully!",
                "data": {
                    "id": order_id,
                    "order_code": f"ORD-{order_id:04d}",
                    "customer": customer,
                    "laundry_weight": weight_val,
                    "service_type": service_type,
                    "total_price": price_val,
                    "status": status
                }
            }), 200

        return redirect('/laundry-orders-page')

    customers = conn.execute("SELECT name FROM customers ORDER BY name ASC").fetchall()
    conn.close()

    return render_template('edit_order.html', order=order, customers=customers)


# ==========================================
# 4. DELETE ORDER
# ==========================================
@order_bp.route('/laundry-orders-page/delete/<int:order_id>', methods=['POST', 'DELETE'])
def delete_order(order_id):
    conn = get_db_connection()
    order = conn.execute("SELECT * FROM laundry_orders WHERE id = ?", (order_id,)).fetchone()
    if order is None:
        conn.close()
        if is_async_request():
            return jsonify({"status": 404, "error": "Order not found or already deleted."}), 404
        flash("Order not found or already deleted.", "warning")
        return redirect('/laundry-orders-page')

    conn.execute("DELETE FROM laundry_orders WHERE id = ?", (order_id,))
    conn.commit()
    conn.close()

    if is_async_request():
        return jsonify({
            "status": 200,
            "message": f"Order #ORD-{order_id:04d} deleted successfully.",
            "id": order_id
        }), 200

    return redirect('/laundry-orders-page')