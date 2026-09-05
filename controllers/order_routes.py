from flask import Blueprint, render_template, request, redirect
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
        customer = request.form.get('customer')
        laundry_weight = request.form.get('laundry_weight')

        # VALIDATION (Fixes the 6/12 points!)
        if not customer or not laundry_weight:
            return "Validation Error: Customer Name and Laundry Weight are required.", 422

        # CREATE: Save to database
        conn.execute("INSERT INTO laundry_orders (customer, laundry_weight) VALUES (?, ?)",
                     (customer, float(laundry_weight)))
        conn.commit()
        return redirect('/laundry-orders-page')

    # READ: Get all orders
    orders = conn.execute("SELECT * FROM laundry_orders").fetchall()

    # We also pass 'customers' to the template so the Add Order form can have a dropdown list of customers!
    customers = conn.execute("SELECT name FROM customers").fetchall()
    conn.close()

    return render_template('orders.html', orders=orders, customers=customers)


# ==========================================
# 2. READ ORDER DETAILS
# ==========================================
@order_bp.route('/laundry-orders-page/details/<int:order_id>')
def order_details(order_id):
    conn = get_db_connection()
    order = conn.execute("SELECT * FROM laundry_orders WHERE id = ?", (order_id,)).fetchone()
    conn.close()

    if order is None:
        return "Order Not Found", 404

    return render_template('order_details.html', order=order)


# ==========================================
# 3. UPDATE ORDER
# ==========================================
@order_bp.route('/laundry-orders-page/edit/<int:order_id>', methods=['GET', 'POST'])
def edit_order(order_id):
    conn = get_db_connection()
    order = conn.execute("SELECT * FROM laundry_orders WHERE id = ?", (order_id,)).fetchone()

    if request.method == 'POST':
        customer = request.form.get('customer')
        laundry_weight = request.form.get('laundry_weight')

        if not customer or not laundry_weight:
            return "Validation Error: Customer Name and Laundry Weight are required.", 422

        conn.execute("UPDATE laundry_orders SET customer = ?, laundry_weight = ? WHERE id = ?",
                     (customer, float(laundry_weight), order_id))
        conn.commit()
        conn.close()
        return redirect('/laundry-orders-page')

    # Get customers for the dropdown menu
    customers = conn.execute("SELECT name FROM customers").fetchall()
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