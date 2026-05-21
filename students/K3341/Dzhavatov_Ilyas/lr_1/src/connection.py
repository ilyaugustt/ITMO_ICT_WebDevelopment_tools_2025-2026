from sqlalchemy.orm import sessionmaker

from sqlalchemy import create_engine

database_url: str = "postgresql://postgres:postgres@localhost/travel"
engine = create_engine(database_url)


def get_db():
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
