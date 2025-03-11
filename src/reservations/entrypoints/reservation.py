from fastapi import APIRouter, Depends, HTTPException
from src.auth.entrypoints.dependencies.userauth import get_uow,get_current_user
from src.services_layer.bus_dependency import get_message_bus
from src.adapters.UOW import UnitOfWork
from redis import Redis
from src.auth.entrypoints.dependencies.otp_dependency import get_redis
from src.books.domain.queries import One_Book
from src.reservations.adapters.command_handler import ReservationCommandHandler
from src.reservations.domain.commands import DeleteReservation

router = APIRouter(prefix='/book',tags=['reservation'])

@router.post('/reserve/{book_id}')
async def reserve_book(book_id: int, repos:UnitOfWork = Depends(get_uow),
                        token = Depends(get_current_user),
                        bus = Depends(get_message_bus), 
                        redis: Redis = Depends(get_redis)):
    
    commnad = One_Book(book_id=book_id)
    return await ReservationCommandHandler.reserve(command=commnad, repos=repos,
                                                   bus=bus, token=token)

@router.post('/return/{reservation_id}')
async def return_book(reservation_id: int, 
                      repos: UnitOfWork = Depends(get_uow), 
                      token = Depends(get_current_user),
                      bus = Depends(get_message_bus)):
    
    command = DeleteReservation(reservation_id=reservation_id)
    return await ReservationCommandHandler.return_book(command=command,
                                                       repos=repos, bus=bus)