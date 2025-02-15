from src.adapters.models_mappers.models import City
from src.domain.entities.Users import City as CityEntity

class Citymapper:
   def to_SQL(dbmodel: CityEntity) -> City:
        return City(city_name=dbmodel.city_name)
