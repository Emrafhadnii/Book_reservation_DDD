from fastapi import APIRouter, Depends, HTTPException
from src.domain.entities.auth import LoginRequest, Token, Verifyotp
from src.services_layer.JWT import JWTService
from src.services_layer.dependencies.userauth import get_uow
from src.adapters.repositories.GenericUOW import UnitOfWork
from src.services_layer.dependencies.otp_dependency import get_redis
from redis.asyncio import Redis
from src.services_layer.dependencies.bus_dependency import get_message_bus
from src.services_layer.messagebus import RabbitMQMessageBus
from src.services_layer.otp_service import otp_generator, otp_validator
from uuid import uuid4
from src.domain.events import Events

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
        value=str(user.phone)
        )

    otp_code = await otp_generator(user.phone, redis)

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

    await Events.usercreated_event(bus,user.model_dump_json())
    

    return {
    "access_token": JWTService.create_access_token({
    "sub": str(user.id),"phone": user.phone,"role": user.user_role}),        
    "refresh_token": JWTService.create_refresh_token({
        "sub": str(user.id)}),"token_type": "bearer"
        }