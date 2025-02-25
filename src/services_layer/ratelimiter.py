from fastapi import HTTPException
from functools import wraps

class RateLimiter:
    def __init__(self, *limits: tuple[int, int]):
        self.limits = limits

    def __call__(self, endpoint):
        
        @wraps(endpoint)
        async def wrapped_endpoint(*args, **kwargs):
            form_data = kwargs.get('form_data')
            redis = kwargs.get('redis')
            phone = form_data.phone
            
            blocked = False
            max_ttl = 0
            
            for max_req, time in self.limits:
                key = f"login_{time}:{phone}"
                current = await redis.incr(key)
                
                if current == 1:
                    await redis.expire(key, time)
                
                if current > max_req:
                    ttl = await redis.ttl(key)
                    max_ttl = max(max_ttl, ttl)
                    blocked = True

            if blocked:
                raise HTTPException(429, detail=f"Try again in {max_ttl}s")
            
            return await endpoint(*args, **kwargs)
        
        return wrapped_endpoint


login_ratelimiter = RateLimiter((5,120),(10,3600))