import json

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse

from src.models.unit_of_work import UnitOfWork, get_uow
from src.models.s3_handler import s3
from src.models.tables import VideoLanguage
from src.auth.authentication import authenticate, AuthenticatedPayload
from src.schemas.video import VideoResponse, VideoUpdate, SubtitleEntry

video_router = APIRouter(prefix="/api/videos", tags=["Video"])


@video_router.get("/")
def get_videos(
    user: AuthenticatedPayload = Depends(authenticate),
    uow: UnitOfWork = Depends(get_uow)
):
    try:
        with uow as u:
            user = u.users.get_user_by_id(user.id)
            return list(map(VideoResponse.model_validate, user.videos))

    except Exception as e:
        print(e)


@video_router.get("/{id}")
def get_video(
    id: int,
    uow: UnitOfWork = Depends(get_uow),
    user: AuthenticatedPayload = Depends(authenticate)
) -> dict[str, str | list[SubtitleEntry]]:
    try:
        with uow as u:
            try:
                video = u.video.get_video_by_id(id)

                if user.id != video.creator_id:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"video id: {id} not found"
                    )
                languages: list[VideoLanguage] = video.languages

            except Exception as e:
                print(e)
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Video {id} not found."
                )

            try:
                presigned_url = s3.create_presigned_url(video.key)
                return JSONResponse(
                    content={
                        "url": presigned_url,
                        "languages": [lang.lang_code for lang in languages],
                        "title": video.title
                    }
                )

            except Exception as e:
                print(e)
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Fetch video from S3 failed."
                )

    except Exception as e:
        print(e)


@video_router.patch("/{id}")
def update_video(
    id: int,
    video_update: VideoUpdate,
    uow: UnitOfWork = Depends(get_uow),
    user: AuthenticatedPayload = Depends(authenticate)
):
    try:
        with uow as u:
            video = u.video.get_video_by_id(id)

            if not video or video.creator_id != user.id:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="video dose not exist"
                )

            for field, value in video_update.model_dump(
                exclude_unset=True
            ).items():
                setattr(video, field, value)
            return {"msg": f"video id: {id} was changed successfully"}

    except Exception as e:
        print(e)


@video_router.get("/bundle/{video_id}/{lang_code}")
def get_bundle(
    video_id: int,
    lang_code: str,
    uow: UnitOfWork = Depends(get_uow),
    user: AuthenticatedPayload = Depends(authenticate)
):
    try:
        with uow as u:
            lang = u.video_language.get_video_language(
                video_id,
                lang_code
            )

            if lang.video.creator_id != user.id:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Video {video_id} not found."
                )

            try:
                audio_presigned_url = s3.create_presigned_url(lang.audio_key)
                subtitle = json.loads(s3.get_object(lang.subtitle_key))
                return JSONResponse(
                    content={
                        "audio": audio_presigned_url,
                        "subtitle": subtitle
                    }
                )

            except Exception as e:
                print(e)
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"video id: {video_id} not found or video have not converted to {lang_code}."
                )

    except Exception as e:
        print(e)
