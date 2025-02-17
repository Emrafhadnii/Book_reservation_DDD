from src.domain.events import Events
from src.domain.entities.Users import User, Customer
from src.adapters.repositories.GenericUOW import UnitOfWork
import json

class Handlers:

    async def usercreated_handler(message: dict):
        async with UnitOfWork() as uow:
            user_data = json.loads(message["user"])
            user = User(**user_data)
            customer = Customer(user=user)
            await uow.customer.add(customer=customer)
