from fastapi import APIRouter, Depends, Request, status
from sqlalchemy.orm import Session

import redis
import time

from src.api.dependencies.auth import get_current_user
from src.config.settings import settings
from src.core.client_ip import get_client_ip
from src.core.jwt import create_access_token
from src.core.logging_config import get_logger
from src.core.redis_client import get_redis_client
from src.core.security import verify_password
from src.db.session import get_db
from src.exceptions.administration.auth import (
    InactiveUserError,
    InvalidCredentialsError,
    TooManyLoginAttemptsError,
)
from src.models.administration.user import User
from src.repositories.administration.user import UserRepository
from src.schemas.administration.auth import (
    CurrentUserResponse,
    LoginRequest,
    LoginResponse,
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

    logger.success(f"User '{user.username}' logged in")

    return LoginResponse(access_token=token, expires_in=expires_in)


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
