from fastapi import HTTPException
from src.users.domain.commands import PurchaseCommand, ChargeCommand, UserDeleteCommand
from datetime import datetime, timedelta


def check_subs(cr_subs: str, req_subs: str):
        validate_dict = {
            "FREE":0,
            "PLUS":1,
            "PREMIUM":2
        }
        return validate_dict[req_subs] > validate_dict[cr_subs]


class CustomerCommandHandler:

    @staticmethod
    async def purchase(command: PurchaseCommand, token, repos):
        try:
            if command.id == int(token["user_id"]):
                customer_repo = repos.customer
                current_customer = await customer_repo.get_by_id(command.id)
                if check_subs(current_customer.sub_model, command.sub_model):
                    price = 50000 if command.sub_model == "PLUS" else 200000
                    if current_customer.wallet >= price:    
                        await customer_repo.add_to_wallet(command.id, -price)
                        await customer_repo.change_subscription(command.id,command.sub_model,
                                                                datetime.now() + timedelta(days=30))
                else:
                    raise HTTPException(400, detail="You cannot decrease sub_model")    
            else:
                raise HTTPException(404, detail="Not authorized")
            return dict(await customer_repo.get_by_id(command.id))
        except Exception as e:
            raise HTTPException(404,detail="Internal Server Error")
        
    @staticmethod
    async def charge(command: ChargeCommand, repos):
        try:
            customer_repo = repos.customer
            await customer_repo.add_to_wallet(int(command.id) , int(command.amount))
            return {
                "message":"account charged successfully"
            }
        except Exception as e:
            raise HTTPException(400,str(e))
        
class UserCommandHandler:

    @staticmethod
    async def delete_user(command: UserDeleteCommand, token, repos):
        if (token["role"] == "ADMIN") or (command.user_id == int(token["user_id"])):
            user_repo = repos.user
            await user_repo.delete(command.user_id)
            return {
                "message": "user deleted successfully"
            }
        else:
            raise HTTPException(404, detail="Not authorized")