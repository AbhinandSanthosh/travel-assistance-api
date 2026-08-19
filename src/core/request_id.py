"""Request-ID correlation.

Every request gets a UUID -- either the caller's own `X-Request-ID`
(so a client's request ID and ours line up end to end) or a freshly
generated one. It's stored in a ContextVar (not request.state) so
that ANY log line emitted while handling this request picks it up
automatically via RequestIDLogFilter, without every function down the
call stack needing to accept and thread through a request_id
parameter. It's also echoed back in the response header so a caller
(or a support conversation) can hand you the exact ID to grep for.
"""

from __future__ import annotations

import logging
import uuid
from contextvars import ContextVar

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

_request_id_ctx: ContextVar[str] = ContextVar("request_id", default="-")

REQUEST_ID_HEADER = "X-Request-ID"


def get_request_id() -> str:
    return _request_id_ctx.get()


class RequestIDMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        incoming = request.headers.get(REQUEST_ID_HEADER)
        request_id = incoming if incoming else uuid.uuid4().hex

        token = _request_id_ctx.set(request_id)
        try:
            response = await call_next(request)
        finally:
            _request_id_ctx.reset(token)

        response.headers[REQUEST_ID_HEADER] = request_id
        return response


class RequestIDLogFilter(logging.Filter):
    """Stamps every log record with the request ID active when it was
    emitted (or '-' for anything logged outside a request, e.g. at
    startup)."""

    def filter(self, record: logging.LogRecord) -> bool:
        record.request_id = get_request_id()
        return True
