from fastapi import HTTPException
from src.reservations.domain.commands import DeleteReservation
from src.reservations.domain.commands import CancelQueuedReservation
from src.reservations.domain.entities.Reservations import Reservation
from src.books.domain.events import BookEvents
from asyncio.locks import Lock
from src.books.domain.queries import One_Book
from datetime import datetime, timedelta
from src.reservations.domain.events import ReservationEvents
from src.adapters.UOW import UnitOfWork


lock = Lock()

class ReservationCommandHandler:

    @staticmethod
    async def delete(command: DeleteReservation, repos: UnitOfWork):
        reservation_repo = repos.reservation
        await reservation_repo.delete(command.reservation_id)

    @staticmethod
    async def cancel_reservation(command: CancelQueuedReservation,
                                 token, repos: UnitOfWork):
        if (token['role'] == "ADMIN") or (command.user_id) == int(token['user_id']):
            try:
                customer = await repos.customer.get_by_id(command.user_id)
                message = {
                    "user_id":command.user_id,
                    "book_id":command.book_id,
                    "sub_model":customer.sub_model
                }
                
                await repos.queue.delete(message)
                return {
                    "message": "user removed from queue successfully"
                }
            except Exception as e:
                raise HTTPException(408,detail="wtf")

        else:
            raise HTTPException(404, detail="Not authorized")
    
    @staticmethod
    async def reserve(command: One_Book, repos: UnitOfWork, bus, token):
        try:
            user_id = int(token["user_id"])
            book_repo = repos.book
            reservation_repo = repos.reservation
            customer_repo = repos.customer
            base_price = 7*1000

            book = await book_repo.get_by_id(command.book_id)
            customer = await customer_repo.get_by_id(user_id)
            reservation_time = 0
            if book.units > 0:
                async with lock:
                    if customer.wallet >= base_price and await customer_repo.check_subs(customer=customer):
                        if customer.sub_model == "PLUS":    
                            await customer_repo.add_to_wallet(customer.user.id,-base_price)
                            reservation_time = 1
                        if customer.sub_model == "PREMIUM" and customer.wallet >= 2*base_price:
                            await customer_repo.add_to_wallet(customer.user.id, -2*base_price)
                            reservation_time = 2
                    if reservation_time > 0:
                        await book_repo.stock_update(command.book_id,-1)
                    
                    reservation = Reservation(customer=customer,book=book,
                                              start_time=datetime.now(),
                                              end_time=datetime.now() + timedelta(reservation_time*7),
                                              price=reservation_time*7000)
                    
                    await reservation_repo.add(reservation=reservation)
                
                event_message = {
                    "aggregate_id": command.book_id,
                    "event_type": "updated"
                }
                
                await BookEvents.booktablechanged_event(bus,event_message)
           
                return {"message":"correct,reservation"}
            else:
                message = {
                    "user_id": user_id,
                    "book_id": command.book_id,
                    "sub_model": customer.sub_model
                }
                await ReservationEvents.queue_event(bus=bus,
                                                    message=message)
                return {
                    "messgae":"The book is not available but you have been added to the reservation queue"
                }
        except Exception as e:
            raise HTTPException(400,detail=[str(e)])
        
    @staticmethod 
    async def return_book(command: DeleteReservation, repos: UnitOfWork, bus):
        reservation = repos.reservation
        customer = repos.customer
        book = repos.book
        reserved_book = await reservation.get_by_id(command.reservation_id)
        if reserved_book:
            time_difference = reserved_book.end_time - datetime.now() 
            new_price = reserved_book.price - (time_difference.days * 1000)
            reserved_book_count = reserved_book.book.units
            reserved_book_id = reserved_book.book.id
            await customer.add_to_wallet(reserved_book.customer.user.id,new_price)        
            await book.stock_update(reserved_book.book.id,1)        
            await reservation.delete(command.reservation_id)
        
        event_message = {
                    "aggregate_id": reserved_book_id,
                    "event_type": "updated"
                }
        await BookEvents.booktablechanged_event(bus,event_message)

        if reserved_book_count == 0:
            await BookEvents.bookisavailable_event(bus=bus,book_id=reserved_book_id)

        return {
            "messgae":"book returned correctly"
            }