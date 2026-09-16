from flask import Blueprint, render_template, request, redirect, flash, session, url_for
import sqlite3

pickup_bp = Blueprint('pickup', __name__)
DATABASE = "laundry.db"


def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.execute("PRAGMA foreign_keys = ON;")
    conn.row_factory = sqlite3.Row
    return conn


def is_authenticated():
    return "user_id" in session


# ============================================================
# 1. READ LIST & CREATE PICKUP SCHEDULE
# ============================================================
@pickup_bp.route('/pickup-schedules-page', methods=['GET', 'POST'])
def manage_pickups():
    conn = get_db_connection()

    if request.method == 'POST':
        customer = (request.form.get('customer') or '').strip()
        pickup_date = (request.form.get('pickup_date') or '').strip()
        pickup_time = (request.form.get('pickup_time') or '09:00 AM - 12:00 PM').strip()
        pickup_address = (request.form.get('pickup_address') or '').strip()
        status = (request.form.get('status') or 'Pending').strip()
        assigned_driver = (request.form.get('assigned_driver') or '').strip()
        notes = (request.form.get('notes') or '').strip()

        # VALIDATION
        if not customer or not pickup_date:
            conn.close()
            return "Validation Error: Customer Name and Pickup Date are required.", 422

        conn.execute(
            """
            INSERT INTO pickup_schedules 
            (customer, pickup_date, pickup_time, pickup_address, status, assigned_driver, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (customer, pickup_date, pickup_time, pickup_address, status, assigned_driver, notes)
        )
        conn.commit()
        conn.close()
        return redirect('/pickup-schedules-page')

    # GET REQUEST: Fetch records, customer details, and KPI metrics
    pickups = conn.execute(
        """
        SELECT p.*, c.contact_number 
        FROM pickup_schedules p
        LEFT JOIN customers c ON p.customer = c.name
        ORDER BY p.id DESC
        """
    ).fetchall()

    customers = conn.execute("SELECT id, name, contact_number FROM customers ORDER BY name ASC").fetchall()

    stats = {
        "total": len(pickups),
        "pending": sum(1 for p in pickups if (p['status'] or '').lower() == 'pending'),
        "assigned": sum(1 for p in pickups if (p['status'] or '').lower() in ['assigned', 'in transit']),
        "picked_up": sum(1 for p in pickups if (p['status'] or '').lower() in ['picked up', 'completed']),
        "cancelled": sum(1 for p in pickups if (p['status'] or '').lower() == 'cancelled')
    }

    conn.close()
    return render_template(
        'pickups.html',
        pickups=pickups,
        customers=customers,
        stats=stats
    )


# ============================================================
# 2. READ PICKUP DETAILS
# ============================================================
@pickup_bp.route('/pickup-schedules-page/details/<int:pickup_id>')
def pickup_details(pickup_id):
    conn = get_db_connection()
    pickup = conn.execute(
        """
        SELECT p.*, c.contact_number 
        FROM pickup_schedules p
        LEFT JOIN customers c ON p.customer = c.name
        WHERE p.id = ?
        """,
        (pickup_id,)
    ).fetchone()
    conn.close()
    if pickup is None:
        return "Pickup Schedule Not Found", 404
    return render_template('pickup_details.html', pickup=pickup)


# ============================================================
# 3. UPDATE PICKUP SCHEDULE
# ============================================================
@pickup_bp.route('/pickup-schedules-page/edit/<int:pickup_id>', methods=['GET', 'POST'])
def edit_pickup(pickup_id):
    conn = get_db_connection()
    pickup = conn.execute("SELECT * FROM pickup_schedules WHERE id = ?", (pickup_id,)).fetchone()

    if pickup is None:
        conn.close()
        return "Pickup Schedule Not Found", 404

    if request.method == 'POST':
        customer = (request.form.get('customer') or '').strip()
        pickup_date = (request.form.get('pickup_date') or '').strip()
        pickup_time = (request.form.get('pickup_time') or '09:00 AM - 12:00 PM').strip()
        pickup_address = (request.form.get('pickup_address') or '').strip()
        status = (request.form.get('status') or 'Pending').strip()
        assigned_driver = (request.form.get('assigned_driver') or '').strip()
        notes = (request.form.get('notes') or '').strip()

        if not customer or not pickup_date:
            conn.close()
            return "Validation Error: Customer and Pickup Date are required.", 422

        conn.execute(
            """
            UPDATE pickup_schedules 
            SET customer = ?, pickup_date = ?, pickup_time = ?, pickup_address = ?, 
                status = ?, assigned_driver = ?, notes = ? 
            WHERE id = ?
            """,
            (customer, pickup_date, pickup_time, pickup_address, status, assigned_driver, notes, pickup_id)
        )
        conn.commit()
        conn.close()
        return redirect('/pickup-schedules-page')

    customers = conn.execute("SELECT name FROM customers ORDER BY name ASC").fetchall()
    conn.close()
    return render_template('edit_pickup.html', pickup=pickup, customers=customers)


# ============================================================
# 4. DELETE PICKUP SCHEDULE
# ============================================================
@pickup_bp.route('/pickup-schedules-page/delete/<int:pickup_id>', methods=['POST'])
def delete_pickup(pickup_id):
    conn = get_db_connection()
    conn.execute("DELETE FROM pickup_schedules WHERE id = ?", (pickup_id,))
    conn.commit()
    conn.close()
    return redirect('/pickup-schedules-page')
