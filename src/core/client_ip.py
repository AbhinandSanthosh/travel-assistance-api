from fastapi import Request

from src.config.settings import settings


def get_client_ip(request: Request) -> str:
    """Resolve the real client IP for rate limiting / IP whitelisting.

    X-Forwarded-For is only honored when the direct connecting peer is
    a configured trusted proxy (settings.trusted_proxy_ips) -- otherwise
    it's just a header anyone can set themselves to spoof past IP
    whitelisting and rate limits. With no trusted proxies configured
    (the default), this always returns the direct socket address.
    """

    direct_ip = request.client.host if request.client else "unknown"

    if direct_ip in settings.trusted_proxy_ip_list:
        forwarded = request.headers.get("x-forwarded-for")
        if forwarded:
            return forwarded.split(",")[0].strip()

    return direct_ip
