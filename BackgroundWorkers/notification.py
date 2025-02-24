import asyncio
from datetime import datetime, timedelta
from src.adapters.UOW import UnitOfWork

async def send_notification():
    while True:
        async with UnitOfWork() as uow:
            reservation_repo = uow.reservation
            reservations = await reservation_repo.get_all(1,10)
            for item in reservations:
                if (item.end_time - datetime.now()) <= timedelta(days=1):
                    print(f"Notification: Reservation is ending in 1 day.")
        await asyncio.sleep(7200)