import pytest
from app import app, init_database


@pytest.fixture
def client():
    app.config['TESTING'] = True
    init_database()
    with app.test_client() as client:
        yield client


def test_switch_account_requires_auth(client):
    """Anonymous user attempting to switch account gets redirected to login."""
    res = client.get("/switch-account/admin", follow_redirects=False)
    assert res.status_code == 302
    assert "/login" in res.location

    api_res = client.post("/api/switch-account", json={"username": "admin"})
    assert api_res.status_code == 401

    notif_res = client.get("/api/system-accounts")
    assert notif_res.status_code == 401


def test_system_accounts_api(client):
    """Logged in user can fetch active system accounts list."""
    client.post("/login", data={"username": "admin", "password": "admin123"}, follow_redirects=True)
    res = client.get("/api/system-accounts")
    assert res.status_code == 200
    data = res.get_json()
    assert data["status"] == 200
    assert data["current_user"] == "admin"
    usernames = [a["username"] for a in data["accounts"]]
    assert "admin" in usernames
    assert "hazil" in usernames
    assert "ephraim" in usernames


def test_quick_switch_admin_to_staff(client):
    """Switching from Admin to Staff updates session and allows staff access."""
    client.post("/login", data={"username": "admin", "password": "admin123"}, follow_redirects=True)

    res = client.get("/switch-account/hazil", follow_redirects=True)
    assert res.status_code == 200

    with client.session_transaction() as sess:
        assert sess["username"] == "hazil"
        assert sess["role"] == "staff"

    # Staff access checks
    assert client.get("/laundry-orders-page").status_code == 200
    # Blocked from admin settings
    assert client.get("/settings-page").status_code == 302


def test_quick_switch_to_rider_redirects_to_rider_app(client):
    """Switching to a Rider role redirects directly to /rider-app."""
    client.post("/login", data={"username": "admin", "password": "admin123"}, follow_redirects=True)

    res = client.get("/switch-account/ephraim", follow_redirects=False)
    assert res.status_code == 302
    assert "/rider-app" in res.location

    with client.session_transaction() as sess:
        assert sess["username"] == "ephraim"
        assert sess["role"] == "rider"


def test_quick_switch_from_rider_to_admin(client):
    """Switching back from Rider to Admin leaves /rider-app and redirects to dashboard."""
    client.post("/login", data={"username": "ephraim", "password": "driver123"}, follow_redirects=True)

    res = client.get("/switch-account/admin", headers={"Referer": "http://localhost/rider-app"}, follow_redirects=False)
    assert res.status_code == 302
    assert "/dashboard-page" in res.location

    with client.session_transaction() as sess:
        assert sess["username"] == "admin"
        assert sess["role"] == "admin"


def test_api_switch_account_json(client):
    """AJAX POST to /api/switch-account updates session and returns JSON with redirect URL."""
    client.post("/login", data={"username": "admin", "password": "admin123"}, follow_redirects=True)

    res = client.post("/api/switch-account", json={"username": "ephraim"})
    assert res.status_code == 200
    data = res.get_json()
    assert data["status"] == 200
    assert data["redirect"] == "/rider-app"
    assert data["user"]["role"] == "rider"
