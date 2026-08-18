from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse, Response

from src.config.settings import settings


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Adds standard defensive response headers to every response.

    Doesn't replace TLS termination/HSTS config at the proxy layer in
    prod, but ensures sane defaults are present even if that layer
    forgets to set them.
    """

    async def dispatch(self, request: Request, call_next) -> Response:
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Permissions-Policy"] = (
            "geolocation=(), microphone=(), camera=()"
        )
        if settings.app_env != "development":
            response.headers["Strict-Transport-Security"] = (
                "max-age=63072000; includeSubDomains"
            )
        return response


class BodySizeLimitMiddleware(BaseHTTPMiddleware):
    """Rejects requests whose declared Content-Length exceeds
    settings.max_request_body_bytes, before the body is read into
    memory / handed to a route.
    """

    async def dispatch(self, request: Request, call_next) -> Response:
        content_length = request.headers.get("content-length")
        if content_length is not None:
            try:
                length = int(content_length)
            except ValueError:
                length = None

            if length is not None and length > settings.max_request_body_bytes:
                return JSONResponse(
                    status_code=413,
                    content={
                        "detail": (
                            "Request body too large. Max allowed is "
                            f"{settings.max_request_body_bytes} bytes."
                        )
                    },
                )

        return await call_next(request)
