from pydantic import BaseModel
from typing import Optional
from src.auth.domain.commands import LoginCommand

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class emailResponsemodel(LoginCommand):
    id: int
    user_role: str

