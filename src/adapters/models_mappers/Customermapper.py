from src.adapters.models_mappers.models import Customer
from src.domain.entities.Users import Customer as CustomerEntity

class Customermapper:
    def to_Entity(dbmodel:Customer) -> CustomerEntity:
        return CustomerEntity(user=dbmodel.user,sub_model=dbmodel.sub_model,subscription_end=dbmodel.subscription_end,
                              wallet=dbmodel.wallet,reservations=dbmodel.reservations
                            )
    def to_SQL(dbmodel: CustomerEntity) -> Customer:
      return Customer(user=dbmodel.user, sub_model=dbmodel.sub_model, subscription_end=dbmodel.subscription_end,
                      wallet=dbmodel.wallet, reservations=dbmodel.reservations)
