# from fastapi_cache import FastAPICache
# from fastapi_cache.backends.redis import RedisBackend
# import redis.asyncio as redis


# redis_client=redis.Redis(
#         host="redis",
#         port=6379,
#         db=2,
#         decode_responses=True
#     )
# async def init_cache():
    
#     FastAPICache.init(RedisBackend(redis_client),prefix="fastapi-cache")

#for cloud
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
import redis.asyncio as redis
import os

REDIS_URL = os.getenv("REDIS_URL") 

redis_client = redis.from_url(REDIS_URL, decode_responses=True)

async def init_cache():
    FastAPICache.init(RedisBackend(redis_client), prefix="fastapi-cache")
