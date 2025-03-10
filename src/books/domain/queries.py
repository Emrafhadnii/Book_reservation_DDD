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


class Book_Queries:
    @staticmethod
    async def get_all_books(page,per_page,redis,repos):
        
        cache_key = f"book_{page}_{per_page}"
        book_cached = await redis.get(cache_key)
        if book_cached:
            return json.loads(book_cached)

        book_repo = repos.book
        books = await book_repo.get_all(page,per_page)
        books_list = list(dict(book) for book in books)

        await redis.setex(cache_key,60,json.dumps(books_list).encode('utf-8'))

        return books
        
    
    @staticmethod
    async def get_one_book(book_id,redis,repos):
        cache_key = f"book_{int(book_id)}"
        book_cached = await redis.get(cache_key)
        
        if book_cached:
            return json.loads(book_cached)
        
        book_repo = repos.book
        book = await book_repo.get_by_id(book_id)

        await redis.setex(cache_key,60,json.dumps(dict(book)).encode('utf-8'))
        
        return dict(book)