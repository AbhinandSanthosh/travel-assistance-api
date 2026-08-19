"""Generic audit-logging middleware for the Admin API.

Problem: the AuditLog table + AuditLogService already existed, but
nothing outside the audit-log router's own CRUD endpoints ever wrote
to it -- every actual admin mutation (rule approvals, API client
changes, user/role changes, etc.) left no trail.

Rather than hand-wiring ~25 services x create/update/delete each,
this middleware exploits the fact that every admin router follows the
same shape: flat prefix (e.g. `/api-clients/{id}`), JWT-authenticated,
mutating via POST/PUT/PATCH/DELETE. That's enough to derive
entity_name/entity_id/action generically and log every current AND
future admin mutation without further router changes.

Known limitation: `old_value` is not captured (would require a
pre-mutation DB read keyed off knowledge of each entity's model,
which defeats the "no per-router wiring" goal). `new_value` is the
request payload as submitted. If a specific entity later needs a real
before/after diff, that's still best done in that entity's service
method -- this middleware is a safety net, not a replacement for
intentional per-entity audit logic where it matters most.
"""

from __future__ import annotations

import json

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from src.core.client_ip import get_client_ip
from src.core.logging_config import get_logger
from src.db.session import SessionLocal
from src.enums.audit_action import AuditAction
from src.models.administration.audit_log import AuditLog

logger = get_logger(__name__)

_ACTION_BY_METHOD = {
    "POST": AuditAction.INSERT,
    "PUT": AuditAction.UPDATE,
    "PATCH": AuditAction.UPDATE,
    "DELETE": AuditAction.DELETE,
}

# Path's first segment for routes that are NOT admin CRUD mutations,
# even though they may use POST/PUT: auth (login has no user yet),
# the audit log's own endpoints (logging writes to the audit log
# would be recursive noise), and the client-portal / autocheck
# surfaces (API-key authenticated, not JWT -- no admin actor to
# attribute the action to).
_EXCLUDED_PREFIXES = {"auth", "audit-logs", "client-portal", "autocheck"}

# Field names to redact from the captured payload regardless of which
# entity they belong to.
_SENSITIVE_FIELDS = {
    "password",
    "new_password",
    "current_password",
    "api_key",
    "secret_key",
    "access_token",
    "refresh_token",
}


def _redact(payload: dict) -> dict:
    return {
        key: ("***REDACTED***" if key.lower() in _SENSITIVE_FIELDS else value)
        for key, value in payload.items()
    }


class AuditLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        method = request.method.upper()
        action = _ACTION_BY_METHOD.get(method)

        path_parts = [p for p in request.url.path.split("/") if p]
        entity_name = path_parts[0] if path_parts else ""

        should_audit = bool(action) and entity_name not in _EXCLUDED_PREFIXES

        request_body: bytes = b""
        if should_audit:
            request_body = await request.body()

        response = await call_next(request)

        if not should_audit:
            return response

        if response.status_code >= 400:
            # Rejected mutations aren't "changes" -- nothing happened.
            return response

        user = getattr(request.state, "current_user", None)
        if user is None:
            # No JWT-authenticated actor (shouldn't normally happen
            # for an included admin router, but audit_logs.user_id is
            # NOT NULL -- fail safe by skipping rather than crashing
            # the response).
            return response

        # `call_next()` hands back a streaming wrapper, not the route
        # handler's original Response -- its `.body` isn't populated.
        # Drain the real bytes off `body_iterator`, then rebuild an
        # equivalent Response so the actual caller still gets the
        # exact same content (draining an iterator is destructive).
        response_body = b""
        async for chunk in response.body_iterator:
            response_body += chunk

        rebuilt_response = Response(
            content=response_body,
            status_code=response.status_code,
            headers=dict(response.headers),
            media_type=response.media_type,
        )

        entity_id = self._resolve_entity_id(path_parts, method, response_body)

        new_value = None
        if method in ("POST", "PUT", "PATCH") and request_body:
            try:
                parsed = json.loads(request_body)
                if isinstance(parsed, dict):
                    new_value = _redact(parsed)
            except (json.JSONDecodeError, UnicodeDecodeError):
                new_value = None

        self._write_audit_log(
            user_id=user.id,
            entity_name=entity_name,
            entity_id=entity_id,
            action=action,
            new_value=new_value,
            ip_address=get_client_ip(request),
        )

        return rebuilt_response

    @staticmethod
    def _resolve_entity_id(
        path_parts: list[str],
        method: str,
        response_body: bytes,
    ) -> int | None:
        # PUT/PATCH/DELETE on /entity/{id} -- id is the last segment.
        if method in ("PUT", "PATCH", "DELETE") and len(path_parts) >= 2:
            try:
                return int(path_parts[-1])
            except ValueError:
                return None

        # POST (create) -- id isn't known until the response; pull it
        # from the JSON body the handler returned.
        if method == "POST" and response_body:
            try:
                parsed = json.loads(response_body)
                if isinstance(parsed, dict) and "id" in parsed:
                    return int(parsed["id"])
            except (json.JSONDecodeError, ValueError, TypeError):
                return None

        return None

    @staticmethod
    def _write_audit_log(
        user_id: int,
        entity_name: str,
        entity_id: int | None,
        action: AuditAction,
        new_value: dict | None,
        ip_address: str | None,
    ) -> None:
        if entity_id is None:
            # Can't satisfy the NOT NULL entity_id column -- log why,
            # so gaps in coverage are visible rather than silent.
            logger.warning(
                f"Audit log skipped: could not resolve entity_id for "
                f"{action.value} on '{entity_name}'"
            )
            return

        db = SessionLocal()
        try:
            db.add(
                AuditLog(
                    user_id=user_id,
                    entity_name=entity_name,
                    entity_id=entity_id,
                    action=action,
                    old_value=None,
                    new_value=new_value,
                    ip_address=ip_address,
                )
            )
            db.commit()
        except Exception:
            db.rollback()
            logger.exception(
                f"Failed to write audit log for {action.value} on "
                f"'{entity_name}' (id={entity_id})"
            )
        finally:
            db.close()
