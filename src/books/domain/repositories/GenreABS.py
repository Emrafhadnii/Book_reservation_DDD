from src.adapters.repositories.first_layer_ABS import FirstAbstractionLayer
from src.books.domain.entities.Books import Genre

class GenreRepository(FirstAbstractionLayer[Genre]):
    pass