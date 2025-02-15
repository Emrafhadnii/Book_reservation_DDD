from src.adapters.models_mappers.models import Genre
from src.domain.entities.Books import Genre as GenreEntity

class Genremapper:
    def to_SQL(dbmodel: GenreEntity) -> Genre:
        return Genre(gen_name=dbmodel.gen_name)

