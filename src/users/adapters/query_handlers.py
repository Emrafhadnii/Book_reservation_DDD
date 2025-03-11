from src.users.domain.queries import AllCustomers, OneCustomer, OneUser, AllUsers
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
        

class UserQueryHandler:

    @staticmethod
    async def get_all(query: AllUsers, redis, repos):
        cache_key = f"user_{query.page}_{query.per_page}"
        user_cached = await redis.get(cache_key)
        if user_cached:
            return json.loads(user_cached)

        user_repo = repos.user
        users = await user_repo.get_all(query.page, query.per_page)
        users_list = list(dict(user) for user in users)

        await redis.setex(cache_key,60,json.dumps(users_list).encode('utf-8'))

        return users_list
    
    @staticmethod
    async def get_one(query: OneUser, token, repos, redis):
        if (token["role"] == "ADMIN") or (query.user_id == int(token["user_id"])):
            user_repo = repos.user
            user = await user_repo.get_by_id(query.user_id)
            return dict(user)
        else:
            raise HTTPException(404, detail="Not authorized")