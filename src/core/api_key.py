

import hashlib
import secrets

_KEY_PREFIX = "tac_live"
_PREFIX_VISIBLE_CHARS = 4  # how many random chars are shown unmasked


def generate_api_key() -> str:
   
    return f"{_KEY_PREFIX}_{secrets.token_urlsafe(32)}"


def hash_api_key(plain_key: str) -> str:
    return hashlib.sha256(plain_key.encode("utf-8")).hexdigest()


def key_display_parts(plain_key: str) -> tuple[str, str]:
    
    body = plain_key[len(_KEY_PREFIX) + 1 :]
    prefix = f"{_KEY_PREFIX}_{body[:_PREFIX_VISIBLE_CHARS]}"
    last_four = plain_key[-4:]
    return prefix, last_four


__all__ = ["generate_api_key", "hash_api_key", "key_display_parts"]