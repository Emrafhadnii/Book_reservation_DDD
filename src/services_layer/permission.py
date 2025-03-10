from functools import wraps
from fastapi import HTTPException


class check_permission:
    
    def __init__(self, only_admin: bool = True):
        self.only_admin = only_admin

    def __call__(self, endpoint):    
        @wraps(endpoint)
        async def wrraped_endpoint(*args, **kwargs):
            token = kwargs.get("token")
            # user_id = token["user_id"]
            if self.only_admin:
                if token["role"] != "ADMIN":
                    raise HTTPException(401, detail="User not accessed")
            else:
                if token["role"] != "ADMIN":
                    raise HTTPException(401, detail="User not accessed")

            return await endpoint(*args, **kwargs)
        return wrraped_endpoint
    
