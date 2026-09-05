from flask import Blueprint, render_template, request, redirect
import sqlite3

delivery_bp = Blueprint('delivery', __name__)
DATABASE = "laundry.db"


def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


@delivery_bp.route('/delivery-records-page', methods=['GET', 'POST'])
def manage_deliveries():
    conn = get_db_connection()
    if request.method == 'POST':
        customer = request.form.get('customer')
        delivery_date = request.form.get('delivery_date')

        # VALIDATION
        if not customer or not delivery_date:
            return "Validation Error: Customer Name and Delivery Date are required.", 422

        conn.execute("INSERT INTO delivery_records (customer, delivery_date) VALUES (?, ?)", (customer, delivery_date))
        conn.commit()
        return redirect('/delivery-records-page')

    deliveries = conn.execute("SELECT * FROM delivery_records").fetchall()
    customers = conn.execute("SELECT name FROM customers").fetchall()
    conn.close()
    return render_template('deliveries.html', deliveries=deliveries, customers=customers)


@delivery_bp.route('/delivery-records-page/details/<int:delivery_id>')
def delivery_details(delivery_id):
    conn = get_db_connection()
    delivery = conn.execute("SELECT * FROM delivery_records WHERE id = ?", (delivery_id,)).fetchone()
    conn.close()
    if delivery is None: return "Delivery Not Found", 404
    return render_template('delivery_details.html', delivery=delivery)


@delivery_bp.route('/delivery-records-page/edit/<int:delivery_id>', methods=['GET', 'POST'])
def edit_delivery(delivery_id):
    conn = get_db_connection()
    delivery = conn.execute("SELECT * FROM delivery_records WHERE id = ?", (delivery_id,)).fetchone()
    if request.method == 'POST':
        customer = request.form.get('customer')
        delivery_date = request.form.get('delivery_date')

        if not customer or not delivery_date:
            return "Validation Error: Customer and Delivery Date are required.", 422

        conn.execute("UPDATE delivery_records SET customer = ?, delivery_date = ? WHERE id = ?",
                     (customer, delivery_date, delivery_id))
        conn.commit()
        conn.close()
        return redirect('/delivery-records-page')

    customers = conn.execute("SELECT name FROM customers").fetchall()
    conn.close()
    return render_template('edit_delivery.html', delivery=delivery, customers=customers)


@delivery_bp.route('/delivery-records-page/delete/<int:delivery_id>', methods=['POST'])
def delete_delivery(delivery_id):
    conn = get_db_connection()
    conn.execute("DELETE FROM delivery_records WHERE id = ?", (delivery_id,))
    conn.commit()
    conn.close()
    return redirect('/delivery-records-page')