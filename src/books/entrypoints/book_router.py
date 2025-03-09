from fastapi import APIRouter, Depends, Query, HTTPException
from src.auth.entrypoints.dependencies.userauth import get_uow,get_current_user
from src.adapters.UOW import UnitOfWork
from src.books.domain.entities.Books import Book
from src.books.adapters.mongo_repositories.Mongo_BookRepo import MongoDBBookRepository

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
async def get_book(book_id, repos: UnitOfWork = Depends(get_uow), token = Depends(get_current_user)):
    book_repo = repos.book
    book = await book_repo.get_by_id(book_id)
    return dict(book)

@router.get('/search/{text}')
async def search_by_name_desc(text: str,mongobook = Depends(get_mongo_repo) , token = Depends(get_current_user)):
    result = await mongobook.search_by_text(text=text)
    return result