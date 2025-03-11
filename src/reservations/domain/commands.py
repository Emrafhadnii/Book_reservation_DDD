from pydantic import BaseModel

class DeleteReservation(BaseModel):
    reservation_id: int

class CancelQueuedReservation(BaseModel):
    user_id: int 
    book_id: int