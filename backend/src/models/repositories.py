from sqlalchemy.orm import Session
from src.models.tables import User, Video, VideoLanguage


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
            .filter(User.id == id)
            .first()
        )


class VideoRepository(BaseRepository):
    def __init__(self, session: Session):
        super().__init__(session=session)

    def get_video_by_id(self, id: int) -> Video | None:
        return (
            self.session
            .query(Video)
            .filter(Video.id == id)
            .first()
        )


class VideoLanguageRepository(BaseRepository):
    def __init__(self, session: Session):
        super().__init__(session=session)

    def get_video_language(self, video_id: int, lang_code: str):
        return (
            self.session
            .query(VideoLanguage)
            .filter(
                VideoLanguage.video_id == video_id,
                VideoLanguage.lang_code == lang_code
            )
            .first()
        )
