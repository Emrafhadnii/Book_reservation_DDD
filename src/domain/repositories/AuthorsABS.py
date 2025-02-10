from abc import ABC, abstractmethod
from typing import List, Optional
from src.domain.entities.Users import Author
from first_layer_ABS import FirstAbstractionLayer


class AuthorRepository(ABC,FirstAbstractionLayer[Author]):
    pass