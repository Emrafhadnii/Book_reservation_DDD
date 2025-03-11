from fastapi import HTTPException
from src.reservations.services.reservation_queue import reservation_queue
from src.reservations.domain.commands import DeleteReservation
from src.reservations.domain.commands import CancelQueuedReservation

class ReservationCommandHandler:

    @staticmethod
    async def delete(command: DeleteReservation, repos):
        reservation_repo = repos.reservation
        await reservation_repo.delete(command.reservation_id)

    @staticmethod
    async def cancel_reservation(command: CancelQueuedReservation,
                                 token, repos):
        if (token['role'] == "ADMIN") or (command.user_id) == int(token['user_id']):
            try:
                customer = await repos.customer.get_by_id(command.user_id)
                message = {
                    "user_id":command.user_id,
                    "book_id":command.book_id,
                    "sub_model":customer.sub_model
                }
                if await reservation_queue.remove_user_from_queue(message):
                    return {
                        "messgae":"removed from queue"
                    }
                else:
                    return {
                        "messgae":"does not removed from queue"
                    }
            except Exception as e:
                raise HTTPException(408,detail="wtf")

        else:
            raise HTTPException(404, detail="Not authorized")