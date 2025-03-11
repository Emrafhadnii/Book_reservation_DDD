from fastapi import Depends, APIRouter
from src.auth.entrypoints.dependencies.userauth import get_uow
from src.adapters.UOW import UnitOfWork
from redis.asyncio import Redis
from src.auth.entrypoints.dependencies.otp_dependency import get_redis
from src.services_layer.bus_dependency import get_message_bus
from src.services_layer.messagebus import RabbitMQMessageBus
from src.auth.domain.commands import SignUpCommand
from src.auth.adapters.command_handlers import Auth_Command_Handler

router = APIRouter(prefix='/sign_up',tags=['sign_up'])


@router.post('/')
async def sign_up(model: SignUpCommand, repos: UnitOfWork = Depends(get_uow), 
                  redis: Redis = Depends(get_redis),
                  bus: RabbitMQMessageBus = Depends(get_message_bus)):
    
    return await Auth_Command_Handler.sign_up(model=model,
                                              repos=repos,
                                              redis=redis)

