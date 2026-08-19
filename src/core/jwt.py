from datetime import datetime, timedelta, UTC
from typing import Any
from uuid import uuid4

from jose import JWTError, jwt

from src.config.settings import settings

ALGORITHM = "HS256"


def create_access_token(
    subject: str,
    extra_claims: dict[str, Any] | None = None,
    expires_minutes: int | None = None,
) -> tuple[str, int]:
    """Create a signed JWT access token.

    Returns (token, expires_in_seconds).
    """
    minutes = (
        expires_minutes
        if expires_minutes is not None
        else settings.access_token_expire_minutes
    )

    now = datetime.now(UTC)
    expire = now + timedelta(minutes=minutes)

    to_encode: dict[str, Any] = {
        "sub": subject,
        "iat": now,
        "exp": expire,
        # Unique per token -- lets a single token be revoked (denylisted)
        # without needing to invalidate the signing key or every token
        # for that user. See src/core/token_store.py.
        "jti": uuid4().hex,
    }
    if extra_claims:
        to_encode.update(extra_claims)

    token = jwt.encode(
        to_encode,
        settings.secret_key,
        algorithm=ALGORITHM,
    )

    return token, minutes * 60


def decode_access_token(token: str) -> dict[str, Any]:
    """Decode and verify a JWT access token.

    Raises jose.JWTError (or subclasses, e.g. ExpiredSignatureError)
    if the token is invalid, tampered with, or expired.
    """
    return jwt.decode(
        token,
        settings.secret_key,
        algorithms=[ALGORITHM],
    )


__all__ = ["create_access_token", "decode_access_token", "JWTError"]
