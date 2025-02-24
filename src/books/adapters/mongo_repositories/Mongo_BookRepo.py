from src.books.domain.repositories.BookABS import BookRepository
from src.adapters.Mongo_DB import db
from src.books.domain.entities.Books import Book as BookEntity
from src.books.adapters.mappers.mongo_mappers.Mongo_Bookmapper import MongoBookMapper
from typing import Optional, List

class MongoDBBookRepository(BookRepository):
    
    def __init__(self):
        self.collection = db['books']

    async def add(self, book: BookEntity) -> None:
        await self.collection.insert_one(MongoBookMapper.to_Mongo(book))
    
    async def update(self, book : BookEntity) -> None:
        await self.collection.update_one(
            {"id": book.id},
            {"$set": MongoBookMapper.to_Mongo(book)}
        )

    async def delete(self, id : int) -> None:
        await self.collection.delete_one({"id" : id})
        
    async def get_by_id(self, id: int) -> Optional[BookEntity]:
        result = await self.collection.find_one({"id" : id})
        if result:
            return MongoBookMapper.to_Entity(result)    
    
    async def get_all(self, page: int = 1, per_page: int = 5) -> List[BookEntity]:
        offset = (page-1)*per_page
        result = await self.collection.find().skip(offset).limit(per_page)        
        book_list = await result.to_list(lenght=per_page)
        return list(map(MongoBookMapper.to_Entity,book_list))

    async def stock_update(self, id: int, new_stock: int) -> None:
        result = await self.collection.find_one({"id":id})
        if result:
            bookentity = MongoBookMapper.to_Entity(result)
            bookentity.units += new_stock
            await self.collection.update_one(
            {"id": id},
            {"$set": {"units": bookentity.units}}
        )
    
    async def search_by_text(self,text: str):
        cursor = self.collection.find(
        {"$text": {"$search": text}},
        {"score": {"$meta": "textScore"}}
        )
        results = await cursor.to_list(length=None)
        return list(map(MongoBookMapper.to_Entity,results))