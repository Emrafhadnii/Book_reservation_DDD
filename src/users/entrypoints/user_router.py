from src.auth.entrypoints.dependencies.userauth import get_uow,get_current_user
from src.adapters.UOW import UnitOfWork
from src.auth.entrypoints.dependencies.otp_dependency import get_redis
from redis import Redis
from src.users.domain.commands import UserDeleteCommand
from src.users.domain.queries import OneUser, AllUsers
from src.services_layer.permission import admin_permission
from src.users.adapters.query_handlers import UserQueryHandler
from src.users.adapters.command_handlers import UserCommandHandler

router = APIRouter(prefix='/user', tags=['user'])

@router.get("/")
@admin_permission
async def get_users(repos: UnitOfWork = Depends(get_uow), 
                    token = Depends(get_current_user),
                    query: AllUsers = Depends(), 
                    redis: Redis = Depends(get_redis)):
    
    return await UserQueryHandler.get_all(query=query,
                                          redis=redis, repos=repos)

@router.get('/{user_id}')
async def get_user(user_id: int, repos: UnitOfWork = Depends(get_uow), 
                   token = Depends(get_current_user), redis: Redis = Depends(get_redis)):
    
    query = OneUser(user_id=user_id)
    return await UserQueryHandler.get_one(query=query, token=token,
                                          repos=repos, redis=redis)
    
@router.delete('/{user_id}')
async def delete_user(user_id: int, repos: UnitOfWork = Depends(get_uow), 
                      token = Depends(get_current_user)):
    
    command = UserDeleteCommand(user_id=user_id)
    return await UserCommandHandler.delete_user(command=command,
                                         token=token, repos=repos)