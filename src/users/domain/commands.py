from pydantic import BaseModel, field_validator

class ChargeCommand(BaseModel):
    id: int
    amount: int

    @field_validator('amount')
    def wallet_check(cls, value):
        if value < 0:
            raise ValueError('charge amount cannot be negative')
        return value

class PurchaseCommand(BaseModel):
    id: int
    sub_model: str

    @field_validator('sub_model')
    def wallet_check(cls, value):
        if value not in ("PLUS","PREMIUM"):
            raise ValueError('sub_model is invalid')
        return value
    
class UserDeleteCommand(BaseModel):
    user_id: int