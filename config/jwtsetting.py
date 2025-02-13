import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()

class JWTSettings(BaseSettings):
    SECRET_KEY: str = "guess_what"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    class config:
        env_file = "/home/emrafhadnii/Python/fastenv/Task3/config/jwt.env"

jwt_settings = JWTSettings()