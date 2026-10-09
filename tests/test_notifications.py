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
            sess['role'] = 'admin'
            sess['full_name'] = 'John Michael Bretaña'
        yield client


@pytest.fixture
def rider_client():
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    init_database()
    with app.test_client() as client:
        with client.session_transaction() as sess:
            sess['user_id'] = 5
            sess['username'] = 'ephraim'
            sess['role'] = 'rider'
            sess['full_name'] = 'Mark Ephraim Nicor'
        yield client


def test_notifications_unauthorized(client=None):
    with app.test_client() as c:
        res = c.get('/api/notifications')
        assert res.status_code == 401


def test_delivery_completion_triggers_notification(rider_client, auth_client):
    # Create test delivery
    conn = sqlite3.connect('laundry.db')
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO delivery_records (customer, delivery_date, delivery_address, status, assigned_rider)
        VALUES ('Test Customer Notif', '2026-10-10', 'Purok 1, Panadtalan', 'Out for Delivery', 'Mark Ephraim Nicor')
    """)
    del_id = cursor.lastrowid
    conn.commit()
    conn.close()

    # Rider marks delivery completed
    res = rider_client.post(f'/rider-app/status/{del_id}', json={'status': 'Delivered'})
    assert res.status_code == 200

    # Staff checks notifications
    notif_res = auth_client.get('/api/notifications')
    assert notif_res.status_code == 200
    data = notif_res.get_json()
    assert data['unread_count'] >= 1
    messages = [n['message'] for n in data['notifications']]
    assert any('Test Customer Notif' in m for m in messages)


def test_pickup_completion_triggers_notification(rider_client, auth_client):
    # Create test pickup
    conn = sqlite3.connect('laundry.db')
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO pickup_schedules (customer, pickup_date, pickup_time, pickup_address, status, assigned_driver)
        VALUES ('Pickup Notif Client', '2026-10-10', 'Morning', 'Purok 2, Panadtalan', 'Scheduled', 'Mark Ephraim Nicor')
    """)
    pck_id = cursor.lastrowid
    conn.commit()
    conn.close()

    # Rider marks pickup completed
    res = rider_client.post(f'/rider-app/pickup-status/{pck_id}', json={'status': 'Picked Up'})
    assert res.status_code == 200

    # Staff checks poll endpoint
    poll_res = auth_client.get('/api/notifications/poll?last_id=0')
    assert poll_res.status_code == 200
    pdata = poll_res.get_json()
    assert pdata['unread_count'] >= 1

    # Mark as read
    mark_res = auth_client.post('/api/notifications/mark-read', json={})
    assert mark_res.status_code == 200
    assert mark_res.get_json()['unread_count'] == 0


def test_notifications_page_renders_for_staff(auth_client):
    res = auth_client.get('/notifications-page')
    assert res.status_code == 200
    assert b'Shop Activity Alerts' in res.data
    assert b'Mark All as Read' in res.data


def test_notifications_page_unauthenticated_redirects():
    with app.test_client() as c:
        res = c.get('/notifications-page')
        assert res.status_code in [302, 401]

