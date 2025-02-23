from sqlalchemy import Column, String, Integer, Numeric, ForeignKey, Sequence, Enum, TIMESTAMP
from sqlalchemy.orm import relationship
from setup_db.database import Base , mapper_registry

class Genre(Base):
    __tablename__ = 'genres'

    id = Column(Integer, autoincrement=True ,primary_key=True)
    gen_name = Column(String(50), nullable=False)
    