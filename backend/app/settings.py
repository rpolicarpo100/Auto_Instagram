from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_env: str = "development"
    app_name: str = "instagram-ai-factory"
    log_level: str = "info"
    cors_origins: str = "http://localhost:5173"

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

    def cors_origin_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]

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
