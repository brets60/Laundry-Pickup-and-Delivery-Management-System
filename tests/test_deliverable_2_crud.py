"""
Deliverable 2 — Routing, Logic & Tests Automated Test Suite
Tests full CRUD across all 5 core modules (/customers, /laundry-orders,
/pickup-schedules, /delivery-records, /payments), covering:
  1. Happy-path full CRUD lifecycle (POST 201 -> GET list 200 -> GET id 200 -> PUT 200 -> DELETE 200)
  2. Guard-clause input validation failures returning standardized HTTP 422 envelopes
  3. Edge cases (whitespace-only strings, negative/zero/non-numeric/boolean values,
     404 Not Found on non-existent IDs or missing foreign customer, 405 Method Not Allowed,
     and malformed/empty request bodies never causing a 500).
"""

import pytest
from app import app, init_database


@pytest.fixture
def api_client():
    app.config["TESTING"] = True
    init_database()
    with app.test_client() as client:
        yield client


def _assert_422_envelope(response, expected_fields):
    """Helper to verify the standardized 422 validation error envelope."""
    assert response.status_code == 422
    body = response.get_json()
    assert body is not None
    assert body["status"] == 422
    assert body["data"] is None
    assert body["error"] is not None
    assert body["error"]["code"] == "VALIDATION_ERROR"
    assert body["error"]["message"] == "Validation failed."
    for field in expected_fields:
        assert field in body["error"]["fields"]


def _assert_404_envelope(response):
    """Helper to verify the standardized 404 Not Found error envelope."""
    assert response.status_code == 404
    body = response.get_json()
    assert body is not None
    assert body["status"] == 404
    assert body["data"] is None
    assert body["error"]["code"] == "NOT_FOUND"


# ============================================================================
# 1. CUSTOMERS MODULE — HAPPY PATH, VALIDATION (422), AND EDGE CASES
# ============================================================================

def test_customers_full_crud_happy_path(api_client):
    # CREATE (POST /customers -> 201)
    create_res = api_client.post("/customers", json={
        "name": "Deliverable Two Customer",
        "contact_number": "09171112222"
    })
    assert create_res.status_code == 201
    created = create_res.get_json()
    assert created["status"] == 201
    assert created["error"] is None
    cust_id = created["data"]["id"]
    assert created["data"]["name"] == "Deliverable Two Customer"
    assert created["data"]["contact_number"] == "09171112222"

    # READ LIST (GET /customers -> 200)
    list_res = api_client.get("/customers")
    assert list_res.status_code == 200
    listed = list_res.get_json()
    assert listed["status"] == 200
    assert any(c["id"] == cust_id for c in listed["data"])

    # READ ONE (GET /customers/:id -> 200)
    show_res = api_client.get(f"/customers/{cust_id}")
    assert show_res.status_code == 200
    shown = show_res.get_json()
    assert shown["data"]["id"] == cust_id
    assert shown["data"]["name"] == "Deliverable Two Customer"

    # UPDATE (PUT /customers/:id -> 200)
    update_res = api_client.put(f"/customers/{cust_id}", json={
        "name": "Deliverable Two Updated",
        "contact_number": "09189998888"
    })
    assert update_res.status_code == 200
    updated = update_res.get_json()
    assert updated["status"] == 200
    assert updated["data"]["name"] == "Deliverable Two Updated"
    assert updated["data"]["contact_number"] == "09189998888"

    # DELETE (DELETE /customers/:id -> 200)
    del_res = api_client.delete(f"/customers/{cust_id}")
    assert del_res.status_code == 200
    deleted = del_res.get_json()
    assert deleted["status"] == 200
    assert deleted["data"]["id"] == cust_id

    # VERIFY DELETED (GET /customers/:id -> 404)
    _assert_404_envelope(api_client.get(f"/customers/{cust_id}"))


def test_customers_validation_and_edge_cases(api_client):
    # Empty body -> 422
    _assert_422_envelope(api_client.post("/customers", json={}), ["name", "contact_number"])
    # Whitespace-only fields -> 422
    _assert_422_envelope(
        api_client.post("/customers", json={"name": "   ", "contact_number": "   "}),
        ["name", "contact_number"]
    )
    # Missing contact_number -> 422
    _assert_422_envelope(api_client.post("/customers", json={"name": "Alice"}), ["contact_number"])
    # PUT validation -> 422 before 404
    _assert_422_envelope(api_client.put("/customers/1", json={"name": ""}), ["name", "contact_number"])
    # PUT / DELETE non-existent ID -> 404
    _assert_404_envelope(api_client.put("/customers/999999", json={"name": "Valid", "contact_number": "09170000000"}))
    _assert_404_envelope(api_client.delete("/customers/999999"))
    # Wrong HTTP method on collection -> 405
    assert api_client.delete("/customers").status_code == 405


# ============================================================================
# 2. LAUNDRY ORDERS MODULE — HAPPY PATH, VALIDATION (422), AND EDGE CASES
# ============================================================================

def test_laundry_orders_full_crud_happy_path(api_client):
    # Ensure customer exists first
    api_client.post("/customers", json={"name": "Order Test Client", "contact_number": "09172223333"})

    # CREATE (POST /laundry-orders -> 201)
    create_res = api_client.post("/laundry-orders", json={
        "customer": "Order Test Client",
        "laundry_weight": 6.5
    })
    assert create_res.status_code == 201
    order_id = create_res.get_json()["data"]["id"]
    assert create_res.get_json()["data"]["laundry_weight"] == 6.5

    # READ LIST (GET /laundry-orders -> 200)
    list_res = api_client.get("/laundry-orders")
    assert list_res.status_code == 200
    assert any(o["id"] == order_id for o in list_res.get_json()["data"])

    # READ ONE (GET /laundry-orders/:id -> 200)
    show_res = api_client.get(f"/laundry-orders/{order_id}")
    assert show_res.status_code == 200
    assert show_res.get_json()["data"]["customer"] == "Order Test Client"

    # UPDATE (PUT /laundry-orders/:id -> 200)
    update_res = api_client.put(f"/laundry-orders/{order_id}", json={
        "customer": "Order Test Client",
        "laundry_weight": 8.25
    })
    assert update_res.status_code == 200
    assert update_res.get_json()["data"]["laundry_weight"] == 8.25

    # DELETE (DELETE /laundry-orders/:id -> 200)
    del_res = api_client.delete(f"/laundry-orders/{order_id}")
    assert del_res.status_code == 200
    _assert_404_envelope(api_client.get(f"/laundry-orders/{order_id}"))


def test_laundry_orders_validation_and_edge_cases(api_client):
    # Missing all fields -> 422
    _assert_422_envelope(api_client.post("/laundry-orders", json={}), ["customer", "laundry_weight"])
    # Zero and negative weight -> 422
    _assert_422_envelope(
        api_client.post("/laundry-orders", json={"customer": "Order Test Client", "laundry_weight": 0}),
        ["laundry_weight"]
    )
    _assert_422_envelope(
        api_client.post("/laundry-orders", json={"customer": "Order Test Client", "laundry_weight": -4.5}),
        ["laundry_weight"]
    )
    # Non-numeric string and boolean weight -> 422 (never 500)
    _assert_422_envelope(
        api_client.post("/laundry-orders", json={"customer": "Order Test Client", "laundry_weight": "abc"}),
        ["laundry_weight"]
    )
    _assert_422_envelope(
        api_client.post("/laundry-orders", json={"customer": "Order Test Client", "laundry_weight": True}),
        ["laundry_weight"]
    )
    # Non-existent customer on create -> 404
    _assert_404_envelope(
        api_client.post("/laundry-orders", json={"customer": "NonExistent Person 999", "laundry_weight": 3.0})
    )
    # Non-existent order ID on PUT / DELETE -> 404
    _assert_404_envelope(
        api_client.put("/laundry-orders/999999", json={"customer": "Order Test Client", "laundry_weight": 3.0})
    )
    _assert_404_envelope(api_client.delete("/laundry-orders/999999"))
    assert api_client.delete("/laundry-orders").status_code == 405


# ============================================================================
# 3. PICKUP SCHEDULES MODULE — HAPPY PATH, VALIDATION (422), AND EDGE CASES
# ============================================================================

def test_pickup_schedules_full_crud_happy_path(api_client):
    api_client.post("/customers", json={"name": "Pickup Test Client", "contact_number": "09173334444"})

    # CREATE (POST /pickup-schedules -> 201)
    create_res = api_client.post("/pickup-schedules", json={
        "customer": "Pickup Test Client",
        "pickup_date": "2026-09-15"
    })
    assert create_res.status_code == 201
    schedule_id = create_res.get_json()["data"]["id"]

    # READ LIST & SHOW (GET -> 200)
    assert api_client.get("/pickup-schedules").status_code == 200
    show_res = api_client.get(f"/pickup-schedules/{schedule_id}")
    assert show_res.status_code == 200
    assert show_res.get_json()["data"]["pickup_date"] == "2026-09-15"

    # UPDATE (PUT /pickup-schedules/:id -> 200)
    update_res = api_client.put(f"/pickup-schedules/{schedule_id}", json={
        "customer": "Pickup Test Client",
        "pickup_date": "2026-09-16"
    })
    assert update_res.status_code == 200
    assert update_res.get_json()["data"]["pickup_date"] == "2026-09-16"

    # DELETE (DELETE /pickup-schedules/:id -> 200)
    assert api_client.delete(f"/pickup-schedules/{schedule_id}").status_code == 200
    _assert_404_envelope(api_client.get(f"/pickup-schedules/{schedule_id}"))


def test_pickup_schedules_validation_and_edge_cases(api_client):
    _assert_422_envelope(api_client.post("/pickup-schedules", json={}), ["pickup_date", "customer"])
    _assert_422_envelope(
        api_client.post("/pickup-schedules", json={"pickup_date": "   ", "customer": ""}),
        ["pickup_date", "customer"]
    )
    _assert_404_envelope(
        api_client.post("/pickup-schedules", json={"customer": "Ghost Customer 999", "pickup_date": "2026-09-15"})
    )
    _assert_404_envelope(
        api_client.put("/pickup-schedules/999999", json={"customer": "Pickup Test Client", "pickup_date": "2026-09-15"})
    )
    _assert_404_envelope(api_client.delete("/pickup-schedules/999999"))
    assert api_client.delete("/pickup-schedules").status_code == 405


# ============================================================================
# 4. DELIVERY RECORDS MODULE — HAPPY PATH, VALIDATION (422), AND EDGE CASES
# ============================================================================

def test_delivery_records_full_crud_happy_path(api_client):
    api_client.post("/customers", json={"name": "Delivery Test Client", "contact_number": "09174445555"})

    # CREATE (POST /delivery-records -> 201)
    create_res = api_client.post("/delivery-records", json={
        "customer": "Delivery Test Client",
        "delivery_date": "2026-09-18"
    })
    assert create_res.status_code == 201
    delivery_id = create_res.get_json()["data"]["id"]

    # READ LIST & SHOW (GET -> 200)
    assert api_client.get("/delivery-records").status_code == 200
    show_res = api_client.get(f"/delivery-records/{delivery_id}")
    assert show_res.status_code == 200
    assert show_res.get_json()["data"]["delivery_date"] == "2026-09-18"

    # UPDATE (PUT /delivery-records/:id -> 200)
    update_res = api_client.put(f"/delivery-records/{delivery_id}", json={
        "customer": "Delivery Test Client",
        "delivery_date": "2026-09-19"
    })
    assert update_res.status_code == 200
    assert update_res.get_json()["data"]["delivery_date"] == "2026-09-19"

    # DELETE (DELETE /delivery-records/:id -> 200)
    assert api_client.delete(f"/delivery-records/{delivery_id}").status_code == 200
    _assert_404_envelope(api_client.get(f"/delivery-records/{delivery_id}"))


def test_delivery_records_validation_and_edge_cases(api_client):
    _assert_422_envelope(api_client.post("/delivery-records", json={}), ["delivery_date", "customer"])
    _assert_422_envelope(
        api_client.put("/delivery-records/1", json={"delivery_date": "", "customer": "   "}),
        ["delivery_date", "customer"]
    )
    _assert_404_envelope(
        api_client.post("/delivery-records", json={"customer": "Ghost Customer 999", "delivery_date": "2026-09-18"})
    )
    _assert_404_envelope(
        api_client.put("/delivery-records/999999", json={"customer": "Delivery Test Client", "delivery_date": "2026-09-18"})
    )
    _assert_404_envelope(api_client.delete("/delivery-records/999999"))
    assert api_client.delete("/delivery-records").status_code == 405


# ============================================================================
# 5. PAYMENTS MODULE — HAPPY PATH, VALIDATION (422), AND EDGE CASES
# ============================================================================

def test_payments_full_crud_happy_path(api_client):
    # CREATE (POST /payments -> 201)
    create_res = api_client.post("/payments", json={
        "customer": "Payment Test Client",
        "payment_amount": 350.0,
        "payment_method": "Cash"
    })
    assert create_res.status_code == 201
    payment_id = create_res.get_json()["data"]["id"]
    assert create_res.get_json()["data"]["payment_amount"] == 350.0

    # READ LIST & SHOW (GET -> 200)
    assert api_client.get("/payments").status_code == 200
    show_res = api_client.get(f"/payments/{payment_id}")
    assert show_res.status_code == 200
    assert show_res.get_json()["data"]["payment_method"] == "Cash"

    # UPDATE (PUT /payments/:id -> 200)
    update_res = api_client.put(f"/payments/{payment_id}", json={
        "customer": "Payment Test Client",
        "payment_amount": 425.5,
        "payment_method": "GCash"
    })
    assert update_res.status_code == 200
    assert update_res.get_json()["data"]["payment_amount"] == 425.5
    assert update_res.get_json()["data"]["payment_method"] == "GCash"

    # DELETE (DELETE /payments/:id -> 200)
    assert api_client.delete(f"/payments/{payment_id}").status_code == 200
    _assert_404_envelope(api_client.get(f"/payments/{payment_id}"))


def test_payments_validation_and_edge_cases(api_client):
    # Missing all fields -> 422
    _assert_422_envelope(
        api_client.post("/payments", json={}),
        ["customer", "payment_amount", "payment_method"]
    )
    # Zero and negative payment_amount -> 422
    _assert_422_envelope(
        api_client.post("/payments", json={"customer": "Client", "payment_amount": 0, "payment_method": "Cash"}),
        ["payment_amount"]
    )
    _assert_422_envelope(
        api_client.post("/payments", json={"customer": "Client", "payment_amount": -100, "payment_method": "Cash"}),
        ["payment_amount"]
    )
    # Non-numeric string and boolean payment_amount -> 422
    _assert_422_envelope(
        api_client.post("/payments", json={"customer": "Client", "payment_amount": "abc", "payment_method": "Cash"}),
        ["payment_amount"]
    )
    _assert_422_envelope(
        api_client.post("/payments", json={"customer": "Client", "payment_amount": False, "payment_method": "Cash"}),
        ["payment_amount"]
    )
    # Non-existent payment ID on PUT / DELETE -> 404
    _assert_404_envelope(
        api_client.put("/payments/999999", json={"customer": "Client", "payment_amount": 150, "payment_method": "Cash"})
    )
    _assert_404_envelope(api_client.delete("/payments/999999"))
    assert api_client.delete("/payments").status_code == 405
