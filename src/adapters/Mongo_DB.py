from src.config.setting import settings
from pymongo import AsyncMongoClient

mongo_url = f"mongodb://{settings.MONGO_USER}:{settings.MONGO_PASSWORD}@mongodb:27017/mydatabase?authSource=admin"
client = AsyncMongoClient(mongo_url)
db = client["mydatabase"]