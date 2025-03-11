from fastapi import APIRouter, Depends
from src.auth.services.JWT import JWTService
from src.auth.entrypoints.dependencies.userauth import get_uow
from src.adapters.UOW import UnitOfWork
from src.auth.entrypoints.dependencies.otp_dependency import get_redis
from redis.asyncio import Redis
from src.services_layer.bus_dependency import get_message_bus
from src.services_layer.ratelimiter import login_ratelimiter
from src.auth.domain.commands import LoginCommand
from src.auth.adapters.command_handlers import Auth_Command_Handler
from src.auth.domain.commands import VerifyCommand

router = APIRouter(prefix='/login', tags=['login'])

@router.post("/")
@login_ratelimiter
async def login_route(form_data: LoginCommand, 
                      uow: UnitOfWork = Depends(get_uow),
                      redis: Redis = Depends(get_redis)):    
    
    return await Auth_Command_Handler.login(form_data=form_data,
                                            uow=uow, redis=redis)


@router.post("/refresh")
async def refresh_token(refresh_token: dict):
    
    payload = JWTService.decode_token(refresh_token['refresh_token'])
    new_access_token = JWTService.create_access_token({"sub": payload.get("sub"),
                                                    "phone": payload.get("phone"),
                                                    "role":payload.get("role")})
    return {"access_token": new_access_token}


@router.post("/verify-otp/")
async def verify_otp(verifyotp: VerifyCommand, redis: Redis = Depends(get_redis), 
                    uow: UnitOfWork = Depends(get_uow), bus = Depends(get_message_bus)):
    
    return await Auth_Command_Handler.verification(verifyotp=verifyotp,
                                                   redis=redis, uow=uow, bus=bus)