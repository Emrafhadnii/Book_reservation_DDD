from abc import abstractmethod
from src.books.domain.entities.Books import Book
from src.abstractions.first_layer_ABS import FirstAbstractionLayer


class BookRepository(FirstAbstractionLayer[Book]):
    
    @abstractmethod
    def stock_update(self, book_id: int, new_quantity: int) -> Book:
        pass