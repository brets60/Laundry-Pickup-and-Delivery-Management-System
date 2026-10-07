import pytest
from app import app, get_db_connection
from controllers.pickup_routes import check_pickup_slot_conflict


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


@pytest.fixture
def auth_operator(client):
    with client.session_transaction() as sess:
        sess['user_id'] = 5
        sess['username'] = 'mark'
        sess['role'] = 'staff'
    return client


def test_check_pickup_slot_conflict_helper():
    """Verify pickup slot capacity and conflict detection helper."""
    conn = get_db_connection()
    result = check_pickup_slot_conflict(conn, '2026-10-15', '09:00 AM - 12:00 PM')
    assert isinstance(result, dict)
    assert 'count' in result
    assert 'is_high_volume' in result
    assert isinstance(result['is_high_volume'], bool)
    conn.close()


def test_pickup_page_renders_clean_courier_deck(auth_operator):
    """Verify pickups page loads cleanly with dedicated motorcycle courier header and without machine intake banner."""
    res = auth_operator.get('/pickup-schedules-page')
    assert res.status_code == 200
    assert b"Mark Ephraim Nicor" in res.data
    assert b"Wash Hub Intake &amp; Machine Status" not in res.data
    assert b"Washers Active" not in res.data


def test_create_pickup_schedule(auth_operator):
    """Verify scheduling a pickup for courier collection."""
    form_data = {
        'customer': 'Carlos Ramos',
        'pickup_date': '2026-10-05',
        'pickup_time': '01:00 PM - 04:00 PM',
        'pickup_address': 'Poblacion, Maramag, Bukidnon',
        'assigned_driver': 'Mark Ephraim Nicor (Motorcycle Courier)',
        'status': 'Pending',
        'notes': 'Heavy curtains intake'
    }
    res = auth_operator.post('/pickup-schedules-page', data=form_data, follow_redirects=True)
    assert res.status_code == 200

    conn = get_db_connection()
    sched = conn.execute("SELECT * FROM pickup_schedules WHERE customer = 'Carlos Ramos' ORDER BY id DESC LIMIT 1").fetchone()
    assert sched is not None
    assert sched['pickup_time'] == '01:00 PM - 04:00 PM'
    assert 'Poblacion' in sched['pickup_address']
    conn.close()


def test_pickup_details_page(auth_operator):
    """Verify pickup details route returns 200 with customer info."""
    conn = get_db_connection()
    sched = conn.execute("SELECT id FROM pickup_schedules LIMIT 1").fetchone()
    conn.close()
    assert sched is not None

    res = auth_operator.get(f"/pickup-schedules-page/details/{sched['id']}")
    assert res.status_code == 200
    assert b"Pickup" in res.data
