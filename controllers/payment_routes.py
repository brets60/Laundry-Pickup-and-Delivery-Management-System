import os
from flask import Blueprint, render_template, request, redirect, flash, session, jsonify, Response
import csv
import io
import sqlite3
from datetime import datetime
import random
from controllers.utils import is_async_request, strip_html_tags

payment_bp = Blueprint('payment', __name__)
DATABASE = os.environ.get("DATABASE", "laundry.db")


from db import get_db_connection


def is_authenticated():
    return "user_id" in session


# ==========================================
# 1. READ LIST & CREATE PAYMENT
# ==========================================
@payment_bp.route('/payments-page', methods=['GET', 'POST'])
def manage_payments():
    if not is_authenticated():
        if is_async_request():
            return jsonify({"status": 401, "error": "Unauthorized"}), 401
        return redirect('/login')

    if session.get('role', 'admin') not in ['admin', 'staff']:
        if is_async_request():
            return jsonify({"status": 403, "error": "Access restricted: Admin or Staff role required"}), 403
        flash("Access restricted: Administrator or Staff role required to view payments.", "error")
        if session.get('role') == 'rider':
            return redirect('/delivery-records-page')
        return redirect('/dashboard-page')

    conn = get_db_connection()

    if request.method == 'POST':
        is_async = is_async_request()
        data = request.get_json(silent=True) if request.is_json else request.form
        customer = str(data.get('customer') or '').strip()
        payment_amount_raw = str(data.get('payment_amount') or '').strip()
        payment_method = str(data.get('payment_method') or '').strip()
        order_id_val = data.get('order_id')
        status = str(data.get('status') or 'Paid').strip()
        reference_no = str(data.get('reference_no') or '').strip()
        notes = str(data.get('notes') or '').strip()

        # Structured Validation
        errors = {}
        if not customer:
            errors['customer'] = "Customer Name is required."
        if not payment_amount_raw:
            errors['payment_amount'] = "Payment Amount is required."
        else:
            try:
                payment_amount = float(payment_amount_raw)
                if payment_amount <= 0:
                    errors['payment_amount'] = "Payment Amount must be greater than 0."
            except ValueError:
                errors['payment_amount'] = "Payment Amount must be a valid number."
        if not payment_method:
            errors['payment_method'] = "Payment Method is required."

        if errors:
            conn.close()
            if is_async:
                return jsonify({"status": 422, "error": errors}), 422
            return "Validation Error: Customer Name, Amount, and Method are required.", 422

        order_id = int(order_id_val) if order_id_val and str(order_id_val).isdigit() else None
        if not reference_no:
            reference_no = f"TXN-{random.randint(1000, 9999)}"

        transaction_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO payments 
            (customer, payment_amount, payment_method, transaction_time, order_id, status, reference_no, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (customer, payment_amount, payment_method, transaction_time, order_id, status, reference_no, notes)
        )
        new_id = cursor.lastrowid
        conn.commit()
        conn.close()

        if is_async:
            return jsonify({
                "status": 201,
                "message": f"Payment #{reference_no} recorded successfully!",
                "data": {
                    "id": new_id,
                    "customer": customer,
                    "payment_amount": payment_amount,
                    "payment_method": payment_method,
                    "transaction_time": transaction_time,
                    "order_id": order_id,
                    "status": status,
                    "reference_no": reference_no,
                    "notes": notes
                }
            }), 201

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

    cash_total = sum(float(p['payment_amount'] or 0.0) for p in paid_payments if 'cash' in (p['payment_method'] or '').lower())
    gcash_total = sum(float(p['payment_amount'] or 0.0) for p in paid_payments if any(k in (p['payment_method'] or '').lower() for k in ['gcash', 'maya', 'qr']))
    bank_total = sum(float(p['payment_amount'] or 0.0) for p in paid_payments if any(k in (p['payment_method'] or '').lower() for k in ['bank', 'card', 'transfer']))

    rev_base = total_rev if total_rev > 0 else 1.0
    cash_pct = int(round((cash_total / rev_base) * 100))
    gcash_pct = int(round((gcash_total / rev_base) * 100))
    bank_pct = max(0, 100 - (cash_pct + gcash_pct)) if (cash_total or gcash_total or bank_total) else 0

    stats = {
        "total_revenue": total_rev,
        "paid_invoices": paid_cnt,
        "pending_collections": pending_cnt,
        "avg_ticket": avg_ticket,
        "cash_total": cash_total,
        "gcash_total": gcash_total,
        "bank_total": bank_total,
        "cash_pct": cash_pct,
        "gcash_pct": gcash_pct,
        "bank_pct": bank_pct
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
        if is_async_request():
            return jsonify({"status": 404, "error": "Payment record not found or has been deleted."}), 404
        return render_template('404.html', message=f"Payment transaction #{payment_id} was not found or has been removed."), 404

    return render_template('payment_details.html', payment=payment)


# ==========================================
# 3. UPDATE PAYMENT
# ==========================================
@payment_bp.route('/payments-page/edit/<int:payment_id>', methods=['GET', 'POST', 'PUT'])
def edit_payment(payment_id):
    conn = get_db_connection()
    payment = conn.execute("SELECT * FROM payments WHERE id = ?", (payment_id,)).fetchone()

    if payment is None:
        conn.close()
        if is_async_request():
            return jsonify({"status": 404, "error": "Payment record not found."}), 404
        return render_template('404.html', message=f"Cannot edit payment #{payment_id} because the record does not exist."), 404

    if request.method in ['POST', 'PUT']:
        is_async = is_async_request()
        data = request.get_json(silent=True) if request.is_json else request.form
        customer = str(data.get('customer') or '').strip()
        payment_amount_raw = str(data.get('payment_amount') or '').strip()
        payment_method = str(data.get('payment_method') or '').strip()
        status = str(data.get('status') or 'Paid').strip()
        notes = str(data.get('notes') or '').strip()

        errors = {}
        if not customer:
            errors['customer'] = "Customer Name is required."
        if not payment_amount_raw:
            errors['payment_amount'] = "Payment Amount is required."
        else:
            try:
                payment_amount = float(payment_amount_raw)
                if payment_amount <= 0:
                    errors['payment_amount'] = "Payment Amount must be greater than 0."
            except ValueError:
                errors['payment_amount'] = "Payment Amount must be a valid number."
        if not payment_method:
            errors['payment_method'] = "Payment Method is required."

        if errors:
            conn.close()
            if is_async:
                return jsonify({"status": 422, "error": errors}), 422
            return "Validation Error: Customer, Amount, and Method are required.", 422

        conn.execute(
            """
            UPDATE payments 
            SET customer = ?, payment_amount = ?, payment_method = ?, status = ?, notes = ? 
            WHERE id = ?
            """,
            (customer, payment_amount, payment_method, status, notes, payment_id)
        )
        conn.commit()
        conn.close()

        if is_async:
            return jsonify({
                "status": 200,
                "message": f"Payment updated successfully!",
                "data": {
                    "id": payment_id,
                    "customer": customer,
                    "payment_amount": payment_amount,
                    "payment_method": payment_method,
                    "status": status,
                    "notes": notes
                }
            }), 200

        return redirect('/payments-page')

    customers = conn.execute("SELECT name FROM customers ORDER BY name ASC").fetchall()
    conn.close()
    return render_template('edit_payment.html', payment=payment, customers=customers)


# ==========================================
# 4. DELETE PAYMENT
# ==========================================
@payment_bp.route('/payments-page/delete/<int:payment_id>', methods=['POST', 'DELETE'])
def delete_payment(payment_id):
    if not is_authenticated():
        if is_async_request():
            return jsonify({"status": 401, "error": "Unauthorized"}), 401
        return redirect('/login')

    conn = get_db_connection()
    payment = conn.execute("SELECT * FROM payments WHERE id = ?", (payment_id,)).fetchone()
    if payment is None:
        conn.close()
        if is_async_request():
            return jsonify({"status": 404, "error": "Payment record not found or already deleted."}), 404
        flash("Payment record not found or already deleted.", "warning")
        return redirect('/payments-page')

    ref_no = payment['reference_no'] or f"#{payment_id}"
    conn.execute("DELETE FROM payments WHERE id = ?", (payment_id,))
    conn.commit()
    conn.close()

    if is_async_request():
        return jsonify({
            "status": 200,
            "message": f"Payment {ref_no} deleted successfully.",
            "id": payment_id
        }), 200

    return redirect('/payments-page')


# ==========================================
# 5. EXPORT PAYMENTS TO CSV (Marvin Oclarino)
# ==========================================
@payment_bp.route('/payments-page/export', methods=['GET'])
def export_payments():
    if not is_authenticated():
        return redirect('/login')

    if session.get('role', 'admin') != 'admin':
        flash("Access restricted: Administrator role required to export financial reports.", "error")
        return redirect('/dashboard-page')

    conn = get_db_connection()
    payments = conn.execute(
        """
        SELECT p.*, o.service_type, o.laundry_weight, c.contact_number
        FROM payments p
        LEFT JOIN laundry_orders o ON p.order_id = o.id
        LEFT JOIN customers c ON p.customer = c.name
        ORDER BY p.id ASC
        """
    ).fetchall()
    conn.close()

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow([
        'Reference No', 'Customer Name', 'Contact Number', 'Amount (PHP)', 
        'Payment Channel', 'Status', 'Transaction Date', 'Order ID', 'Remarks'
    ])

    for p in payments:
        writer.writerow([
            p['reference_no'] or f"TXN-{p['id']}",
            p['customer'],
            p['contact_number'] or 'N/A',
            f"{float(p['payment_amount'] or 0.0):.2f}",
            p['payment_method'],
            p['status'],
            p['transaction_time'],
            f"ORD-{p['order_id']}" if p['order_id'] else 'N/A',
            p['notes'] or ''
        ])

    output.seek(0)
    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment;filename=laundrycare_payments_ledger.csv"}
    )
