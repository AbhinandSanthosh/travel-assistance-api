from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from src.core.jwt import JWTError, decode_access_token
from src.db.session import get_db
from src.exceptions.administration.client_portal import (
    ClientPortalAccountInactiveError,
    InvalidOrExpiredPortalTokenError,
)
from src.models.administration.api_client import APIClient
from src.repositories.administration.api_client import APIClientRepository
from src.services.administration.client_portal_service import PORTAL_TOKEN_TYPE

_bearer_scheme = HTTPBearer(
    scheme_name="ClientPortalJWT",
    description=(
        "JWT Bearer token obtained from "
        "POST /api/v1/client-portal/login. This is a *portal session* "
        "token, not the API key -- it cannot be used against "
        "/autocheck."
    ),
)

_api_client_repository = APIClientRepository()


def get_current_portal_client(
    credentials: HTTPAuthorizationCredentials = Depends(_bearer_scheme),
    db: Session = Depends(get_db),
) -> APIClient:
    """Resolve the currently authenticated client-portal contact.

    Deliberately rejects admin JWTs (and vice versa): both token
    families are signed with the same secret, so the `type` claim is
    what keeps a token issued for one auth surface from being replayed
    against the other.
    """

    token = credentials.credentials

    try:
        payload = decode_access_token(token)
    except JWTError:
        raise InvalidOrExpiredPortalTokenError() from None

    if payload.get("type") != PORTAL_TOKEN_TYPE:
        raise InvalidOrExpiredPortalTokenError()

    client_id_raw = payload.get("sub")
    if client_id_raw is None:
        raise InvalidOrExpiredPortalTokenError()

    try:
        client_id = int(client_id_raw)
    except (TypeError, ValueError):
        raise InvalidOrExpiredPortalTokenError() from None

    client = _api_client_repository.get_by_id(db, client_id)
    if client is None:
        raise InvalidOrExpiredPortalTokenError()

    if not client.status:
        raise ClientPortalAccountInactiveError()

    return client