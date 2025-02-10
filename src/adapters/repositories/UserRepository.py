from sqlalchemy.orm import Session
from src.domain.repositories.UserABS import UserRepository
from src.domain.entities.Users import User as UserEntity
from src.adapters.models import User
from typing import Optional, List

class SqlAlchemyUserRepository(UserRepository):
    def __init__(self, db: Session):
        self.db = db 

    def get_by_id(self, id: int) -> Optional[User]:
        return self.db.query(User).filter(User.id == id).first()

    def get_all(self) -> List[User]:
        return self.db.query(User).all()

    def delete(self, id: int) -> None:
        user_to_delete = self.db.query(User).filter(User.id == id).first()
        if user_to_delete:
            self.db.delete(user_to_delete)
            self.db.commit()

    def update(self, t: User) -> None:
        self.db.merge(t)
        self.db.commit()

    def add(self, t: User) -> None:
        self.db.add(t)
        self.db.commit()

    def get_role(self, id: int) -> User:
        user = self.db.query(User).filter(User.id == id).first()
        if not user:
            raise ValueError(f"User with id {id} not found")
        return user