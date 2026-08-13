from fastapi.testclient import TestClient

from app.main import app
from app.settings import normalize_database_url

client = TestClient(app)


def test_normalize_render_postgres_url():
    assert normalize_database_url("postgres://u:p@h/db").startswith(
        "postgresql+psycopg://"
    )


def test_media_rejects_garbage_and_lists_empty():
    client.post(
        "/api/v1/auth/register",
        json={"email": "media@example.com", "password": "correct-horse"},
    )
    listed = client.get("/api/v1/media")
    assert listed.status_code == 200
    assert listed.json()["status"] == "NO DATA"
    assert listed.json()["items"] == []

    bad = client.post(
        "/api/v1/media",
        files={"file": ("x.bin", b"not-a-real-image", "application/octet-stream")},
    )
    assert bad.status_code == 400

    png = (
        b"\x89PNG\r\n\x1a\n"
        + b"\x00\x00\x00\rIHDR"
        + b"\x00\x00\x00\x01\x00\x00\x00\x01\x08\x02\x00\x00\x00"
        + b"\x90wS\xde"
        + b"\x00\x00\x00\x00IEND\xaeB`\x82"
    )
    ok = client.post("/api/v1/media", files={"file": ("a.png", png, "image/png")})
    assert ok.status_code == 200
    assert ok.json()["mime_type"] == "image/png"
    listed2 = client.get("/api/v1/media")
    assert listed2.json()["status"] == "REAL"
    assert len(listed2.json()["items"]) == 1


def test_security_headers_on_health():
    r = client.get("/api/health")
    assert r.headers.get("X-Content-Type-Options") == "nosniff"
    assert r.headers.get("X-Frame-Options") == "DENY"
