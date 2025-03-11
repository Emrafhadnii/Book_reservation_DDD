from src.auth.entrypoints.dependencies.userauth import get_uow,get_current_user
from fastapi import APIRouter, Depends, Query, HTTPException
from src.adapters.UOW import UnitOfWork
from src.auth.entrypoints.dependencies.otp_dependency import get_redis
from redis import Redis
from src.services_layer.permission import admin_permission
from src.reservations.adapters.query_handlers import ReservationQueryHandler
from src.reservations.domain.queries import AllReservations, OneReservation
from src.reservations.domain.commands import DeleteReservation,CancelQueuedReservation
from src.reservations.adapters.command_handler import ReservationCommandHandler

router = APIRouter(prefix='/reservation', tags=['reservation'])

@router.get('/')
@admin_permission
async def get_reservations(token = Depends(get_current_user), repos: UnitOfWork = Depends(get_uow),
                           query: AllReservations = Depends(), redis: Redis = Depends(get_redis)):
    
    return await ReservationQueryHandler.get_all(query=query,
                                                repos=repos, redis=redis)
    
@router.get('/{reservation_id}')
async def get_user(reservation_id: int, repos: UnitOfWork = Depends(get_uow), 
                   token = Depends(get_current_user), redis: Redis = Depends(get_redis)):
    
    query = OneReservation(reservation_id=reservation_id)
    return await ReservationQueryHandler.get_one(query=query, repos=repos,
                                                token=token, redis=redis)
    
@router.delete('/{reservation_id}')
@admin_permission
async def delete_user(reservation_id: int, 
                    repos: UnitOfWork = Depends(get_uow), 
                    token = Depends(get_current_user)):
    
    command = DeleteReservation(reservation_id=reservation_id)
    return await ReservationCommandHandler.delete(command=command,
                                                  repos=repos)

@router.put('/cancel-queue')
async def cancel(command: CancelQueuedReservation, repos: UnitOfWork = Depends(get_uow),
                token = Depends(get_current_user), redis: Redis = Depends(get_redis)):

    return await ReservationCommandHandler.cancel_reservation(command=command,
                                                            token=token, repos=repos)