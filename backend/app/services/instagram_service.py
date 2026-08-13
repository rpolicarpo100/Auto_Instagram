from app.providers.instagram.factory import get_instagram_provider
from app.settings import settings


class InstagramService:
    def __init__(self) -> None:
        self.provider = get_instagram_provider()

    def public_status(self) -> dict:
        caps = self.provider.capabilities()
        return {
            "provider": self.provider.name(),
            "meta_configured": settings.meta_configured(),
            "capabilities": caps,
            "connection": "NOT_CONFIGURED"
            if not settings.meta_configured()
            else "READY_TO_CONNECT",
        }
