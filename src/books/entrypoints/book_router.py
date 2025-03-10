from fastapi import APIRouter, Depends, Query, HTTPException, Request
from src.auth.entrypoints.dependencies.userauth import get_uow,get_current_user
from src.adapters.UOW import UnitOfWork
from src.books.domain.entities.Books import Book
from src.books.adapters.mongo_repositories.Mongo_BookRepo import MongoDBBookRepository
from src.auth.entrypoints.dependencies.otp_dependency import get_redis
from redis import Redis
import json
from src.auth.services.JWT import JWTService
from src.services_layer.permission import check_permission

router = APIRouter(prefix='/book',tags=['book'])

def get_mongo_repo():
    return MongoDBBookRepository()

admin_permission = check_permission(only_admin=True)
@router.get("/")
@admin_permission
async def get_books(repos: UnitOfWork = Depends(get_uow), token = Depends(get_current_user),
                    page: int = Query(1,ge=1), per_page: int = Query(5,ge=5), redis: Redis = Depends(get_redis)):
    
    if token["role"] == "ADMIN":
        cache_key = f"book_{page}_{per_page}"
        book_cached = await redis.get(cache_key)
        if book_cached:
            return json.loads(book_cached)

        book_repo = repos.book
        books = await book_repo.get_all(page,per_page)
        books_list = list(dict(book) for book in books)

        await redis.setex(cache_key,60,json.dumps(books_list).encode('utf-8'))

        return books
    else:
        raise HTTPException(401)

@router.get('/{book_id}')
async def get_book(book_id: int, repos: UnitOfWork = Depends(get_uow), token = Depends(get_current_user),
                   redis: Redis = Depends(get_redis)):
    
    if token["role"] == "ADMIN":
        cache_key = f"book_{int(book_id)}"
        book_cached = await redis.get(cache_key)
        
        if book_cached:
            return json.loads(book_cached)
        
        book_repo = repos.book
        book = await book_repo.get_by_id(book_id)

        await redis.setex(cache_key,60,json.dumps(dict(book)).encode('utf-8'))
        
        return dict(book)
    else:
        raise HTTPException(401)
@router.get('/search/{text}')
async def search_by_name_desc(text: str,mongobook = Depends(get_mongo_repo) , token = Depends(get_current_user)):
    result = await mongobook.search_by_text(text=text)
    return result