from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from src.services_layer.JWT import JWTService
# from src.services_layer.RepositoriesUOW import UserUoW,BookUoW,CustomerUoW,ReservationUoW,AuthorUoW
from src.adapters.repositories.GenericUOW import UnitOfWork
from sqlalchemy.ext.asyncio import AsyncSession
from src.adapters.repositories.UserRepository import SqlAlchemyUserRepository

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login/")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    return JWTService.get_current_user(token)

async def get_uow():
    async with UnitOfWork() as uow:
        yield uow


# async def get_user_repo():
#     async with UserUoW() as uow:
#         yield uow
# async def get_book_repo():
#     async with BookUoW() as uow:
#         yield uow
# async def get_customer_repo():
#     async with CustomerUoW() as uow:
#         yield uow
# async def get_reservation_repo():
#     async with ReservationUoW() as uow:
#         yield uow
# async def get_author_repo():
#     async with AuthorUoW() as uow:
#         yield uow