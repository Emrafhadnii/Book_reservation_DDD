from sqlalchemy import Column, DateTime, Boolean, Integer, Enum
from setup_db.database import Base
from datetime import datetime
from src.users.domain.enums import SubscriptionModel

class QueueOutbox(Base):
    __tablename__ = "queueoutbox"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=False)
    book_id = Column(Integer, nullable=False)
    sub_model = Column(Enum(SubscriptionModel), nullable=False)
    created_at = Column(DateTime, default=datetime.now())
    processed = Column(Boolean, default=False)