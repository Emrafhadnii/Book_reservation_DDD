from pydantic import BaseModel
from src.domain.enums import UserRole

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class LoginRequest(BaseModel):
    phone: str
    password: str

class emailResponsemodel(LoginRequest):
    id: int
    user_role: str

class Verifyotp(BaseModel):
    otp_code: str
    user_identifier: str
