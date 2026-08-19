"""Lightweight security alerting.

Not a full alerting platform -- this fires a single notification when
the same event+identity crosses a threshold within a one-minute
window (same INCR+EXPIRE pattern as the rate limiters elsewhere in
this codebase), so a sustained attack produces one alert, not one per
rejected request. If ALERT_WEBHOOK_URL isn't configured, the
threshold crossing is still logged at ERROR (so it's visible in
logs/errors.log and on the console either way) -- the webhook is an
additional push notification on top of that, not a replacement.

Deliberately synchronous and best-effort: alert delivery must never
be the reason a request is slow or fails, so failures here are caught
and logged, never raised.
"""

from __future__ import annotations

import time

import redis
import requests

from src.config.settings import settings
from src.core.logging_config import get_logger
from src.core.redis_client import get_redis_client
from src.core.request_id import get_request_id

logger = get_logger(__name__)

_WEBHOOK_TIMEOUT_SECONDS = 2


def maybe_alert(event: str, identity: str, detail: dict | None = None) -> None:
    """Call at the point an alert-worthy event happens. Increments a
    per-event+identity counter; fires exactly once per minute-window
    the moment the count reaches the configured threshold."""

    window = int(time.time() // 60)
    key = f"alertcount:{event}:{identity}:{window}"

    try:
        client = get_redis_client()
        count = client.incr(key)
        if count == 1:
            client.expire(key, 60)
    except redis.exceptions.RedisError as exc:
        logger.warning(f"Alert threshold tracking unavailable (Redis down): {exc}")
        return

    if count != settings.alert_threshold_per_minute:
        # Below threshold: nothing yet. Above it: already alerted for
        # this window, don't repeat.
        return

    message = (
        f"Security alert: '{event}' from '{identity}' reached "
        f"{count}/min (request_id={get_request_id()})"
    )
    logger.error(message)

    if detail:
        logger.error(f"Alert detail: {detail}")

    if not settings.alert_webhook_url:
        return

    try:
        requests.post(
            settings.alert_webhook_url,
            json={"text": message, "event": event, "identity": identity, **(detail or {})},
            timeout=_WEBHOOK_TIMEOUT_SECONDS,
        )
    except requests.exceptions.RequestException as exc:
        logger.warning(f"Alert webhook delivery failed: {exc}")
