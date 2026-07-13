import pytest
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture(scope="module")
def client():
    with TestClient(app) as test_client:
        yield test_client

def test_predict_returns_expected_schema(client):
    response = client.post(
        "/api/v1/predict",
        json={"text": "The mitochondria is the powerhouse of the cell."},
    )

    assert response.status_code == 200
    body = response.json()

    assert body["prediction"] in {"Human", "AI"}
    assert 0.0 <= body["confidence"] <= 1.0
    assert body["label_id"] in {0, 1}
    assert set(body["probabilities"].keys()) == {"Human", "AI"}
    assert isinstance(body["processing_time_ms"], float)

def test_predict_rejects_empty_text(client):
    response = client.post("/api/v1/predict", json={"text": ""})
    assert response.status_code == 422

def test_predict_rejects_whitespace_only_text(client):
    response = client.post("/api/v1/predict", json={"text": "     "})
    assert response.status_code == 422

def test_predict_rejects_missing_text_field(client):
    response = client.post("/api/v1/predict", json={})
    assert response.status_code == 422

def test_predict_probabilities_sum_to_one(client):
    response = client.post("/api/v1/predict", json={"text": "A short test sentence."})
    body = response.json()
    total = sum(body["probabilities"].values())
    assert abs(total - 1.0) < 1e-3
