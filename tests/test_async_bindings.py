import pytest
import sqlite3
from app import app, init_database


@pytest.fixture
def auth_client():
    """Sets up a Flask test client with an authenticated admin session."""
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    init_database()

    with app.test_client() as client:
        with client.session_transaction() as sess:
            sess['user_id'] = 1
            sess['username'] = 'admin'
            sess['role'] = 'admin'
        yield client


# ============================================================================
# 1. LAUNDRY ORDERS - ASYNC BINDING TESTS
# ============================================================================

def test_async_create_order_success(auth_client):
    """Test: Intercepted async POST to create order returns 201 and JSON payload."""
    payload = {
        'customer': 'Async Maria',
        'laundry_weight': '4.5',
        'service_type': 'Wash & Fold',
        'status': 'Received',
        'total_price': '225.00'
    }
    response = auth_client.post(
        '/laundry-orders-page',
        json=payload,
        headers={'X-Requested-With': 'XMLHttpRequest', 'Accept': 'application/json'}
    )
    assert response.status_code == 201
    data = response.get_json()
    assert data['status'] == 201
    assert data['data']['customer'] == 'Async Maria'
    assert data['data']['laundry_weight'] == 4.5
    assert 'Order #' in data['message']


def test_async_create_order_validation_error_422(auth_client):
    """Test: Submitting invalid/empty order returns 422 with structured field errors."""
    payload = {
        'customer': '',
        'laundry_weight': '',
    }
    response = auth_client.post(
        '/laundry-orders-page',
        json=payload,
        headers={'X-Requested-With': 'XMLHttpRequest', 'Accept': 'application/json'}
    )
    assert response.status_code == 422
    data = response.get_json()
    assert data['status'] == 422
    assert 'customer' in data['error']
    assert 'laundry_weight' in data['error']


def test_async_edit_order_success(auth_client):
    """Test: Async PUT/POST to edit order updates record and returns 200."""
    # First create an order
    conn = sqlite3.connect('laundry.db')
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO laundry_orders (customer, laundry_weight, service_type, status) VALUES (?, ?, ?, ?)",
        ('Original Customer', 3.0, 'Wash & Fold', 'Received')
    )
    order_id = cursor.lastrowid
    conn.commit()
    conn.close()

    update_payload = {
        'customer': 'Updated Customer',
        'laundry_weight': '5.0',
        'service_type': 'Dry Cleaning',
        'status': 'In Wash',
        'total_price': '400.00'
    }
    response = auth_client.post(
        f'/laundry-orders-page/edit/{order_id}',
        json=update_payload,
        headers={'X-Requested-With': 'XMLHttpRequest', 'Accept': 'application/json'}
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 200
    assert data['data']['customer'] == 'Updated Customer'
    assert data['data']['laundry_weight'] == 5.0


# ============================================================================
# 2. DELIVERIES - ASYNC BINDING TESTS
# ============================================================================

def test_async_create_delivery_success(auth_client):
    """Test: Async POST to dispatch delivery returns 201 and JSON payload."""
    payload = {
        'customer': 'Carlos Mendoza',
        'delivery_date': '2026-09-25',
        'delivery_address': 'Block 12 Lot 5, Maramag, Bukidnon',
        'status': 'Scheduled',
        'assigned_rider': 'Rider Mike',
        'delivery_notes': 'Leave at porch'
    }
    response = auth_client.post(
        '/delivery-records-page',
        json=payload,
        headers={'X-Requested-With': 'XMLHttpRequest', 'Accept': 'application/json'}
    )
    assert response.status_code == 201
    data = response.get_json()
    assert data['status'] == 201
    assert data['data']['customer'] == 'Carlos Mendoza'


def test_async_create_delivery_validation_error_422(auth_client):
    """Test: Submitting delivery without customer or delivery_date returns 422."""
    payload = {
        'customer': '',
        'delivery_date': ''
    }
    response = auth_client.post(
        '/delivery-records-page',
        json=payload,
        headers={'X-Requested-With': 'XMLHttpRequest', 'Accept': 'application/json'}
    )
    assert response.status_code == 422
    data = response.get_json()
    assert data['status'] == 422
    assert 'customer' in data['error']
    assert 'delivery_date' in data['error']


# ============================================================================
# 3. PICKUPS - ASYNC BINDING TESTS
# ============================================================================

def test_async_create_pickup_success(auth_client):
    """Test: Async POST to schedule pickup returns 201 and JSON payload."""
    payload = {
        'customer': 'Ana Reyes',
        'pickup_date': '2026-09-26',
        'pickup_time': '02:00 PM - 05:00 PM',
        'pickup_address': 'Poblacion, Valencia City',
        'status': 'Pending'
    }
    response = auth_client.post(
        '/pickup-schedules-page',
        json=payload,
        headers={'X-Requested-With': 'XMLHttpRequest', 'Accept': 'application/json'}
    )
    assert response.status_code == 201
    data = response.get_json()
    assert data['status'] == 201
    assert data['data']['customer'] == 'Ana Reyes'


def test_async_create_pickup_validation_error_422(auth_client):
    """Test: Submitting pickup without required customer returns 422."""
    payload = {
        'customer': '',
        'pickup_date': '2026-09-26'
    }
    response = auth_client.post(
        '/pickup-schedules-page',
        json=payload,
        headers={'X-Requested-With': 'XMLHttpRequest', 'Accept': 'application/json'}
    )
    assert response.status_code == 422
    data = response.get_json()
    assert data['status'] == 422
    assert 'customer' in data['error']


# ============================================================================
# 4. CUSTOMERS - ASYNC BINDING TESTS
# ============================================================================

def test_async_create_customer_success(auth_client):
    """Test: Async POST to create customer returns 201 and JSON."""
    payload = {
        'name': 'Gabriel Ramos',
        'contact_number': '0918-765-4321',
        'email': 'gabriel@example.com',
        'address': 'Base Camp, Maramag',
        'membership': 'VIP'
    }
    response = auth_client.post(
        '/customers-page',
        json=payload,
        headers={'X-Requested-With': 'XMLHttpRequest', 'Accept': 'application/json'}
    )
    assert response.status_code == 201
    data = response.get_json()
    assert data['status'] == 201
    assert data['data']['name'] == 'Gabriel Ramos'


def test_async_create_customer_validation_error_422(auth_client):
    """Test: Submitting empty customer returns 422 field errors."""
    payload = {
        'name': '',
        'contact_number': ''
    }
    response = auth_client.post(
        '/customers-page',
        json=payload,
        headers={'X-Requested-With': 'XMLHttpRequest', 'Accept': 'application/json'}
    )
    assert response.status_code == 422
    data = response.get_json()
    assert data['status'] == 422
    assert 'name' in data['error']
    assert 'contact_number' in data['error']


# ============================================================================
# 5. PAYMENTS - ASYNC BINDING TESTS
# ============================================================================

def test_async_create_payment_success(auth_client):
    """Test: Async POST to record payment returns 201 and JSON."""
    payload = {
        'customer': 'Gabriel Ramos',
        'payment_amount': '350.00',
        'payment_method': 'GCash',
        'status': 'Paid',
        'notes': 'Online checkout'
    }
    response = auth_client.post(
        '/payments-page',
        json=payload,
        headers={'X-Requested-With': 'XMLHttpRequest', 'Accept': 'application/json'}
    )
    assert response.status_code == 201
    data = response.get_json()
    assert data['status'] == 201
    assert data['data']['customer'] == 'Gabriel Ramos'
    assert data['data']['payment_amount'] == 350.0


def test_async_create_payment_validation_error_422(auth_client):
    """Test: Submitting invalid payment returns 422 field errors."""
    payload = {
        'customer': '',
        'payment_amount': '-50',
        'payment_method': ''
    }
    response = auth_client.post(
        '/payments-page',
        json=payload,
        headers={'X-Requested-With': 'XMLHttpRequest', 'Accept': 'application/json'}
    )
    assert response.status_code == 422
    data = response.get_json()
    assert data['status'] == 422
    assert 'customer' in data['error']
    assert 'payment_amount' in data['error']
    assert 'payment_method' in data['error']
