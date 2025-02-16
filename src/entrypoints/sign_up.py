from fastapi import Depends, APIRouter, HTTPException
from src.domain.entities.auth import signup_model
from src.services_layer.dependencies.userauth import get_uow
from src.adapters.repositories.GenericUOW import UnitOfWork
from src.domain.entities.Users import User
from redis.asyncio import Redis
from src.services_layer.dependencies.otp_dependency import get_redis
from uuid import uuid4
from src.services_layer.otp_service import otp_generator

router = APIRouter(prefix='/sign_up',tags=['sign_up'])


@router.post('/')
async def sign_up(model: signup_model, repos: UnitOfWork = Depends(get_uow), redis: Redis = Depends(get_redis)):
    try:
        user_repo = repos.user
        customer_repo = repos.customer
        
        user = User(username=model.username,first_name=model.first_name,last_name=model.last_name,
                    user_password=model.user_password,email=model.email,phone=model.phone,user_role=model.user_role)
        
        await user_repo.add(user)

        user_identifier = str(uuid4())
        await redis.setex(
        name=f"login_identifier:{user_identifier}",
        time=120,
        value=str(user.phone)
        )

        otp_code = await otp_generator(user_identifier=user.phone,redis=redis)

        return {
            "messgae": "account created successfully",
            "user_identifier": user_identifier,
            "otp_code": otp_code
        }

    except Exception as e:
        raise HTTPException(400,detail=[str(e)])



