import pytest
from app import app, get_db_connection


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


@pytest.fixture
def auth_driver(client):
    with client.session_transaction() as sess:
        sess['user_id'] = 4
        sess['username'] = 'ephraim'
        sess['role'] = 'rider'
    return client


def test_delivery_page_renders_fleet_logistics(auth_driver):
    """Verify delivery dashboard loads fleet telemetry and active stops."""
    res = auth_driver.get('/delivery-records-page')
    assert res.status_code == 200
    assert b"Active Fleet Logistics" in res.data or b"Driver Stop Timeline" in res.data
    assert b"Mark Ephraim Nicor" in res.data


def test_create_and_assign_delivery_to_rider(auth_driver):
    """Verify dispatching a delivery to a specific courier unit."""
    form_data = {
        'customer': 'Elena Gomez',
        'delivery_date': '2026-10-02',
        'delivery_address': 'Dorm 2, CMU Musuan, Maramag',
        'assigned_rider': 'Mark Ephraim Nicor (Motorcycle Courier)',
        'status': 'Scheduled',
        'delivery_notes': 'Call upon arriving at the guardhouse'
    }
    res = auth_driver.post('/delivery-records-page', data=form_data, follow_redirects=True)
    assert res.status_code == 200

    conn = get_db_connection()
    deliv = conn.execute("SELECT * FROM delivery_records WHERE customer = 'Elena Gomez' ORDER BY id DESC LIMIT 1").fetchone()
    assert deliv is not None
    assert 'Mark Ephraim Nicor' in deliv['assigned_rider']
    assert 'CMU Musuan' in deliv['delivery_address']
    assert deliv['status'] == 'Scheduled'
    conn.close()


def test_delivery_status_transition_to_delivered(auth_driver):
    """Verify updating delivery status to Delivered after customer sign-off."""
    conn = get_db_connection()
    deliv = conn.execute("SELECT id FROM delivery_records ORDER BY id DESC LIMIT 1").fetchone()
    conn.close()
    assert deliv is not None

    update_data = {
        'customer': 'Elena Gomez',
        'delivery_date': '2026-10-02',
        'delivery_address': 'Dorm 2, CMU Musuan, Maramag',
        'assigned_rider': 'Mark Ephraim Nicor (Motorcycle Courier)',
        'status': 'Delivered',
        'delivery_notes': 'Handed over and customer signature verified'
    }
    res = auth_driver.post(f"/delivery-records-page/edit/{deliv['id']}", data=update_data, follow_redirects=True)
    assert res.status_code == 200

    conn = get_db_connection()
    updated = conn.execute("SELECT * FROM delivery_records WHERE id = ?", (deliv['id'],)).fetchone()
    assert updated['status'] == 'Delivered'
    conn.close()


def test_delivery_details_api(auth_driver):
    """Verify delivery details route returns 200 with record data."""
    conn = get_db_connection()
    deliv = conn.execute("SELECT id FROM delivery_records LIMIT 1").fetchone()
    conn.close()
    assert deliv is not None

    res = auth_driver.get(f"/delivery-records-page/details/{deliv['id']}")
    assert res.status_code == 200
    assert b"Delivery Information" in res.data or b"Delivery" in res.data
