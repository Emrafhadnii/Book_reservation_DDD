from src.users.adapters.models.Authormodel import Author
from src.users.domain.entities.Users import Author as AuthorEntity

class Authormapper:
    def to_SQL(dbmodel: AuthorEntity) -> Author:
        return Author(city_id=dbmodel.city_id, goodreads_link=dbmodel.goodreads_link,
                    bank_account=dbmodel.bank_account)
