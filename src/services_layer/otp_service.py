from random import randint
from redis.asyncio import Redis
from datetime import timedelta


async def otp_generator(user_identifier: str, redis: Redis):
    otp_code = str(randint(100000,999999))
    print(otp_code)
    redis.setex(
        name=f"otp:{user_identifier}",
        time=timedelta(seconds=120),
        value=otp_code)
    return otp_code


async def otp_validator(user_identifier: str, otp: str, redis: Redis):
    stored_otp = await redis.get(f"otp:{user_identifier}")
    if not stored_otp:
        return False
    return stored_otp == otp