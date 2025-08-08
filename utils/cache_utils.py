import json 
from config.cache import redis_client 

async def cache_or_fetch(key: str, fetch_func, ttl=300, *args , **kwargs):
    cached = await redis_client.get(key)
    if cached:
        return json.loads(cached)
    result = await fetch_func(*args, **kwargs)
    await redis_client.setex(key, ttl , json.dumps(result))
    return result 