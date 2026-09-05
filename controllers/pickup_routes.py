from flask import Blueprint, render_template, request, redirect
import sqlite3

pickup_bp = Blueprint('pickup', __name__)
DATABASE = "laundry.db"


def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


@pickup_bp.route('/pickup-schedules-page', methods=['GET', 'POST'])
def manage_pickups():
    conn = get_db_connection()
    if request.method == 'POST':
        customer = request.form.get('customer')
        pickup_date = request.form.get('pickup_date')

        # VALIDATION
        if not customer or not pickup_date:
            return "Validation Error: Customer Name and Pickup Date are required.", 422

        conn.execute("INSERT INTO pickup_schedules (customer, pickup_date) VALUES (?, ?)", (customer, pickup_date))
        conn.commit()
        return redirect('/pickup-schedules-page')

    pickups = conn.execute("SELECT * FROM pickup_schedules").fetchall()
    customers = conn.execute("SELECT name FROM customers").fetchall()
    conn.close()
    return render_template('pickups.html', pickups=pickups, customers=customers)


@pickup_bp.route('/pickup-schedules-page/details/<int:pickup_id>')
def pickup_details(pickup_id):
    conn = get_db_connection()
    pickup = conn.execute("SELECT * FROM pickup_schedules WHERE id = ?", (pickup_id,)).fetchone()
    conn.close()
    if pickup is None: return "Pickup Schedule Not Found", 404
    return render_template('pickup_details.html', pickup=pickup)


@pickup_bp.route('/pickup-schedules-page/edit/<int:pickup_id>', methods=['GET', 'POST'])
def edit_pickup(pickup_id):
    conn = get_db_connection()
    pickup = conn.execute("SELECT * FROM pickup_schedules WHERE id = ?", (pickup_id,)).fetchone()
    if request.method == 'POST':
        customer = request.form.get('customer')
        pickup_date = request.form.get('pickup_date')
        if not customer or not pickup_date:
            return "Validation Error: Customer and Pickup Date are required.", 422

        conn.execute("UPDATE pickup_schedules SET customer = ?, pickup_date = ? WHERE id = ?",
                     (customer, pickup_date, pickup_id))
        conn.commit()
        conn.close()
        return redirect('/pickup-schedules-page')

    customers = conn.execute("SELECT name FROM customers").fetchall()
    conn.close()
    return render_template('edit_pickup.html', pickup=pickup, customers=customers)


@pickup_bp.route('/pickup-schedules-page/delete/<int:pickup_id>', methods=['POST'])
def delete_pickup(pickup_id):
    conn = get_db_connection()
    conn.execute("DELETE FROM pickup_schedules WHERE id = ?", (pickup_id,))
    conn.commit()
    conn.close()
    return redirect('/pickup-schedules-page')