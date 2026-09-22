import pytest
from app import app, get_db_connection
from controllers.customer_routes import clean_phone_number, format_customer_name


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


@pytest.fixture
def auth_client(client):
    with client.session_transaction() as sess:
        sess['user_id'] = 1
        sess['username'] = 'admin'
        sess['role'] = 'admin'
    return client


def test_clean_phone_number():
    """Verify phone normalization removes punctuation and extra spacing."""
    assert clean_phone_number("  0917-123-4567  ") == "09171234567"
    assert clean_phone_number("+63 (917) 555-1234") == "+639175551234"
    assert clean_phone_number("") == ""
    assert clean_phone_number(None) == ""


def test_format_customer_name():
    """Verify customer name capitalization and trim."""
    assert format_customer_name("  maria   santos  ") == "Maria Santos"
    assert format_customer_name("JOHN DOE") == "John Doe"
    assert format_customer_name("") == ""
    assert format_customer_name(None) == ""


def test_customer_details_crm_stats(auth_client):
    """Verify customer details route calculates CRM loyalty stats."""
    conn = get_db_connection()
    cust = conn.execute("SELECT id FROM customers LIMIT 1").fetchone()
    conn.close()
    assert cust is not None, "At least one customer must exist in test database"

    res = auth_client.get(f"/customers-page/details/{cust['id']}")
    assert res.status_code == 200
    assert b"Cashier Loyalty Hub" in res.data
    assert b"Reward Points Balance" in res.data
    assert b"Total Revenue" in res.data


def test_export_customers_csv(auth_client):
    """Verify CSV export endpoint returns formatted customer directory."""
    res = auth_client.get('/customers-page/export')
    assert res.status_code == 200
    assert "text/csv" in res.content_type
    assert b"Customer ID,Full Name,Contact Number,Email,Address" in res.data
    assert b"CUST-" in res.data


def test_export_customers_unauthenticated(client):
    """Verify unauthenticated user cannot export customer CSV."""
    res = client.get('/customers-page/export')
    assert res.status_code == 302
    assert '/login' in res.location
