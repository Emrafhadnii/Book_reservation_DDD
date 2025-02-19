from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_NAME: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_DAYS: int
    REIDIS_HOST:str
    REIDIS_PASS:str
    REIDIS_PORT:int
    RabbitURL: str
    class Config:
        env_file = "/home/emrafhadnii/Python/fastenv/Task3/config/.env"

settings = Settings()