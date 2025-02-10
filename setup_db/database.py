from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, registry
from config.setting import settings


DATABASE_URL = f"postgresql://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:5432/{settings.DB_NAME}"


mapper_registry = registry()

engine = create_engine(DATABASE_URL)
Base = mapper_registry.generate_base()


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

