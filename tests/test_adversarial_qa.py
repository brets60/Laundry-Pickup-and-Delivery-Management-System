import pytest
from app import app, get_db_connection


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


@pytest.fixture
def auth_admin(client):
    with client.session_transaction() as sess:
        sess['user_id'] = 1
        sess['username'] = 'admin'
        sess['role'] = 'admin'
    return client


@pytest.fixture
def auth_rider(client):
    with client.session_transaction() as sess:
        sess['user_id'] = 4
        sess['username'] = 'tristan'
        sess['role'] = 'rider'
    return client


# ============================================================
# 1. ADVERSARIAL INPUT & MALFORMED REQUEST TESTS
# ============================================================

def test_negative_weight_rejected(auth_admin):
    """Adversarial Test: Submitting negative laundry weight must return 422."""
    payload = {
        'customer': 'Juan Dela Cruz',
        'laundry_weight': '-12.5',
        'service_type': 'Wash & Fold'
    }
    res = auth_admin.post('/laundry-orders-page', data=payload, headers={'X-Requested-With': 'XMLHttpRequest'})
    assert res.status_code == 422
    data = res.get_json()
    assert 'weight' in str(data).lower() or 'error' in data


def test_negative_payment_amount_rejected(auth_admin):
    """Adversarial Test: Submitting negative payment amount must return 422."""
    payload = {
        'customer': 'Juan Dela Cruz',
        'payment_amount': '-450.00',
        'payment_method': 'Cash'
    }
    res = auth_admin.post('/payments-page', data=payload, headers={'X-Requested-With': 'XMLHttpRequest'})
    assert res.status_code == 422
    data = res.get_json()
    assert 'payment_amount' in str(data).lower() or 'error' in data


def test_non_existent_customer_details_returns_404(auth_admin):
    """Adversarial Test: Accessing a non-existent customer ID returns 404 HTML."""
    res = auth_admin.get('/customers-page/details/999999')
    assert res.status_code == 404
    assert b"not found" in res.data.lower() or b"404" in res.data


def test_stale_delete_action_returns_404(auth_admin):
    """Adversarial Test: Deleting an already deleted record returns 404 JSON."""
    res = auth_admin.post('/customers-page/delete/999999', headers={'X-Requested-With': 'XMLHttpRequest'})
    assert res.status_code == 404
    data = res.get_json()
    assert 'not found' in data.get('error', '').lower()


# ============================================================
# 2. MALFORMED TRACKING CODE TESTS
# ============================================================

def test_track_invalid_code_format(client):
    """Adversarial Test: Tracking with random unformatted string gracefully renders Not Found state."""
    res = client.get('/track/MALFORMED_TRACK_CODE_XYZ')
    assert res.status_code == 200
    assert b"No Record Found" in res.data or b"not found" in res.data.lower()


def test_track_non_existent_order_code(client):
    """Adversarial Test: Valid prefix with non-existent ID gracefully renders Not Found state."""
    res = client.get('/track/ORD-999999')
    assert res.status_code == 200
    assert b"No Record Found" in res.data or b"not found" in res.data.lower()


# ============================================================
# 3. RBAC SECURITY BOUNDARY TESTS
# ============================================================

def test_rider_blocked_from_payments_export(auth_rider):
    """RBAC Test: Rider role is blocked from exporting financial CSV."""
    res = auth_rider.get('/payments-page/export')
    assert res.status_code in [302, 403]
    if res.status_code == 302:
        assert '/dashboard' in res.location or '/login' in res.location or '/delivery' in res.location


def test_unauthenticated_blocked_from_staff_page(client):
    """RBAC Test: Unauthenticated user is redirected to login from staff management."""
    res = client.get('/staff-page')
    assert res.status_code == 302
    assert '/login' in res.location
