from pydantic import BaseModel
from typing import Optional

class LoginCommand(BaseModel):
    phone: str
    password: str

class VerifyCommand(BaseModel):
    otp_code: str
    user_identifier: str

class SignUpCommand(BaseModel):
    username: str
    first_name: str
    last_name: str
    phone: str
    user_password: str
    email: Optional[str] = None
    user_role: str = "CUSTOMER"
    sub_model: str = "FREE"