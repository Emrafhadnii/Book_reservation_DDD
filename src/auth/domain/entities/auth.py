from pydantic import BaseModel
from typing import Optional

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


class signup_model(BaseModel):
    username: str
    first_name: str
    last_name: str
    phone: str
    user_password: str
    email: Optional[str] = None
    user_role: str = "CUSTOMER"
    sub_model: str = "FREE"

