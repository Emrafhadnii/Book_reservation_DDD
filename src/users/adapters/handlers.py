from src.users.domain.entities.Users import User, Customer
from src.adapters.UOW import UnitOfWork
import json

class UserHandler:
    async def usercreated_handler(message: dict):
        async with UnitOfWork() as uow:
            user_data = json.loads(message["user"])
            user = User(**user_data)
            if await uow.customer.get_by_id(user.id) or user.user_role != "CUSTOMER":
                return
            customer = Customer(user=user)
            await uow.customer.add(customer=customer)