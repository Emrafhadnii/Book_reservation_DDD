from src.reservations.domain.entities.Reservations import Reservation
from src.adapters.UOW import UnitOfWork
from datetime import datetime,timedelta
from src.reservations.services.reservation_queue import reservation_queue
from time import sleep
from asyncio.locks import Lock

lock = Lock()

class BookHandler:
    
    async def bookisavailable_handler(message: dict):
        sleep(2)
        user = await reservation_queue.get_next_user(int(message['book_id']))
        book_id = int(message['book_id'])
        user_id = int(user['user_id'])
        async with UnitOfWork() as uow:
            base_price = 7000
            customer = await uow.customer.get_by_id(user_id)
            book = await uow.book.get_by_id(book_id)
            reservation_time = 0
            if book.units > 0:
                async with lock:
                    if customer.wallet >= base_price and await uow.customer.check_subs(customer=customer):
                        if customer.sub_model == "PLUS":    
                            await uow.customer.add_to_wallet(customer.user.id,-base_price)
                            reservation_time = 1
                        if customer.sub_model == "PREMIUM" and customer.wallet >= 2*base_price:
                            await uow.customer.add_to_wallet(customer.user.id, -2*base_price)
                            reservation_time = 2
                    if reservation_time > 0:
                        await uow.book.stock_update(book.id,-1)
                    reservation = Reservation(customer=customer,book=book,start_time=datetime.now(),end_time=datetime.now() + timedelta(reservation_time*7),price=reservation_time*7000)
                    await uow.reservation.add(reservation=reservation)
    
    async def booktablechanged_event(message: dict):
        async with UnitOfWork() as uow:
            await uow.outbox.add(event=message)