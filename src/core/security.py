import bcrypt
import re

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


_SPECIAL_CHARS = re.compile(r"[^A-Za-z0-9]")


def password_policy_errors(password: str) -> list[str]:
    """Return a list of human-readable violations of the password
    policy, empty if the password is acceptable.

    Policy (Phase 2): 8+ chars (already enforced at the schema level
    via Field(min_length=8), checked again here defensively), at
    least one uppercase, one lowercase, one digit, one special char.
    Deliberately not checking against a common-password/breach list
    here -- that's an external dependency/data-freshness concern,
    better added later as its own piece if wanted.
    """

    errors = []
    if len(password) < 8:
        errors.append("must be at least 8 characters")
    if not any(c.isupper() for c in password):
        errors.append("must contain at least one uppercase letter")
    if not any(c.islower() for c in password):
        errors.append("must contain at least one lowercase letter")
    if not any(c.isdigit() for c in password):
        errors.append("must contain at least one digit")
    if not _SPECIAL_CHARS.search(password):
        errors.append("must contain at least one special character")
    return errors
