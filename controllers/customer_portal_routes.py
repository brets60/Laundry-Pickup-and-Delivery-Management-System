from flask import Blueprint, render_template, request, redirect, jsonify, url_for
import sqlite3
from datetime import datetime, date

portal_bp = Blueprint('customer_portal', __name__)
DATABASE = "laundry.db"


def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.execute("PRAGMA foreign_keys = ON;")
    conn.row_factory = sqlite3.Row
    return conn


def resolve_maramag_zone_and_rider(barangay_or_address):
    addr = (barangay_or_address or '').lower()
    if any(k in addr for k in ['cmu', 'musuan', 'camp 1', 'sampaguita', 'dorm', 'university', 'colambugan']):
        return 'Zone 1: CMU & Musuan', 'Rider Mike (Van 1)'
    elif any(k in addr for k in ['dologon', 'base camp', 'kuya', 'anoling', 'dagumba', 'purok 3']):
        return 'Zone 3: Dologon & Base Camp', 'Rider Dave (Moto 3)'
    else:
        return 'Zone 2: Poblacion Center', 'Rider Alex (Moto 2)'


# ============================================================
# 1. ONLINE LAUNDRY PICKUP BOOKING FORM
# ============================================================
@portal_bp.route('/book-pickup', methods=['GET', 'POST'])
def book_pickup():
    conn = get_db_connection()
    today_str = date.today().strftime('%Y-%m-%d')

    if request.method == 'POST':
        name = (request.form.get('name') or '').strip()
        contact_number = (request.form.get('contact_number') or '').strip()
        email = (request.form.get('email') or '').strip()
        barangay = (request.form.get('barangay') or 'Poblacion').strip()
        address_details = (request.form.get('address_details') or '').strip()
        service_type = (request.form.get('service_type') or 'Wash & Fold').strip()
        estimated_load = (request.form.get('estimated_load') or 'Medium Bag (~6-8 kg)').strip()
        pickup_date = (request.form.get('pickup_date') or today_str).strip()
        pickup_time = (request.form.get('pickup_time') or '09:00 AM - 12:00 PM').strip()
        payment_method = (request.form.get('payment_method') or 'Cash on Delivery (COD)').strip()
        notes = (request.form.get('notes') or '').strip()

        # Validation
        if not name or not contact_number:
            conn.close()
            return render_template(
                'customer_book_pickup.html',
                error="Please provide both your Full Name and Mobile Contact Number.",
                today_str=today_str,
                form_data=request.form
            )

        # Assemble full formatted address in Maramag
        if address_details:
            full_address = f"{address_details}, {barangay}, Maramag, Bukidnon"
        else:
            full_address = f"{barangay}, Maramag, Bukidnon"

        # Check or register customer
        existing_cust = conn.execute(
            "SELECT * FROM customers WHERE contact_number = ? OR name = ?",
            (contact_number, name)
        ).fetchone()

        if existing_cust:
            conn.execute(
                "UPDATE customers SET address = ?, email = COALESCE(NULLIF(?, ''), email) WHERE id = ?",
                (full_address, email, existing_cust['id'])
            )
        else:
            conn.execute(
                """
                INSERT INTO customers (name, contact_number, email, address, membership)
                VALUES (?, ?, ?, ?, 'Regular')
                """,
                (name, contact_number, email, full_address)
            )

        # Automatic Barangay-to-Rider Zone Allocation
        zone_name, assigned_rider = resolve_maramag_zone_and_rider(full_address)

        # Formulate operational notes for staff and courier
        combined_notes = f"[{zone_name}] Rider: {assigned_rider} | Service: {service_type} | Est. Load: {estimated_load} | Pay: {payment_method}"
        if notes:
            combined_notes += f" | Notes: {notes}"

        # Insert pickup schedule with dedicated zone courier assigned
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO pickup_schedules 
            (customer, pickup_date, pickup_time, pickup_address, status, assigned_driver, notes, created_at)
            VALUES (?, ?, ?, ?, 'Assigned', ?, ?, ?)
            """,
            (name, pickup_date, pickup_time, full_address, assigned_rider, combined_notes, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        )
        pickup_id = cursor.lastrowid
        conn.commit()
        conn.close()

        booking_info = {
            'id': pickup_id,
            'ref': f"PCK-{pickup_id:04d}",
            'customer': name,
            'contact_number': contact_number,
            'address': full_address,
            'pickup_date': pickup_date,
            'pickup_time': pickup_time,
            'service_type': service_type,
            'estimated_load': estimated_load,
            'payment_method': payment_method,
            'zone': zone_name,
            'rider': assigned_rider
        }

        return render_template(
            'customer_book_pickup.html',
            success=True,
            booking=booking_info,
            today_str=today_str
        )


    conn.close()
    return render_template('customer_book_pickup.html', today_str=today_str)


# ============================================================
# 2. LIVE ORDER & PICKUP TRACKER
# ============================================================
@portal_bp.route('/track', methods=['GET'])
@portal_bp.route('/track/<path:query_code>', methods=['GET'])
def track_order(query_code=None):
    raw_query = (query_code or request.args.get('ref') or request.args.get('q') or '').strip()
    
    if not raw_query:
        return render_template('customer_track.html', result=None, query="")

    clean_query = raw_query.replace('#', '').replace('ORD-', '').replace('ord-', '').replace('DEL-', '').replace('del-', '').replace('PCK-', '').replace('pck-', '').strip()

    conn = get_db_connection()

    order = None
    delivery = None
    pickup = None
    customer = None
    payments = []

    # 1. Try finding by Order ID (if numeric)
    if clean_query.isdigit():
        order_id = int(clean_query)
        order = conn.execute("SELECT * FROM laundry_orders WHERE id = ?", (order_id,)).fetchone()
        if order:
            delivery = conn.execute("SELECT * FROM delivery_records WHERE order_id = ?", (order['id'],)).fetchone()
            customer = conn.execute("SELECT * FROM customers WHERE name = ?", (order['customer'],)).fetchone()
            payments = conn.execute("SELECT * FROM payments WHERE order_id = ?", (order['id'],)).fetchall()

    # 2. Try finding by Pickup ID (if not found in order)
    if not order and clean_query.isdigit():
        pickup_id = int(clean_query)
        pickup = conn.execute("SELECT * FROM pickup_schedules WHERE id = ?", (pickup_id,)).fetchone()
        if pickup:
            customer = conn.execute("SELECT * FROM customers WHERE name = ?", (pickup['customer'],)).fetchone()

    # 3. Try finding by Phone Number or Customer Name
    if not order and not pickup:
        cust = conn.execute(
            "SELECT * FROM customers WHERE contact_number LIKE ? OR name LIKE ?",
            (f"%{raw_query}%", f"%{raw_query}%")
        ).fetchone()

        if cust:
            customer = cust
            order = conn.execute(
                "SELECT * FROM laundry_orders WHERE customer = ? ORDER BY id DESC LIMIT 1",
                (cust['name'],)
            ).fetchone()
            if order:
                delivery = conn.execute("SELECT * FROM delivery_records WHERE order_id = ?", (order['id'],)).fetchone()
                payments = conn.execute("SELECT * FROM payments WHERE order_id = ?", (order['id'],)).fetchall()
            else:
                pickup = conn.execute(
                    "SELECT * FROM pickup_schedules WHERE customer = ? ORDER BY id DESC LIMIT 1",
                    (cust['name'],)
                ).fetchone()

    # 4. If neither order nor pickup, search pickup by customer name directly
    if not order and not pickup:
        pickup = conn.execute("SELECT * FROM pickup_schedules WHERE customer LIKE ? ORDER BY id DESC LIMIT 1", (f"%{raw_query}%",)).fetchone()
        if pickup:
            customer = conn.execute("SELECT * FROM customers WHERE name = ?", (pickup['customer'],)).fetchone()

    conn.close()

    if not order and not pickup:
        return render_template(
            'customer_track.html',
            not_found=True,
            query=raw_query
        )

    current_step = 1
    step_name = "Intake Received"
    step_desc = "Your laundry has been logged at our Maramag branch."

    if order:
        st = (order['status'] or 'Received').lower()
        del_st = (delivery['status'] if delivery else '').lower()

        if del_st == 'delivered' or st in ['delivered', 'completed']:
            current_step = 6
            step_name = "Delivered & Completed"
            step_desc = "Your fresh clothes have been handed over. Thank you for trusting LaundryCare!"
        elif del_st == 'out for delivery' or st == 'out for delivery':
            current_step = 5
            step_name = "Out for Delivery"
            step_desc = f"Your package is en route with {delivery['assigned_rider'] if delivery and delivery['assigned_rider'] else 'our courier'}."
        elif st in ['ready', 'ready for dispatch', 'folded']:
            current_step = 4
            step_name = "Ironed, Folded & Packaged"
            step_desc = "Your laundry is fresh, neatly pressed, sealed in bags, and waiting for driver dispatch."
        elif st in ['drying', 'in drying']:
            current_step = 3
            step_name = "Drying & Sanitizing Cycle"
            step_desc = "Clothes are in commercial high-heat tumblers for fluff drying and sanitization."
        elif st in ['washing', 'in washing', 'wash']:
            current_step = 2
            step_name = "Washing & Fabric Conditioning"
            step_desc = "Garments are currently being washed with premium detergents and fabric softeners."
        else:
            current_step = 1
            step_name = "Intake Received & Weighed"
            step_desc = f"Order logged with verified weight of {order['laundry_weight']} kg."
    elif pickup:
        p_st = (pickup['status'] or 'Pending').lower()
        if p_st in ['picked up', 'completed']:
            current_step = 1
            step_name = "Bag Collected by Courier"
            step_desc = "Your laundry bag has been picked up and is arriving at our Maramag branch for weighing."
        elif p_st in ['assigned', 'in transit']:
            current_step = 1
            step_name = "Rider Dispatched for Pickup"
            step_desc = f"Courier {pickup['assigned_driver'] or 'Rider'} is en route to collect your laundry."
        else:
            current_step = 1
            step_name = "Pickup Request Booked"
            step_desc = f"Scheduled for {pickup['pickup_date']} during {pickup['pickup_time']}."

    paid_sum = sum(float(p['payment_amount'] or 0.0) for p in payments if (p['status'] or '').lower() == 'paid')
    total_price = float(order['total_price'] if order and order['total_price'] else 0.0)
    is_fully_paid = paid_sum >= total_price and total_price > 0
    balance_due = max(0.0, total_price - paid_sum)

    result_data = {
        'order': order,
        'delivery': delivery,
        'pickup': pickup,
        'customer': customer,
        'payments': payments,
        'current_step': current_step,
        'step_name': step_name,
        'step_desc': step_desc,
        'is_fully_paid': is_fully_paid,
        'balance_due': balance_due,
        'paid_sum': paid_sum,
        'total_price': total_price
    }

    return render_template('customer_track.html', result=result_data, query=raw_query)


# ============================================================
# 3. FAST API LOOKUP
# ============================================================
@portal_bp.route('/api/track-lookup', methods=['GET'])
def api_track_lookup():
    q = (request.args.get('q') or '').strip()
    if not q:
        return jsonify({'status': 'empty'})

    conn = get_db_connection()
    orders = conn.execute(
        """
        SELECT id, customer, total_price, status, created_at 
        FROM laundry_orders 
        WHERE id = ? OR customer LIKE ? 
        ORDER BY id DESC LIMIT 3
        """,
        (q if q.isdigit() else -1, f"%{q}%")
    ).fetchall()
    conn.close()

    return jsonify({
        'status': 'ok',
        'matches': [dict(o) for o in orders]
    })
