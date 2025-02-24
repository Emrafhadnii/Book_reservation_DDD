from src.adapters.UOW import UnitOfWork
import asyncio
from src.books.adapters.mongo_repositories.Mongo_BookRepo import MongoDBBookRepository

book_mongo_repo = MongoDBBookRepository()

async def outbox_event_listener():
    async with UnitOfWork() as uow:
        books = await uow.book.get_all(1,10)
        
        for book in books:
            await book_mongo_repo.add(book=book)


    while True:
        async with UnitOfWork() as uow:

            events = await uow.outbox.get_all_unprocessed()
            for event in events:
                try:
                    book = await uow.book.get_by_id(event.aggregate_id)
                    if event.event_type == "update":
                        await book_mongo_repo.update(book=book)
                    elif event.event_type == "add":
                        await book_mongo_repo.add(book=book)
                    event.processed = True

                except Exception as e:
                    print(f"Failed to process event {event.id}: {str(e)}")
        
        await asyncio.sleep(2)
