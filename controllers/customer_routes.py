from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
import sqlite3

customer_bp = Blueprint('customer', __name__)
DATABASE = "laundry.db"


def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.execute("PRAGMA foreign_keys = ON;")
    conn.row_factory = sqlite3.Row
    return conn


def is_authenticated():
    return "user_id" in session


def is_async_request():
    return (
        request.is_json
        or request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        or 'application/json' in request.headers.get('Accept', '')
    )


# ==========================================
# 1. READ LIST & CREATE CUSTOMER
# ==========================================
@customer_bp.route('/customers-page', methods=['GET', 'POST'])
def manage_customers():
    conn = get_db_connection()

    if request.method == 'POST':
        is_async = is_async_request()
        data = request.get_json(silent=True) if request.is_json else request.form
        name = (data.get('name') or '').strip()
        contact_number = (data.get('contact_number') or '').strip()
        email = (data.get('email') or '').strip()
        address = (data.get('address') or 'Kalagutay, Base Camp, Maramag, Bukidnon').strip()
        membership = (data.get('membership') or 'Regular').strip()

        # Structured Validation
        errors = {}
        if not name:
            errors['name'] = "Customer Name is required."
        if not contact_number:
            errors['contact_number'] = "Contact Number is required."

        if errors:
            conn.close()
            if is_async:
                return jsonify({"status": 422, "error": errors}), 422
            return "Validation Error: Customer Name and Contact Number are required.", 422

        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO customers (name, contact_number, email, address, membership)
            VALUES (?, ?, ?, ?, ?)
            """,
            (name, contact_number, email, address, membership)
        )
        new_id = cursor.lastrowid
        conn.commit()
        conn.close()

        if is_async:
            return jsonify({
                "status": 201,
                "message": f"Customer '{name}' registered successfully!",
                "data": {
                    "id": new_id,
                    "name": name,
                    "contact_number": contact_number,
                    "email": email,
                    "address": address,
                    "membership": membership
                }
            }), 201

        return redirect('/customers-page')

    # READ: Get all customers and aggregate stats
    customers = conn.execute("""
        SELECT c.*, 
               (SELECT COUNT(*) FROM laundry_orders o WHERE o.customer = c.name) as order_count,
               (SELECT COALESCE(SUM(total_price), 0) FROM laundry_orders o WHERE o.customer = c.name) as total_spent
        FROM customers c
        ORDER BY c.id DESC
    """).fetchall()

    stats = {
        "total": len(customers),
        "vip": sum(1 for c in customers if (c['membership'] or '').upper() in ['VIP', 'GOLD']),
        "repeat": sum(1 for c in customers if (c['order_count'] or 0) > 1),
        "pending_balance": sum(float(c['pending_balance'] or 0.0) for c in customers)
    }

    conn.close()
    return render_template('customers.html', customers=customers, stats=stats)


# ==========================================
# 2. READ CUSTOMER DETAILS
# ==========================================
@customer_bp.route('/customers-page/details/<int:customer_id>')
def customer_details(customer_id):
    conn = get_db_connection()
    customer = conn.execute("SELECT * FROM customers WHERE id = ?", (customer_id,)).fetchone()
    if customer is None:
        conn.close()
        return "Customer Not Found", 404

    orders = conn.execute("SELECT * FROM laundry_orders WHERE customer = ? ORDER BY id DESC", (customer['name'],)).fetchall()
    conn.close()
    return render_template('customer_details.html', customer=customer, orders=orders)


# ==========================================
# 3. UPDATE CUSTOMER
# ==========================================
@customer_bp.route('/customers-page/edit/<int:customer_id>', methods=['GET', 'POST', 'PUT'])
def edit_customer(customer_id):
    conn = get_db_connection()
    customer = conn.execute("SELECT * FROM customers WHERE id = ?", (customer_id,)).fetchone()

    if customer is None:
        conn.close()
        return "Customer Not Found", 404

    if request.method in ['POST', 'PUT']:
        is_async = is_async_request()
        data = request.get_json(silent=True) if request.is_json else request.form
        name = (data.get('name') or '').strip()
        contact_number = (data.get('contact_number') or '').strip()
        email = (data.get('email') or '').strip()
        address = (data.get('address') or 'Kalagutay, Base Camp, Maramag, Bukidnon').strip()
        membership = (data.get('membership') or 'Regular').strip()

        errors = {}
        if not name:
            errors['name'] = "Customer Name is required."
        if not contact_number:
            errors['contact_number'] = "Contact Number is required."

        if errors:
            conn.close()
            if is_async:
                return jsonify({"status": 422, "error": errors}), 422
            return "Validation Error: Customer Name and Contact Number are required.", 422

        conn.execute(
            """
            UPDATE customers 
            SET name = ?, contact_number = ?, email = ?, address = ?, membership = ? 
            WHERE id = ?
            """,
            (name, contact_number, email, address, membership, customer_id)
        )
        conn.commit()
        conn.close()

        if is_async:
            return jsonify({
                "status": 200,
                "message": f"Customer '{name}' updated successfully!",
                "data": {
                    "id": customer_id,
                    "name": name,
                    "contact_number": contact_number,
                    "email": email,
                    "address": address,
                    "membership": membership
                }
            }), 200

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


# ==========================================
# 5. STAFF MANAGEMENT ROUTE
# ==========================================
@customer_bp.route('/staff-page', methods=['GET', 'POST'])
def manage_staff():
    if not is_authenticated():
        return redirect('/login')

    if session.get('role', 'admin') != 'admin':
        flash("Access restricted: Administrator role required to view staff management.", "error")
        if session.get('role') == 'rider':
            return redirect('/delivery-records-page')
        return redirect('/dashboard-page')

    conn = get_db_connection()

    if request.method == 'POST':
        name = (request.form.get('name') or '').strip()
        role = (request.form.get('role') or 'Laundry Operator').strip()
        contact_number = (request.form.get('contact_number') or '').strip()
        status = (request.form.get('status') or 'Active').strip()
        vehicle_station = (request.form.get('vehicle_station') or '').strip()

        if not name or not contact_number:
            conn.close()
            return "Validation Error: Staff Name and Contact Number are required.", 422

        conn.execute(
            """
            INSERT INTO staff_members (name, role, contact_number, status, vehicle_station)
            VALUES (?, ?, ?, ?, ?)
            """,
            (name, role, contact_number, status, vehicle_station)
        )
        conn.commit()
        conn.close()
        return redirect('/staff-page')

    staff = conn.execute("SELECT * FROM staff_members ORDER BY id DESC").fetchall()

    stats = {
        "total": len(staff),
        "drivers": sum(1 for s in staff if 'driver' in (s['role'] or '').lower()),
        "operators": sum(1 for s in staff if 'operator' in (s['role'] or '').lower() or 'washer' in (s['role'] or '').lower()),
        "on_duty": sum(1 for s in staff if (s['status'] or '').lower() in ['active', 'on route'])
    }

    conn.close()
    return render_template('staff.html', staff=staff, stats=stats)


@customer_bp.route('/staff-page/edit/<int:staff_id>', methods=['POST'])
def edit_staff(staff_id):
    conn = get_db_connection()
    name = (request.form.get('name') or '').strip()
    role = (request.form.get('role') or 'Laundry Operator').strip()
    contact_number = (request.form.get('contact_number') or '').strip()
    status = (request.form.get('status') or 'Active').strip()
    vehicle_station = (request.form.get('vehicle_station') or '').strip()

    if not name or not contact_number:
        conn.close()
        return "Validation Error: Staff Name and Contact Number are required.", 422

    conn.execute(
        """
        UPDATE staff_members 
        SET name = ?, role = ?, contact_number = ?, status = ?, vehicle_station = ? 
        WHERE id = ?
        """,
        (name, role, contact_number, status, vehicle_station, staff_id)
    )
    conn.commit()
    conn.close()
    return redirect('/staff-page')


@customer_bp.route('/staff-page/delete/<int:staff_id>', methods=['POST'])
def delete_staff(staff_id):
    conn = get_db_connection()
    conn.execute("DELETE FROM staff_members WHERE id = ?", (staff_id,))
    conn.commit()
    conn.close()
    return redirect('/staff-page')
