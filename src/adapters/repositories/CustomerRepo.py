from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.domain.repositories.CustomerABS import CustomerRepository
from src.domain.entities.Users import Customer as CustomerEntity
from src.adapters.models_mappers.models import Customer as CustomerSQL
from typing import Optional, List
from src.adapters.models_mappers.Customermapper import Customermapper
from src.domain.enums import SubscriptionModel
from datetime import datetime, UTC

class SqlAlchemyCustomerRepository(CustomerRepository):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def add(self, customer: CustomerEntity) -> None:
        customerSQL = Customermapper.to_SQL(customer)
        self.db.add(customerSQL)
    
    async def update(self, customer: CustomerEntity) -> None:
        customerSQL = Customermapper.to_SQL(customer)
        self.db.flush(customerSQL)
    
    async def delete(self, id : int) -> None:
        result = await self.db.execute(select(CustomerSQL).filter(CustomerSQL.id == id))
        customer_to_delete = result.scalar_one_or_none()
        if customer_to_delete:
            await self.db.delete(customer_to_delete)
    
    async def get_by_id(self, id: int) -> Optional[CustomerEntity]:
        result = await self.db.execute(select(CustomerSQL).filter(CustomerSQL.id == id))
        customer = result.scalar_one_or_none()
        return Customermapper.to_Entity(customer) if customer else None
    
    async def get_all(self) -> List[CustomerEntity]:
        result = await self.db.execute(select(CustomerSQL))
        customers_list = result.scalars().all()
        return list(map(Customermapper.to_Entity,customers_list))
    
    async def change_subscription(self, id:int, new_model:SubscriptionModel, end_date:datetime) -> None:
        result = await self.db.execute(select(CustomerSQL).filter(CustomerSQL.id == id))
        customer = result.scalar_one_or_none()
        if customer:
            customerentity = Customermapper.to_Entity(customer)
            customerentity.sub_model = new_model
            customerentity.subscription_end = end_date
            await self.update(customerentity)
    
    async def add_to_wallet(self, id:int, amount:int) -> None:
        result = await self.db.execute(select(CustomerSQL).filter(CustomerSQL.id == id))
        customer = result.scalar_one_or_none()
        if customer:
            customerentity = Customermapper.to_Entity(customer)
            customerentity.wallet += amount
            await self.update(customerentity)

    async def check_subs(self,customer:CustomerEntity) -> bool:
        return True if (customer.subscription_end > datetime.now(UTC)) else False