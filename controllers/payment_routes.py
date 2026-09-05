from flask import Blueprint, render_template, request, redirect
import sqlite3
from datetime import datetime

payment_bp = Blueprint('payment', __name__)
DATABASE = "laundry.db"


def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


# ==========================================
# 1. READ LIST & CREATE PAYMENT
# ==========================================
@payment_bp.route('/payments-page', methods=['GET', 'POST'])
def manage_payments():
    conn = get_db_connection()
    if request.method == 'POST':
        customer = request.form.get('customer')
        payment_amount = request.form.get('payment_amount')
        payment_method = request.form.get('payment_method')
        transaction_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # VALIDATION (6/12 points)
        if not customer or not payment_amount or not payment_method:
            return "Validation Error: Customer Name, Amount, and Method are required.", 422

        conn.execute(
            "INSERT INTO payments (customer, payment_amount, payment_method, transaction_time) VALUES (?, ?, ?, ?)",
            (customer, float(payment_amount), payment_method, transaction_time))
        conn.commit()
        return redirect('/payments-page')

    payments = conn.execute("SELECT * FROM payments").fetchall()
    customers = conn.execute("SELECT name FROM customers").fetchall()
    conn.close()

    return render_template('payments.html', payments=payments, customers=customers)


# ==========================================
# 2. READ PAYMENT DETAILS
# ==========================================
@payment_bp.route('/payments-page/details/<int:payment_id>')
def payment_details(payment_id):
    conn = get_db_connection()
    payment = conn.execute("SELECT * FROM payments WHERE id = ?", (payment_id,)).fetchone()
    conn.close()

    if payment is None:
        return "Payment Not Found", 404

    return render_template('payment_details.html', payment=payment)


# ==========================================
# 3. UPDATE PAYMENT
# ==========================================
@payment_bp.route('/payments-page/edit/<int:payment_id>', methods=['GET', 'POST'])
def edit_payment(payment_id):
    conn = get_db_connection()
    payment = conn.execute("SELECT * FROM payments WHERE id = ?", (payment_id,)).fetchone()

    if request.method == 'POST':
        customer = request.form.get('customer')
        payment_amount = request.form.get('payment_amount')
        payment_method = request.form.get('payment_method')

        if not customer or not payment_amount or not payment_method:
            return "Validation Error: Customer, Amount, and Method are required.", 422

        conn.execute("UPDATE payments SET customer = ?, payment_amount = ?, payment_method = ? WHERE id = ?",
                     (customer, float(payment_amount), payment_method, payment_id))
        conn.commit()
        conn.close()
        return redirect('/payments-page')

    customers = conn.execute("SELECT name FROM customers").fetchall()
    conn.close()

    return render_template('edit_payment.html', payment=payment, customers=customers)


# ==========================================
# 4. DELETE PAYMENT
# ==========================================
@payment_bp.route('/payments-page/delete/<int:payment_id>', methods=['POST'])
def delete_payment(payment_id):
    conn = get_db_connection()
    conn.execute("DELETE FROM payments WHERE id = ?", (payment_id,))
    conn.commit()
    conn.close()
    return redirect('/payments-page')