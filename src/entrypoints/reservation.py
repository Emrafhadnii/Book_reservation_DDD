from fastapi import APIRouter, Depends, HTTPException
from src.domain.entities.auth import LoginRequest, Token
from src.services_layer.JWT import JWTService
from src.adapters.repositories.BookRepo import SqlAlchemyBookRepository
from src.services_layer.dependencies.userauth import get_uow,get_current_user
from src.adapters.repositories.GenericUOW import UnitOfWork
from datetime import datetime, UTC, timedelta
from src.domain.entities.Users import User, Customer
from src.domain.entities.Books import Book
from src.domain.entities.Reservations import Reservation
from src.adapters.models_mappers.Usermapper import Usermapper
from src.adapters.models_mappers.Bookmapper import Bookmapper
from src.adapters.models_mappers.Customermapper import Customermapper
from src.adapters.models_mappers.Reservationmapper import Reservationmapper


router = APIRouter(prefix='/book',tags=['reservation'])

@router.post('/reserve/{book_id}')
async def reserve_book(book_id: int, repos:UnitOfWork = Depends(get_uow), token = Depends(get_current_user)):
    try:
        user_id = int(token["user_id"])
        book_repo = repos.book
        reservation_repo = repos.reservation
        customer_repo = repos.customer
        base_price = 7*1000

        book = await book_repo.get_by_id(book_id)
        customer = await customer_repo.get_by_id(user_id)
        reservation_time = 0

        if book.units > 0 and customer.wallet >= base_price and await customer_repo.check_subs(customer=customer):
            if customer.sub_model == "PLUS":    
                await customer_repo.add_to_wallet(customer.user.id,-base_price)
                reservation_time = 1
            if customer.sub_model == "PREMIUM" and customer.wallet >= 2*base_price:
                await customer_repo.add_to_wallet(customer.user.id, -2*base_price)
                reservation_time = 2

        reservation = Reservation(customer=customer,book=book,start_time=datetime.now(),end_time=datetime.now() + timedelta(reservation_time*7),price=reservation_time*7000)
        await reservation_repo.add(reservation=reservation)
        
        return {"message":"correct,reservation"}
    
    except Exception as e:
        raise HTTPException(400,detail=[str(e)])
