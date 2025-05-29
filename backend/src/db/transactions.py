from sqlalchemy.orm import Session
from datetime import time

from src.db.video import Video
from src.db.video_language import VideoLanguage

def add_video(
    db: Session,
    segments: dict,
    title: str,
    length: time,
    lang_code: str,
    user_id: int,
):
    try:
        video = Video(
            title=title,
            length=length,
            key=None,
            user_id=user_id
        )

        db.add(video)
        db.flush()
        video.key = f"videos/{video.id}.mp4"

        languages = VideoLanguage(
            lang_code=lang_code,
            audio_key=f"audios/{video.id}/{lang_code}.wav",
            subtitle_key=f"subtitles/{video.id}/{lang_code}.csv"
        )

        video.languages = languages

        db.commit()
        db.refresh(video)
        return video

    except Exception as e:
        db.rollback()
        raise e