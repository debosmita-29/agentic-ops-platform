from fastapi.testclient import TestClient

from operational_dashboard.api.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_analyze():
    response = client.post("/analyze", json={"prompt": "Analyze readiness"})
    assert response.status_code == 200
    body = response.json()
    assert "scores" in body
    assert "summary" in body
