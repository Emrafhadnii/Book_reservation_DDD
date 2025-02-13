from abc import ABC
from src.domain.repositories.first_layer_ABS import FirstAbstractionLayer
from src.domain.entities.Users import City

class CityRepository(FirstAbstractionLayer[City]):
    pass