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
# 1. 404 ERROR HANDLING TESTS (SYNC & ASYNC)
# ============================================================================

def test_404_page_rendering_sync(auth_client):
    """Test: Navigating to a non-existent route returns 404 with custom dark-glass error page."""
    response = auth_client.get('/definitely-non-existent-route-404')
    assert response.status_code == 404
    html = response.data.decode('utf-8')
    assert 'Page Not Found' in html or '404' in html
    assert 'Return to Dashboard' in html or 'dashboard' in html.lower()


def test_404_async_request_json(auth_client):
    """Test: Sending an async fetch to a non-existent route returns 404 JSON."""
    response = auth_client.get(
        '/definitely-non-existent-route-404',
        headers={'X-Requested-With': 'XMLHttpRequest', 'Accept': 'application/json'}
    )
    assert response.status_code == 404
    data = response.get_json()
    assert data is not None
    assert data.get('status') == 404
    assert 'error' in data or 'message' in data


# ============================================================================
# 2. MISSING RECORD 404 LOOKUP TESTS ACROSS ALL 5 MODULES
# ============================================================================

def test_missing_order_details_returns_404(auth_client):
    """Test: Accessing details for a non-existent order ID returns 404 error page."""
    response = auth_client.get('/laundry-orders-page/details/999999')
    assert response.status_code == 404
    html = response.data.decode('utf-8')
    assert '404' in html


def test_missing_order_edit_returns_404(auth_client):
    """Test: Accessing edit page for a non-existent order ID returns 404."""
    response = auth_client.get('/laundry-orders-page/edit/999999')
    assert response.status_code == 404
    html = response.data.decode('utf-8')
    assert '404' in html


def test_missing_delivery_details_returns_404(auth_client):
    """Test: Accessing details for a non-existent delivery ID returns 404."""
    response = auth_client.get('/delivery-records-page/details/999999')
    assert response.status_code == 404
    html = response.data.decode('utf-8')
    assert '404' in html


def test_missing_pickup_details_returns_404(auth_client):
    """Test: Accessing details for a non-existent pickup ID returns 404."""
    response = auth_client.get('/pickup-schedules-page/details/999999')
    assert response.status_code == 404
    html = response.data.decode('utf-8')
    assert '404' in html


def test_missing_customer_details_returns_404(auth_client):
    """Test: Accessing details for a non-existent customer ID returns 404."""
    response = auth_client.get('/customers-page/details/999999')
    assert response.status_code == 404
    html = response.data.decode('utf-8')
    assert '404' in html


def test_missing_payment_details_returns_404(auth_client):
    """Test: Accessing details for a non-existent payment ID returns 404."""
    response = auth_client.get('/payments-page/details/999999')
    assert response.status_code == 404
    html = response.data.decode('utf-8')
    assert '404' in html


# ============================================================================
# 3. ASYNC DELETION TESTS & 404 INTEGRATION ACROSS ALL 5 MODULES
# ============================================================================

def test_async_delete_order(auth_client):
    """Test: Async deleting an order removes it and returns 200 JSON; repeat delete returns 404."""
    # 1. Create order
    create_res = auth_client.post(
        '/laundry-orders-page',
        json={'customer': 'Test Order Delete', 'laundry_weight': 5.0, 'service_type': 'Wash & Fold'},
        headers={'X-Requested-With': 'XMLHttpRequest', 'Accept': 'application/json'}
    )
    assert create_res.status_code == 201
    order_id = create_res.get_json()['data']['id']

    # 2. Delete order asynchronously
    del_res = auth_client.post(
        f'/laundry-orders-page/delete/{order_id}',
        headers={'X-Requested-With': 'XMLHttpRequest', 'Accept': 'application/json'}
    )
    assert del_res.status_code == 200
    data = del_res.get_json()
    assert data['status'] == 200
    assert 'deleted' in data['message'].lower()

    # 3. Verify gone from database
    conn = sqlite3.connect('laundry.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM laundry_orders WHERE id = ?", (order_id,))
    assert cursor.fetchone() is None
    conn.close()

    # 4. Attempt second delete -> should return 404
    repeat_del = auth_client.post(
        f'/laundry-orders-page/delete/{order_id}',
        headers={'X-Requested-With': 'XMLHttpRequest', 'Accept': 'application/json'}
    )
    assert repeat_del.status_code == 404
    assert repeat_del.get_json()['status'] == 404


def test_async_delete_delivery(auth_client):
    """Test: Async deleting a delivery record returns 200; repeat delete returns 404."""
    create_res = auth_client.post(
        '/delivery-records-page',
        json={'customer': 'Test Delivery Delete', 'delivery_date': '2026-09-30'},
        headers={'X-Requested-With': 'XMLHttpRequest', 'Accept': 'application/json'}
    )
    assert create_res.status_code == 201
    del_id = create_res.get_json()['data']['id']

    # Delete
    del_res = auth_client.post(
        f'/delivery-records-page/delete/{del_id}',
        headers={'X-Requested-With': 'XMLHttpRequest', 'Accept': 'application/json'}
    )
    assert del_res.status_code == 200

    # Repeat delete -> 404
    repeat_res = auth_client.post(
        f'/delivery-records-page/delete/{del_id}',
        headers={'X-Requested-With': 'XMLHttpRequest', 'Accept': 'application/json'}
    )
    assert repeat_res.status_code == 404


def test_async_delete_pickup(auth_client):
    """Test: Async deleting a pickup schedule returns 200; repeat delete returns 404."""
    create_res = auth_client.post(
        '/pickup-schedules-page',
        json={'customer': 'Test Pickup Delete', 'pickup_date': '2026-09-30'},
        headers={'X-Requested-With': 'XMLHttpRequest', 'Accept': 'application/json'}
    )
    assert create_res.status_code == 201
    pck_id = create_res.get_json()['data']['id']

    # Delete
    del_res = auth_client.post(
        f'/pickup-schedules-page/delete/{pck_id}',
        headers={'X-Requested-With': 'XMLHttpRequest', 'Accept': 'application/json'}
    )
    assert del_res.status_code == 200

    # Repeat delete -> 404
    repeat_res = auth_client.post(
        f'/pickup-schedules-page/delete/{pck_id}',
        headers={'X-Requested-With': 'XMLHttpRequest', 'Accept': 'application/json'}
    )
    assert repeat_res.status_code == 404


def test_async_delete_customer(auth_client):
    """Test: Async deleting a customer returns 200; repeat delete returns 404."""
    create_res = auth_client.post(
        '/customers-page',
        json={'name': 'Delete Me Customer', 'contact_number': '0999-000-1111'},
        headers={'X-Requested-With': 'XMLHttpRequest', 'Accept': 'application/json'}
    )
    assert create_res.status_code == 201
    cust_id = create_res.get_json()['data']['id']

    # Delete
    del_res = auth_client.post(
        f'/customers-page/delete/{cust_id}',
        headers={'X-Requested-With': 'XMLHttpRequest', 'Accept': 'application/json'}
    )
    assert del_res.status_code == 200

    # Repeat delete -> 404
    repeat_res = auth_client.post(
        f'/customers-page/delete/{cust_id}',
        headers={'X-Requested-With': 'XMLHttpRequest', 'Accept': 'application/json'}
    )
    assert repeat_res.status_code == 404


def test_async_delete_payment(auth_client):
    """Test: Async deleting a payment transaction returns 200; repeat delete returns 404."""
    create_res = auth_client.post(
        '/payments-page',
        json={'customer': 'Delete Me Payment', 'payment_amount': 350.0, 'payment_method': 'Cash'},
        headers={'X-Requested-With': 'XMLHttpRequest', 'Accept': 'application/json'}
    )
    assert create_res.status_code == 201
    pay_id = create_res.get_json()['data']['id']

    # Delete
    del_res = auth_client.post(
        f'/payments-page/delete/{pay_id}',
        headers={'X-Requested-With': 'XMLHttpRequest', 'Accept': 'application/json'}
    )
    assert del_res.status_code == 200

    # Repeat delete -> 404
    repeat_res = auth_client.post(
        f'/payments-page/delete/{pay_id}',
        headers={'X-Requested-With': 'XMLHttpRequest', 'Accept': 'application/json'}
    )
    assert repeat_res.status_code == 404


# ============================================================================
# 4. 500 SERVER ERROR & SAFETY TESTS
# ============================================================================

def test_500_error_page_rendering(auth_client):
    """Test: Triggering a 500 error handler renders custom 500 page without stack traces."""
    from app import handle_500_error
    with app.test_request_context('/trigger-500'):
        response, status = handle_500_error(Exception("Simulated Failure"))
        assert status == 500
        # Verify no traceback in output
        assert 'Traceback (most recent call last)' not in response
        assert '500' in response or 'Internal Server Error' in response


def test_500_error_async_json(auth_client):
    """Test: Triggering a 500 error handler with async headers returns JSON 500."""
    from app import handle_500_error
    with app.test_request_context(
        '/trigger-500',
        headers={'X-Requested-With': 'XMLHttpRequest', 'Accept': 'application/json'}
    ):
        response, status = handle_500_error(Exception("Simulated Failure"))
        assert status == 500
        data = response.get_json()
        assert data['status'] == 500
        assert 'error' in data
