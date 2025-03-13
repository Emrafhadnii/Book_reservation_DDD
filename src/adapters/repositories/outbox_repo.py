from sqlalchemy.ext.asyncio import AsyncSession
from src.adapters.outbox_model import OutboxEvent
from sqlalchemy import select

class OutBoxEventRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def add(self, event: dict) -> None:
        sqlmodel = OutboxEvent(
            aggregate_id=event["aggregate_id"],
            event_type=event["event_type"]
        )
        self.db.add(sqlmodel)

    async def get_all_unprocessed(self):
        result = await self.db.execute(select(OutboxEvent).filter(OutboxEvent.processed == False).order_by(OutboxEvent.created_at))
        events = result.scalars().all()
        return events