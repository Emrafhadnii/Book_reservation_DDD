from sqlalchemy.ext.asyncio import AsyncSession
from src.adapters.models.queue import QueueOutbox
from sqlalchemy import select, case
from src.users.domain.enums import SubscriptionModel

class QueueOutboxRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def add(self, event: dict) -> None:
        sqlmodel = QueueOutbox(
            book_id=int(event["book_id"]),
            user_id=int(event["user_id"]),
            sub_model=event["sub_model"]
        )
        self.db.add(sqlmodel)
    
    async def delete(self, command: dict):
        result = await self.db.execute(select(QueueOutbox).filter(QueueOutbox.book_id == command['book_id'],
                                                                  QueueOutbox.user_id == command['user_id']))
        queued = result.scalar_one_or_none()
        if queued:
            await self.db.delete(queued)

    async def get_first_unprocessed(self):
        role_priority = case((QueueOutbox.sub_model == SubscriptionModel.PREMIUM, 1),else_=2)
        result = await self.db.execute(select(QueueOutbox).filter(QueueOutbox.processed == False).order_by(role_priority.asc(),
                                                                                                           QueueOutbox.created_at.asc()))
        return result.scalars().first()
    
    async def set_processed(self, command: dict):
        result = await self.db.execute(select(QueueOutbox).filter(QueueOutbox.book_id == command['book_id'],
                                                                  QueueOutbox.user_id == command['user_id']))
        queued = result.scalar_one_or_none()
        if queued:
            queued.processed = True
            await self.db.merge(queued)