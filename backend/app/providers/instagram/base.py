from abc import ABC, abstractmethod
from typing import Any


class InstagramProvider(ABC):
    @abstractmethod
    def name(self) -> str: ...

    @abstractmethod
    def capabilities(self) -> dict[str, str]: ...

    @abstractmethod
    def authorization_url(self, state: str) -> str: ...

    @abstractmethod
    def exchange_code(self, code: str) -> dict[str, Any]: ...

    @abstractmethod
    def get_profile(self, access_token: str) -> dict[str, Any]: ...

    @abstractmethod
    def get_media(self, access_token: str, ig_user_id: str) -> list[dict[str, Any]]: ...

    @abstractmethod
    def get_insights(self, access_token: str, ig_user_id: str) -> dict[str, Any]: ...
