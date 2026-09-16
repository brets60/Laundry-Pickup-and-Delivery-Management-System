import pytest
from app import app, get_db_connection


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_book_pickup_get(client):
    """Test that the customer booking form loads properly with Maramag options."""
    res = client.get('/book-pickup')
    assert res.status_code == 200
    assert b"Request Doorstep Laundry Pickup" in res.data
    assert b"CMU Campus / Musuan" in res.data
    assert b"Poblacion" in res.data


def test_book_pickup_post_success(client):
    """Test submitting a customer pickup booking."""
    form_data = {
        'name': 'Juan de la Cruz',
        'contact_number': '0918-987-6543',
        'email': 'juan@example.com',
        'barangay': 'CMU Campus / Musuan (Dormitory/Apartment)',
        'address_details': 'Dorm 3, Room 101',
        'service_type': 'Wash & Fold',
        'estimated_load': 'Medium Bag (~6-8 kg)',
        'pickup_date': '2026-09-16',
        'pickup_time': '09:00 AM - 12:00 PM',
        'payment_method': 'Cash on Delivery (COD)',
        'notes': 'Please ring the dorm bell upon arrival.'
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
    assert 'Dorm 3, Room 101' in pickup['pickup_address']
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
    """Test that booking in different Maramag barangays routes to dedicated zone couriers."""
    from controllers.customer_portal_routes import resolve_maramag_zone_and_rider

    # Zone 1: CMU & Musuan
    z1, r1 = resolve_maramag_zone_and_rider("Sampaguita Dorm, CMU Campus / Musuan, Maramag")
    assert "Zone 1" in z1
    assert "Mike" in r1

    # Zone 2: Poblacion
    z2, r2 = resolve_maramag_zone_and_rider("Sayre Highway, Poblacion, Maramag")
    assert "Zone 2" in z2
    assert "Alex" in r2

    # Zone 3: Dologon & Base Camp
    z3, r3 = resolve_maramag_zone_and_rider("Purok 3, Dologon, Maramag")
    assert "Zone 3" in z3
    assert "Dave" in r3

