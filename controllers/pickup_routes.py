from flask import Blueprint, render_template, request, redirect, flash, session, url_for, jsonify
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


def is_async_request():
    return (
        request.is_json
        or request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        or 'application/json' in request.headers.get('Accept', '')
    )


# ============================================================
# 1. READ LIST & CREATE PICKUP SCHEDULE
# ============================================================
@pickup_bp.route('/pickup-schedules-page', methods=['GET', 'POST'])
def manage_pickups():
    conn = get_db_connection()

    if request.method == 'POST':
        is_async = is_async_request()
        data = request.get_json(silent=True) if request.is_json else request.form
        customer = (data.get('customer') or '').strip()
        pickup_date = (data.get('pickup_date') or '').strip()
        pickup_time = (data.get('pickup_time') or '09:00 AM - 12:00 PM').strip()
        pickup_address = (data.get('pickup_address') or '').strip()
        status = (data.get('status') or 'Pending').strip()
        assigned_driver = (data.get('assigned_driver') or '').strip()
        notes = (data.get('notes') or '').strip()

        # Structured Validation
        errors = {}
        if not customer:
            errors['customer'] = "Customer Name is required."
        if not pickup_date:
            errors['pickup_date'] = "Pickup Date is required."

        if errors:
            conn.close()
            if is_async:
                return jsonify({"status": 422, "error": errors}), 422
            return "Validation Error: Customer Name and Pickup Date are required.", 422

        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO pickup_schedules 
            (customer, pickup_date, pickup_time, pickup_address, status, assigned_driver, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (customer, pickup_date, pickup_time, pickup_address, status, assigned_driver, notes)
        )
        new_id = cursor.lastrowid
        conn.commit()
        conn.close()

        if is_async:
            return jsonify({
                "status": 201,
                "message": f"Pickup #{new_id:04d} booked successfully!",
                "data": {
                    "id": new_id,
                    "customer": customer,
                    "pickup_date": pickup_date,
                    "pickup_time": pickup_time,
                    "pickup_address": pickup_address,
                    "status": status,
                    "assigned_driver": assigned_driver,
                    "notes": notes
                }
            }), 201

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
        if is_async_request():
            return jsonify({"status": 404, "error": "Pickup schedule not found or has been deleted."}), 404
        return render_template('404.html', message=f"Pickup schedule #{pickup_id:04d} was not found or has been removed."), 404
    return render_template('pickup_details.html', pickup=pickup)


# ============================================================
# 3. UPDATE PICKUP SCHEDULE
# ============================================================
@pickup_bp.route('/pickup-schedules-page/edit/<int:pickup_id>', methods=['GET', 'POST', 'PUT'])
def edit_pickup(pickup_id):
    conn = get_db_connection()
    pickup = conn.execute("SELECT * FROM pickup_schedules WHERE id = ?", (pickup_id,)).fetchone()

    if pickup is None:
        conn.close()
        if is_async_request():
            return jsonify({"status": 404, "error": "Pickup schedule not found."}), 404
        return render_template('404.html', message=f"Cannot edit Pickup schedule #{pickup_id:04d} because it does not exist."), 404

    if request.method in ['POST', 'PUT']:
        is_async = is_async_request()
        data = request.get_json(silent=True) if request.is_json else request.form
        customer = (data.get('customer') or '').strip()
        pickup_date = (data.get('pickup_date') or '').strip()
        pickup_time = (data.get('pickup_time') or '09:00 AM - 12:00 PM').strip()
        pickup_address = (data.get('pickup_address') or '').strip()
        status = (data.get('status') or 'Pending').strip()
        assigned_driver = (data.get('assigned_driver') or '').strip()
        notes = (data.get('notes') or '').strip()

        errors = {}
        if not customer:
            errors['customer'] = "Customer Name is required."
        if not pickup_date:
            errors['pickup_date'] = "Pickup Date is required."

        if errors:
            conn.close()
            if is_async:
                return jsonify({"status": 422, "error": errors}), 422
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

        if is_async:
            return jsonify({
                "status": 200,
                "message": f"Pickup #{pickup_id:04d} updated successfully!",
                "data": {
                    "id": pickup_id,
                    "customer": customer,
                    "pickup_date": pickup_date,
                    "pickup_time": pickup_time,
                    "pickup_address": pickup_address,
                    "status": status,
                    "assigned_driver": assigned_driver,
                    "notes": notes
                }
            }), 200

        return redirect('/pickup-schedules-page')

    customers = conn.execute("SELECT name FROM customers ORDER BY name ASC").fetchall()
    conn.close()
    return render_template('edit_pickup.html', pickup=pickup, customers=customers)


# ============================================================
# 4. DELETE PICKUP SCHEDULE
# ============================================================
@pickup_bp.route('/pickup-schedules-page/delete/<int:pickup_id>', methods=['POST', 'DELETE'])
def delete_pickup(pickup_id):
    conn = get_db_connection()
    pickup = conn.execute("SELECT * FROM pickup_schedules WHERE id = ?", (pickup_id,)).fetchone()
    if pickup is None:
        conn.close()
        if is_async_request():
            return jsonify({"status": 404, "error": "Pickup schedule not found or already deleted."}), 404
        flash("Pickup schedule not found or already deleted.", "warning")
        return redirect('/pickup-schedules-page')

    conn.execute("DELETE FROM pickup_schedules WHERE id = ?", (pickup_id,))
    conn.commit()
    conn.close()

    if is_async_request():
        return jsonify({
            "status": 200,
            "message": f"Pickup schedule #{pickup_id:04d} deleted successfully.",
            "id": pickup_id
        }), 200

    return redirect('/pickup-schedules-page')
