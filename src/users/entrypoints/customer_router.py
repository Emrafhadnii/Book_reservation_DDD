from src.auth.entrypoints.dependencies.userauth import get_uow,get_current_user
from fastapi import APIRouter, Depends, Query, HTTPException
from src.adapters.UOW import UnitOfWork
from src.users.domain.entities.Users import Customer, charge_account_model, purchase_model
from datetime import datetime, timedelta
from src.auth.entrypoints.dependencies.otp_dependency import get_redis
from fastapi import HTTPException
from redis import Redis
import json
from src.users.domain.entities.Users import Customer

router = APIRouter(prefix='/customer', tags=['customer'])

@router.get("/")
async def get_customers(repos: UnitOfWork = Depends(get_uow), token = Depends(get_current_user),
                        page: int = Query(1, ge=1), per_page: int = Query(5, ge=5), redis: Redis = Depends(get_redis)):

    if token['role'] == "ADMIN":
        # cache_key = f"page_{page}_{per_page}"
        # customer_cached = await redis.get(cache_key)
        # if customer_cached:
        #     return json.loads(customer_cached)
        customer_repo = repos.customer
        customers = await customer_repo.get_all(page, per_page)
        customers_list = list(dict(customer) for customer in customers)
        # await redis.setex(cache_key,60,json.dumps(customers_list))
        return customers_list
    else:
        raise HTTPException(404, detail="Not authorized")

@router.get('/{customer_id}')
async def get_customer(customer_id: int, repos: UnitOfWork = Depends(get_uow), token = Depends(get_current_user),
                       redis: Redis = Depends(get_redis)):
    if token["role"] == "ADMIN" or customer_id == int(token["user_id"]):
        cache_key = f"customer_{customer_id}"
        customer_cached = await redis.get(cache_key)
        if customer_cached:
            return json.loads(customer_cached)

        customer_repo = repos.customer
        customer = await customer_repo.get_by_id(customer_id)
        
        await redis.setex(cache_key,60,json.dumps(dict(customer)).encode('utf-8'))
        
        return dict(customer)
    else:
        raise HTTPException(404, detail="Not authorized")



def check_subs(cr_subs: str, req_subs: str):
    validate_dict = {
        "FREE":0,
        "PLUS":1,
        "PREMIUM":2
    }
    return validate_dict[req_subs] > validate_dict[cr_subs]

@router.put('/purchase/')
async def update_subs(customer: purchase_model, repos: UnitOfWork = Depends(get_uow),
                    token = Depends(get_current_user)):
    try:
        if customer.id == int(token["user_id"]):
            customer_repo = repos.customer
            current_customer = await customer_repo.get_by_id(customer.id)
            if check_subs(current_customer.sub_model, customer.sub_model):
                price = 50000 if customer.sub_model == "PLUS" else 200000
                if current_customer.wallet >= price:
                    await customer_repo.add_to_wallet(customer.id, -price)
                    await customer_repo.change_subscription(customer.id,customer.sub_model,datetime.now() + timedelta(days=30))
            else:
                raise HTTPException(400, detail="You cannot decrease sub_model")    
        else:
            raise HTTPException(404, detail="Not authorized")
        return dict(await customer_repo.get_by_id(customer.id))
    except Exception as e:
        raise HTTPException(404,detail="Internal Server Error")
    
@router.put('/charge/')
async def charge_account(amount: charge_account_model, repos: UnitOfWork = Depends(get_uow), token = Depends(get_current_user)):
    try:
        customer_repo = repos.customer
        await customer_repo.add_to_wallet(int(amount.id) , int(amount.amount))
        return {
            "message":"account charged successfully"
        }
    except Exception as e:
        raise HTTPException(400,str(e))