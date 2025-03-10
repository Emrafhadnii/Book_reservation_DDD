from fastapi import APIRouter, Depends, Query
from src.auth.entrypoints.dependencies.userauth import get_uow,get_current_user
from src.adapters.UOW import UnitOfWork
from src.books.entrypoints.mongo_dependency import get_mongo_repo
from src.auth.entrypoints.dependencies.otp_dependency import get_redis
from redis import Redis
from src.services_layer.permission import check_permission
from src.books.domain.queries import Book_Queries

router = APIRouter(prefix='/book',tags=['book'])

admin_permission = check_permission(only_admin=True)

@router.get("/")
@admin_permission
async def get_books(repos: UnitOfWork = Depends(get_uow), token = Depends(get_current_user),
                    page: int = Query(1,ge=1), per_page: int = Query(5,ge=5), redis: Redis = Depends(get_redis)):
    
    return await Book_Queries.get_all_books(page=page, per_page=per_page,
                                            redis=redis, repos=repos)


@router.get('/{book_id}')
async def get_book(book_id: int, repos: UnitOfWork = Depends(get_uow), token = Depends(get_current_user),
                   redis: Redis = Depends(get_redis)):
    
    return await Book_Queries.get_one_book(book_id=book_id, redis=redis, 
                                           repos=repos)
    

@router.get('/search/{text}')
async def search_by_name_desc(text: str,mongobook = Depends(get_mongo_repo) , token = Depends(get_current_user)):
    result = await mongobook.search_by_text(text=text)
    return result