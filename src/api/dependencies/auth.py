from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from src.core.jwt import JWTError, decode_access_token
from src.core.logging_config import get_logger
from src.db.session import get_db
from src.exceptions.administration.auth import (
    InactiveUserError,
    InsufficientPermissionsError,
    InvalidOrExpiredTokenError,
)
from src.models.administration.user import User
from src.repositories.administration.user import UserRepository

_bearer_scheme = HTTPBearer(
    scheme_name="AdminJWT",
    description="JWT Bearer token obtained from POST /api/v1/auth/login.",
)

_user_repository = UserRepository()
logger = get_logger(__name__)


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(_bearer_scheme),
    db: Session = Depends(get_db),
) -> User:

    token = credentials.credentials
    
    try:
        payload = decode_access_token(token)
    except JWTError as e:
        # Never log the token itself, even to the file -- only the
        # failure reason and enough of the token to correlate it in
        # support conversations without exposing a usable credential.
        logger.warning(
            f"JWT decode failed: {type(e).__name__} "
            f"(token prefix: {token[:8]}...)"
        )
        raise InvalidOrExpiredTokenError() from None

    user_id_raw = payload.get("sub")
    if user_id_raw is None:
        raise InvalidOrExpiredTokenError()

    try:
        user_id = int(user_id_raw)
    except (TypeError, ValueError):
        raise InvalidOrExpiredTokenError() from None

    user = _user_repository.get_by_id(db, user_id)
    if user is None:
        raise InvalidOrExpiredTokenError()

    if not user.status:
        raise InactiveUserError()

    return user


_SUPER_ADMIN_ROLE_NAME = "Super Administrator"


def require_permission(permission_code: str):
    """Dependency factory: require the current user's role to have a
    specific permission (via role_permissions -> permissions).

    The "Super Administrator" role always passes, matching its stated
    "Full system access with unrestricted administrative privileges"
    (see seed_data/roles.csv) -- it isn't meant to depend on whichever
    permission rows happen to be seeded.

    Usage: dependencies=[Depends(require_permission("RULE_APPROVE"))]
    """

    def _check(user: User = Depends(get_current_user)) -> User:
        role = user.role

        if role.role_name == _SUPER_ADMIN_ROLE_NAME:
            return user

        codes = {
            rp.permission.permission_code
            for rp in role.role_permissions
            if rp.permission is not None
        }
        if permission_code not in codes:
            raise InsufficientPermissionsError()
        return user

    return _check
