from fastapi.testclient import TestClient

from app.main import app
from app.settings import Settings

client = TestClient(app)


def test_video_status_honest():
    r = client.get("/api/v1/video/status")
    assert r.status_code == 200
    assert r.json()["ffmpeg"] in {"AVAILABLE", "NOT AVAILABLE"}


def test_cors_strips_comments():
    s = Settings(
        cors_origins="http://localhost:5173 (atualizas quando o frontend tiver URL),https://app.example.com"
    )
    assert s.cors_origin_list() == [
        "http://localhost:5173",
        "https://app.example.com",
    ]
