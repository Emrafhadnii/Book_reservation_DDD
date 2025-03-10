from src.books.adapters.mongo_repositories.Mongo_BookRepo import MongoDBBookRepository
def get_mongo_repo():
    return MongoDBBookRepository()