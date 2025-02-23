from src.books.adapters.models.Genremodel import Genre
from src.books.domain.entities.Books import Genre as GenreEntity

class Genremapper:
    def to_SQL(dbmodel: GenreEntity) -> Genre:
        return Genre(gen_name=dbmodel.gen_name)

