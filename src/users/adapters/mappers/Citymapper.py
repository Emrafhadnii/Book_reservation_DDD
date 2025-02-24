from src.users.adapters.models.Citymodel import City
from src.users.domain.entities.Users import City as CityEntity

class Citymapper:
   def to_SQL(dbmodel: CityEntity) -> City:
        return City(city_name=dbmodel.city_name)
