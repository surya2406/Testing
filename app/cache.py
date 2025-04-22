from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
import redis.asyncio as redis


redis_client=redis.Redis(
        host="redis",
        port=6379,
        db=2,
        decode_responses=True
    )
async def init_cache():
    
    FastAPICache.init(RedisBackend(redis_client),prefix="fastapi-cache")