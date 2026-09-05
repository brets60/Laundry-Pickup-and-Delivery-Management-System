import pytest
import sqlite3
# This imports your app and database function from app.py
from app import app, init_database


@pytest.fixture
def client():
    """This sets up a 'dummy' web browser for testing your app."""
    app.config['TESTING'] = True

    # Initialize database before tests
    init_database()

    with app.test_client() as client:
        yield client


def test_app_is_running(client):
    """Test 1: Checks if the main dashboard route works without crashing."""
    response = client.get('/')
    # It should return 200 (OK) or 302 (Redirect to login)
    assert response.status_code in [200, 302]


def test_database_tables_exist():
    """Test 2: Checks if all the database tables were created successfully."""
    conn = sqlite3.connect("laundry.db")
    cursor = conn.cursor()

    # Check for Customers table
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='customers'")
    assert cursor.fetchone() is not None

    # Check for Orders table
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='laundry_orders'")
    assert cursor.fetchone() is not None

    # Check for Users table
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
    assert cursor.fetchone() is not None

    conn.close()


def test_default_admin_created():
    """Test 3: Checks if the default admin account exists."""
    conn = sqlite3.connect("laundry.db")
    cursor = conn.cursor()

    cursor.execute("SELECT username FROM users WHERE username='admin'")
    admin_user = cursor.fetchone()

    assert admin_user is not None
    assert admin_user[0] == 'admin'

    conn.close()