from models import Genre
from src.domain.entities.Books import Genre as GenreEntity

class Genremapper:
    def to_Entity(dbmodel:Genre) -> GenreEntity:
        return GenreEntity(id=dbmodel.id,gen_name=dbmodel.gen_name,books=dbmodel.books)
    def to_SQL(dbmodel: GenreEntity) -> Genre:
        return Genre(id=dbmodel.id, gen_name=dbmodel.gen_name, books=dbmodel.books)

