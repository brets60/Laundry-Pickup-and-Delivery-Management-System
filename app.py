from flask import Flask, render_template, request, redirect, session, jsonify
from datetime import datetime
import sqlite3

#controllers
from controllers.customer_routes import customer_bp
from controllers.order_routes import order_bp
from controllers.pickup_routes import pickup_bp
from controllers.delivery_routes import delivery_bp
from controllers.payment_routes import payment_bp

app = Flask(__name__)
app.secret_key = "laundry-system-secret-key"

app.register_blueprint(customer_bp)
app.register_blueprint(order_bp)
app.register_blueprint(pickup_bp)
app.register_blueprint(delivery_bp)
app.register_blueprint(payment_bp)

DATABASE = "laundry.db"


# ============================================================
# DATABASE CONNECTION
# ============================================================

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


# ============================================================
# DATABASE INITIALIZATION
# ============================================================

def init_database():

    conn = get_db_connection()

    # -------------------------
    # CUSTOMERS
    # -------------------------
    conn.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            contact_number TEXT NOT NULL
        )
    """)

    # -------------------------
    # LAUNDRY ORDERS
    # -------------------------
    conn.execute("""
        CREATE TABLE IF NOT EXISTS laundry_orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer TEXT NOT NULL,
            laundry_weight REAL NOT NULL
        )
    """)

    # -------------------------
    # PICKUP SCHEDULES
    # -------------------------
    conn.execute("""
        CREATE TABLE IF NOT EXISTS pickup_schedules (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer TEXT NOT NULL,
            pickup_date TEXT NOT NULL
        )
    """)

    # -------------------------
    # DELIVERY RECORDS
    # -------------------------
    conn.execute("""
        CREATE TABLE IF NOT EXISTS delivery_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer TEXT NOT NULL,
            delivery_date TEXT NOT NULL
        )
    """)

    # -------------------------
    # PAYMENTS
    # -------------------------
    conn.execute("""
        CREATE TABLE IF NOT EXISTS payments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer TEXT NOT NULL,
            payment_amount REAL NOT NULL,
            payment_method TEXT NOT NULL,
            transaction_time TEXT
        )
    """)

    # -------------------------
    # USERS
    # -------------------------
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    # -------------------------
    # CREATE DEFAULT ADMIN
    # -------------------------
    existing_user = conn.execute(
        "SELECT id FROM users WHERE username = ?",
        ("admin",)
    ).fetchone()

    if existing_user is None:
        conn.execute(
            """
            INSERT INTO users (username, password)
            VALUES (?, ?)
            """,
            ("admin", "admin123")
        )

    conn.commit()
    conn.close()


init_database()


# ============================================================
# LOGIN REQUIRED HELPER
# ============================================================

def login_required():
    return "user_id" in session




# ============================================================
# DASHBOARD
# ============================================================

@app.route("/")
def dashboard():
    return redirect("/dashboard-page")

    if not login_required():
        return redirect("/login")

    conn = get_db_connection()

    customer_count = conn.execute(
        "SELECT COUNT(*) FROM customers"
    ).fetchone()[0]

    order_count = conn.execute(
        "SELECT COUNT(*) FROM laundry_orders"
    ).fetchone()[0]

    pickup_count = conn.execute(
        "SELECT COUNT(*) FROM pickup_schedules"
    ).fetchone()[0]

    delivery_count = conn.execute(
        "SELECT COUNT(*) FROM delivery_records"
    ).fetchone()[0]

    payment_count = conn.execute(
        "SELECT COUNT(*) FROM payments"
    ).fetchone()[0]

    total_revenue = conn.execute(
        "SELECT COALESCE(SUM(payment_amount), 0) FROM payments"
    ).fetchone()[0]

    conn.close()

    return render_template(
        "index.html",
        customer_count=customer_count,
        order_count=order_count,
        pickup_count=pickup_count,
        delivery_count=delivery_count,
        payment_count=payment_count,
        total_revenue=total_revenue
    )


@app.route("/dashboard-page")
def dashboard_page():

    if not login_required():
        return redirect("/login")

    conn = get_db_connection()

    try:
        # ==========================================
        # DASHBOARD COUNTS
        # ==========================================

        customers_count = conn.execute(
            "SELECT COUNT(*) FROM customers"
        ).fetchone()[0]

        orders_count = conn.execute(
            "SELECT COUNT(*) FROM laundry_orders"
        ).fetchone()[0]

        pickups_count = conn.execute(
            "SELECT COUNT(*) FROM pickup_schedules"
        ).fetchone()[0]

        deliveries_count = conn.execute(
            "SELECT COUNT(*) FROM delivery_records"
        ).fetchone()[0]

        payments_count = conn.execute(
            "SELECT COUNT(*) FROM payments"
        ).fetchone()[0]


        # ==========================================
        # TOTAL REVENUE
        # ==========================================

        total_revenue = conn.execute(
            """
            SELECT COALESCE(SUM(payment_amount), 0)
            FROM payments
            """
        ).fetchone()[0]


        # ==========================================
        # DASHBOARD
        # ==========================================

        return render_template(
            "dashboard.html",

            customers_count=customers_count,
            orders_count=orders_count,
            pickups_count=pickups_count,
            deliveries_count=deliveries_count,
            payments_count=payments_count,

            total_revenue=total_revenue
        )

    finally:
        conn.close()


# ============================================================
# LOGIN
# ============================================================

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        conn = get_db_connection()

        user = conn.execute(
            """
            SELECT id, username
            FROM users
            WHERE username = ? AND password = ?
            """,
            (username, password)
        ).fetchone()

        conn.close()

        if user:

            session["user_id"] = user["id"]
            session["username"] = user["username"]

            return redirect("/")

        return render_template(
            "login.html",
            error="Invalid username or password."
        )

    return render_template("login.html")


# ============================================================
# LOGOUT
# ============================================================

@app.route("/logout")
def logout():

    session.clear()

    return redirect("/login")


# ============================================================
# CUSTOMERS PAGE
# ============================================================

@app.route("/customers-page", methods=["GET", "POST"])
def customers_page():

    if not login_required():
        return redirect("/login")

    if request.method == "POST":

        name = request.form.get("name", "").strip()
        contact_number = request.form.get(
            "contact_number",
            ""
        ).strip()

        if name and contact_number:

            conn = get_db_connection()

            conn.execute(
                """
                INSERT INTO customers
                (name, contact_number)
                VALUES (?, ?)
                """,
                (
                    name,
                    contact_number
                )
            )

            conn.commit()
            conn.close()

            return redirect("/customers-page")

    conn = get_db_connection()

    customers = conn.execute(
        """
        SELECT id, name, contact_number
        FROM customers
        ORDER BY id DESC
        """
    ).fetchall()

    conn.close()

    return render_template(
        "customers.html",
        customers=customers
    )

@app.route("/customer/<int:customer_id>")
def customer_details(customer_id):

    if not login_required():
        return redirect("/login")

    conn = get_db_connection()

    customer = conn.execute(
        """
        SELECT id, name, contact_number
        FROM customers
        WHERE id = ?
        """,
        (customer_id,)
    ).fetchone()

    conn.close()

    if customer is None:
        return "Customer not found", 404

    return render_template(
        "customer_details.html",
        customer=customer
    )

# ============================================================
# EDIT CUSTOMER
# ============================================================

@app.route(
    "/customers-page/edit/<int:id>",
    methods=["GET", "POST"]
)
def edit_customer_page(id):

    if not login_required():
        return redirect("/login")

    conn = get_db_connection()

    customer = conn.execute(
        """
        SELECT id, name, contact_number
        FROM customers
        WHERE id = ?
        """,
        (id,)
    ).fetchone()

    if customer is None:

        conn.close()

        return "Customer not found.", 404

    if request.method == "POST":

        name = request.form.get(
            "name",
            ""
        ).strip()

        contact_number = request.form.get(
            "contact_number",
            ""
        ).strip()

        if name and contact_number:

            conn.execute(
                """
                UPDATE customers
                SET name = ?, contact_number = ?
                WHERE id = ?
                """,
                (
                    name,
                    contact_number,
                    id
                )
            )

            conn.commit()
            conn.close()

            return redirect("/customers-page")

    conn.close()

    return render_template(
        "edit_customer.html",
        customer=customer
    )


# ============================================================
# DELETE CUSTOMER
# ============================================================

@app.route(
    "/customers-page/delete/<int:id>",
    methods=["POST"]
)
def delete_customer_page(id):

    if not login_required():
        return redirect("/login")

    conn = get_db_connection()

    conn.execute(
        """
        DELETE FROM customers
        WHERE id = ?
        """,
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect("/customers-page")


# ============================================================
# LAUNDRY ORDERS PAGE
# ============================================================

@app.route(
    "/laundry-orders-page",
    methods=["GET", "POST"]
)
def laundry_orders_page():

    if not login_required():
        return redirect("/login")

    # ADD ORDER
    if request.method == "POST":

        customer = request.form.get(
            "customer",
            ""
        ).strip()

        laundry_weight = request.form.get(
            "laundry_weight",
            ""
        ).strip()

        if customer and laundry_weight:

            try:
                laundry_weight = float(
                    laundry_weight
                )

                if laundry_weight <= 0:
                    return redirect(
                        "/laundry-orders-page"
                    )

            except ValueError:

                return redirect(
                    "/laundry-orders-page"
                )

            conn = get_db_connection()

            conn.execute(
                """
                INSERT INTO laundry_orders
                (customer, laundry_weight)
                VALUES (?, ?)
                """,
                (
                    customer,
                    laundry_weight
                )
            )

            conn.commit()
            conn.close()

            return redirect(
                "/laundry-orders-page"
            )

    # GET ORDERS
    conn = get_db_connection()

    orders = conn.execute(
        """
        SELECT id, customer, laundry_weight
        FROM laundry_orders
        ORDER BY id DESC
        """
    ).fetchall()

    conn.close()

    return render_template(
        "laundry_orders.html",
        orders=orders
    )


# ============================================================
# EDIT LAUNDRY ORDER
# ============================================================

@app.route(
    "/laundry-orders-page/edit/<int:id>",
    methods=["GET", "POST"]
)
def edit_laundry_order_page(id):

    if not login_required():
        return redirect("/login")

    conn = get_db_connection()

    order = conn.execute(
        """
        SELECT id, customer, laundry_weight
        FROM laundry_orders
        WHERE id = ?
        """,
        (id,)
    ).fetchone()

    if order is None:

        conn.close()

        return "Laundry order not found.", 404

    if request.method == "POST":

        customer = request.form.get(
            "customer",
            ""
        ).strip()

        laundry_weight = request.form.get(
            "laundry_weight",
            ""
        ).strip()

        if customer and laundry_weight:

            try:

                laundry_weight = float(
                    laundry_weight
                )

                conn.execute(
                    """
                    UPDATE laundry_orders
                    SET customer = ?,
                        laundry_weight = ?
                    WHERE id = ?
                    """,
                    (
                        customer,
                        laundry_weight,
                        id
                    )
                )

                conn.commit()
                conn.close()

                return redirect(
                    "/laundry-orders-page"
                )

            except ValueError:
                pass

    conn.close()

    return render_template(
        "edit_laundry_order.html",
        order=order
    )


# ============================================================
# DELETE LAUNDRY ORDER
# ============================================================

@app.route(
    "/laundry-orders-page/delete/<int:id>",
    methods=["POST"]
)
def delete_laundry_order_page(id):

    if not login_required():
        return redirect("/login")

    conn = get_db_connection()

    conn.execute(
        """
        DELETE FROM laundry_orders
        WHERE id = ?
        """,
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect(
        "/laundry-orders-page"
    )


# ============================================================
# PICKUP SCHEDULE PAGE
# ============================================================

@app.route(
    "/pickup-schedules-page",
    methods=["GET", "POST"]
)
def pickup_schedules_page():

    if not login_required():
        return redirect("/login")

    # ADD PICKUP
    if request.method == "POST":

        customer = request.form.get(
            "customer",
            ""
        ).strip()

        pickup_date = request.form.get(
            "pickup_date",
            ""
        ).strip()

        if customer and pickup_date:

            conn = get_db_connection()

            conn.execute(
                """
                INSERT INTO pickup_schedules
                (customer, pickup_date)
                VALUES (?, ?)
                """,
                (
                    customer,
                    pickup_date
                )
            )

            conn.commit()
            conn.close()

            return redirect(
                "/pickup-schedules-page"
            )

    conn = get_db_connection()

    pickups = conn.execute(
        """
        SELECT id, customer, pickup_date
        FROM pickup_schedules
        ORDER BY id DESC
        """
    ).fetchall()

    conn.close()

    return render_template(
        "pickup_schedules.html",
        pickups=pickups
    )


# ============================================================
# EDIT PICKUP SCHEDULE
# ============================================================

@app.route(
    "/pickup-schedules-page/edit/<int:id>",
    methods=["GET", "POST"]
)
def edit_pickup_schedule_page(id):

    if not login_required():
        return redirect("/login")

    conn = get_db_connection()

    pickup = conn.execute(
        """
        SELECT id, customer, pickup_date
        FROM pickup_schedules
        WHERE id = ?
        """,
        (id,)
    ).fetchone()

    if pickup is None:

        conn.close()

        return "Pickup schedule not found.", 404

    if request.method == "POST":

        customer = request.form.get(
            "customer",
            ""
        ).strip()

        pickup_date = request.form.get(
            "pickup_date",
            ""
        ).strip()

        if customer and pickup_date:

            conn.execute(
                """
                UPDATE pickup_schedules
                SET customer = ?,
                    pickup_date = ?
                WHERE id = ?
                """,
                (
                    customer,
                    pickup_date,
                    id
                )
            )

            conn.commit()
            conn.close()

            return redirect(
                "/pickup-schedules-page"
            )

    conn.close()

    return render_template(
        "edit_pickup_schedule.html",
        pickup=pickup
    )


# ============================================================
# DELETE PICKUP SCHEDULE
# ============================================================

@app.route(
    "/pickup-schedules-page/delete/<int:id>",
    methods=["POST"]
)
def delete_pickup_schedule_page(id):

    if not login_required():
        return redirect("/login")

    conn = get_db_connection()

    conn.execute(
        """
        DELETE FROM pickup_schedules
        WHERE id = ?
        """,
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect(
        "/pickup-schedules-page"
    )


# ============================================================
# DELIVERY RECORDS PAGE
# ============================================================

@app.route(
    "/delivery-records-page",
    methods=["GET", "POST"]
)
def delivery_records_page():

    if not login_required():
        return redirect("/login")

    # ADD DELIVERY
    if request.method == "POST":

        customer = request.form.get(
            "customer",
            ""
        ).strip()

        delivery_date = request.form.get(
            "delivery_date",
            ""
        ).strip()

        if customer and delivery_date:

            conn = get_db_connection()

            conn.execute(
                """
                INSERT INTO delivery_records
                (customer, delivery_date)
                VALUES (?, ?)
                """,
                (
                    customer,
                    delivery_date
                )
            )

            conn.commit()
            conn.close()

            return redirect(
                "/delivery-records-page"
            )

    conn = get_db_connection()

    deliveries = conn.execute(
        """
        SELECT id, customer, delivery_date
        FROM delivery_records
        ORDER BY id DESC
        """
    ).fetchall()

    conn.close()

    return render_template(
        "delivery_records.html",
        deliveries=deliveries
    )


# ============================================================
# EDIT DELIVERY RECORD
# ============================================================

@app.route(
    "/delivery-records-page/edit/<int:id>",
    methods=["GET", "POST"]
)
def edit_delivery_record_page(id):

    if not login_required():
        return redirect("/login")

    conn = get_db_connection()

    delivery = conn.execute(
        """
        SELECT id, customer, delivery_date
        FROM delivery_records
        WHERE id = ?
        """,
        (id,)
    ).fetchone()

    if delivery is None:

        conn.close()

        return "Delivery record not found.", 404

    if request.method == "POST":

        customer = request.form.get(
            "customer",
            ""
        ).strip()

        delivery_date = request.form.get(
            "delivery_date",
            ""
        ).strip()

        if customer and delivery_date:

            conn.execute(
                """
                UPDATE delivery_records
                SET customer = ?,
                    delivery_date = ?
                WHERE id = ?
                """,
                (
                    customer,
                    delivery_date,
                    id
                )
            )

            conn.commit()
            conn.close()

            return redirect(
                "/delivery-records-page"
            )

    conn.close()

    return render_template(
        "edit_delivery_record.html",
        delivery=delivery
    )


# ============================================================
# DELETE DELIVERY RECORD
# ============================================================

@app.route(
    "/delivery-records-page/delete/<int:id>",
    methods=["POST"]
)
def delete_delivery_record_page(id):

    if not login_required():
        return redirect("/login")

    conn = get_db_connection()

    conn.execute(
        """
        DELETE FROM delivery_records
        WHERE id = ?
        """,
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect(
        "/delivery-records-page"
    )


# ============================================================
# PAYMENTS PAGE
# ============================================================

# ============================================================
# PAYMENTS PAGE
# ============================================================

@app.route(
    "/payments-page",
    methods=["GET", "POST"]
)
def payments_page():

    if not login_required():
        return redirect("/login")

    # -------------------------
    # ADD PAYMENT
    # -------------------------

    if request.method == "POST":

        customer = request.form.get(
            "customer",
            ""
        ).strip()

        payment_amount = request.form.get(
            "payment_amount",
            ""
        ).strip()

        payment_method = request.form.get(
            "payment_method",
            ""
        ).strip()

        if not customer:
            return redirect("/payments-page")

        if not payment_amount:
            return redirect("/payments-page")

        if not payment_method:
            return redirect("/payments-page")

        try:
            payment_amount = float(payment_amount)

            if payment_amount <= 0:
                return redirect("/payments-page")

        except ValueError:
            return redirect("/payments-page")

        transaction_time = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        conn = get_db_connection()

        conn.execute(
            """
            INSERT INTO payments
            (
                customer,
                payment_amount,
                payment_method,
                transaction_time
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                customer,
                payment_amount,
                payment_method,
                transaction_time
            )
        )

        conn.commit()
        conn.close()

        return redirect("/payments-page?success=1")

    # -------------------------
    # GET PAYMENTS
    # -------------------------

    conn = get_db_connection()

    payments = conn.execute(
        """
        SELECT *
        FROM payments
        ORDER BY id DESC
        """
    ).fetchall()

    conn.close()

    formatted_payments = []

    for payment in payments:

        payment_data = dict(payment)

        transaction_time = payment_data.get(
            "transaction_time"
        )

        if transaction_time:

            try:

                dt = datetime.strptime(
                    transaction_time,
                    "%Y-%m-%d %H:%M:%S"
                )

                payment_data[
                    "formatted_transaction_time"
                ] = dt.strftime("%B %d, %Y")

                payment_data[
                    "formatted_transaction_clock"
                ] = dt.strftime("%I:%M %p").lstrip("0")

            except ValueError:

                payment_data[
                    "formatted_transaction_time"
                ] = transaction_time

                payment_data[
                    "formatted_transaction_clock"
                ] = ""

        else:

            payment_data[
                "formatted_transaction_time"
            ] = "—"

            payment_data[
                "formatted_transaction_clock"
            ] = ""

        formatted_payments.append(payment_data)

    return render_template(
        "payments.html",
        payments=formatted_payments
    )


# ============================================================
# EDIT PAYMENT
# ============================================================

@app.route(
    "/payments-page/edit/<int:id>",
    methods=["GET", "POST"]
)
def edit_payment_page(id):

    if not login_required():
        return redirect("/login")

    conn = get_db_connection()

    payment = conn.execute(
        """
        SELECT *
        FROM payments
        WHERE id = ?
        """,
        (id,)
    ).fetchone()

    if payment is None:

        conn.close()

        return "Payment not found.", 404

    if request.method == "POST":

        customer = request.form.get(
            "customer",
            ""
        ).strip()

        payment_amount = request.form.get(
            "payment_amount",
            ""
        ).strip()

        payment_method = request.form.get(
            "payment_method",
            ""
        ).strip()

        if (
            customer
            and payment_amount
            and payment_method
        ):

            try:

                payment_amount = float(
                    payment_amount
                )

                conn.execute(
                    """
                    UPDATE payments
                    SET customer = ?,
                        payment_amount = ?,
                        payment_method = ?
                    WHERE id = ?
                    """,
                    (
                        customer,
                        payment_amount,
                        payment_method,
                        id
                    )
                )

                conn.commit()
                conn.close()

                return redirect(
                    "/payments-page"
                )

            except ValueError:
                pass

    conn.close()

    return render_template(
        "edit_payment.html",
        payment=payment
    )


# ============================================================
# DELETE PAYMENT
# ============================================================

@app.route(
    "/payments-page/delete/<int:id>",
    methods=["POST"]
)
def delete_payment_page(id):

    if not login_required():
        return redirect("/login")

    conn = get_db_connection()

    conn.execute(
        """
        DELETE FROM payments
        WHERE id = ?
        """,
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect(
        "/payments-page"
    )


# ============================================================
# CUSTOMER EXISTS
# ============================================================

def customer_exists(customer_name):

    conn = get_db_connection()

    customer = conn.execute(
        """
        SELECT id
        FROM customers
        WHERE name = ?
        """,
        (customer_name,)
    ).fetchone()

    conn.close()

    return customer is not None


# ============================================================
# CUSTOMERS API
# ============================================================

@app.route("/customers", methods=["POST"])
def createCustomer():

    data = request.get_json(silent=True) or {}

    errors = {}

    if not data.get("name"):
        errors["name"] = "Name is required."

    if not data.get("contact_number"):
        errors["contact_number"] = (
            "Contact number is required."
        )

    if errors:

        return jsonify({
            "status": 422,
            "data": None,
            "error": {
                "code": "VALIDATION_ERROR",
                "message": "Validation failed.",
                "fields": errors
            }
        }), 422

    conn = get_db_connection()

    cursor = conn.execute(
        """
        INSERT INTO customers
        (name, contact_number)
        VALUES (?, ?)
        """,
        (
            data["name"],
            data["contact_number"]
        )
    )

    customer_id = cursor.lastrowid

    conn.commit()
    conn.close()

    return jsonify({
        "status": 201,
        "data": {
            "id": customer_id,
            "name": data["name"],
            "contact_number": data["contact_number"]
        },
        "error": None
    }), 201


@app.route("/customers", methods=["GET"])
def listCustomers():

    conn = get_db_connection()

    customers = conn.execute(
        """
        SELECT id, name, contact_number
        FROM customers
        ORDER BY id
        """
    ).fetchall()

    conn.close()

    return jsonify({
        "status": 200,
        "data": [
            dict(customer)
            for customer in customers
        ],
        "error": None
    }), 200


@app.route("/customers/<id>", methods=["GET"])
def showCustomer(id):

    conn = get_db_connection()

    customer = conn.execute(
        """
        SELECT id, name, contact_number
        FROM customers
        WHERE id = ?
        """,
        (id,)
    ).fetchone()

    conn.close()

    if customer is None:

        return jsonify({
            "status": 404,
            "data": None,
            "error": {
                "code": "NOT_FOUND",
                "message": "Customer not found."
            }
        }), 404

    return jsonify({
        "status": 200,
        "data": dict(customer),
        "error": None
    }), 200


@app.route("/customers/<id>", methods=["PUT"])
def updateCustomer(id):

    data = request.get_json(silent=True) or {}

    errors = {}

    if not data.get("name"):
        errors["name"] = "Name is required."

    if not data.get("contact_number"):
        errors["contact_number"] = (
            "Contact number is required."
        )

    if errors:

        return jsonify({
            "status": 422,
            "data": None,
            "error": {
                "code": "VALIDATION_ERROR",
                "message": "Validation failed.",
                "fields": errors
            }
        }), 422

    conn = get_db_connection()

    customer = conn.execute(
        """
        SELECT id
        FROM customers
        WHERE id = ?
        """,
        (id,)
    ).fetchone()

    if customer is None:

        conn.close()

        return jsonify({
            "status": 404,
            "data": None,
            "error": {
                "code": "NOT_FOUND",
                "message": "Customer not found."
            }
        }), 404

    conn.execute(
        """
        UPDATE customers
        SET name = ?, contact_number = ?
        WHERE id = ?
        """,
        (
            data["name"],
            data["contact_number"],
            id
        )
    )

    conn.commit()
    conn.close()

    return jsonify({
        "status": 200,
        "data": {
            "id": int(id),
            "name": data["name"],
            "contact_number": data["contact_number"]
        },
        "error": None
    }), 200


@app.route("/customers/<id>", methods=["DELETE"])
def deleteCustomer(id):

    conn = get_db_connection()

    customer = conn.execute(
        """
        SELECT id
        FROM customers
        WHERE id = ?
        """,
        (id,)
    ).fetchone()

    if customer is None:

        conn.close()

        return jsonify({
            "status": 404,
            "data": None,
            "error": {
                "code": "NOT_FOUND",
                "message": "Customer not found."
            }
        }), 404

    conn.execute(
        """
        DELETE FROM customers
        WHERE id = ?
        """,
        (id,)
    )

    conn.commit()
    conn.close()

    return jsonify({
        "status": 200,
        "data": {
            "message": "Customer deleted successfully.",
            "id": int(id)
        },
        "error": None
    }), 200


# ============================================================
# LAUNDRY ORDERS API
# ============================================================

@app.route("/laundry-orders", methods=["POST"])
def createLaundryOrder():

    data = request.get_json(silent=True) or {}

    errors = {}

    if not data.get("customer"):
        errors["customer"] = "Customer is required."

    if "laundry_weight" not in data:

        errors["laundry_weight"] = (
            "Laundry weight is required."
        )

    else:

        try:

            laundry_weight = float(
                data["laundry_weight"]
            )

            if laundry_weight <= 0:
                errors["laundry_weight"] = (
                    "Laundry weight must be greater than zero."
                )

        except (TypeError, ValueError):

            errors["laundry_weight"] = (
                "Laundry weight must be a number."
            )

    if errors:

        return jsonify({
            "status": 422,
            "data": None,
            "error": {
                "code": "VALIDATION_ERROR",
                "message": "Validation failed.",
                "fields": errors
            }
        }), 422

    if not customer_exists(
        data["customer"]
    ):

        return jsonify({
            "status": 404,
            "data": None,
            "error": {
                "code": "NOT_FOUND",
                "message": "Customer not found."
            }
        }), 404

    conn = get_db_connection()

    cursor = conn.execute(
        """
        INSERT INTO laundry_orders
        (customer, laundry_weight)
        VALUES (?, ?)
        """,
        (
            data["customer"],
            laundry_weight
        )
    )

    order_id = cursor.lastrowid

    conn.commit()
    conn.close()

    return jsonify({
        "status": 201,
        "data": {
            "id": order_id,
            "customer": data["customer"],
            "laundry_weight": laundry_weight
        },
        "error": None
    }), 201


@app.route("/laundry-orders", methods=["GET"])
def listLaundryOrders():

    conn = get_db_connection()

    orders = conn.execute(
        """
        SELECT id, customer, laundry_weight
        FROM laundry_orders
        ORDER BY id
        """
    ).fetchall()

    conn.close()

    return jsonify({
        "status": 200,
        "data": [
            dict(order)
            for order in orders
        ],
        "error": None
    }), 200


@app.route("/laundry-orders/<id>", methods=["GET"])
def showLaundryOrder(id):

    conn = get_db_connection()

    order = conn.execute(
        """
        SELECT id, customer, laundry_weight
        FROM laundry_orders
        WHERE id = ?
        """,
        (id,)
    ).fetchone()

    conn.close()

    if order is None:

        return jsonify({
            "status": 404,
            "data": None,
            "error": {
                "code": "NOT_FOUND",
                "message": "Laundry order not found."
            }
        }), 404

    return jsonify({
        "status": 200,
        "data": dict(order),
        "error": None
    }), 200


@app.route("/laundry-orders/<id>", methods=["PUT"])
def updateLaundryOrder(id):

    data = request.get_json(silent=True) or {}

    errors = {}

    if not data.get("customer"):
        errors["customer"] = "Customer is required."

    if "laundry_weight" not in data:

        errors["laundry_weight"] = (
            "Laundry weight is required."
        )

    else:

        try:

            laundry_weight = float(
                data["laundry_weight"]
            )

            if laundry_weight <= 0:
                errors["laundry_weight"] = (
                    "Laundry weight must be greater than zero."
                )

        except (TypeError, ValueError):

            errors["laundry_weight"] = (
                "Laundry weight must be a number."
            )

    if errors:

        return jsonify({
            "status": 422,
            "data": None,
            "error": {
                "code": "VALIDATION_ERROR",
                "message": "Validation failed.",
                "fields": errors
            }
        }), 422

    conn = get_db_connection()

    order = conn.execute(
        """
        SELECT id
        FROM laundry_orders
        WHERE id = ?
        """,
        (id,)
    ).fetchone()

    if order is None:

        conn.close()

        return jsonify({
            "status": 404,
            "data": None,
            "error": {
                "code": "NOT_FOUND",
                "message": "Laundry order not found."
            }
        }), 404

    conn.execute(
        """
        UPDATE laundry_orders
        SET customer = ?,
            laundry_weight = ?
        WHERE id = ?
        """,
        (
            data["customer"],
            laundry_weight,
            id
        )
    )

    conn.commit()
    conn.close()

    return jsonify({
        "status": 200,
        "data": {
            "id": int(id),
            "customer": data["customer"],
            "laundry_weight": laundry_weight
        },
        "error": None
    }), 200


@app.route("/laundry-orders/<id>", methods=["DELETE"])
def deleteLaundryOrder(id):

    conn = get_db_connection()

    order = conn.execute(
        """
        SELECT id
        FROM laundry_orders
        WHERE id = ?
        """,
        (id,)
    ).fetchone()

    if order is None:

        conn.close()

        return jsonify({
            "status": 404,
            "data": None,
            "error": {
                "code": "NOT_FOUND",
                "message": "Laundry order not found."
            }
        }), 404

    conn.execute(
        """
        DELETE FROM laundry_orders
        WHERE id = ?
        """,
        (id,)
    )

    conn.commit()
    conn.close()

    return jsonify({
        "status": 200,
        "data": {
            "message": "Laundry order deleted successfully.",
            "id": int(id)
        },
        "error": None
    }), 200


# ============================================================
# PICKUP SCHEDULE API
# ============================================================

@app.route("/pickup-schedules", methods=["GET"])
def listPickupSchedules():

    conn = get_db_connection()

    schedules = conn.execute(
        """
        SELECT id, customer, pickup_date
        FROM pickup_schedules
        ORDER BY id
        """
    ).fetchall()

    conn.close()

    return jsonify({
        "status": 200,
        "data": [
            dict(schedule)
            for schedule in schedules
        ],
        "error": None
    }), 200


@app.route("/pickup-schedules", methods=["POST"])
def createPickupSchedule():

    data = request.get_json(silent=True) or {}

    errors = {}

    if not data.get("pickup_date"):
        errors["pickup_date"] = (
            "Pickup date is required."
        )

    if not data.get("customer"):
        errors["customer"] = (
            "Customer is required."
        )

    if errors:

        return jsonify({
            "status": 422,
            "data": None,
            "error": {
                "code": "VALIDATION_ERROR",
                "message": "Validation failed.",
                "fields": errors
            }
        }), 422

    if not customer_exists(
        data["customer"]
    ):

        return jsonify({
            "status": 404,
            "data": None,
            "error": {
                "code": "NOT_FOUND",
                "message": "Customer not found."
            }
        }), 404

    conn = get_db_connection()

    cursor = conn.execute(
        """
        INSERT INTO pickup_schedules
        (customer, pickup_date)
        VALUES (?, ?)
        """,
        (
            data["customer"],
            data["pickup_date"]
        )
    )

    schedule_id = cursor.lastrowid

    conn.commit()
    conn.close()

    return jsonify({
        "status": 201,
        "data": {
            "id": schedule_id,
            "customer": data["customer"],
            "pickup_date": data["pickup_date"]
        },
        "error": None
    }), 201


@app.route("/pickup-schedules/<id>", methods=["GET"])
def showPickupSchedule(id):

    conn = get_db_connection()

    schedule = conn.execute(
        """
        SELECT id, customer, pickup_date
        FROM pickup_schedules
        WHERE id = ?
        """,
        (id,)
    ).fetchone()

    conn.close()

    if schedule is None:

        return jsonify({
            "status": 404,
            "data": None,
            "error": {
                "code": "NOT_FOUND",
                "message": "Pickup schedule not found."
            }
        }), 404

    return jsonify({
        "status": 200,
        "data": dict(schedule),
        "error": None
    }), 200


@app.route("/pickup-schedules/<id>", methods=["PUT"])
def updatePickupSchedule(id):

    data = request.get_json(silent=True) or {}

    errors = {}

    if not data.get("pickup_date"):
        errors["pickup_date"] = (
            "Pickup date is required."
        )

    if not data.get("customer"):
        errors["customer"] = (
            "Customer is required."
        )

    if errors:

        return jsonify({
            "status": 422,
            "data": None,
            "error": {
                "code": "VALIDATION_ERROR",
                "message": "Validation failed.",
                "fields": errors
            }
        }), 422

    conn = get_db_connection()

    schedule = conn.execute(
        """
        SELECT id
        FROM pickup_schedules
        WHERE id = ?
        """,
        (id,)
    ).fetchone()

    if schedule is None:

        conn.close()

        return jsonify({
            "status": 404,
            "data": None,
            "error": {
                "code": "NOT_FOUND",
                "message": "Pickup schedule not found."
            }
        }), 404

    conn.execute(
        """
        UPDATE pickup_schedules
        SET customer = ?,
            pickup_date = ?
        WHERE id = ?
        """,
        (
            data["customer"],
            data["pickup_date"],
            id
        )
    )

    conn.commit()
    conn.close()

    return jsonify({
        "status": 200,
        "data": {
            "id": int(id),
            "customer": data["customer"],
            "pickup_date": data["pickup_date"]
        },
        "error": None
    }), 200


@app.route("/pickup-schedules/<id>", methods=["DELETE"])
def deletePickupSchedule(id):

    conn = get_db_connection()

    schedule = conn.execute(
        """
        SELECT id
        FROM pickup_schedules
        WHERE id = ?
        """,
        (id,)
    ).fetchone()

    if schedule is None:

        conn.close()

        return jsonify({
            "status": 404,
            "data": None,
            "error": {
                "code": "NOT_FOUND",
                "message": "Pickup schedule not found."
            }
        }), 404

    conn.execute(
        """
        DELETE FROM pickup_schedules
        WHERE id = ?
        """,
        (id,)
    )

    conn.commit()
    conn.close()

    return jsonify({
        "status": 200,
        "data": {
            "message": "Pickup schedule deleted successfully.",
            "id": int(id)
        },
        "error": None
    }), 200


# ============================================================
# DELIVERY RECORDS API
# ============================================================

@app.route("/delivery-records", methods=["POST"])
def createDeliveryRecord():

    data = request.get_json(silent=True) or {}

    errors = {}

    if not data.get("delivery_date"):
        errors["delivery_date"] = (
            "Delivery date is required."
        )

    if not data.get("customer"):
        errors["customer"] = (
            "Customer is required."
        )

    if errors:

        return jsonify({
            "status": 422,
            "data": None,
            "error": {
                "code": "VALIDATION_ERROR",
                "message": "Validation failed.",
                "fields": errors
            }
        }), 422

    if not customer_exists(
        data["customer"]
    ):

        return jsonify({
            "status": 404,
            "data": None,
            "error": {
                "code": "NOT_FOUND",
                "message": "Customer not found."
            }
        }), 404

    conn = get_db_connection()

    cursor = conn.execute(
        """
        INSERT INTO delivery_records
        (customer, delivery_date)
        VALUES (?, ?)
        """,
        (
            data["customer"],
            data["delivery_date"]
        )
    )

    delivery_id = cursor.lastrowid

    conn.commit()
    conn.close()

    return jsonify({
        "status": 201,
        "data": {
            "id": delivery_id,
            "customer": data["customer"],
            "delivery_date": data["delivery_date"]
        },
        "error": None
    }), 201


@app.route("/delivery-records", methods=["GET"])
def listDeliveryRecords():

    conn = get_db_connection()

    records = conn.execute(
        """
        SELECT id, customer, delivery_date
        FROM delivery_records
        ORDER BY id
        """
    ).fetchall()

    conn.close()

    return jsonify({
        "status": 200,
        "data": [
            dict(record)
            for record in records
        ],
        "error": None
    }), 200


@app.route("/delivery-records/<id>", methods=["GET"])
def showDeliveryRecord(id):

    conn = get_db_connection()

    record = conn.execute(
        """
        SELECT id, customer, delivery_date
        FROM delivery_records
        WHERE id = ?
        """,
        (id,)
    ).fetchone()

    conn.close()

    if record is None:

        return jsonify({
            "status": 404,
            "data": None,
            "error": {
                "code": "NOT_FOUND",
                "message": "Delivery record not found."
            }
        }), 404

    return jsonify({
        "status": 200,
        "data": dict(record),
        "error": None
    }), 200


@app.route("/delivery-records/<id>", methods=["PUT"])
def updateDeliveryRecord(id):

    data = request.get_json(silent=True) or {}

    errors = {}

    if not data.get("delivery_date"):
        errors["delivery_date"] = (
            "Delivery date is required."
        )

    if not data.get("customer"):
        errors["customer"] = (
            "Customer is required."
        )

    if errors:

        return jsonify({
            "status": 422,
            "data": None,
            "error": {
                "code": "VALIDATION_ERROR",
                "message": "Validation failed.",
                "fields": errors
            }
        }), 422

    conn = get_db_connection()

    record = conn.execute(
        """
        SELECT id
        FROM delivery_records
        WHERE id = ?
        """,
        (id,)
    ).fetchone()

    if record is None:

        conn.close()

        return jsonify({
            "status": 404,
            "data": None,
            "error": {
                "code": "NOT_FOUND",
                "message": "Delivery record not found."
            }
        }), 404

    conn.execute(
        """
        UPDATE delivery_records
        SET customer = ?,
            delivery_date = ?
        WHERE id = ?
        """,
        (
            data["customer"],
            data["delivery_date"],
            id
        )
    )

    conn.commit()
    conn.close()

    return jsonify({
        "status": 200,
        "data": {
            "id": int(id),
            "customer": data["customer"],
            "delivery_date": data["delivery_date"]
        },
        "error": None
    }), 200


@app.route("/delivery-records/<id>", methods=["DELETE"])
def deleteDeliveryRecord(id):

    conn = get_db_connection()

    record = conn.execute(
        """
        SELECT id
        FROM delivery_records
        WHERE id = ?
        """,
        (id,)
    ).fetchone()

    if record is None:

        conn.close()

        return jsonify({
            "status": 404,
            "data": None,
            "error": {
                "code": "NOT_FOUND",
                "message": "Delivery record not found."
            }
        }), 404

    conn.execute(
        """
        DELETE FROM delivery_records
        WHERE id = ?
        """,
        (id,)
    )

    conn.commit()
    conn.close()

    return jsonify({
        "status": 200,
        "data": {
            "message": "Delivery record deleted successfully.",
            "id": int(id)
        },
        "error": None
    }), 200


# ============================================================
# PAYMENTS API
# ============================================================

@app.route("/payments", methods=["POST"])
def createPayment():

    data = request.get_json(silent=True) or {}

    errors = {}

    if not data.get("customer"):
        errors["customer"] = (
            "Customer is required."
        )

    if "payment_amount" not in data:

        errors["payment_amount"] = (
            "Payment amount is required."
        )

    else:

        try:

            payment_amount = float(
                data["payment_amount"]
            )

            if payment_amount <= 0:
                errors["payment_amount"] = (
                    "Payment amount must be greater than zero."
                )

        except (TypeError, ValueError):

            errors["payment_amount"] = (
                "Payment amount must be a number."
            )

    if not data.get("payment_method"):
        errors["payment_method"] = (
            "Payment method is required."
        )

    if errors:

        return jsonify({
            "status": 422,
            "data": None,
            "error": {
                "code": "VALIDATION_ERROR",
                "message": "Validation failed.",
                "fields": errors
            }
        }), 422

    conn = get_db_connection()

    transaction_time = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    cursor = conn.execute(
        """
        INSERT INTO payments
        (
            customer,
            payment_amount,
            payment_method,
            transaction_time
        )
        VALUES (?, ?, ?, ?)
        """,
        (
            data["customer"],
            payment_amount,
            data["payment_method"],
            transaction_time
        )
    )

    payment_id = cursor.lastrowid

    conn.commit()
    conn.close()

    return jsonify({
        "status": 201,
        "data": {
            "id": payment_id,
            "customer": data["customer"],
            "payment_amount": payment_amount,
            "payment_method": data["payment_method"],
            "transaction_time": transaction_time
        },
        "error": None
    }), 201


@app.route("/payments", methods=["GET"])
def listPayments():

    conn = get_db_connection()

    payments = conn.execute(
        """
        SELECT
            id,
            customer,
            payment_amount,
            payment_method,
            transaction_time
        FROM payments
        ORDER BY id
        """
    ).fetchall()

    conn.close()

    return jsonify({
        "status": 200,
        "data": [
            dict(payment)
            for payment in payments
        ],
        "error": None
    }), 200


@app.route("/payments/<id>", methods=["GET"])
def showPayment(id):

    conn = get_db_connection()

    payment = conn.execute(
        """
        SELECT
            id,
            customer,
            payment_amount,
            payment_method,
            transaction_time
        FROM payments
        WHERE id = ?
        """,
        (id,)
    ).fetchone()

    conn.close()

    if payment is None:

        return jsonify({
            "status": 404,
            "data": None,
            "error": {
                "code": "NOT_FOUND",
                "message": "Payment not found."
            }
        }), 404

    return jsonify({
        "status": 200,
        "data": dict(payment),
        "error": None
    }), 200


@app.route("/payments/<id>", methods=["PUT"])
def updatePayment(id):

    data = request.get_json(silent=True) or {}

    errors = {}

    if not data.get("customer"):
        errors["customer"] = (
            "Customer is required."
        )

    if "payment_amount" not in data:

        errors["payment_amount"] = (
            "Payment amount is required."
        )

    else:

        try:

            payment_amount = float(
                data["payment_amount"]
            )

            if payment_amount <= 0:
                errors["payment_amount"] = (
                    "Payment amount must be greater than zero."
                )

        except (TypeError, ValueError):

            errors["payment_amount"] = (
                "Payment amount must be a number."
            )

    if not data.get("payment_method"):
        errors["payment_method"] = (
            "Payment method is required."
        )

    if errors:

        return jsonify({
            "status": 422,
            "data": None,
            "error": {
                "code": "VALIDATION_ERROR",
                "message": "Validation failed.",
                "fields": errors
            }
        }), 422

    conn = get_db_connection()

    payment = conn.execute(
        """
        SELECT id
        FROM payments
        WHERE id = ?
        """,
        (id,)
    ).fetchone()

    if payment is None:

        conn.close()

        return jsonify({
            "status": 404,
            "data": None,
            "error": {
                "code": "NOT_FOUND",
                "message": "Payment not found."
            }
        }), 404

    conn.execute(
        """
        UPDATE payments
        SET customer = ?,
            payment_amount = ?,
            payment_method = ?
        WHERE id = ?
        """,
        (
            data["customer"],
            payment_amount,
            data["payment_method"],
            id
        )
    )

    conn.commit()
    conn.close()

    return jsonify({
        "status": 200,
        "data": {
            "id": int(id),
            "customer": data["customer"],
            "payment_amount": payment_amount,
            "payment_method": data["payment_method"]
        },
        "error": None
    }), 200


@app.route("/payments/<id>", methods=["DELETE"])
def deletePayment(id):

    conn = get_db_connection()

    payment = conn.execute(
        """
        SELECT id
        FROM payments
        WHERE id = ?
        """,
        (id,)
    ).fetchone()

    if payment is None:

        conn.close()

        return jsonify({
            "status": 404,
            "data": None,
            "error": {
                "code": "NOT_FOUND",
                "message": "Payment not found."
            }
        }), 404

    conn.execute(
        """
        DELETE FROM payments
        WHERE id = ?
        """,
        (id,)
    )

    conn.commit()
    conn.close()

    return jsonify({
        "status": 200,
        "data": {
            "message": "Payment deleted successfully.",
            "id": int(id)
        },
        "error": None
    }), 200


# ============================================================
# RUN APPLICATION
# ============================================================

# ============================================================
# RUN APPLICATION
# ============================================================

if __name__ == "__main__":
    app.run(
        debug=True,
        host="127.0.0.1",
        port=5000
    )