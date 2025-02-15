from src.adapters.models_mappers.models import Customer
from src.domain.entities.Users import Customer as CustomerEntity

class Customermapper:
    def to_SQL(dbmodel: CustomerEntity) -> Customer:
      return Customer(id=dbmodel.user.id, sub_model=dbmodel.sub_model, subscription_end=dbmodel.subscription_end,
                      wallet=dbmodel.wallet)
