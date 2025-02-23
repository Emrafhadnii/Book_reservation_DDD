from src.adapters.dependencies.userauth import get_uow,get_current_user
from fastapi import APIRouter, Depends, Query, HTTPException
from src.adapters.repositories.GenericUOW import UnitOfWork
from src.domain.entities.Reservations import Reservation
from src.domain.entities.Reservations import cancel_queued_reservation
from fastapi import HTTPException
from src.adapters.dependencies.otp_dependency import get_redis
from redis import Redis
from src.services_layer.reservation_queue import remove_user_from_queue

router = APIRouter(prefix='/reservation', tags=['reservation'])

@router.get('/')
async def get_reservations(token = Depends(get_current_user), repos: UnitOfWork = Depends(get_uow),
                           page: int = Query(1,ge=1), per_page: int = Query(5,ge=5)):
    if (token['role'] == "ADMIN"):
        reservation_repo = repos.reservation
        reservations = await reservation_repo.get_all(page, per_page)
        return list(Reservation.model_validate(reservation) for reservation in reservations)
    else:
        raise HTTPException(404, detail="Not authorized")
    
@router.get('/{reservation_id}')
async def get_user(reservation_id: int, repos: UnitOfWork = Depends(get_uow), token = Depends(get_current_user)):
    reservation_repo = repos.reservation
    reservation = await reservation_repo.get_by_id(reservation_id)
    if (token["role"] == "ADMIN") or (reservation.customer.user.id == int(token["user_id"])):
        return dict(reservation)
    else:
        raise HTTPException(404, detail="Not authorized")
    
@router.delete('/{reservation_id}')
async def delete_user(reservation_id: int, repos: UnitOfWork = Depends(get_uow), token = Depends(get_current_user)):
    if (token["role"] == "ADMIN"):
        reservation_repo = repos.reservation
        await reservation_repo.delete(reservation_id)
    else:
        raise HTTPException(404, detail="Not authorized")

@router.put('/cancel-queue')
async def cancel(user_to_dequeue: cancel_queued_reservation, repos: UnitOfWork = Depends(get_uow),
                token = Depends(get_current_user), redis: Redis = Depends(get_redis)):

    if (token['role'] == "ADMIN") or (user_to_dequeue.user_id) == int(token['user_id']):
        try:
            customer = await repos.customer.get_by_id(user_to_dequeue.user_id)
            message = {
                "user_id":user_to_dequeue.user_id,
                "book_id":user_to_dequeue.book_id,
                "sub_model":customer.sub_model
            }
            if await remove_user_from_queue(message):
                return {
                    "messgae":"removed from queue"
                }
            else:
                return {
                    "messgae":"does not removed from queue"
                }
        except Exception as e:
            raise HTTPException(408,detail="wtf")
        
        pass
    else:
        raise HTTPException(404, detail="Not authorized")
