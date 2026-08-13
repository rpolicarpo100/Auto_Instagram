from app.providers.instagram.base import InstagramProvider
from app.providers.instagram.meta import MetaInstagramProvider
from app.providers.instagram.mock import MockInstagramProvider
from app.settings import settings


def get_instagram_provider(*, allow_mock: bool = False) -> InstagramProvider:
    if settings.app_env == "production":
        return MetaInstagramProvider()
    if allow_mock and settings.app_env == "test":
        return MockInstagramProvider()
    return MetaInstagramProvider()
