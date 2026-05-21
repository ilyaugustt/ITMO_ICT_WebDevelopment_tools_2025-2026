import os
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

database_url: str = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:postgres@postgres:5432/travel"
)
engine = create_engine(database_url)


def get_db():
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()