from typing import Any

from app.providers.instagram.base import InstagramProvider


class MockInstagramProvider(InstagramProvider):
    """Automated tests only. Never used when APP_ENV=production."""

    def name(self) -> str:
        return "mock"

    def capabilities(self) -> dict[str, str]:
        return {
            "oauth": "SUPPORTED",
            "profile": "SUPPORTED",
            "media": "SUPPORTED",
            "insights": "NOT_AVAILABLE",
            "publish": "NOT_SUPPORTED",
        }

    def authorization_url(self, state: str) -> str:
        return f"https://example.test/oauth?state={state}"

    def exchange_code(self, code: str) -> dict[str, Any]:
        return {"access_token": f"mock-{code}", "user_id": "0"}

    def get_profile(self, access_token: str) -> dict[str, Any]:
        return {"id": "0", "username": "test_only"}

    def get_media(self, access_token: str, ig_user_id: str) -> list[dict[str, Any]]:
        return []

    def get_insights(self, access_token: str, ig_user_id: str) -> dict[str, Any]:
        return {"status": "NOT_AVAILABLE"}
