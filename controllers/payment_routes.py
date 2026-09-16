from flask import Blueprint, render_template, request, redirect, flash, session
import sqlite3
from datetime import datetime
import random

payment_bp = Blueprint('payment', __name__)
DATABASE = "laundry.db"


def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.execute("PRAGMA foreign_keys = ON;")
    conn.row_factory = sqlite3.Row
    return conn


def is_authenticated():
    return "user_id" in session


# ==========================================
# 1. READ LIST & CREATE PAYMENT
# ==========================================
@payment_bp.route('/payments-page', methods=['GET', 'POST'])
def manage_payments():
    if not is_authenticated():
        return redirect('/login')

    if session.get('role', 'admin') != 'admin':
        flash("Access restricted: Administrator role required to view financial reports.", "error")
        if session.get('role') == 'rider':
            return redirect('/delivery-records-page')
        return redirect('/dashboard-page')

    conn = get_db_connection()

    if request.method == 'POST':
        customer = (request.form.get('customer') or '').strip()
        payment_amount_raw = (request.form.get('payment_amount') or '').strip()
        payment_method = (request.form.get('payment_method') or '').strip()
        order_id_val = request.form.get('order_id')
        status = (request.form.get('status') or 'Paid').strip()
        reference_no = (request.form.get('reference_no') or '').strip()
        notes = (request.form.get('notes') or '').strip()

        # VALIDATION
        if not customer or not payment_amount_raw or not payment_method:
            conn.close()
            return "Validation Error: Customer Name, Amount, and Method are required.", 422

        try:
            payment_amount = float(payment_amount_raw)
        except ValueError:
            conn.close()
            return "Validation Error: Invalid payment amount.", 422

        order_id = int(order_id_val) if order_id_val and order_id_val.isdigit() else None
        if not reference_no:
            reference_no = f"TXN-{random.randint(1000, 9999)}"

        transaction_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        conn.execute(
            """
            INSERT INTO payments 
            (customer, payment_amount, payment_method, transaction_time, order_id, status, reference_no, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (customer, payment_amount, payment_method, transaction_time, order_id, status, reference_no, notes)
        )
        conn.commit()
        conn.close()
        return redirect('/payments-page')

    # READ: Get all payments and calculate financial KPIs
    payments = conn.execute(
        """
        SELECT p.*, o.service_type, o.laundry_weight, c.contact_number
        FROM payments p
        LEFT JOIN laundry_orders o ON p.order_id = o.id
        LEFT JOIN customers c ON p.customer = c.name
        ORDER BY p.id DESC
        """
    ).fetchall()

    customers = conn.execute("SELECT id, name FROM customers ORDER BY name ASC").fetchall()
    orders = conn.execute("SELECT id, customer, total_price FROM laundry_orders ORDER BY id DESC").fetchall()

    paid_payments = [p for p in payments if (p['status'] or '').lower() == 'paid']
    total_rev = sum(float(p['payment_amount'] or 0.0) for p in paid_payments)
    paid_cnt = len(paid_payments)
    pending_cnt = sum(1 for p in payments if (p['status'] or '').lower() == 'pending')
    avg_ticket = round(total_rev / max(1, paid_cnt), 2) if paid_cnt > 0 else 0.0

    stats = {
        "total_revenue": total_rev,
        "paid_invoices": paid_cnt,
        "pending_collections": pending_cnt,
        "avg_ticket": avg_ticket
    }

    conn.close()
    return render_template(
        'payments.html',
        payments=payments,
        customers=customers,
        orders=orders,
        stats=stats
    )


# ==========================================
# 2. READ PAYMENT DETAILS
# ==========================================
@payment_bp.route('/payments-page/details/<int:payment_id>')
def payment_details(payment_id):
    conn = get_db_connection()
    payment = conn.execute(
        """
        SELECT p.*, o.service_type, o.laundry_weight, c.contact_number, c.address
        FROM payments p
        LEFT JOIN laundry_orders o ON p.order_id = o.id
        LEFT JOIN customers c ON p.customer = c.name
        WHERE p.id = ?
        """,
        (payment_id,)
    ).fetchone()
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

    if payment is None:
        conn.close()
        return "Payment Not Found", 404

    if request.method == 'POST':
        customer = (request.form.get('customer') or '').strip()
        payment_amount = (request.form.get('payment_amount') or '').strip()
        payment_method = (request.form.get('payment_method') or '').strip()
        status = (request.form.get('status') or 'Paid').strip()
        notes = (request.form.get('notes') or '').strip()

        if not customer or not payment_amount or not payment_method:
            conn.close()
            return "Validation Error: Customer, Amount, and Method are required.", 422

        conn.execute(
            """
            UPDATE payments 
            SET customer = ?, payment_amount = ?, payment_method = ?, status = ?, notes = ? 
            WHERE id = ?
            """,
            (customer, float(payment_amount), payment_method, status, notes, payment_id)
        )
        conn.commit()
        conn.close()
        return redirect('/payments-page')

    customers = conn.execute("SELECT name FROM customers ORDER BY name ASC").fetchall()
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
