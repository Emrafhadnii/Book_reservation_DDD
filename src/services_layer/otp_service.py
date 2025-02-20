from random import randint
from redis.asyncio import Redis
from datetime import timedelta
from time import time

class SMSIR:
    def is_accessible():
        access = randint(1,200000)
        return True if access%2 == 0 else False

class KaveNegar:
    def is_accessible():
        access = randint(1,200000)
        return False if access%2 == 0 else True

class CircuitBreaker:
    def __init__(self,break_time: timedelta = timedelta(seconds=100)):
        self.break_time = break_time.seconds
        self.failure = {
            "kavenegar":0,
            "smsir":0
        }

    def request(self):
        if SMSIR.is_accessible() and (time() - self.failure['smsir']) > self.break_time:
            return [randint(100000,999999),"smsir"]
        elif KaveNegar.is_accessible() and (time() - self.failure['kavenegar']) > self.break_time:
            self.failure['smsir'] = time()
            return [randint(100000,999999),"kavenegar"]
        else:
            self.failure['kavenegar'] = time()
            self.failure['smsir'] = time()
            return [randint(100000,999999),"ha?"]
        

async def otp_generator(user_identifier: str, redis: Redis):
    circ = CircuitBreaker(timedelta(seconds=1))
    otp_generated = circ.request()
    otp_code = str(otp_generated[0])
    print(otp_generated[1])
    await redis.setex(
        name=f"otp:{user_identifier}",
        time=timedelta(seconds=120),
        value=otp_code)
    return otp_code


async def otp_validator(user_identifier: str, otp: str, redis: Redis):
    stored_otp = await redis.get(f"otp:{user_identifier}")
    if not stored_otp:
        return False
    return stored_otp == otp