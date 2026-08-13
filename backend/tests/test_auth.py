from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_register_login_me_logout():
    email = "owner@example.com"
    password = "correct-horse"
    r = client.post("/api/v1/auth/register", json={"email": email, "password": password})
    assert r.status_code == 200
    me = client.get("/api/v1/auth/me")
    assert me.status_code == 200
    assert me.json()["email"] == email

    client.post("/api/v1/auth/logout")
    assert client.get("/api/v1/auth/me").status_code == 401

    bad = client.post(
        "/api/v1/auth/login", json={"email": email, "password": "wrong-pass"}
    )
    assert bad.status_code == 401

    ok = client.post("/api/v1/auth/login", json={"email": email, "password": password})
    assert ok.status_code == 200
    assert client.get("/api/v1/auth/me").status_code == 200


def test_dashboard_without_instagram():
    client.post(
        "/api/v1/auth/register",
        json={"email": "dash@example.com", "password": "correct-horse"},
    )
    d = client.get("/api/v1/dashboard")
    assert d.status_code == 200
    body = d.json()
    assert body["followers"]["status"] == "NO DATA"
    assert body["followers"]["value"] is None
    assert body["reach"]["status"] == "NO DATA"


def test_instagram_status_not_configured():
    client.post(
        "/api/v1/auth/register",
        json={"email": "ig@example.com", "password": "correct-horse"},
    )
    s = client.get("/api/v1/instagram/status")
    assert s.status_code == 200
    assert s.json()["account"]["status"] == "NOT_CONFIGURED"

    c = client.get("/api/v1/instagram/connect")
    assert c.status_code == 503
    assert c.json()["detail"] == "META_NOT_CONFIGURED"
