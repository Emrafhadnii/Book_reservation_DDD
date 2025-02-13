from abc import ABC
from src.domain.repositories.first_layer_ABS import FirstAbstractionLayer
from src.domain.entities.Books import Genre

class GenreRepository(FirstAbstractionLayer[Genre]):
    pass