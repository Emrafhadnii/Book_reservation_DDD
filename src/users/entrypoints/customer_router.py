from src.auth.entrypoints.dependencies.userauth import get_uow,get_current_user
from fastapi import APIRouter, Depends
from src.adapters.UOW import UnitOfWork
from src.auth.entrypoints.dependencies.otp_dependency import get_redis
from redis import Redis
from src.services_layer.permission import admin_permission
from src.users.domain.queries import AllCustomers, OneCustomer
from src.users.adapters.query_handlers import CustomerQueryHandler
from src.users.domain.commands import PurchaseCommand, ChargeCommand
from src.users.adapters.command_handlers import CustomerCommandHandler

router = APIRouter(prefix='/customer', tags=['customer'])

@router.get("/")
@admin_permission
async def get_customers(repos: UnitOfWork = Depends(get_uow), 
                        token = Depends(get_current_user),
                        query: AllCustomers = Depends(), 
                        redis: Redis = Depends(get_redis)):

    return await CustomerQueryHandler.get_all(query=query, 
                                              repos=repos, redis=redis)

@router.get('/{customer_id}')
async def get_customer(customer_id: int, repos: UnitOfWork = Depends(get_uow), token = Depends(get_current_user),
                       redis: Redis = Depends(get_redis)):
    
    query = OneCustomer(customer_id=customer_id)
    return await CustomerQueryHandler.get_one(query=query, token=token,
                                              redis=redis, repos=repos)

@router.put('/purchase/')
async def update_subs(command: PurchaseCommand, repos: UnitOfWork = Depends(get_uow),
                    token = Depends(get_current_user)):
    
    return await CustomerCommandHandler.purchase(command=command,
                                                token=token, repos=repos)
    
@router.put('/charge/')
async def charge_account(command: ChargeCommand, repos: UnitOfWork = Depends(get_uow), token = Depends(get_current_user)):
    
    return await CustomerCommandHandler.charge(command=command,
                                               repos=repos)