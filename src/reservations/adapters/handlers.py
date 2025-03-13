from src.adapters.UOW import UnitOfWork
from asyncio.locks import Lock

lock = Lock()

class ReservationHandler:

    async def queue_event_handler(message: dict):
        async with UnitOfWork() as uow:
            await uow.queue.add(message)        