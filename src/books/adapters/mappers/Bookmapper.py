from src.books.adapters.models.Bookmodel import Book
from src.books.domain.entities.Books import Book as BookEntity

class Bookmapper:
    def to_SQL(dbmodel: BookEntity) -> Book:
        return Book(id=dbmodel.id,title=dbmodel.title, isbn=dbmodel.isbn, price=dbmodel.price,
                    units=dbmodel.units,genre_id = dbmodel.genre_id ,book_desc=dbmodel.book_desc)

