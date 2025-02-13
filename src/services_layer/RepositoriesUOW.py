from setup_db.database import SessionLocal
from src.adapters.repositories.GenericUOW import GenericUnitOfWork
from src.adapters.repositories.AuthorRepo import SqlAlchemyAuthorRepository
from src.adapters.repositories.BookRepo import SqlAlchemyBookRepository
from src.adapters.repositories.CustomerRepo import SqlAlchemyCustomerRepository
from src.adapters.repositories.ReservationRepo import SqlAlchemyReservationRepository
from src.adapters.repositories.UserRepository import SqlAlchemyUserRepository

CustomerUoW = GenericUnitOfWork(
    repo_class=SqlAlchemyCustomerRepository,
    session_factory=SessionLocal
)
AuthorUoW = GenericUnitOfWork(
    repo_class=SqlAlchemyAuthorRepository,
    session_factory=SessionLocal
)
BookUoW = GenericUnitOfWork(
    repo_class=SqlAlchemyBookRepository,
    session_factory=SessionLocal
)
ReservationUoW = GenericUnitOfWork(
    repo_class=SqlAlchemyReservationRepository,
    session_factory=SessionLocal
)
UserUoW = GenericUnitOfWork(
    repo_class=SqlAlchemyUserRepository,
    session_factory=SessionLocal
)