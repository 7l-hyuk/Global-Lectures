from sqlalchemy.orm import Session
from datetime import timedelta

from src.db.video import Video
from src.db.video_language import VideoLanguage
from src.utils.path import UserPath
from src.utils.audio.audio import length
from src.db.aws_handler import s3, S3



class S3ObjectKey:
    def __init__(self, s3_client: S3, video_id: int, src_lang: str, tar_lang: str):
        self.s3_client = s3_client
        self.video_key = f"videos/{video_id}.mp4"
        self.src_audio_key = f"audios/{video_id}/{src_lang}.wav"
        self.tar_audio_key = f"audios/{video_id}/{tar_lang}.wav"
        self.src_subtitle_key = f"subtitles/{video_id}/{src_lang}.json"
        self.tar_subtitle_key = f"subtitles/{video_id}/{tar_lang}.json"
    
    def add_objects_to_s3(self, userpath: UserPath):
        keys = [
            {
                "file_name": userpath.video,
                "object_name": self.video_key
            },
            {
                "file_name": userpath.reference_speaker,
                "object_name": self.src_audio_key
            },
            {
                "file_name": userpath.dub_audio,
                "object_name": self.tar_audio_key
            },
            {
                "file_name": userpath.src_subtitle,
                "object_name": self.src_subtitle_key
            },
            {
                "file_name": userpath.tar_subtitle,
                "object_name": self.tar_subtitle_key
            }
        ]

        for key in keys:
            self.s3_client.upload_file(**key)



def add_video_to_postgres(
    db: Session,
    user_id: int,
    userpath: UserPath,
    title: str,
    src_lang: str,
    tar_lang: str
):
    try:
        video_length = length(userpath.video)
        video = Video(
            title=title,
            length=timedelta(seconds=video_length),
            key=None,
            creator_id=user_id
        )

        db.add(video)
        db.flush()

        s3_object_key = S3ObjectKey(
            s3_client=s3,
            video_id=video.id,
            src_lang=src_lang,
            tar_lang=tar_lang
        )

        video.key = s3_object_key.video_key

        languages = [
            VideoLanguage(
                lang_code=src_lang,
                audio_key=s3_object_key.src_audio_key,
                subtitle_key=s3_object_key.src_subtitle_key
            ),
            VideoLanguage(
                lang_code=tar_lang,
                audio_key=s3_object_key.tar_audio_key,
                subtitle_key=s3_object_key.tar_subtitle_key
            )
        ]

        video.languages = languages

        try:
            s3_object_key.add_objects_to_s3(userpath=userpath)
            db.commit()
            db.refresh(video)
            return video
        except Exception as e:
            db.rollback()
            print(e)
    except Exception as e:
        db.rollback()
        print(e)

