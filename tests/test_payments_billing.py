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


def test_payments_page_loads_with_breakdown(auth_admin):
    """Verify payments page renders revenue breakdown by channel."""
    res = auth_admin.get('/payments-page')
    assert res.status_code == 200
    assert b"Financial Reports &amp; Payments" in res.data or b"Financial Reports & Payments" in res.data
    assert b"Revenue Settlement Breakdown" in res.data
    assert b"Cash on Delivery" in res.data
    assert b"GCash / Maya QR" in res.data
    assert b"Bank Transfer" in res.data


def test_export_payments_csv_authenticated(auth_admin):
    """Verify CSV payments ledger export returns valid CSV format."""
    res = auth_admin.get('/payments-page/export')
    assert res.status_code == 200
    assert "text/csv" in res.content_type
    assert b"Reference No,Customer Name,Contact Number,Amount (PHP)" in res.data
    assert "attachment;filename=laundrycare_payments_ledger.csv" in res.headers.get('Content-Disposition', '')


def test_export_payments_unauthenticated(client):
    """Verify unauthenticated user cannot export payment CSV."""
    res = client.get('/payments-page/export')
    assert res.status_code == 302
    assert '/login' in res.location


def test_create_and_read_payment(auth_admin):
    """Test recording a new payment transaction and verifying in DB."""
    form_data = {
        'customer': 'Juan Dela Cruz',
        'payment_amount': '350.00',
        'payment_method': 'Cash',
        'status': 'Paid',
        'notes': 'Settled at front desk - test run'
    }
    res = auth_admin.post('/payments-page', data=form_data, follow_redirects=True)
    assert res.status_code == 200

    conn = get_db_connection()
    pmt = conn.execute("SELECT * FROM payments WHERE customer = 'Juan Dela Cruz' ORDER BY id DESC LIMIT 1").fetchone()
    assert pmt is not None
    assert float(pmt['payment_amount']) == 350.00
    assert pmt['payment_method'] == 'Cash'
    assert pmt['status'] == 'Paid'

    # Test payment details route
    details_res = auth_admin.get(f"/payments-page/details/{pmt['id']}")
    assert details_res.status_code == 200
    assert b"350.00" in details_res.data
    conn.close()


def test_staff_can_record_payment(client):
    """Test staff role (Cashier Hazil Enoc) can record customer payment."""
    with client.session_transaction() as sess:
        sess['user_id'] = 2
        sess['username'] = 'staff'
        sess['role'] = 'staff'

    form_data = {
        'customer': 'Hazil Walk-in Customer',
        'payment_amount': '180.00',
        'payment_method': 'GCash',
        'status': 'Paid',
        'notes': 'Recorded by staff cashier at front desk'
    }
    res = client.post('/payments-page', data=form_data, follow_redirects=True)
    assert res.status_code == 200

    conn = get_db_connection()
    pmt = conn.execute("SELECT * FROM payments WHERE customer = 'Hazil Walk-in Customer'").fetchone()
    assert pmt is not None
    assert float(pmt['payment_amount']) == 180.00
    assert pmt['payment_method'] == 'GCash'
    conn.close()

