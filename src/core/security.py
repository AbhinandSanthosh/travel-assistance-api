import bcrypt

# NOTE: uses the bcrypt library directly rather than going through
# passlib.CryptContext. passlib==1.7.4's bcrypt backend probes
# bcrypt.__about__.__version__ to detect the installed version, which
# was removed in bcrypt>=4.1 (we're pinned to bcrypt==5.0.0), causing
# every hash_password/verify_password call to raise at runtime. Talking
# to bcrypt directly avoids that broken detection shim entirely.

_BCRYPT_MAX_BYTES = 72  # bcrypt silently ignores anything past this


def hash_password(password: str) -> str:
    """Hash a plain-text password."""
    password_bytes = password.encode("utf-8")[:_BCRYPT_MAX_BYTES]
    hashed = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
    return hashed.decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain-text password against its bcrypt hash."""
    try:
        return bcrypt.checkpw(
            plain_password.encode("utf-8")[:_BCRYPT_MAX_BYTES],
            hashed_password.encode("utf-8"),
        )
    except ValueError:
        # Malformed/foreign hash format (e.g. not a bcrypt hash at all).
        return False
