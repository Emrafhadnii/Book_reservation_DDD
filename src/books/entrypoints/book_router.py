from fastapi import APIRouter, Depends, Query, HTTPException
from src.auth.entrypoints.dependencies.userauth import get_uow,get_current_user
from src.adapters.UOW import UnitOfWork
from src.books.domain.entities.Books import Book
from src.books.adapters.mongo_repositories.Mongo_BookRepo import MongoDBBookRepository
from src.auth.entrypoints.dependencies.otp_dependency import get_redis
from redis import Redis
import json


router = APIRouter(prefix='/book',tags=['book'])

def get_mongo_repo():
    return MongoDBBookRepository()


@router.get("/")
async def get_books(repos: UnitOfWork = Depends(get_uow), token = Depends(get_current_user),
                    page: int = Query(1,ge=1), per_page: int = Query(5,ge=5)):
    book_repo = repos.book
    books = await book_repo.get_all(page,per_page)
    return list(Book.model_validate(book) for book in books)

@router.get('/{book_id}')
async def get_book(book_id: int, repos: UnitOfWork = Depends(get_uow), token = Depends(get_current_user),
                   redis: Redis = Depends(get_redis)):
    
    cache_key = f"book_{int(book_id)}"
    book_cached = await redis.get(cache_key)
    
    if book_cached:
        return json.loads(book_cached)
    
    book_repo = repos.book
    book = await book_repo.get_by_id(book_id)
    
    await redis.setex(cache_key,60,json.dumps(dict(book)).encode('utf-8'))
    
    return dict(book)

@router.get('/search/{text}')
async def search_by_name_desc(text: str,mongobook = Depends(get_mongo_repo) , token = Depends(get_current_user)):
    result = await mongobook.search_by_text(text=text)
    return result