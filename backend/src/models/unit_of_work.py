from sqlalchemy.orm import sessionmaker, Session
from src.models.repositories import UserRepository, VideoRepository, VideoLanguageRepository
from src.models.postgres import SessionLocal


class UnitOfWork:
    def __init__(self, session_factory: sessionmaker):
        self.session_factory = session_factory
        self.session = None
    
    def __enter__(self):
        self.session: Session = self.session_factory()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            self.session.rollback()
        else:
            self.session.commit()
        self.session.close()
    
    @property
    def users(self):
        return UserRepository(self.session)

    @property
    def video(self):
        return VideoRepository(self.session)

    @property
    def video_language(self):
        return VideoLanguageRepository(self.session)


def get_uow():
    uow = UnitOfWork(SessionLocal)

    yield uow 

    if uow.session is not None:
        uow.session.close()
