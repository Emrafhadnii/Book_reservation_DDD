from fastapi import APIRouter, Depends, Query, HTTPException
from src.adapters.dependencies.userauth import get_uow,get_current_user
from src.adapters.repositories.GenericUOW import UnitOfWork
from src.domain.entities.Books import Book


router = APIRouter(prefix='/book',tags=['book'])

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
