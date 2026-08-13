from typing import Any
from urllib.parse import urlencode

import httpx

from app.providers.instagram.base import InstagramProvider
from app.settings import settings

SCOPES = [
    "instagram_business_basic",
    "instagram_business_manage_insights",
]


class MetaInstagramProvider(InstagramProvider):
    def name(self) -> str:
        return "meta"

    def capabilities(self) -> dict[str, str]:
        if not settings.meta_configured():
            return {
                "oauth": "NOT_CONFIGURED",
                "profile": "NOT_CONFIGURED",
                "media": "NOT_CONFIGURED",
                "insights": "NOT_CONFIGURED",
                "publish": "NOT_CONFIGURED",
            }
        return {
            "oauth": "SUPPORTED",
            "profile": "SUPPORTED",
            "media": "SUPPORTED",
            "insights": "REQUIRES_PERMISSION",
            "publish": "NOT_IMPLEMENTED",
        }

    def authorization_url(self, state: str) -> str:
        if not settings.meta_configured():
            raise RuntimeError("META_NOT_CONFIGURED")
        qs = urlencode(
            {
                "client_id": settings.meta_app_id,
                "redirect_uri": settings.meta_redirect_uri,
                "response_type": "code",
                "scope": ",".join(SCOPES),
                "state": state,
            }
        )
        return f"{settings.instagram_oauth_base}/oauth/authorize?{qs}"

    def exchange_code(self, code: str) -> dict[str, Any]:
        if not settings.meta_configured():
            raise RuntimeError("META_NOT_CONFIGURED")
        url = f"{settings.instagram_graph_base}/oauth/access_token"
        with httpx.Client(timeout=20) as client:
            res = client.post(
                url,
                data={
                    "client_id": settings.meta_app_id,
                    "client_secret": settings.meta_app_secret,
                    "grant_type": "authorization_code",
                    "redirect_uri": settings.meta_redirect_uri,
                    "code": code,
                },
            )
            res.raise_for_status()
            return res.json()

    def get_profile(self, access_token: str) -> dict[str, Any]:
        fields = "user_id,username,name,account_type,profile_picture_url,followers_count,follows_count,media_count"
        url = f"{settings.instagram_graph_base}/me"
        with httpx.Client(timeout=20) as client:
            res = client.get(
                url, params={"fields": fields, "access_token": access_token}
            )
            res.raise_for_status()
            return res.json()

    def get_media(self, access_token: str, ig_user_id: str) -> list[dict[str, Any]]:
        url = f"{settings.instagram_graph_base}/{ig_user_id}/media"
        with httpx.Client(timeout=20) as client:
            res = client.get(
                url,
                params={
                    "fields": "id,caption,media_type,media_url,permalink,timestamp",
                    "access_token": access_token,
                },
            )
            res.raise_for_status()
            return res.json().get("data") or []

    def get_insights(self, access_token: str, ig_user_id: str) -> dict[str, Any]:
        url = f"{settings.instagram_graph_base}/{ig_user_id}/insights"
        with httpx.Client(timeout=20) as client:
            res = client.get(
                url,
                params={
                    "metric": "reach,follower_count",
                    "period": "day",
                    "access_token": access_token,
                },
            )
            if res.status_code >= 400:
                return {"status": "NOT_AVAILABLE", "http_status": res.status_code}
            return res.json()
