from flask import Blueprint, render_template, request, redirect, flash
import sqlite3

order_bp = Blueprint('order', __name__)
DATABASE = "laundry.db"


def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


# ==========================================
# 1. READ LIST & CREATE ORDER
# ==========================================
@order_bp.route('/laundry-orders-page', methods=['GET', 'POST'])
def manage_orders():
    conn = get_db_connection()

    if request.method == 'POST':
        customer = request.form.get('customer', '').strip()
        laundry_weight = request.form.get('laundry_weight', '').strip()
        service_type = request.form.get('service_type', 'Wash & Fold').strip()
        status = request.form.get('status', 'Received').strip()
        price_input = request.form.get('total_price', '').strip()

        # Validation
        if not customer or not laundry_weight:
            conn.close()
            return "Validation Error: Customer Name and Laundry Weight are required.", 422

        try:
            weight_val = float(laundry_weight)
            price_val = float(price_input) if price_input else (weight_val * 50.0)
        except ValueError:
            conn.close()
            return "Validation Error: Invalid number for weight or price.", 422

        # Insert new order
        conn.execute(
            """
            INSERT INTO laundry_orders (customer, laundry_weight, service_type, total_price, status, created_at)
            VALUES (?, ?, ?, ?, ?, datetime('now'))
            """,
            (customer, weight_val, service_type, price_val, status)
        )
        conn.commit()
        conn.close()
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
        return "Order Not Found", 404

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
        return "Order Not Found", 404

    return render_template('order_details.html', order=order, print_mode=True)


# ==========================================
# 3. UPDATE ORDER
# ==========================================
@order_bp.route('/laundry-orders-page/edit/<int:order_id>', methods=['GET', 'POST'])
def edit_order(order_id):
    conn = get_db_connection()
    order = conn.execute("SELECT * FROM laundry_orders WHERE id = ?", (order_id,)).fetchone()

    if order is None:
        conn.close()
        return "Order Not Found", 404

    if request.method == 'POST':
        customer = request.form.get('customer', '').strip()
        laundry_weight = request.form.get('laundry_weight', '').strip()
        service_type = request.form.get('service_type', 'Wash & Fold').strip()
        status = request.form.get('status', 'Received').strip()
        price_input = request.form.get('total_price', '').strip()

        if not customer or not laundry_weight:
            conn.close()
            return "Validation Error: Customer Name and Laundry Weight are required.", 422

        try:
            weight_val = float(laundry_weight)
            price_val = float(price_input) if price_input else (weight_val * 50.0)
        except ValueError:
            conn.close()
            return "Validation Error: Invalid number for weight or price.", 422

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
        return redirect('/laundry-orders-page')

    customers = conn.execute("SELECT name FROM customers ORDER BY name ASC").fetchall()
    conn.close()

    return render_template('edit_order.html', order=order, customers=customers)


# ==========================================
# 4. DELETE ORDER
# ==========================================
@order_bp.route('/laundry-orders-page/delete/<int:order_id>', methods=['POST'])
def delete_order(order_id):
    conn = get_db_connection()
    conn.execute("DELETE FROM laundry_orders WHERE id = ?", (order_id,))
    conn.commit()
    conn.close()
    return redirect('/laundry-orders-page')