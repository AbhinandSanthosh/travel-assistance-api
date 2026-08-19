from __future__ import annotations

import hashlib
import secrets

import redis

from src.config.settings import settings
from src.core.logging_config import get_logger
from src.core.redis_client import get_redis_client

logger = get_logger(__name__)

_REVOKED_JTI_PREFIX = "revoked_jti:"
_REFRESH_TOKEN_PREFIX = "refresh_token:"  
_USER_REFRESH_SET_PREFIX = "user_refresh_tokens:"


def _hash_token(token: str) -> str:
    return hashlib.sha256(token.encode("utf-8")).hexdigest()




def revoke_access_token(jti: str, seconds_remaining: int) -> None:
    """Denylist a JWT's `jti` for however long it would otherwise
    still be valid. seconds_remaining <= 0 means it's already expired
    -- nothing to do."""

    if seconds_remaining <= 0:
        return

    try:
        get_redis_client().setex(
            f"{_REVOKED_JTI_PREFIX}{jti}",
            seconds_remaining,
            "1",
        )
    except redis.exceptions.RedisError as exc:
        logger.warning(f"Could not revoke access token (Redis unavailable): {exc}")


def is_access_token_revoked(jti: str) -> bool:
    try:
        return bool(get_redis_client().exists(f"{_REVOKED_JTI_PREFIX}{jti}"))
    except redis.exceptions.RedisError as exc:
        logger.warning(
            f"Revocation check unavailable (Redis down); allowing token: {exc}"
        )
        return False


# --- Refresh tokens -----------------------------------------------------


def issue_refresh_token(user_id: int) -> str:
    """Generate, store, and return a new plaintext refresh token.
    Only ever returned here -- from then on only its hash is kept."""

    token = secrets.token_urlsafe(32)
    token_hash = _hash_token(token)
    ttl_seconds = settings.refresh_token_expire_days * 86400

    try:
        client = get_redis_client()
        client.setex(f"{_REFRESH_TOKEN_PREFIX}{token_hash}", ttl_seconds, user_id)
        client.sadd(f"{_USER_REFRESH_SET_PREFIX}{user_id}", token_hash)
    except redis.exceptions.RedisError as exc:
        logger.warning(f"Could not persist refresh token (Redis unavailable): {exc}")

    return token


def resolve_refresh_token(token: str) -> int | None:
    """Return the owning user_id for a live refresh token, or None if
    it's unknown/expired/already revoked."""

    token_hash = _hash_token(token)
    try:
        value = get_redis_client().get(f"{_REFRESH_TOKEN_PREFIX}{token_hash}")
    except redis.exceptions.RedisError as exc:
        logger.warning(f"Refresh token lookup unavailable (Redis down): {exc}")
        return None

    if value is None:
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def revoke_refresh_token(token: str) -> None:
    """Revoke a single refresh token (e.g. on logout or rotation)."""

    token_hash = _hash_token(token)
    try:
        client = get_redis_client()
        user_id = client.get(f"{_REFRESH_TOKEN_PREFIX}{token_hash}")
        client.delete(f"{_REFRESH_TOKEN_PREFIX}{token_hash}")
        if user_id is not None:
            client.srem(f"{_USER_REFRESH_SET_PREFIX}{user_id}", token_hash)
    except redis.exceptions.RedisError as exc:
        logger.warning(f"Could not revoke refresh token (Redis unavailable): {exc}")


def revoke_all_refresh_tokens(user_id: int) -> None:
    """Revoke every refresh token for a user -- 'log out everywhere'.
    Called explicitly (POST /auth/logout-all) and automatically on
    password change, role change, or account deactivation."""

    set_key = f"{_USER_REFRESH_SET_PREFIX}{user_id}"
    try:
        client = get_redis_client()
        hashes = client.smembers(set_key)
        if hashes:
            client.delete(*(f"{_REFRESH_TOKEN_PREFIX}{h}" for h in hashes))
        client.delete(set_key)
    except redis.exceptions.RedisError as exc:
        logger.warning(
            f"Could not revoke all refresh tokens for user {user_id} "
            f"(Redis unavailable): {exc}"
        )