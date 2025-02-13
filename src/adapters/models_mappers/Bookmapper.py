from src.adapters.models_mappers.models import Book
from src.domain.entities.Books import Book as BookEntity

class Bookmapper:
    def to_Entity(dbmodel:Book) -> BookEntity:
        return BookEntity(id=dbmodel.id, title=dbmodel.title,isbn=dbmodel.isbn,price=dbmodel.price,
                          genre=dbmodel.genre,units=dbmodel.units,authors=dbmodel.authors,book_desc=dbmodel.book_desc
                          )
    def to_SQL(dbmodel: BookEntity) -> Book:
        return Book(id=dbmodel.id, title=dbmodel.title, isbn=dbmodel.isbn, price=dbmodel.price,
                    genre=dbmodel.genre, units=dbmodel.units, authors=dbmodel.authors, book_desc=dbmodel.book_desc)

