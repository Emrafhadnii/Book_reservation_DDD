from fastapi import APIRouter, Depends, HTTPException
from src.domain.entities.auth import LoginRequest, Token, Verifyotp
from src.services_layer.JWT import JWTService
from src.adapters.repositories.UserRepository import SqlAlchemyUserRepository
from src.services_layer.dependencies.userauth import get_uow
from src.adapters.repositories.GenericUOW import UnitOfWork
from src.services_layer.dependencies.otp_dependency import get_redis
from redis.asyncio import Redis
from src.services_layer.otp_service import otp_generator, otp_validator
from uuid import uuid4


router = APIRouter(prefix='/login', tags=['login'])

@router.post("/")
async def login_route(form_data: LoginRequest, user_repo: UnitOfWork = Depends(get_uow), redis: Redis = Depends(get_redis)):    
    
    user_uow = user_repo.user
    user = await user_uow.get_by_phone(form_data.phone)

    if not user or (str(form_data.password) != str(user.password)):
        raise HTTPException(status_code=400,detail="Incorrect email or password")

    user_identifier = str(uuid4())
    await redis.setex(
        name=f"login_identifier:{user_identifier}",
        time=120,
        value=str(user.id)
        )

    await otp_generator(user.id, redis)

    return {
        "message": "otp sent",
        "identifier": user_identifier
            }
    # return {
    #     "access_token": JWTService.create_access_token({
    #     "sub": str(user.id),"phone": user.phone,"role": user.user_role}),        
    #     "refresh_token": JWTService.create_refresh_token({
    #         "sub": str(user.id)}),"token_type": "bearer"
    #         }


@router.post("/refresh")
async def refresh_token(refresh_token: str):
    payload = JWTService.decode_token(refresh_token)
    new_access_token = JWTService.create_access_token({"sub": payload.get("sub")})
    return {"access_token": new_access_token}


@router.post("/verify-otp/")
async def verify_otp(verifyotp: Verifyotp, redis: Redis = Depends(get_redis), uow: UnitOfWork = Depends(get_uow)):
    
    user_id = await redis.get(f"login_identifier:{verifyotp.user_identifier}")
    if not user_id:
        raise HTTPException(400, "identifier expired or invalid")

    print(user_id)
    print(verifyotp.user_identifier)
    print(verifyotp.otp_code)

    if not await otp_validator(user_identifier=user_id, otp=verifyotp.otp_code, redis=redis):
        raise HTTPException(400, "Invalid OTP")
    
    user = await uow.user.get_by_id(int(user_id))

    return {
    "access_token": JWTService.create_access_token({
    "sub": str(user.id),"phone": user.phone,"role": user.user_role}),        
    "refresh_token": JWTService.create_refresh_token({
        "sub": str(user.id)}),"token_type": "bearer"
        }