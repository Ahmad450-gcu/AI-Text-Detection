from fastapi.testclient import TestClient
from app.main import app

def test_health_reports_model_loaded():
    with TestClient(app) as client:
        response = client.get("/api/v1/health")

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert body["model_loaded"] is True
    assert body["model_name"]
    assert body["device"] in {"cpu", "cuda", "cuda:0"}

def test_root_endpoint():
    with TestClient(app) as client:
        response = client.get("/")

    assert response.status_code == 200
    assert "docs" in response.json()
