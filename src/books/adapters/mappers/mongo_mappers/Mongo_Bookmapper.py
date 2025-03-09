from src.books.adapters.mongo_models.Mongo_Bookmodel import Book as mongoBook
from src.books.domain.entities.Books import Book

class MongoBookMapper:
    
    @staticmethod
    def to_Mongo(book: Book) -> dict:
        return {
            "id": book.id,
            "title": book.title,
            "book_desc": book.book_desc,
            "isbn": book.isbn,
            "genre_id": book.genre_id,
            "price": book.price,
            "units": book.units
        }
    @staticmethod
    def to_Entity(book:mongoBook) -> Book:
        return Book(
            id=book["id"],
            title=book["title"],
            isbn=book["isbn"],
            price=book["price"],
            book_desc=book.get("book_desc", ""),
            units=book["units"],
            genre_id=book["genre_id"]
        )