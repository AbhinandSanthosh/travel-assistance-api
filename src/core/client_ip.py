from fastapi import Request

from src.config.settings import settings


def get_client_ip(request: Request) -> str:

    direct_ip = request.client.host if request.client else "unknown"

    if direct_ip in settings.trusted_proxy_ip_list:
        forwarded = request.headers.get("x-forwarded-for")
        if forwarded:
            return forwarded.split(",")[0].strip()

    return direct_ip