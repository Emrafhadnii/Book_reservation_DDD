from src.domain.entities.Users import User, Customer
from src.domain.entities.Reservations import Reservation
from src.adapters.repositories.GenericUOW import UnitOfWork
import json
from src.services_layer.dependencies.bus_dependency import messagebus
from datetime import datetime,timedelta


bus = messagebus

class Handlers:

    async def usercreated_handler(message: dict):
        async with UnitOfWork() as uow:
            user_data = json.loads(message["user"])
            user = User(**user_data)
            if await uow.customer.get_by_id(user.id) or user.user_role != "CUSTOMER":
                return
            customer = Customer(user=user)
            await uow.customer.add(customer=customer)
            
    async def bookisavailable_handler(message: dict):
        await bus.consume_queue("reservation_queue")

    async def userenqueued_handler(message: dict):
        async with UnitOfWork() as uow:
            base_price = 7000
            customer = await uow.customer.get_by_id(int(message['user_id']))
            book = await uow.book.get_by_id(message['book_id'])
            reservation_time = 0
            if book.units > 0:
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