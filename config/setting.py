from pydantic_settings import BaseSettings
class Settings(BaseSettings):
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_NAME: str
    class Config:
        env_file = "/home/emrafhadnii/Python/fastenv/Task3/config/postgresql.env"
settings = Settings()