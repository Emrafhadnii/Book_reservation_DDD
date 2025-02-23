from redis import Redis
from time import time
from src.auth.entrypoints.dependencies.otp_dependency import redis_dependency

class Reservation_queue:
    
    def __init__(self,redis: Redis):
        self.redis = redis
        self.QUEUE_NAME = "reservation_queue"

    async def add_user_to_queue(self, message: dict):
        user_id = message["user_id"]
        book_id = message["book_id"]
        sub_model = message["sub_model"]
        priority = 1 if sub_model == "Premium" else 2
        timestamp = int(time() * 1e6)
        final_score = priority + (timestamp / 1e10)
        key = f"{user_id}:{book_id}"
        await self.redis.zadd(self.QUEUE_NAME, {key: final_score})
    
    async def get_next_user(self,book_id):
        book_id_str = str(book_id)
        users = await self.redis.zrange(self.QUEUE_NAME, 0, -1, withscores=True)
        candidates = []
        for key, score in users:
            try:
                user_id_part, book_id_part = key.split(":")
                if int(book_id_part) == book_id:
                    candidates.append((key, score))
            except ValueError:
                continue

        if not candidates:
            return None
        
        next_user_key, _ = min(candidates, key=lambda x: x[1])
        await self.redis.zrem(self.QUEUE_NAME, next_user_key)
        user_id, book = next_user_key.split(':', 1)
        return {"user_id": user_id, "book_id": book}

    async def remove_user_from_queue(self,message: dict):
        user_id = message["user_id"]
        book_id = message["book_id"]

        key = f"{user_id}:{book_id}"
        result = await self.redis.zrem(self.QUEUE_NAME, key)
        if result:
            return True
        else:
            return False
        
reservation_queue = Reservation_queue(redis=redis_dependency.redis)