from fastapi import APIRouter, Depends, HTTPException
from src.domain.entities.auth import LoginRequest, Token
from src.services_layer.JWT import JWTService
from src.adapters.repositories.UserRepository import SqlAlchemyUserRepository
from src.services_layer.dependencies.userauth import get_uow
from src.adapters.repositories.GenericUOW import UnitOfWork
from random import randint
import redis


router = APIRouter(prefix='/login', tags=['login'])

@router.post("/", response_model=Token)
async def login_route(form_data: LoginRequest, user_repo: UnitOfWork = Depends(get_uow)):    
    
    user_uow = user_repo.user
    user = await user_uow.get_by_phone(form_data.phone)

    if not user or (str(form_data.password) != str(user.password)):
        raise HTTPException(status_code=400,detail="Incorrect email or password")

    return {
        "access_token": JWTService.create_access_token({
        "sub": str(user.id),"phone": user.phone,"role": user.user_role}),        
        "refresh_token": JWTService.create_refresh_token({
            "sub": str(user.id)}),"token_type": "bearer"
            }


@router.post("/refresh")
async def refresh_token(refresh_token: str):
    payload = JWTService.decode_token(refresh_token)
    new_access_token = JWTService.create_access_token({"sub": payload.get("sub")})
    return {"access_token": new_access_token}


@router.post("/otp")
async def send_opt():
    print(randint(100000,999999))
    pass
    

