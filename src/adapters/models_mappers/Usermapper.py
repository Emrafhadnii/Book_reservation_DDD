from src.adapters.models_mappers.models import User
from src.domain.entities.Users import User as UserEntity

class Usermapper:
    def to_SQL(dbmodel: UserEntity) -> User:
        return User(username=dbmodel.username, email=dbmodel.email, user_role=dbmodel.user_role,
                    user_password=dbmodel.user_password, first_name=dbmodel.first_name, last_name=dbmodel.last_name,
                    phone=dbmodel.phone)
