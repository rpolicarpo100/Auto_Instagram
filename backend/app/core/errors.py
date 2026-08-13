from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException


def _rid(request: Request) -> str:
    return getattr(request.state, "request_id", "")


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(StarletteHTTPException)
    async def http_exc(request: Request, exc: StarletteHTTPException):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": True,
                "status": exc.status_code,
                "detail": exc.detail,
                "request_id": _rid(request),
            },
        )

    @app.exception_handler(RequestValidationError)
    async def valid_exc(request: Request, exc: RequestValidationError):
        return JSONResponse(
            status_code=422,
            content={
                "error": True,
                "status": 422,
                "detail": "validation_error",
                "errors": exc.errors(),
                "request_id": _rid(request),
            },
        )

    @app.exception_handler(Exception)
    async def unhandled(request: Request, exc: Exception):
        return JSONResponse(
            status_code=500,
            content={
                "error": True,
                "status": 500,
                "detail": "internal_error",
                "request_id": _rid(request),
            },
        )
