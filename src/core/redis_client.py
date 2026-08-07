import redis

from src.config.settings import settings

_redis_client: redis.Redis | None = None


def get_redis_client() -> redis.Redis:
   

    global _redis_client

    if _redis_client is None:
        _redis_client = redis.Redis.from_url(
            settings.redis_url,
            decode_responses=True,
            socket_connect_timeout=1,
            socket_timeout=1,
        )

    return _redis_client