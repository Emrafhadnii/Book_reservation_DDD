import json
from src.books.domain.queries import All_Books, One_Book

class Book_Query_Handlers:
    
    @staticmethod
    async def get_all_books(all_query: All_Books, redis, repos):
        
        cache_key = f"book_{all_query.page}_{all_query.per_page}"
        book_cached = await redis.get(cache_key)
        if book_cached:
            return json.loads(book_cached)

        book_repo = repos.book
        books = await book_repo.get_all(all_query.page,all_query.per_page)
        books_list = list(dict(book) for book in books)

        await redis.setex(cache_key,60,json.dumps(books_list).encode('utf-8'))

        return books
        
    
    @staticmethod
    async def get_one_book(one_query: One_Book,redis,repos):
        
        cache_key = f"book_{int(one_query.book_id)}"
        book_cached = await redis.get(cache_key)
        
        if book_cached:
            return json.loads(book_cached)
        
        book_repo = repos.book
        book = await book_repo.get_by_id(one_query.book_id)

        await redis.setex(cache_key,60,json.dumps(dict(book)).encode('utf-8'))
        
        return dict(book)