import pytest
import sqlite3
from app import app, init_database


@pytest.fixture
def client():
    app.config['TESTING'] = True
    init_database()
    with app.test_client() as client:
        yield client


def test_three_users_exist():
    """Verify admin, staff, and rider exist in database with correct roles."""
    conn = sqlite3.connect("laundry.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    users = cursor.execute("SELECT username, role, full_name FROM users").fetchall()
    conn.close()

    user_dict = {u["username"]: dict(u) for u in users}

    assert "admin" in user_dict
    assert user_dict["admin"]["role"] == "admin"

    assert "staff" in user_dict
    assert user_dict["staff"]["role"] == "staff"

    assert "rider" in user_dict
    assert user_dict["rider"]["role"] == "rider"


def test_admin_login_and_full_access(client):
    """Admin logs in and can access all sections including staff, reports, settings."""
    res = client.post("/login", data={"username": "admin", "password": "admin123"}, follow_redirects=True)
    assert res.status_code == 200

    with client.session_transaction() as sess:
        assert sess["role"] == "admin"
        assert sess["username"] == "admin"

    # Admin can access staff, payments/reports, and settings
    assert client.get("/staff-page").status_code == 200
    assert client.get("/payments-page").status_code == 200
    assert client.get("/settings-page").status_code == 200


def test_staff_login_and_restricted_access(client):
    """Staff logs in, can access operational modules, but blocked from admin-only sections."""
    res = client.post("/login", data={"username": "staff", "password": "staff123"}, follow_redirects=True)
    assert res.status_code == 200

    with client.session_transaction() as sess:
        assert sess["role"] == "staff"

    # Operational modules allowed
    assert client.get("/dashboard-page").status_code == 200
    assert client.get("/laundry-orders-page").status_code == 200
    assert client.get("/customers-page").status_code == 200

    # Admin-only modules redirect
    staff_res = client.get("/staff-page")
    assert staff_res.status_code == 302
    assert "/dashboard-page" in staff_res.location

    pay_res = client.get("/payments-page")
    assert pay_res.status_code == 302
    assert "/dashboard-page" in pay_res.location

    sett_res = client.get("/settings-page")
    assert sett_res.status_code == 302
    assert "/dashboard-page" in sett_res.location


def test_rider_login_and_redirection(client):
    """Rider logs in and redirects to rider mobile app, and is restricted from admin pages."""
    res = client.post("/login", data={"username": "rider", "password": "rider123"})
    assert res.status_code == 302
    assert ("/rider-app" in res.location) or ("/delivery-records-page" in res.location)

    with client.session_transaction() as sess:
        assert sess["role"] == "rider"

    # Rider App, Deliveries, and Pickups accessible
    assert client.get("/rider-app").status_code == 200
    assert client.get("/delivery-records-page").status_code == 200
    assert client.get("/pickup-schedules-page").status_code == 200

    # Blocked from staff-page -> redirects
    blocked_res = client.get("/staff-page")
    assert blocked_res.status_code == 302


def test_rider_app_gps_and_status(client):
    """Test Rider mobile app view with GPS navigation links and status transitions."""
    client.post("/login", data={"username": "rider", "password": "rider123"})
    res = client.get("/rider-app")
    assert res.status_code == 200
    assert b"Google Maps" in res.data
    assert b"Waze" in res.data
    assert b"LaundryCare Rider" in res.data

    # Test PWA manifest
    manifest_res = client.get("/manifest.json")
    assert manifest_res.status_code == 200
    assert manifest_res.is_json

