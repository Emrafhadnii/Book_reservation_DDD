from pydantic import BaseModel, Field
    
class All_Books(BaseModel):
    page: int = Field(1, ge=1)
    per_page: int = Field(5, ge=5)

class One_Book(BaseModel):
    book_id: int