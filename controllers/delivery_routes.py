import os
from flask import Blueprint, render_template, request, redirect, session, flash, url_for, jsonify
import sqlite3
from controllers.utils import is_async_request, strip_html_tags
from controllers.notification_service import add_notification

delivery_bp = Blueprint('delivery', __name__)
DATABASE = os.environ.get("DATABASE", "laundry.db")


def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.execute("PRAGMA foreign_keys = ON;")
    conn.row_factory = sqlite3.Row
    return conn


def is_authenticated():
    return "user_id" in session


@delivery_bp.route('/deliveries/new')
def new_delivery_redirect():
    order_id = request.args.get('order_id', '')
    customer = request.args.get('customer', '')
    params = {}
    if order_id:
        params['order_id'] = order_id
    if customer:
        params['customer'] = customer
    return redirect(url_for('delivery.manage_deliveries', **params))


# ============================================================
# 1. READ LIST & CREATE DELIVERY RECORD
# ============================================================
@delivery_bp.route('/delivery-records-page', methods=['GET', 'POST'])
def manage_deliveries():
    if not is_authenticated():
        if is_async_request():
            return jsonify({"status": 401, "error": "Unauthorized"}), 401
        return redirect('/login')

    conn = get_db_connection()

    if request.method == 'POST':
        is_async = is_async_request()
        data = request.get_json(silent=True) if request.is_json else request.form
        customer = (data.get('customer') or '').strip()
        delivery_date = (data.get('delivery_date') or '').strip()
        delivery_address = (data.get('delivery_address') or '').strip()
        status = (data.get('status') or 'Scheduled').strip()
        assigned_rider = (data.get('assigned_rider') or 'Mark Ephraim Nicor').strip()
        if not assigned_rider:
            assigned_rider = 'Mark Ephraim Nicor'
        delivery_notes = (data.get('delivery_notes') or '').strip()
        order_id_val = data.get('order_id')

        # Clean order_id
        order_id = int(order_id_val) if order_id_val and str(order_id_val).isdigit() else None

        # Field Validation
        errors = {}
        if not customer:
            errors['customer'] = "Customer Name is required."
        if not delivery_date:
            errors['delivery_date'] = "Delivery Date is required."

        if errors:
            conn.close()
            if is_async:
                return jsonify({"status": 422, "error": errors}), 422
            first_err = next(iter(errors.values()))
            flash(f"Validation Error: {first_err}", "danger")
            return redirect('/delivery-records-page')

        try:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO delivery_records 
                (customer, order_id, delivery_date, delivery_address, status, assigned_rider, delivery_notes)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (customer, order_id, delivery_date, delivery_address, status, assigned_rider, delivery_notes)
            )
            new_id = cursor.lastrowid
            if order_id:
                conn.execute("UPDATE laundry_orders SET status = 'Out for Delivery' WHERE id = ?", (order_id,))
            conn.commit()
            flash(f"Delivery record for '{customer}' created successfully!", "success")

            if is_async:
                conn.close()
                return jsonify({
                    "status": 201,
                    "message": f"Delivery #{new_id:04d} dispatched successfully!",
                    "data": {
                        "id": new_id,
                        "customer": customer,
                        "order_id": order_id,
                        "delivery_date": delivery_date,
                        "delivery_address": delivery_address,
                        "status": status,
                        "assigned_rider": assigned_rider,
                        "delivery_notes": delivery_notes
                    }
                }), 201

        except Exception as e:
            flash(f"Database Error: {str(e)}", "danger")
            if is_async:
                conn.close()
                return jsonify({"status": 500, "error": str(e)}), 500
        finally:
            conn.close()

        return redirect('/delivery-records-page')

    # GET REQUEST: Fetch records, customers, and active orders
    deliveries = conn.execute(
        """
        SELECT d.*, o.laundry_weight, o.service_type, o.total_price, c.contact_number 
        FROM delivery_records d
        LEFT JOIN laundry_orders o ON d.order_id = o.id
        LEFT JOIN customers c ON d.customer = c.name
        ORDER BY d.id DESC
        """
    ).fetchall()

    customers = conn.execute("SELECT id, name, contact_number, address FROM customers ORDER BY name ASC").fetchall()
    orders = conn.execute("""
        SELECT o.id, o.customer, o.laundry_weight, o.service_type, c.address as customer_address
        FROM laundry_orders o
        LEFT JOIN customers c ON o.customer = c.name
        ORDER BY o.id DESC
    """).fetchall()

    # Calculate status counts for UI summary cards
    stats = {
        "total": len(deliveries),
        "scheduled": sum(1 for d in deliveries if (d['status'] or '').lower() == 'scheduled'),
        "out_for_delivery": sum(1 for d in deliveries if (d['status'] or '').lower() == 'out for delivery'),
        "delivered": sum(1 for d in deliveries if (d['status'] or '').lower() == 'delivered'),
        "cancelled": sum(1 for d in deliveries if (d['status'] or '').lower() == 'cancelled')
    }

    conn.close()
    return render_template(
        'deliveries.html',
        deliveries=deliveries,
        customers=customers,
        orders=orders,
        stats=stats
    )


# ============================================================
# 2. READ DELIVERY DETAILS
# ============================================================
@delivery_bp.route('/delivery-records-page/details/<int:delivery_id>')
def delivery_details(delivery_id):
    if not is_authenticated():
        return redirect('/login')

    conn = get_db_connection()
    delivery = conn.execute(
        """
        SELECT d.*, o.laundry_weight, c.contact_number
        FROM delivery_records d
        LEFT JOIN laundry_orders o ON d.order_id = o.id
        LEFT JOIN customers c ON d.customer = c.name
        WHERE d.id = ?
        """,
        (delivery_id,)
    ).fetchone()
    conn.close()

    if delivery is None:
        if is_async_request():
            return jsonify({"status": 404, "error": "Delivery record not found."}), 404
        return render_template('404.html', message=f"Delivery record #{delivery_id:03d} was not found or has been removed."), 404

    return render_template('delivery_details.html', delivery=delivery)


# ============================================================
# 3. UPDATE DELIVERY RECORD
# ============================================================
@delivery_bp.route('/delivery-records-page/edit/<int:delivery_id>', methods=['GET', 'POST', 'PUT'])
def edit_delivery(delivery_id):
    if not is_authenticated():
        if is_async_request():
            return jsonify({"status": 401, "error": "Unauthorized"}), 401
        return redirect('/login')

    conn = get_db_connection()
    delivery = conn.execute("SELECT * FROM delivery_records WHERE id = ?", (delivery_id,)).fetchone()

    if delivery is None:
        conn.close()
        if is_async_request():
            return jsonify({"status": 404, "error": "Delivery record not found."}), 404
        flash("Delivery record not found.", "warning")
        return redirect('/delivery-records-page')

    if request.method in ['POST', 'PUT']:
        is_async = is_async_request()
        data = request.get_json(silent=True) if request.is_json else request.form
        customer = (data.get('customer') or '').strip()
        delivery_date = (data.get('delivery_date') or '').strip()
        delivery_address = (data.get('delivery_address') or '').strip()
        status = (data.get('status') or 'Scheduled').strip()
        assigned_rider = (data.get('assigned_rider') or '').strip()
        delivery_notes = (data.get('delivery_notes') or '').strip()
        order_id_val = data.get('order_id')

        order_id = int(order_id_val) if order_id_val and str(order_id_val).isdigit() else None

        errors = {}
        if not customer:
            errors['customer'] = "Customer Name is required."
        if not delivery_date:
            errors['delivery_date'] = "Delivery Date is required."

        if errors:
            if is_async:
                conn.close()
                return jsonify({"status": 422, "error": errors}), 422
            first_err = next(iter(errors.values()))
            flash(f"Validation Error: {first_err}", "danger")
            customers = conn.execute("SELECT id, name FROM customers ORDER BY name ASC").fetchall()
            orders = conn.execute("SELECT id, customer, laundry_weight FROM laundry_orders ORDER BY id DESC").fetchall()
            conn.close()
            return render_template('edit_delivery.html', delivery=delivery, customers=customers, orders=orders)

        try:
            conn.execute(
                """
                UPDATE delivery_records 
                SET customer = ?, order_id = ?, delivery_date = ?, delivery_address = ?, 
                    status = ?, assigned_rider = ?, delivery_notes = ? 
                WHERE id = ?
                """,
                (customer, order_id, delivery_date, delivery_address, status, assigned_rider, delivery_notes, delivery_id)
            )
            conn.commit()
            flash(f"Delivery record #{delivery_id} updated successfully!", "success")

            if is_async:
                conn.close()
                return jsonify({
                    "status": 200,
                    "message": f"Delivery #{delivery_id:04d} updated successfully!",
                    "data": {
                        "id": delivery_id,
                        "customer": customer,
                        "order_id": order_id,
                        "delivery_date": delivery_date,
                        "delivery_address": delivery_address,
                        "status": status,
                        "assigned_rider": assigned_rider,
                        "delivery_notes": delivery_notes
                    }
                }), 200

        except Exception as e:
            flash(f"Database Error: {str(e)}", "danger")
            if is_async:
                conn.close()
                return jsonify({"status": 500, "error": str(e)}), 500
        finally:
            conn.close()

        return redirect('/delivery-records-page')

    customers = conn.execute("SELECT id, name FROM customers ORDER BY name ASC").fetchall()
    orders = conn.execute("SELECT id, customer, laundry_weight FROM laundry_orders ORDER BY id DESC").fetchall()
    conn.close()

    return render_template('edit_delivery.html', delivery=delivery, customers=customers, orders=orders)


# ============================================================
# 4. DELETE DELIVERY RECORD
# ============================================================
@delivery_bp.route('/delivery-records-page/delete/<int:delivery_id>', methods=['POST', 'DELETE'])
def delete_delivery(delivery_id):
    is_async = is_async_request()
    if not is_authenticated():
        if is_async:
            return jsonify({"status": 401, "error": "Unauthorized"}), 401
        return redirect('/login')

    conn = get_db_connection()
    delivery = conn.execute("SELECT * FROM delivery_records WHERE id = ?", (delivery_id,)).fetchone()
    if delivery is None:
        conn.close()
        if is_async:
            return jsonify({"status": 404, "error": "Delivery record not found or already deleted."}), 404
        flash("Delivery record not found or already deleted.", "warning")
        return redirect('/delivery-records-page')

    try:
        conn.execute("DELETE FROM delivery_records WHERE id = ?", (delivery_id,))
        conn.commit()
        if is_async:
            return jsonify({
                "status": 200,
                "message": f"Delivery record #{delivery_id:03d} deleted successfully.",
                "id": delivery_id
            }), 200
        flash(f"Delivery record #{delivery_id} was deleted successfully.", "info")
    except Exception as e:
        if is_async:
            return jsonify({"status": 500, "error": "Failed to delete delivery record."}), 500
        flash("Failed to delete delivery record.", "danger")
    finally:
        conn.close()

    return redirect('/delivery-records-page')

# ============================================================
# RIDER MOBILE APP & GPS NAVIGATION ROUTES
# ============================================================
@delivery_bp.route('/rider-app')
def rider_app_view():
    if not is_authenticated():
        return redirect('/login')

    conn = get_db_connection()
    try:
        # Fetch deliveries for current rider (or all if admin/demo)
        role = session.get('role', 'admin')
        username = session.get('username', '')

        if role == 'rider':
            # Single dedicated courier Mark Ephraim Nicor manages all fleet deliveries & pickups
            deliveries = conn.execute("""
                SELECT d.*, o.laundry_weight, o.service_type, o.total_price, c.contact_number, c.name as customer_name
                FROM delivery_records d
                LEFT JOIN laundry_orders o ON d.order_id = o.id
                LEFT JOIN customers c ON d.customer = c.name
                ORDER BY CASE 
                    WHEN d.status = 'Out for Delivery' THEN 1
                    WHEN d.status = 'Scheduled' THEN 2
                    ELSE 3 END, d.id ASC
            """).fetchall()

            pickups = conn.execute("""
                SELECT p.*, c.contact_number
                FROM pickup_schedules p
                LEFT JOIN customers c ON p.customer = c.name
                WHERE p.status != 'Picked Up' AND p.status != 'Cancelled'
                ORDER BY p.id ASC
            """).fetchall()
        else:
            deliveries = conn.execute("""
                SELECT d.*, o.laundry_weight, o.service_type, o.total_price, c.contact_number, c.name as customer_name
                FROM delivery_records d
                LEFT JOIN laundry_orders o ON d.order_id = o.id
                LEFT JOIN customers c ON d.customer = c.name
                ORDER BY CASE 
                    WHEN d.status = 'Out for Delivery' THEN 1
                    WHEN d.status = 'Scheduled' THEN 2
                    ELSE 3 END, d.id ASC
            """).fetchall()

            pickups = conn.execute("""
                SELECT p.*, c.contact_number
                FROM pickup_schedules p
                LEFT JOIN customers c ON p.customer = c.name
                WHERE p.status != 'Picked Up' AND p.status != 'Cancelled'
                ORDER BY p.id ASC
            """).fetchall()

        # Stats
        total = len(deliveries)
        delivered = sum(1 for d in deliveries if (d['status'] or '').lower() == 'delivered')
        cod_total = sum((d['total_price'] or 0.0) for d in deliveries if (d['status'] or '').lower() != 'delivered')
        stats = {
            'total': total,
            'delivered': delivered,
            'cod_total': cod_total
        }

        return render_template(
            'rider_mobile.html',
            deliveries=deliveries,
            pickups=pickups,
            stats=stats
        )
    finally:
        conn.close()


@delivery_bp.route('/rider-app/status/<int:id>', methods=['POST'])
def rider_update_delivery_status(id):
    if not is_authenticated():
        return jsonify({'error': 'Unauthorized'}), 401

    data = request.get_json() or {}
    new_status = data.get('status', 'Delivered')

    conn = get_db_connection()
    try:
        conn.execute("""
            UPDATE delivery_records
            SET status = ?
            WHERE id = ?
        """, (new_status, id))

        # If delivered, also update linked order if present and alert shop staff
        del_row = conn.execute("SELECT customer, order_id, assigned_rider FROM delivery_records WHERE id = ?", (id,)).fetchone()
        if del_row and new_status == 'Delivered':
            if del_row['order_id']:
                conn.execute("UPDATE laundry_orders SET status = 'Completed' WHERE id = ?", (del_row['order_id'],))
            rider_name = del_row['assigned_rider'] or session.get('full_name') or 'Mark Ephraim Nicor'
            cust_name = del_row['customer'] or 'Customer'
            order_ref = f"#ORD-{del_row['order_id']:04d}" if del_row['order_id'] else f"#DEL-{id:04d}"
            add_notification(
                conn,
                title="Delivery Completed",
                message=f"Rider {rider_name} completed Delivery {order_ref} for {cust_name}.",
                notif_type="delivery_completed",
                reference_id=id,
                reference_type="delivery"
            )

        conn.commit()
        return jsonify({'success': True, 'status': new_status})
    finally:
        conn.close()


@delivery_bp.route('/rider-app/pickup-status/<int:id>', methods=['POST'])
def rider_update_pickup_status(id):
    if not is_authenticated():
        return jsonify({'error': 'Unauthorized'}), 401

    data = request.get_json() or {}
    new_status = data.get('status', 'Picked Up')

    conn = get_db_connection()
    try:
        conn.execute("""
            UPDATE pickup_schedules
            SET status = ?
            WHERE id = ?
        """, (new_status, id))

        pck_row = conn.execute("SELECT customer, assigned_driver FROM pickup_schedules WHERE id = ?", (id,)).fetchone()
        if pck_row and new_status in ['Picked Up', 'Completed']:
            rider_name = pck_row['assigned_driver'] or session.get('full_name') or 'Mark Ephraim Nicor'
            cust_name = pck_row['customer'] or 'Customer'
            add_notification(
                conn,
                title="Pickup Completed",
                message=f"Rider {rider_name} collected laundry bag for Pickup #PCK-{id:04d} from {cust_name}.",
                notif_type="pickup_completed",
                reference_id=id,
                reference_type="pickup"
            )

        conn.commit()
        return jsonify({'success': True, 'status': new_status})
    finally:
        conn.close()
