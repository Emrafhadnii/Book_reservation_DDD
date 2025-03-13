from sqlalchemy import Column, String,DateTime,Boolean,Integer
from setup_db.database import Base
from datetime import datetime

class OutboxEvent(Base):
    __tablename__ = "outbox_events"
    id = Column(Integer, primary_key=True, autoincrement=True)
    aggregate_id = Column(String)
    event_type = Column(String)
    created_at = Column(DateTime, default=datetime.now())
    processed = Column(Boolean, default=False)