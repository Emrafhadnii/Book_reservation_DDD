from src.users.domain.queries import AllCustomers, OneCustomer
import json
from fastapi import HTTPException


class CustomerQueryHandler:

    @staticmethod
    async def get_all(query: AllCustomers, repos):
        customer_repo = repos.customer
        customers = await customer_repo.get_all(query.page, query.per_page)
        customers_list = list(dict(customer) for customer in customers)
        return customers_list
    
    @staticmethod
    async def get_one(query: OneCustomer, token, redis, repos):
        if token["role"] == "ADMIN" or query.customer_id == int(token["user_id"]):
            cache_key = f"customer_{query.customer_id}"
            customer_cached = await redis.get(cache_key)
            if customer_cached:
                return json.loads(customer_cached)

            customer_repo = repos.customer
            customer = await customer_repo.get_by_id(query.customer_id)
            
            await redis.setex(cache_key,60,json.dumps(dict(customer)).encode('utf-8'))
            
            return dict(customer)
        else:
            raise HTTPException(404, detail="Not authorized")