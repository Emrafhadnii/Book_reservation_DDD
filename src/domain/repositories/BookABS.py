from abc import ABC, abstractmethod
from typing import List, Optional
from src.domain.entities.Books import Book
from src.domain.repositories.first_layer_ABS import FirstAbstractionLayer


class BookRepository(FirstAbstractionLayer[Book]):
    
    @abstractmethod
    def stock_update(self, book_id: int, new_quantity: int) -> Book:
        pass