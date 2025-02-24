from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from src.auth.services.JWT import JWTService
from src.adapters.UOW import UnitOfWork

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login/")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    return JWTService.get_current_user(token)

async def get_uow():
    async with UnitOfWork() as uow:
        yield uow