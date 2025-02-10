from abc import ABC
from first_layer_ABS import FirstAbstractionLayer
from src.domain.entities.Books import Genre

class GenreRepository(ABC,FirstAbstractionLayer[Genre]):
    pass