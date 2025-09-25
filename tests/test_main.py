"""Integration smoke tests ensuring the API serves seeded data."""

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_healthcheck() -> None:
    """Health endpoint should confirm the service is operational."""

    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_products_pagination_and_search() -> None:
    """Products endpoint should support pagination and keyword filtering."""

    limited = client.get("/products/?limit=1")
    assert limited.status_code == 200
    assert len(limited.json()) == 1

    searched = client.get("/products/?q=aurora")
    assert searched.status_code == 200
    assert searched.json()[0]["brand"] == "Aurora Botanics"


def test_product_offer_summary_present() -> None:
    """Products should include aggregated offer summary data."""

    product = client.get("/products/?q=luna").json()[0]
    summary = product["offer_summary"]
    assert summary["lowest_price"] <= summary["highest_price"]


def test_offer_snapshot_endpoint() -> None:
    """Offer snapshot endpoint should provide pricing intelligence."""

    product_id = client.get("/products/").json()[0]["id"]
    response = client.get(f"/offers/snapshot/{product_id}")
    assert response.status_code == 200
    snapshot = response.json()
    assert snapshot["count"] >= 1


def test_review_highlights_endpoint() -> None:
    """Review highlights should expose positive ratio for seeded data."""

    product_id = client.get("/products/").json()[0]["id"]
    response = client.get(f"/reviews/highlights/{product_id}")
    assert response.status_code == 200
    highlights = response.json()
    assert highlights["positive_ratio"] > 0


def test_rfq_create_and_update_flow() -> None:
    """RFQ endpoints should support creation and status updates."""

    product = client.get("/products/").json()[0]
    supplier = client.get("/suppliers/").json()[0]

    create_response = client.post(
        "/rfqs/",
        json={
            "product_id": product["id"],
            "supplier_id": supplier["id"],
            "status": "open",
            "quotes": [{"unit_price": 20.0, "currency": "USD"}],
        },
    )
    assert create_response.status_code == 200
    rfq_id = create_response.json()["id"]

    update_response = client.patch(
        f"/rfqs/{rfq_id}",
        json={"status": "closed"},
    )
    assert update_response.status_code == 200
    assert update_response.json()["status"] == "closed"


def test_insight_endpoint() -> None:
    """Insight endpoint should return computed metrics for the demo product."""

    product_id = client.get("/products/").json()[0]["id"]
    response = client.get(f"/insights/{product_id}")
    assert response.status_code == 200
    payload = response.json()
    assert payload["sales_score"] == 0.82
