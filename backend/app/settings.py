from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


def normalize_database_url(url: str) -> str:
    raw = url.strip()
    if raw.startswith("postgres://"):
        return "postgresql+psycopg://" + raw[len("postgres://") :]
    if raw.startswith("postgresql://") and "+psycopg" not in raw:
        return "postgresql+psycopg://" + raw[len("postgresql://") :]
    return raw


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_env: str = "development"
    app_name: str = "instagram-ai-factory"
    log_level: str = "info"
    cors_origins: str = "http://localhost:5173"
    frontend_origin: str = ""

    database_url: str = ""

    session_secret: str = "dev-only-change-me"
    session_cookie_name: str = "iaf_session"
    session_ttl_hours: int = 168
    token_encryption_key: str = ""

    meta_app_id: str = ""
    meta_app_secret: str = ""
    meta_redirect_uri: str = ""
    instagram_oauth_base: str = "https://www.instagram.com"
    instagram_graph_base: str = "https://graph.instagram.com"

    local_storage_dir: str = "storage/local"
    max_upload_bytes: int = 50 * 1024 * 1024

    @field_validator("database_url", mode="before")
    @classmethod
    def _db_url(cls, v: object) -> str:
        if not v:
            return ""
        return normalize_database_url(str(v))

    def cors_origin_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]

    def public_frontend_origin(self) -> str:
        if self.frontend_origin.strip():
            return self.frontend_origin.strip().rstrip("/")
        origins = self.cors_origin_list()
        return origins[0].rstrip("/") if origins else ""

    def database_configured(self) -> bool:
        return bool(self.database_url.strip())

    def meta_configured(self) -> bool:
        return bool(
            self.meta_app_id.strip()
            and self.meta_app_secret.strip()
            and self.meta_redirect_uri.strip()
        )

    def cookie_secure(self) -> bool:
        return self.app_env == "production"


settings = Settings()
