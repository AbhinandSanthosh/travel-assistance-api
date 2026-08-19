from fastapi import APIRouter, Depends, Request, status
from sqlalchemy.orm import Session

import redis
import time

from src.api.dependencies.auth import get_current_user
from src.config.settings import settings
from src.core.alerting import maybe_alert
from src.core.client_ip import get_client_ip
from src.core.jwt import create_access_token
from src.core.logging_config import get_logger
from src.core.redis_client import get_redis_client
from src.core.security import verify_password
from src.core.token_store import (
    issue_refresh_token,
    resolve_refresh_token,
    revoke_access_token,
    revoke_all_refresh_tokens,
    revoke_refresh_token,
)
from src.db.session import get_db
from src.exceptions.administration.auth import (
    InactiveUserError,
    InvalidCredentialsError,
    InvalidRefreshTokenError,
    TooManyLoginAttemptsError,
)
from src.models.administration.user import User
from src.repositories.administration.user import UserRepository
from src.schemas.administration.auth import (
    CurrentUserResponse,
    LoginRequest,
    LoginResponse,
    LogoutRequest,
    RefreshRequest,
)

router = APIRouter(
    prefix="/api/v1/auth",
    tags=["Admin Auth"],
)

_user_repository = UserRepository()
logger = get_logger(__name__)


def _check_login_rate_limit(client_ip: str) -> None:
    """Fixed one-minute window per source IP, enforced via Redis
    (same INCR + EXPIRE pattern as the /autocheck rate limiter).
    Fails open if Redis itself is unreachable -- an unavailable cache
    shouldn't take login down.
    """

    window = int(time.time() // 60)
    key = f"ratelimit:login:{client_ip}:{window}"

    try:
        redis_client = get_redis_client()
        current = redis_client.incr(key)
        if current == 1:
            redis_client.expire(key, 60)
    except redis.exceptions.RedisError as exc:
        logger.warning(f"Login rate limiting unavailable ({exc}); allowing request.")
        return

    if current > settings.login_rate_limit_per_minute:
        logger.warning(f"Login rate limit exceeded for {client_ip}")
        raise TooManyLoginAttemptsError(settings.login_rate_limit_per_minute)


@router.post(
    "/login",
    response_model=LoginResponse,
    status_code=status.HTTP_200_OK,
    summary="Admin/Compliance Officer login (JWT)",
)
def login(
    payload: LoginRequest,
    request: Request,
    db: Session = Depends(get_db),
) -> LoginResponse:
    """Authenticate an administrative user (username/email + password)
    and issue a short-lived JWT for accessing the Admin APIs.

    API clients (airlines, booking platforms, etc.) do NOT use this
    endpoint -- they authenticate to /autocheck with an X-API-Key.
    """

    _check_login_rate_limit(get_client_ip(request))

    user = _user_repository.get_by_username(db, payload.username)
    if user is None:
        user = _user_repository.get_by_email(db, payload.username)

    if user is None or not verify_password(
        payload.password,
        user.password_hash,
    ):
        # Never log the submitted password. File-only (warning) --
        # a wrong password is routine, not a terminal-worthy event.
        # Repeated failures for the same identity are the signal
        # worth alerting on; that belongs in rate-limiting, not here.
        logger.warning(f"Failed login attempt for '{payload.username}'")
        maybe_alert("failed_login", get_client_ip(request), {"username": payload.username})
        raise InvalidCredentialsError()

    if not user.status:
        logger.warning(f"Login attempt on inactive account '{user.username}'")
        raise InactiveUserError()

    token, expires_in = create_access_token(
        subject=str(user.id),
        extra_claims={
            "username": user.username,
            "role_id": user.role_id,
        },
    )
    refresh_token = issue_refresh_token(user.id)

    logger.success(f"User '{user.username}' logged in")

    return LoginResponse(
        access_token=token,
        expires_in=expires_in,
        refresh_token=refresh_token,
    )


@router.post(
    "/refresh",
    response_model=LoginResponse,
    status_code=status.HTTP_200_OK,
    summary="Exchange a refresh token for a new access token",
)
def refresh(
    payload: RefreshRequest,
    db: Session = Depends(get_db),
) -> LoginResponse:
    """Issue a new access token from a still-valid refresh token.

    Rotates the refresh token on every use (the old one is revoked
    and a new one issued) -- standard refresh-token-rotation practice,
    so a stolen-but-unused refresh token becomes useless the moment
    the legitimate client next refreshes.
    """

    user_id = resolve_refresh_token(payload.refresh_token)
    if user_id is None:
        raise InvalidRefreshTokenError()

    user = _user_repository.get_by_id(db, user_id)
    if user is None or not user.status:
        raise InvalidRefreshTokenError()

    revoke_refresh_token(payload.refresh_token)

    token, expires_in = create_access_token(
        subject=str(user.id),
        extra_claims={
            "username": user.username,
            "role_id": user.role_id,
        },
    )
    new_refresh_token = issue_refresh_token(user.id)

    return LoginResponse(
        access_token=token,
        expires_in=expires_in,
        refresh_token=new_refresh_token,
    )


@router.post(
    "/logout",
    status_code=status.HTTP_200_OK,
    summary="Revoke the current access token (and refresh token, if provided)",
)
def logout(
    payload: LogoutRequest,
    request: Request,
    user: User = Depends(get_current_user),
) -> dict:
    jti = getattr(request.state, "token_jti", None)
    exp = getattr(request.state, "token_exp", None)
    if jti is not None and exp is not None:
        seconds_remaining = int(exp - time.time())
        revoke_access_token(jti, seconds_remaining)

    if payload.refresh_token:
        revoke_refresh_token(payload.refresh_token)

    logger.success(f"User '{user.username}' logged out")

    return {"message": "Logged out successfully."}


@router.post(
    "/logout-all",
    status_code=status.HTTP_200_OK,
    summary="Revoke every refresh token for the current user (log out all sessions)",
)
def logout_all(
    request: Request,
    user: User = Depends(get_current_user),
) -> dict:
    """Log out every session for this account, not just the current
    one. Also called automatically on password change, role change,
    or account deactivation -- see UserService.update_user."""

    jti = getattr(request.state, "token_jti", None)
    exp = getattr(request.state, "token_exp", None)
    if jti is not None and exp is not None:
        revoke_access_token(jti, int(exp - time.time()))

    revoke_all_refresh_tokens(user.id)

    logger.success(f"User '{user.username}' logged out of all sessions")

    return {"message": "Logged out of all sessions."}


@router.get(
    "/me",
    response_model=CurrentUserResponse,
    status_code=status.HTTP_200_OK,
    summary="Get the currently authenticated admin user",
)
def read_current_user(
    user: User = Depends(get_current_user),
) -> CurrentUserResponse:
    return CurrentUserResponse(
        id=user.id,
        username=user.username,
        full_name=user.full_name,
        email=user.email,
        role_id=user.role_id,
        role_name=user.role.role_name,
    )
