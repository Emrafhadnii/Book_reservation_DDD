from fastapi import APIRouter, Depends, HTTPException
from src.auth.domain.entities.auth import LoginRequest, Token, Verifyotp
from src.auth.services.JWT import JWTService
from src.auth.entrypoints.dependencies.userauth import get_uow
from src.adapters.UOW import UnitOfWork
from src.auth.entrypoints.dependencies.otp_dependency import get_redis
from redis.asyncio import Redis
from src.services_layer.bus_dependency import get_message_bus
from src.auth.services.otp_service import otp_generator, otp_validator
from uuid import uuid4
from src.users.domain.events import UserEvents
from src.services_layer.ratelimiter import login_ratelimiter


router = APIRouter(prefix='/login', tags=['login'])

@router.post("/")
@login_ratelimiter
async def login_route(form_data: LoginRequest, user_repo: UnitOfWork = Depends(get_uow), redis: Redis = Depends(get_redis)):    
    
    user_uow = user_repo.user
    user = await user_uow.get_by_phone(form_data.phone)

    if not user or (str(form_data.password) != str(user.password)):
        raise HTTPException(status_code=400,detail="Incorrect email or password")

    user_identifier = str(uuid4())
    await redis.setex(
        name=f"login_identifier:{user_identifier}",
        time=120,
        value=str(user.phone)
        )

    otp_code = await otp_generator(user.phone, redis)

    await redis.delete(f"login_{120}:{form_data.phone}")
    await redis.delete(f"login_{3600}:{form_data.phone}")
    
    return {
        "message": "otp sent",
        "user_identifier": user_identifier,
        "otp_code": otp_code
            }


@router.post("/refresh")
async def refresh_token(refresh_token: dict):
    
    payload = JWTService.decode_token(refresh_token['refresh_token'])
    new_access_token = JWTService.create_access_token({"sub": payload.get("sub"),
                                                    "phone": payload.get("phone"),"role":payload.get("role")})
    return {"access_token": new_access_token}


@router.post("/verify-otp/")
async def verify_otp(verifyotp: Verifyotp, redis: Redis = Depends(get_redis), 
                    uow: UnitOfWork = Depends(get_uow), bus = Depends(get_message_bus)):
    
    user_phone = await redis.get(f"login_identifier:{verifyotp.user_identifier}")
    if not user_phone:
        raise HTTPException(400, "identifier expired or invalid")

    if not await otp_validator(user_identifier=user_phone, otp=verifyotp.otp_code, redis=redis):
        raise HTTPException(400, "Invalid OTP")
    
    await uow.commit()

    user = await uow.user.get_by_phone_all(user_phone)

    await UserEvents.usercreated_event(bus,user.model_dump_json())
    

    return {
    "access_token": JWTService.create_access_token({
    "sub": str(user.id),"phone": user.phone,"role": user.user_role}),        
    "refresh_token": JWTService.create_refresh_token({
        "sub": str(user.id)}),"token_type": "bearer"
        }