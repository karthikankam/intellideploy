from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health():
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}


def test_predict_valid_payload():
    resp = client.post(
        "/api/predict",
        json={
            "age": 22,
            "vehicle_age_years": 15,
            "prior_claims": 2,
            "annual_mileage_thousands": 25,
        },
    )
    assert resp.status_code == 200
    body = resp.json()
    assert body["risk_label"] in ("high", "low")
    assert 0.0 <= body["risk_probability"] <= 1.0


def test_predict_rejects_bad_input():
    resp = client.post("/api/predict", json={"age": -5})
    assert resp.status_code == 422


def test_policy_crud_flow():
    create_resp = client.post(
        "/api/policies", json={"holder_name": "Jane Doe", "vehicle": "Honda Civic"}
    )
    assert create_resp.status_code == 201
    policy_id = create_resp.json()["id"]

    list_resp = client.get("/api/policies")
    assert list_resp.status_code == 200
    assert any(p["id"] == policy_id for p in list_resp.json())

    delete_resp = client.delete(f"/api/policies/{policy_id}")
    assert delete_resp.status_code == 204

    delete_again = client.delete(f"/api/policies/{policy_id}")
    assert delete_again.status_code == 404
