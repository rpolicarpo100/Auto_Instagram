from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_api_health():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "service": "instagram-ai-factory",
    }


def test_root_health_alias():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
