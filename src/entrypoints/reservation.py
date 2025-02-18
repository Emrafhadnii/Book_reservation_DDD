from fastapi import APIRouter, Depends, HTTPException
from src.domain.entities.auth import LoginRequest, Token
from src.services_layer.JWT import JWTService
from src.adapters.repositories.BookRepo import SqlAlchemyBookRepository
from src.services_layer.dependencies.userauth import get_uow,get_current_user
from src.services_layer.dependencies.bus_dependency import get_message_bus
from src.adapters.repositories.GenericUOW import UnitOfWork
from datetime import datetime, UTC, timedelta
from src.domain.entities.Users import User, Customer
from src.domain.entities.Books import Book
from src.domain.entities.Reservations import Reservation
from src.adapters.models_mappers.Usermapper import Usermapper
from src.adapters.models_mappers.Bookmapper import Bookmapper
from src.adapters.models_mappers.Customermapper import Customermapper
from src.adapters.models_mappers.Reservationmapper import Reservationmapper
from src.domain.events import Events


router = APIRouter(prefix='/book',tags=['reservation'])

@router.post('/reserve/{book_id}')
async def reserve_book(book_id: int, repos:UnitOfWork = Depends(get_uow),
                        token = Depends(get_current_user), bus = Depends(get_message_bus)):
    try:
        user_id = int(token["user_id"])
        book_repo = repos.book
        reservation_repo = repos.reservation
        customer_repo = repos.customer
        base_price = 7*1000

        book = await book_repo.get_by_id(book_id)
        customer = await customer_repo.get_by_id(user_id)
        reservation_time = 0

        if book.units > 0:
            if customer.wallet >= base_price and await customer_repo.check_subs(customer=customer):
                if customer.sub_model == "PLUS":    
                    await customer_repo.add_to_wallet(customer.user.id,-base_price)
                    reservation_time = 1
                if customer.sub_model == "PREMIUM" and customer.wallet >= 2*base_price:
                    await customer_repo.add_to_wallet(customer.user.id, -2*base_price)
                    reservation_time = 2

            if reservation_time > 0:
                await book_repo.stock_update(book_id,-1)
            reservation = Reservation(customer=customer,book=book,start_time=datetime.now(),end_time=datetime.now() + timedelta(reservation_time*7),price=reservation_time*7000)
            await reservation_repo.add(reservation=reservation)

            return {"message":"correct,reservation"}
        else:
            message = {
                "user_id": user_id,
                "book_id": book_id,
                "sub_model": customer.sub_model
            }
            await Events.userenqueued_event(bus=bus,message=message)

            pass       
    except Exception as e:
        raise HTTPException(400,detail=[str(e)])



@router.post('/return/{reservation_id}')
async def return_book(reservation_id: int, repos: UnitOfWork = Depends(get_uow), token = Depends(get_current_user),
                       bus = Depends(get_message_bus)):
    reservation = repos.reservation
    customer = repos.customer
    book = repos.book
    reserved_book = await reservation.get_by_id(reservation_id)
    if reserved_book:
        time_difference = reserved_book.end_time - datetime.now() 
        new_price = reserved_book.price - (time_difference.days * 1000)
        reserved_book_count = reserved_book.book.units
        reserved_book_id = reserved_book.id
        await customer.add_to_wallet(reserved_book.customer.user.id,new_price)        
        await book.stock_update(reserved_book.book.id,1)        
        await reservation.delete(reservation_id)
    if reserved_book_count == 0:
        await Events.bookisavailable_event(bus=bus,book_id=reserved_book_id)

    else:
        raise HTTPException(404,detail=['reservation not found'])
    

    
