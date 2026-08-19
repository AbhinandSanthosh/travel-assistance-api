"""Purge operational log records older than the configured retention
window.

Scope, deliberately: this purges api_request_logs and
rule_execution_logs by default -- high-volume, purely operational,
no regulatory hold on them. It does NOT touch compliance_checks
(the actual compliance decision record) or audit_logs (the admin
action trail) unless explicitly asked to, via --include-compliance-
checks / --include-audit-logs -- those are the two tables an
enterprise client or regulator would actually expect you to be able
to produce, and "how long" is a legal/contractual answer this script
shouldn't guess at by running silently in a cron job.

Retention windows come from settings (API_REQUEST_LOG_RETENTION_DAYS
etc. in .env) -- a *_retention_days of 0 means "keep indefinitely,"
and that table is skipped even if its --include flag is passed.

Usage:
    python -m scripts.purge_old_records                       # operational logs only
    python -m scripts.purge_old_records --dry-run              # preview only
    python -m scripts.purge_old_records --include-compliance-checks --include-audit-logs
"""

from __future__ import annotations

import sys
from datetime import UTC, datetime, timedelta

from src.config.settings import settings
from src.core.logging_config import get_logger, setup_logging
from src.db.session import SessionLocal
from src.models.administration.api_request_log import APIRequestLog
from src.models.administration.audit_log import AuditLog
from src.models.compliance.compliance_check import ComplianceCheck
from src.models.compliance.rule_execution_log import RuleExecutionLog

logger = get_logger(__name__)


def _purge_table(db, model, retention_days: int, dry_run: bool) -> int:
    if retention_days <= 0:
        logger.warning(
            f"Skipping {model.__tablename__}: retention_days=0 "
            f"(keep indefinitely)"
        )
        return 0

    cutoff = datetime.now(UTC) - timedelta(days=retention_days)
    query = db.query(model).filter(model.created_at < cutoff)
    count = query.count()

    if count == 0:
        logger.success(f"{model.__tablename__}: nothing older than {retention_days}d")
        return 0

    if dry_run:
        logger.warning(
            f"[dry-run] Would delete {count} row(s) from "
            f"{model.__tablename__} older than {retention_days}d "
            f"(cutoff {cutoff.isoformat()})"
        )
        return count

    deleted = query.delete(synchronize_session=False)
    logger.success(
        f"{model.__tablename__}: deleted {deleted} row(s) older than "
        f"{retention_days}d (cutoff {cutoff.isoformat()})"
    )
    return deleted


def purge(
    dry_run: bool = False,
    include_compliance_checks: bool = False,
    include_audit_logs: bool = False,
) -> None:
    db = SessionLocal()
    try:
        total = 0
        total += _purge_table(
            db, APIRequestLog, settings.api_request_log_retention_days, dry_run
        )
        total += _purge_table(
            db, RuleExecutionLog, settings.rule_execution_log_retention_days, dry_run
        )

        if include_compliance_checks:
            total += _purge_table(
                db,
                ComplianceCheck,
                settings.compliance_check_retention_days,
                dry_run,
            )
        if include_audit_logs:
            total += _purge_table(
                db, AuditLog, settings.audit_log_retention_days, dry_run
            )

        if not dry_run:
            db.commit()

        logger.success(f"Purge complete. {total} row(s) {'would be ' if dry_run else ''}deleted.")
    except Exception:
        db.rollback()
        logger.exception("Purge failed; rolled back.")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    setup_logging()
    purge(
        dry_run="--dry-run" in sys.argv,
        include_compliance_checks="--include-compliance-checks" in sys.argv,
        include_audit_logs="--include-audit-logs" in sys.argv,
    )
