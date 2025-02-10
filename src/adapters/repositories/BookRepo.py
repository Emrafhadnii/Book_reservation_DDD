from sqlalchemy.orm import Session
from src.domain.repositories.BookABS import BookRepository
from src.domain.entities.Books import Book as BookEntity
from src.adapters.models import Book
from src.adapters.models import BookMapper

class SqlAlchemyBookRepository(BookRepository):
    def __init__(self, session: Session):
        self.session = session

    def add(self, book: Book) -> None:
       pass
    def update(self, book : Book) -> None:
        pass
    def delete(self, book_id : int) -> None:
        pass
    def get_by_id(self, book_id: int) -> Book | None:
        pass
    def get_all(self) -> list:
        pass
