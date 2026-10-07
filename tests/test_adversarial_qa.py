from datetime import date
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
        sess['username'] = 'ephraim'
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


# ============================================================
# 4. WEEK 11 REGRESSION SUITE (P0/P1 BUG SQUASH VERIFICATION)
# ============================================================

def test_order_weight_exceeding_ceiling_rejected(auth_admin):
    """
    BUG-002 Regression Test:
    Orders exceeding 150 kg must be rejected with HTTP 422 and commercial contract notice.
    """
    payload = {
        'customer': 'Juan Dela Cruz',
        'laundry_weight': '999999',
        'service_type': 'Wash & Fold'
    }
    res = auth_admin.post('/laundry-orders-page', data=payload, headers={'X-Requested-With': 'XMLHttpRequest'})
    assert res.status_code == 422
    data = res.get_json()
    err_msg = str(data)
    assert '150 kg' in err_msg or 'commercial contract' in err_msg.lower()


def test_booking_notes_xss_tags_stripped(client):
    """
    BUG-001 Regression Test:
    HTML / Script injection in customer booking notes must be cleanly stripped before DB persistence.
    """
    xss_payload = "<script>alert('pwned')</script>Please handle with care <img src=x onerror=alert(1)>"
    form_data = {
        'name': 'Malicious Customer',
        'contact_number': '09171234567',
        'barangay': 'Poblacion',
        'address_details': 'Purok 2',
        'service_type': 'Wash & Fold',
        'estimated_load': 'Medium Bag (~6-8 kg)',
        'pickup_date': date.today().strftime('%Y-%m-%d'),
        'pickup_time': '09:00 AM - 12:00 PM',
        'payment_method': 'Cash on Delivery (COD)',
        'notes': xss_payload
    }
    res = client.post('/book-pickup', data=form_data, follow_redirects=True)
    assert res.status_code == 200

    conn = get_db_connection()
    record = conn.execute("SELECT * FROM pickup_schedules WHERE customer = 'Malicious Customer' ORDER BY id DESC LIMIT 1").fetchone()
    conn.close()

    assert record is not None
    # Verify no raw <script> or <img tags exist in stored notes
    assert '<script>' not in record['notes']
    assert '<img' not in record['notes']
    assert 'alert(' not in record['notes']
    assert 'Please handle with care' in record['notes']


def test_booking_historical_pickup_date_rejected(client):
    """
    BUG-003 Regression Test:
    Selecting historical pickup dates in the booking portal must return an error.
    """
    form_data = {
        'name': 'Backdate Tester',
        'contact_number': '09179876543',
        'barangay': 'Poblacion',
        'address_details': 'Purok 1',
        'pickup_date': '2020-01-01',  # Historical date in the past
        'pickup_time': '09:00 AM - 12:00 PM',
        'notes': 'Test backdated booking'
    }
    res = client.post('/book-pickup', data=form_data)
    assert res.status_code == 200
    assert b"cannot be in the past" in res.data

