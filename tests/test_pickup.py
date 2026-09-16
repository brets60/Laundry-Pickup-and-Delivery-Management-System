import pytest
import sqlite3
from app import app, init_database


@pytest.fixture
def auth_client():
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    init_database()

    with app.test_client() as client:
        with client.session_transaction() as sess:
            sess['user_id'] = 1
            sess['username'] = 'admin'
        yield client


def test_pickup_page_renders(auth_client):
    response = auth_client.get('/pickup-schedules-page')
    assert response.status_code == 200
    assert b"Pickup Schedules" in response.data


def test_create_pickup_schedule(auth_client):
    response = auth_client.post('/pickup-schedules-page', data={
        'customer': 'Juan Dela Cruz',
        'pickup_date': '2026-09-25',
        'pickup_time': '09:00 AM - 11:00 AM',
        'pickup_address': 'Unit 802, Highrise Tower, Makati',
        'status': 'Pending',
        'assigned_driver': 'Driver Alex',
        'notes': 'Call 15 mins before arrival'
    }, follow_redirects=True)
    assert response.status_code == 200

    conn = sqlite3.connect('laundry.db')
    conn.row_factory = sqlite3.Row
    record = conn.execute(
        "SELECT * FROM pickup_schedules WHERE customer = ? ORDER BY id DESC LIMIT 1",
        ('Juan Dela Cruz',)
    ).fetchone()
    conn.close()

    assert record is not None
    assert record['customer'] == 'Juan Dela Cruz'
    assert record['pickup_date'] == '2026-09-25'
    assert record['pickup_time'] == '09:00 AM - 11:00 AM'
    assert record['pickup_address'] == 'Unit 802, Highrise Tower, Makati'
    assert record['status'] == 'Pending'


def test_create_pickup_validation_empty_customer(auth_client):
    response = auth_client.post('/pickup-schedules-page', data={
        'customer': '',
        'pickup_date': '2026-09-25'
    })
    assert response.status_code == 422
