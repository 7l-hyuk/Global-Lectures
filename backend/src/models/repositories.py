from sqlalchemy.orm import Session
from src.models.tables import User


class BaseRepository:
    def __init__(self, session: Session):
        self.session = session
    
    def add(self, instance, refresh=False):
        self.session.add(instance)
        self.session.flush()

        if refresh:
            self.session.refresh(instance)


class UserRepository(BaseRepository):
    def __init__(self, session: Session):
        super().__init__(session=session)
    
    def get_user_by_name(self, username: str) -> User | None:
        return (
            self.session
            .query(User)
            .filter(User.username == username)
            .first()
        )
    
    def get_user_by_id(self, id: int) -> User | None:
        return (
            self.session
            .query(User)
            .filter(User.id== id)
            .first()
        )


class VideoRepository(BaseRepository):
    def __init__(self, session: Session):
        super().__init__(session=session)
    


class VideoLanguageRepository(BaseRepository):
    def __init__(self, session: Session):
        super().__init__(session=session)