from pydantic import BaseModel, Field

class AllReservations(BaseModel):
    page: int = Field(1, ge=1)
    per_page: int = Field(5, ge=5)

class OneReservation(BaseModel):
    reservation_id: int