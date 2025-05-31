from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
import json

from src.db.aws_handler import s3
from src.db.postgres import get_db
from src.db.user import User
from src.db.video import Video
from src.db.video_language import VideoLanguage
from src.auth.authenticate import authenticate
from src.schema.video import VideoResponse
from src.utils.logger import logger

video_router = APIRouter(prefix="/api/videos", tags=["Videos"])


@video_router.get("/", response_model=list[VideoResponse])
async def get_videos(
    user: dict = Depends(authenticate),
    db: Session = Depends(get_db)
):
    current_user = db.query(User).filter(User.id == user["id"]).first()
    return current_user.videos


@video_router.get("/{id}")
async def get_video(
    id: int,
    user: dict = Depends(authenticate),
    db: Session = Depends(get_db)
) -> dict[str, str | list[str]]:
    try:
        video = db.query(Video).filter(Video.id == id).first()
        presigned_url = s3.create_presigned_url(video.key)
        languages = video.languages
        title = video.title
        content = {
            "url": presigned_url,
            "languages": [language.lang_code for language in languages],
            "title": title
        }
        return JSONResponse(content=content)
    except Exception as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Video {id} not found."
        )


# TODO: service layer 분리
@video_router.get("/bundle/{video_id}/{lang_code}")
async def get_subtitle(
    video_id: int,
    lang_code: str,
    user: dict = Depends(authenticate),
    db: Session = Depends(get_db)
) -> dict[str, str | dict]:
    try:
        language = db.query(VideoLanguage).filter(
            VideoLanguage.video_id == video_id,
            VideoLanguage.lang_code == lang_code
        ).first()

        audio_presigned_url = s3.create_presigned_url(language.audio_key)
        subtitle_json = json.loads(s3.get_object(language.subtitle_key))
        print(language.audio_key, language.subtitle_key)
        content = {
            "audio": audio_presigned_url,
            "subtitle": subtitle_json
        }
        return JSONResponse(content=content)
    except Exception as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"subtitle {id} not found."
        )
