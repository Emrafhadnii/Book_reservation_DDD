from src.users.domain.entities.Users import Author
from src.adapters.repositories.first_layer_ABS import FirstAbstractionLayer


class AuthorRepository(FirstAbstractionLayer[Author]):
    pass