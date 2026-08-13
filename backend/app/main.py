from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.settings import settings

app = FastAPI(
    title="Instagram AI Factory",
    version="0.1.0",
    description="Phase 01 foundation. Instagram features are not implemented yet.",
)

origins = [o.strip() for o in settings.cors_origins.split(",") if o.strip()]
if origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["GET", "HEAD", "OPTIONS"],
        allow_headers=["*"],
    )


@app.get("/api/health")
@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "instagram-ai-factory"}
