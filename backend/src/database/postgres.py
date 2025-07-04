from sqlalchemy import create_engine, URL
from sqlalchemy.orm import sessionmaker, declarative_base

from src.config import database_settings

engine = create_engine(url=str(database_settings.POSTGRES_DSN))
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()
