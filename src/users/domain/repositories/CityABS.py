from abc import ABC
from src.adapters.repositories.first_layer_ABS import FirstAbstractionLayer
from src.users.domain.entities.Users import City

class CityRepository(FirstAbstractionLayer[City]):
    pass