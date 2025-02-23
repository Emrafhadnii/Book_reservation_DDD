from src.adapters.dependencies.userauth import get_uow,get_current_user
from fastapi import APIRouter, Depends, Query, HTTPException
from src.adapters.repositories.GenericUOW import UnitOfWork
from src.domain.entities.Users import User

router = APIRouter(prefix='/user', tags=['user'])

@router.get("/")
async def get_users(repos: UnitOfWork = Depends(get_uow), token = Depends(get_current_user),
                    page: int = Query(1, ge=1), per_page: int = Query(5, ge=5)):
    if (token['role'] == "ADMIN"):
        user_repo = repos.user
        users = await user_repo.get_all(page, per_page)
        return list(User.model_validate(user) for user in users)
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