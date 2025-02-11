from models import City
from src.domain.entities.Users import City as CityEntity

class Citymapper:
    def to_Entity(dbmodel:City) -> CityEntity:
        return CityEntity(id=dbmodel.id,city_name=dbmodel.city_name,authors=dbmodel.authors)
    def to_SQL(dbmodel: CityEntity) -> City:
        return City(id=dbmodel.id, city_name=dbmodel.city_name, authors=dbmodel.authors)
