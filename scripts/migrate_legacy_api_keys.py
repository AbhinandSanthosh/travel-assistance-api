"""Migrate legacy plaintext API keys (APIClient.api_key) to the hashed
lookup column (api_key_hash) used by every client created through the
self-service portal.

Why this is safe to run without breaking existing integrations: it
hashes the EXISTING plaintext value with the same SHA-256 used for
portal-generated keys (src/core/api_key.hash_api_key) and writes that
into api_key_hash. The key a client is already sending in
X-API-Key doesn't change -- only how we look it up server-side does.
After this runs, AutoCheckService._validate_api_key's hash-lookup
path finds these clients directly; the legacy plaintext fallback path
becomes dead code (kept for one release as a safety net, then safe to
delete along with the `api_key` column).

Safe to re-run: rows that already have api_key_hash populated, or
have no api_key at all, are skipped.

Usage:
    python -m scripts.migrate_legacy_api_keys            # apply
    python -m scripts.migrate_legacy_api_keys --dry-run   # preview only
"""

import sys

from src.core.api_key import hash_api_key, key_display_parts
from src.core.logging_config import get_logger, setup_logging
from src.db.session import SessionLocal
from src.models.administration.api_client import APIClient

logger = get_logger(__name__)


def migrate(dry_run: bool = False) -> None:
    db = SessionLocal()
    try:
        candidates = (
            db.query(APIClient)
            .filter(
                APIClient.api_key.isnot(None),
                APIClient.api_key_hash.is_(None),
            )
            .all()
        )

        if not candidates:
            logger.success("No legacy plaintext API keys found -- nothing to do.")
            return

        logger.warning(
            f"Found {len(candidates)} client(s) with a legacy plaintext "
            f"key: {', '.join(c.client_code for c in candidates)}"
        )

        for client in candidates:
            plain_key = client.api_key
            prefix, last_four = key_display_parts(plain_key)

            if dry_run:
                logger.warning(
                    f"[dry-run] Would migrate '{client.client_code}' "
                    f"({prefix}...{last_four})"
                )
                continue

            client.api_key_hash = hash_api_key(plain_key)
            client.api_key_prefix = prefix
            client.api_key_last_four = last_four
            # Plaintext column is no longer the source of truth once
            # api_key_hash is populated -- clear it so the fallback
            # lookup path in AutoCheckService._validate_api_key is
            # never exercised again for this client.
            client.api_key = None

            logger.success(
                f"Migrated '{client.client_code}' to hashed key lookup "
                f"({prefix}...{last_four})"
            )

        if not dry_run:
            db.commit()
            logger.success(f"Migration complete: {len(candidates)} client(s) updated.")
    except Exception:
        db.rollback()
        logger.exception("Migration failed; rolled back.")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    setup_logging()
    migrate(dry_run="--dry-run" in sys.argv)
