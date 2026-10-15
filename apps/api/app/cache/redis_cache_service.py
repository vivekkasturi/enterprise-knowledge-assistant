import json

from redis.exceptions import RedisError
from app.cache.cache_service import CacheService
from app.core.logging import get_logger

logger = get_logger(__name__)


class RedisCacheService(CacheService):
    def __init__(self, cache):
        self.cache = cache

    async def get(self, key):
        try:
            redis_value = await self.cache.get(key)
            if redis_value is not None:
                return json.loads(redis_value)
        except RedisError as e:
            logger.warning("Redis GET failed | error=%s | bypassing cache", e)
            return None
        except json.JSONDecodeError as e:
            logger.warning("Redis deserilation failed | error=%s | bypassing cache", e)
            return None

    async def set(self, key, value, timeout=None):
        logger.info(f"Setting value in Redis for key: {key} with timeout: {timeout}")
        try:
            serialized_value = json.dumps(value)
            return await self.cache.set(key, serialized_value, ex=timeout)
        except RedisError as e:
            logger.warning("Redis SET failed  | error=%s | continuing without cache", e)
            return None
        except (TypeError, ValueError) as e:
            logger.warning(
                "Redis serialization failed | error=%s | continuing without cache", e
            )
            return None

    async def delete(self, key):
        logger.info(f"Deleting key from Redis: {key}")
        try:
            return await self.cache.delete(key)
        except RedisError as e:
            logger.warning(
                "Redis DELETE failed | error=%s | continuing without cache", e
            )
            return None
