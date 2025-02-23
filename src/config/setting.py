from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_NAME: str
    DB_PORT: int
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_DAYS: int
    REIDIS_HOST:str
    REIDIS_PASS:str
    REIDIS_PORT:int
    RABBITMQ_USER: str
    RABBITMQ_PASSWORD: str
    MONGO_USER: str
    MONGO_PASSWORD: str
    RabbitURL: str
    class Config:
        env_file = ".env"

settings = Settings()