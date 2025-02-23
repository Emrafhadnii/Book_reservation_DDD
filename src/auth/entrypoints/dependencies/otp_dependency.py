from redis.asyncio import Redis
from src.config.setting import settings

class RedisDependency:
    def __init__(self):
        self.redis = None
    
    async def connect(self):
        self.redis = Redis(port=settings.REIDIS_PORT,host=settings.REIDIS_HOST,db=0,
                        password=None,decode_responses=True
                        )   
        
    async def disconnect(self):
        await self.redis.close()

redis_dependency = RedisDependency()

def get_redis() -> Redis:
    return redis_dependency.redis