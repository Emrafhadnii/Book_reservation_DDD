from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from src.domain.entities.auth import LoginRequest, Token
from src.services_layer.JWT import JWTService
from src.adapters.repositories.UserRepository import SqlAlchemyUserRepository
from src.services_layer.dependencies.userauth import get_uow,get_current_user
from src.adapters.repositories.GenericUOW import UnitOfWork

router = APIRouter(prefix='/book', tags = ['book'])


@router.get('/{id}')
async def readbook(id:int,token = Depends(get_current_user) , user_repo: UnitOfWork = Depends(get_uow)):
    
    user_uow = user_repo.user
    
    if token:
        user = await user_uow.get_by_id(id)
    return user