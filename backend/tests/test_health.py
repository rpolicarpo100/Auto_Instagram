from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_api_health():
    response = client.get("/api/health")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert body["service"] == "instagram-ai-factory"
    assert body["database"] in {"CONFIGURED", "NOT_CONFIGURED"}
    assert "X-Request-ID" in response.headers


def test_root_health_alias():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_v1_health_version_config():
    h = client.get("/api/v1/health")
    assert h.status_code == 200
    v = client.get("/api/v1/version")
    assert v.status_code == 200
    assert "version" in v.json()
    c = client.get("/api/v1/config")
    assert c.status_code == 200
    body = c.json()
    assert "meta_oauth" in body
    assert "database" in body
    assert "instagram" in body
