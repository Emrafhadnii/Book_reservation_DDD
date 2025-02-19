from fastapi import APIRouter, Depends, Query, HTTPException
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


router = APIRouter(prefix='/book',tags=['book'])

@router.get("/")
async def get_books(repos: UnitOfWork = Depends(get_uow), token = Depends(get_current_user),
                    page: int = Query(1,ge=1), per_page: int = Query(5,ge=5)):
    book_repo = repos.book
    books = await book_repo.get_all(page,per_page)
    return list(Book.model_validate(book) for book in books)

@router.get('/{book_id}')
async def get_book(book_id, repos: UnitOfWork = Depends(get_uow), token = Depends(get_current_user)):
    book_repo = repos.book
    book = await book_repo.get_by_id(book_id)
    return dict(book)
