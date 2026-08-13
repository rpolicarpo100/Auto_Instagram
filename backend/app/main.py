from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import api_router
from app.core.errors import register_exception_handlers
from app.core.request_id import RequestIdMiddleware
from app.core.security_headers import SecurityHeadersMiddleware
from app.db.bootstrap import create_schema
from app.settings import settings

app = FastAPI(
    title="Instagram AI Factory",
    version="0.1.0",
    description="Instagram Content OS. No fake metrics.",
)

app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(RequestIdMiddleware)
origins = settings.cors_origin_list()
if origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "HEAD", "OPTIONS"],
        allow_headers=["*"],
    )

register_exception_handlers(app)
app.include_router(api_router, prefix="/api/v1")
create_schema()


@app.get("/api/health")
@app.get("/health")
def health() -> dict[str, str]:
    return {
        "status": "ok",
        "service": "instagram-ai-factory",
        "database": "CONFIGURED" if settings.database_configured() else "NOT_CONFIGURED",
    }
