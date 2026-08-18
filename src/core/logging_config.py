"""Central logging configuration.

Design:
- Terminal (console): shows ONLY high-signal events -- SUCCESS and
  ERROR/CRITICAL. Nothing else touches stdout, so the terminal stays
  readable during normal operation.
- logs/app.log: everything (DEBUG and up), rotated, for full-detail
  troubleshooting and audits.
- logs/errors.log: ERROR and up only, rotated, so incidents can be
  triaged without wading through app.log.

Usage:
    from src.core.logging_config import get_logger
    logger = get_logger(__name__)

    logger.debug("low-level detail")      # file only
    logger.info("routine event")          # file only
    logger.warning("something odd")       # file only
    logger.success("user logged in")      # console + file
    logger.error("something failed")      # console + file
    logger.exception("failed")            # console + file, includes traceback
"""

from __future__ import annotations

import logging
import logging.config
import os
from pathlib import Path

# --- Custom SUCCESS level, between INFO (20) and WARNING (30) -----------
SUCCESS = 25
logging.addLevelName(SUCCESS, "SUCCESS")


def _success(self: logging.Logger, message, *args, **kwargs) -> None:
    if self.isEnabledFor(SUCCESS):
        kwargs.setdefault("stacklevel", 2)
        self._log(SUCCESS, message, args, **kwargs)


logging.Logger.success = _success  # type: ignore[attr-defined]


class ConsoleFilter(logging.Filter):
    """Console only ever sees SUCCESS, ERROR, and CRITICAL records.

    Applied as a filter (not a handler level) so it works regardless
    of which logger a record came from -- our own code, uvicorn,
    SQLAlchemy, etc. -- without needing to reconfigure every one of
    those loggers individually.
    """

    def filter(self, record: logging.LogRecord) -> bool:
        return record.levelno == SUCCESS or record.levelno >= logging.ERROR


def setup_logging(log_dir: str = "logs", log_level: str = "DEBUG") -> None:
    """Configure logging for the whole app. Call once, at process
    startup, before anything else logs."""

    Path(log_dir).mkdir(parents=True, exist_ok=True)

    config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "detailed": {
                "format": (
                    "%(asctime)s | %(levelname)-8s | %(name)s | "
                    "%(filename)s:%(lineno)d | %(message)s"
                ),
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
            "console": {
                "format": "%(asctime)s | %(levelname)-8s | %(message)s",
                "datefmt": "%H:%M:%S",
            },
        },
        "filters": {
            "console_only": {"()": f"{__name__}.ConsoleFilter"},
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "console",
                "filters": ["console_only"],
                "level": "DEBUG",
            },
            "app_file": {
                "class": "logging.handlers.RotatingFileHandler",
                "formatter": "detailed",
                "filename": os.path.join(log_dir, "app.log"),
                "maxBytes": 10 * 1024 * 1024,  # 10 MB
                "backupCount": 5,
                "level": "DEBUG",
                "encoding": "utf-8",
            },
            "error_file": {
                "class": "logging.handlers.RotatingFileHandler",
                "formatter": "detailed",
                "filename": os.path.join(log_dir, "errors.log"),
                "maxBytes": 10 * 1024 * 1024,
                "backupCount": 5,
                "level": "ERROR",
                "encoding": "utf-8",
            },
        },
        "root": {
            "handlers": ["console", "app_file", "error_file"],
            "level": log_level,
        },
        "loggers": {
            # Reset uvicorn's own handlers so its messages flow through
            # OUR handlers/filter instead of printing everything raw.
            "uvicorn": {"level": "INFO", "propagate": True, "handlers": []},
            "uvicorn.error": {"level": "INFO", "propagate": True, "handlers": []},
            # Access logs (every request line) are routine noise --
            # file only, never console, even though they're INFO.
            "uvicorn.access": {"level": "INFO", "propagate": True, "handlers": []},
            "sqlalchemy.engine": {"level": "WARNING", "propagate": True, "handlers": []},
        },
    }

    logging.config.dictConfig(config)


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)
