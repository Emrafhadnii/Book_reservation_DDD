from models import Author
from src.domain.entities.Users import Author as AuthorEntity

class Authormapper:
    def to_Entity(dbmodel:Author) -> AuthorEntity:
        return AuthorEntity(city_id=dbmodel.city_id,goodreads_link=dbmodel.goodreads_link,
                            bank_account=dbmodel.bank_account,books=dbmodel.books,user=dbmodel.user
                            )
    def to_SQL(dbmodel: AuthorEntity) -> Author:
        return Author(city_id=dbmodel.city_id, goodreads_link=dbmodel.goodreads_link,
                    bank_account=dbmodel.bank_account, books=dbmodel.books, user=dbmodel.user)
