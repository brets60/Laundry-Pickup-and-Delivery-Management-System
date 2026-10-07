from datetime import date
import pytest
from app import app, get_db_connection


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_book_pickup_get(client):
    """Test that the customer booking form loads properly with TCCI and Panadtalan options."""
    res = client.get('/book-pickup')
    assert res.status_code == 200
    assert b"Request Doorstep Laundry Pickup" in res.data
    assert b"Torres Capitol College Inc." in res.data
    assert b"P2B Sayre Highway" in res.data


def test_book_pickup_post_success(client):
    """Test submitting a customer pickup booking."""
    form_data = {
        'name': 'Juan de la Cruz',
        'contact_number': '0918-987-6543',
        'email': 'juan@example.com',
        'barangay': 'Base Camp Proper & Junction',
        'address_details': 'Near Central Crossing, Store #4',
        'service_type': 'Wash & Fold',
        'estimated_load': 'Medium Bag (~6-8 kg)',
        'pickup_date': date.today().strftime('%Y-%m-%d'),
        'pickup_time': '09:00 AM - 12:00 PM',
        'payment_method': 'Cash on Delivery (COD)',
        'notes': 'Please ring the doorbell upon arrival.'
    }

    res = client.post('/book-pickup', data=form_data, follow_redirects=True)
    assert res.status_code == 200
    assert b"Pickup Request Booked!" in res.data
    assert b"Juan de la Cruz" in res.data
    assert b"PCK-" in res.data

    # Verify in DB
    conn = get_db_connection()
    cust = conn.execute("SELECT * FROM customers WHERE contact_number = '0918-987-6543'").fetchone()
    assert cust is not None
    assert cust['name'] == 'Juan de la Cruz'

    pickup = conn.execute("SELECT * FROM pickup_schedules WHERE customer = 'Juan de la Cruz' ORDER BY id DESC LIMIT 1").fetchone()
    assert pickup is not None
    assert 'Near Central Crossing' in pickup['pickup_address']
    conn.close()


def test_track_page_get(client):
    """Test that the live tracker landing page loads."""
    res = client.get('/track')
    assert res.status_code == 200
    assert b"Track Your Laundry in Real Time" in res.data


def test_track_existing_order_or_pickup(client):
    """Test tracking with an existing ID or query."""
    conn = get_db_connection()
    first_order = conn.execute("SELECT id, customer FROM laundry_orders LIMIT 1").fetchone()
    conn.close()

    if first_order:
        res = client.get(f'/track?ref={first_order["id"]}')
        assert res.status_code == 200
        assert b"Current Status" in res.data
        assert first_order['customer'].encode('utf-8') in res.data


def test_api_track_lookup(client):
    """Test the fast JSON lookup endpoint."""
    res = client.get('/api/track-lookup?q=1')
    assert res.status_code == 200
    data = res.get_json()
    assert 'status' in data
    assert data['status'] == 'ok'


def test_barangay_zone_auto_assignment(client):
    """Test that booking in different Panadtalan sectors routes to dedicated Bajaj motorcycle couriers."""
    from controllers.customer_portal_routes import resolve_maramag_zone_and_rider

    # Zone 1: Torres Capitol College Inc. & Dorms -> Mark Ephraim Nicor
    z1, r1 = resolve_maramag_zone_and_rider("Torres Capitol College Inc. (TCCI Campus)")
    assert "Zone 1" in z1
    assert "Nicor" in r1 or "Ephraim" in r1

    # Zone 2: Sayre Highway & Commercial -> Mark Ephraim Nicor
    z2, r2 = resolve_maramag_zone_and_rider("Sayre Highway, Panadtalan, Maramag")
    assert "Zone 2" in z2
    assert "Nicor" in r2 or "Ephraim" in r2

    # Zone 3: Puroks 1-5 Residential -> Mark Ephraim Nicor
    z3, r3 = resolve_maramag_zone_and_rider("Purok 3 (Riverside), Panadtalan")
    assert "Zone 3" in z3
    assert "Nicor" in r3 or "Ephraim" in r3

    z3_b, r3_b = resolve_maramag_zone_and_rider("Purok 1 Central, Panadtalan, Maramag")
    assert "Zone 3" in z3_b
    assert "Nicor" in r3_b or "Ephraim" in r3_b


def test_welcome_home_routes_and_navigation(client):
    """Test that customer welcome page is accessible via / and /welcome with return links."""
    res_root = client.get('/')
    assert res_root.status_code == 200
    assert b"LaundryCare" in res_root.data
    assert b"Panadtalan" in res_root.data
    assert b"Torres Capitol College Inc." in res_root.data

    res_welcome = client.get('/welcome')
    assert res_welcome.status_code == 200
    assert b"LaundryCare" in res_welcome.data

    # Verify return links from book-pickup, track, and login
    res_booking = client.get('/book-pickup')
    assert b'href="/"' in res_booking.data
    assert b"Back to Customer Welcome Page" in res_booking.data

    res_track = client.get('/track')
    assert b'href="/"' in res_track.data
    assert b"Back to Customer Welcome Page" in res_track.data

    res_login = client.get('/login')
    assert b'href="/"' in res_login.data
    assert b"Back to Customer Welcome Page" in res_login.data

