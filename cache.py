import redis
import json
from config import get_settings

settings = get_settings()

# Redis connection
redis_client = redis.from_url(settings.REDIS_URL, decode_responses=True)

def set_cache(key: str, value: dict, expire_seconds: int = 3600):
    """Store data in Redis"""
    redis_client.setex(key, expire_seconds, json.dumps(value))

def get_cache(key: str):
    """Retrieve data from Redis"""
    data = redis_client.get(key)
    return json.loads(data) if data else None

def delete_cache(key: str):
    """Delete cache entry"""
    redis_client.delete(key)

def clear_user_cache(user_id: int):
    """Clear all cache for a user (logout)"""
    pattern = f"user:{user_id}:*"
    for key in redis_client.scan_iter(match=pattern):
        redis_client.delete(key)