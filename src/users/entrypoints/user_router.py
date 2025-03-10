from src.auth.entrypoints.dependencies.userauth import get_uow,get_current_user
from fastapi import APIRouter, Depends, Query, HTTPException
from src.adapters.UOW import UnitOfWork
from src.users.domain.entities.Users import User
from src.auth.entrypoints.dependencies.otp_dependency import get_redis
from redis import Redis
import json


router = APIRouter(prefix='/user', tags=['user'])

@router.get("/")
async def get_users(repos: UnitOfWork = Depends(get_uow), token = Depends(get_current_user),
                    page: int = Query(1, ge=1), per_page: int = Query(5, ge=5), redis: Redis = Depends(get_redis)):
    if (token['role'] == "ADMIN"):

        cache_key = f"user_{page}_{per_page}"
        user_cached = await redis.get(cache_key)
        if user_cached:
            return json.loads(user_cached)

        user_repo = repos.user
        users = await user_repo.get_all(page, per_page)
        users_list = list(dict(user) for user in users)

        await redis.setex(cache_key,60,json.dumps(users_list).encode('utf-8'))

        return users_list
    else:
        raise HTTPException(404, detail="Not authorized")

@router.get('/{user_id}')
async def get_user(user_id: int, repos: UnitOfWork = Depends(get_uow), token = Depends(get_current_user)):
    if (token["role"] == "ADMIN") or (user_id == int(token["user_id"])):
        user_repo = repos.user
        user = await user_repo.get_by_id(user_id)
        return dict(user)
    else:
        raise HTTPException(404, detail="Not authorized")
    
@router.delete('/{user_id}')
async def delete_user(user_id: int, repos: UnitOfWork = Depends(get_uow), token = Depends(get_current_user)):
    if (token["role"] == "ADMIN") or (user_id == int(token["user_id"])):
        user_repo = repos.user
        await user_repo.delete(user_id)
    else:
        raise HTTPException(404, detail="Not authorized")