from flask import Blueprint, render_template, request, redirect, url_for
import sqlite3

# Initialize Blueprint
customer_bp = Blueprint('customer', __name__)
DATABASE = "laundry.db"


# Helper function to connect to the database
def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


# ==========================================
# 1. READ LIST & CREATE CUSTOMER
# ==========================================
@customer_bp.route('/customers-page', methods=['GET', 'POST'])
def manage_customers():
    conn = get_db_connection()

    if request.method == 'POST':
        name = request.form.get('name')
        contact_number = request.form.get('contact_number')

        # VALIDATION (Fixes the 6/12 points!)
        if not name or not contact_number:
            return "Validation Error: Customer Name and Contact Number are required.", 422

        # CREATE: Save to database
        conn.execute("INSERT INTO customers (name, contact_number) VALUES (?, ?)", (name, contact_number))
        conn.commit()
        return redirect('/customers-page')

    # READ: Get all customers from database
    customers = conn.execute("SELECT * FROM customers").fetchall()
    conn.close()

    return render_template('customers.html', customers=customers)


# ==========================================
# 2. READ CUSTOMER DETAILS
# ==========================================
@customer_bp.route('/customers-page/details/<int:customer_id>')
def customer_details(customer_id):
    conn = get_db_connection()
    customer = conn.execute("SELECT * FROM customers WHERE id = ?", (customer_id,)).fetchone()
    conn.close()

    if customer is None:
        return "Customer Not Found", 404

    return render_template('customer_details.html', customer=customer)


# ==========================================
# 3. UPDATE CUSTOMER
# ==========================================
@customer_bp.route('/customers-page/edit/<int:customer_id>', methods=['GET', 'POST'])
def edit_customer(customer_id):
    conn = get_db_connection()
    customer = conn.execute("SELECT * FROM customers WHERE id = ?", (customer_id,)).fetchone()

    if request.method == 'POST':
        name = request.form.get('name')
        contact_number = request.form.get('contact_number')

        if not name or not contact_number:
            return "Validation Error: Customer Name and Contact Number are required.", 422

        conn.execute("UPDATE customers SET name = ?, contact_number = ? WHERE id = ?",
                     (name, contact_number, customer_id))
        conn.commit()
        conn.close()
        return redirect('/customers-page')

    conn.close()
    return render_template('edit_customer.html', customer=customer)


# ==========================================
# 4. DELETE CUSTOMER
# ==========================================
@customer_bp.route('/customers-page/delete/<int:customer_id>', methods=['POST'])
def delete_customer(customer_id):
    conn = get_db_connection()
    conn.execute("DELETE FROM customers WHERE id = ?", (customer_id,))
    conn.commit()
    conn.close()
    return redirect('/customers-page')