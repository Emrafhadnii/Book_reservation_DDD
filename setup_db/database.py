from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, registry
from config.setting import settings


DATABASE_URL = (
    f"postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:5432/{settings.DB_NAME}"
)

mapper_registry = registry()

engine = create_async_engine(DATABASE_URL, echo=True, future=True)
Base = mapper_registry.generate_base()


SessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession,expire_on_commit=False)

async def get_session():
    async with SessionLocal() as db:
        yield db