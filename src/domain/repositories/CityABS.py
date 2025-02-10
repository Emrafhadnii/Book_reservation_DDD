from abc import ABC
from first_layer_ABS import FirstAbstractionLayer
from src.domain.entities.Users import City

class CityRepository(ABC,FirstAbstractionLayer[City]):
    pass