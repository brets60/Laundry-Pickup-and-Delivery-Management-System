import pytest
import sqlite3
from app import app, init_database


@pytest.fixture
def auth_client():
    """Sets up a Flask test client with an authenticated session."""
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    init_database()

    with app.test_client() as client:
        # Simulate logged-in user
        with client.session_transaction() as sess:
            sess['user_id'] = 1
            sess['username'] = 'admin'
        yield client


@pytest.fixture
def unauth_client():
    """Sets up an unauthenticated Flask test client."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_delivery_requires_authentication(unauth_client):
    """Test: Accessing delivery records without logging in redirects to login page."""
    response = unauth_client.get('/delivery-records-page')
    assert response.status_code == 302
    assert '/login' in response.headers.get('Location', '')


def test_create_delivery_success(auth_client):
    """Test: Successfully creating a delivery record with all enhanced fields."""
    response = auth_client.post('/delivery-records-page', data={
        'customer': 'Juan Dela Cruz',
        'delivery_date': '2026-09-20',
        'delivery_address': 'Unit 402, Sunset Towers, Manila',
        'status': 'Scheduled',
        'assigned_rider': 'Rider Mike',
        'delivery_notes': 'Please call 10 minutes before arrival',
        'order_id': ''
    }, follow_redirects=True)

    assert response.status_code == 200

    # Verify database insertion
    conn = sqlite3.connect('laundry.db')
    conn.row_factory = sqlite3.Row
    record = conn.execute(
        "SELECT * FROM delivery_records WHERE customer = ? ORDER BY id DESC LIMIT 1",
        ('Juan Dela Cruz',)
    ).fetchone()
    conn.close()

    assert record is not None
    assert record['customer'] == 'Juan Dela Cruz'
    assert record['delivery_date'] == '2026-09-20'
    assert record['delivery_address'] == 'Unit 402, Sunset Towers, Manila'
    assert record['status'] == 'Scheduled'
    assert record['assigned_rider'] == 'Rider Mike'
    assert record['delivery_notes'] == 'Please call 10 minutes before arrival'


def test_create_delivery_validation_missing_fields(auth_client):
    """Test: Form validation prevents submission with missing required fields."""
    # Missing delivery date
    response = auth_client.post('/delivery-records-page', data={
        'customer': 'Test Customer',
        'delivery_date': ''
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b"Validation Error: Delivery Date is required" in response.data

    # Missing customer name
    response2 = auth_client.post('/delivery-records-page', data={
        'customer': '',
        'delivery_date': '2026-09-25'
    }, follow_redirects=True)
    assert response2.status_code == 200
    assert b"Validation Error: Customer Name is required" in response2.data


def test_edit_delivery_status(auth_client):
    """Test: Updating a delivery record's status and rider."""
    # Insert a test record
    conn = sqlite3.connect('laundry.db')
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO delivery_records (customer, delivery_date, status) VALUES (?, ?, ?)",
        ('Maria Santos', '2026-09-21', 'Scheduled')
    )
    delivery_id = cursor.lastrowid
    conn.commit()
    conn.close()

    # Post update
    response = auth_client.post(f'/delivery-records-page/edit/{delivery_id}', data={
        'customer': 'Maria Santos',
        'delivery_date': '2026-09-21',
        'delivery_address': '77 Oak St, Quezon City',
        'status': 'Delivered',
        'assigned_rider': 'Rider Alex',
        'delivery_notes': 'Left with concierge',
        'order_id': ''
    }, follow_redirects=True)

    assert response.status_code == 200

    conn = sqlite3.connect('laundry.db')
    conn.row_factory = sqlite3.Row
    updated = conn.execute("SELECT * FROM delivery_records WHERE id = ?", (delivery_id,)).fetchone()
    conn.close()

    assert updated['status'] == 'Delivered'
    assert updated['delivery_address'] == '77 Oak St, Quezon City'
    assert updated['assigned_rider'] == 'Rider Alex'


def test_delivery_details_page(auth_client):
    """Test: Viewing delivery details page."""
    conn = sqlite3.connect('laundry.db')
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO delivery_records (customer, delivery_date, delivery_address, status) VALUES (?, ?, ?, ?)",
        ('Carlos Reyes', '2026-09-22', 'Block 5 Lot 2, Pasig', 'Out for Delivery')
    )
    delivery_id = cursor.lastrowid
    conn.commit()
    conn.close()

    response = auth_client.get(f'/delivery-records-page/details/{delivery_id}')
    assert response.status_code == 200
    assert b"Carlos Reyes" in response.data
    assert b"Block 5 Lot 2, Pasig" in response.data
    assert b"Out for Delivery" in response.data


def test_delete_delivery(auth_client):
    """Test: Deleting a delivery record."""
    conn = sqlite3.connect('laundry.db')
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO delivery_records (customer, delivery_date) VALUES (?, ?)",
        ('Delete Me', '2026-09-23')
    )
    delivery_id = cursor.lastrowid
    conn.commit()
    conn.close()

    response = auth_client.post(f'/delivery-records-page/delete/{delivery_id}', follow_redirects=True)
    assert response.status_code == 200

    conn = sqlite3.connect('laundry.db')
    deleted = conn.execute("SELECT * FROM delivery_records WHERE id = ?", (delivery_id,)).fetchone()
    conn.close()
    assert deleted is None


def test_dispatch_order_creates_delivery_and_updates_status(auth_client):
    """Test: Dispatching an order creates a delivery_record and updates laundry_orders status."""
    conn = sqlite3.connect('laundry.db')
    cursor = conn.cursor()
    # Create test customer with TCCI address
    cursor.execute(
        "INSERT INTO customers (name, contact_number, address) VALUES (?, ?, ?)",
        ('Test Dorm Student', '09171234567', 'Torres Capitol College Dorms, Panadtalan')
    )
    # Create test order
    cursor.execute(
        "INSERT INTO laundry_orders (customer, laundry_weight, service_type, status, total_price) VALUES (?, ?, ?, ?, ?)",
        ('Test Dorm Student', 5.0, 'Wash-Dry-Fold', 'Ready for Delivery', 175.0)
    )
    order_id = cursor.lastrowid
    conn.commit()
    conn.close()

    # Dispatch the order
    response = auth_client.get(f'/laundry-orders-page/dispatch/{order_id}', follow_redirects=True)
    assert response.status_code == 200
    assert b"successfully dispatched" in response.data

    conn = sqlite3.connect('laundry.db')
    conn.row_factory = sqlite3.Row
    del_rec = conn.execute("SELECT * FROM delivery_records WHERE order_id = ?", (order_id,)).fetchone()
    order_rec = conn.execute("SELECT * FROM laundry_orders WHERE id = ?", (order_id,)).fetchone()
    conn.close()

    assert del_rec is not None
    assert del_rec['customer'] == 'Test Dorm Student'
    assert del_rec['assigned_rider'] == 'Tristan Dave Plaza'
    assert order_rec['status'] == 'Out for Delivery'


def test_dispatch_order_already_dispatched(auth_client):
    """Test: Dispatching an already dispatched order redirects with info message without duplicate records."""
    conn = sqlite3.connect('laundry.db')
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO laundry_orders (customer, laundry_weight, service_type, status, total_price) VALUES (?, ?, ?, ?, ?)",
        ('Repeat Customer', 4.0, 'Wash-Dry-Fold', 'Out for Delivery', 140.0)
    )
    order_id = cursor.lastrowid
    cursor.execute(
        "INSERT INTO delivery_records (customer, order_id, delivery_date, status) VALUES (?, ?, '2026-10-08', 'Scheduled')",
        ('Repeat Customer', order_id)
    )
    conn.commit()
    conn.close()

    response = auth_client.get(f'/laundry-orders-page/dispatch/{order_id}', follow_redirects=True)
    assert response.status_code == 200
    assert b"is already dispatched" in response.data

