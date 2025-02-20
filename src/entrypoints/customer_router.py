from src.services_layer.dependencies.userauth import get_uow,get_current_user
from fastapi import APIRouter, Depends, Query, HTTPException
from src.adapters.repositories.GenericUOW import UnitOfWork
from src.domain.entities.Users import User, Customer, charge_account_model, purchase_model
from datetime import datetime, timedelta

from fastapi import HTTPException

router = APIRouter(prefix='/customer', tags=['customer'])

@router.get("/")
async def get_customers(repos: UnitOfWork = Depends(get_uow), token = Depends(get_current_user),
                        page: int = Query(1, ge=1), per_page: int = Query(5, ge=5)):
    print(token)
    if token['role'] == "ADMIN":
        customer_repo = repos.customer
        customers = await customer_repo.get_all(page, per_page)
        return list(Customer.model_validate(customer) for customer in customers)
    else:
        raise HTTPException(404, detail="Not authorized")

@router.get('/{customer_id}')
async def get_customer(customer_id: int, repos: UnitOfWork = Depends(get_uow), token = Depends(get_current_user)):
    if token["role"] == "ADMIN" or customer_id == int(token["user_id"]):
        customer_repo = repos.customer
        customer = await customer_repo.get_by_id(customer_id)
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