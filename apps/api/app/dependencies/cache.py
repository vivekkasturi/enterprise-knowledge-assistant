from app.cache.cache_service import CacheService
from app.cache.redis_client import redis_client
from app.cache.redis_cache_service import RedisCacheService


def get_cache_service() -> CacheService:
    return RedisCacheService(redis_client)