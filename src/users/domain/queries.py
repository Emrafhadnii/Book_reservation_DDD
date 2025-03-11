from pydantic import BaseModel, Field

class AllCustomers(BaseModel):
    page: int = Field(1, ge=1)
    per_page: int = Field(5, ge=5)

class OneCustomer(BaseModel):
    customer_id: int