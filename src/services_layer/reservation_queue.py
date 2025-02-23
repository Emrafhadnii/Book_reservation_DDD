from redis import Redis
from time import time
from src.adapters.dependencies.otp_dependency import redis_dependency

QUEUE_NAME = "reservation_queue"

async def add_user_to_queue(message: dict):
    
    user_id = message["user_id"]
    book_id = message["book_id"]
    sub_model = message["sub_model"]
    priority = 1 if sub_model == "Premium" else 2
    timestamp = int(time() * 1e6)
    final_score = priority + (timestamp / 1e10)
    key = f"{user_id}:{book_id}"
    await redis_dependency.redis.zadd(QUEUE_NAME, {key: final_score})
    
async def get_next_user(book_id):
    book_id_str = str(book_id)
    users = await redis_dependency.redis.zrange(QUEUE_NAME, 0, -1, withscores=True)
    candidates = []
    for key, score in users:
        try:
            user_id_part, book_id_part = key.split(":")
            print(book_id)
            if int(book_id_part) == book_id:
                candidates.append((key, score))
        except ValueError:
            continue

    if not candidates:
        return None
    
    next_user_key, _ = min(candidates, key=lambda x: x[1])
    await redis_dependency.redis.zrem(QUEUE_NAME, next_user_key)
    user_id, book = next_user_key.split(':', 1)
    
    return {"user_id": user_id, "book_id": book}
    
async def remove_user_from_queue(message: dict):
    user_id = message["user_id"]
    book_id = message["book_id"]

    key = f"{user_id}:{book_id}"
    result = await redis_dependency.redis.zrem(QUEUE_NAME, key)
    if result:
        return True
    else:
        return False

        