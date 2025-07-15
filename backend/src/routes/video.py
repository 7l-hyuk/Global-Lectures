import json

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse

from src.models.unit_of_work import UnitOfWork, get_uow
from src.models.s3_handler import s3
from src.models.tables import VideoLanguage
from src.auth.authentication import authenticate, AuthenticatedPayload
from src.schemas.video import VideoResponse, VideoUpdate, SubtitleEntry

video_router = APIRouter(prefix="/api/videos", tags=["Video"])


@video_router.get(
    "/",
    status_code=status.HTTP_200_OK,
    responses={
        200: {
            "description": "Fetch videos success",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "id": 1,
                            "title": "My First Lecture",
                            "description": "no description",
                            "length": "00:00:30"
                        },
                        {
                            "id": 2,
                            "title": "Your Lectures",
                            "description": "This Lecture is boring...",
                            "length": "99:59:59"
                        }
                    ]
                }
            }
        },
        400: {
            "description": "Authentication fail",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Invalid token"
                    }
                }
            }
        },
    }
)
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


@video_router.get(
    "/{id}",
    status_code=status.HTTP_200_OK,
    responses={
        200: {
            "description": "Fetch video success",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "url": "https://aws.presigned.url/...",
                            "languages": [
                                "en",
                                "ko",
                                "ja"
                            ],
                            "title": "My Lecture"
                        }
                    ]
                }
            }
        },
        400: {
            "description": "Authentication fail",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Invalid token"
                    }
                }
            }
        },
        404: {
            "description": "User have no access rights or video dose not exist.",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Video 1 not found."
                    }
                }
            }
        },
        502: {
            "description": "S3 request fail",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Fetch video from S3 failed."
                    }
                }
            }
        },
    }
)
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
                    status_code=status.HTTP_502_BAD_GATEWAY,
                    detail="Fetch video from S3 failed."
                )

    except Exception as e:
        print(e)


@video_router.patch(
    "/{id}",
    status_code=status.HTTP_200_OK,
    responses={
        200: {
            "description": "Update video success",
            "content": {
                "application/json": {
                    "example": {"msg": "video id: 1 was changed successfully"}
                }
            }
        },
        400: {
            "description": "Authentication fail",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Invalid token"
                    }
                }
            }
        },
        404: {
            "description": "Video not found",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "video dose not exist"
                    }
                }
            }
        },
    }
)
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


@video_router.get(
    "/bundle/{video_id}/{lang_code}",
    status_code=status.HTTP_200_OK,
    responses={
        200: {
            "description": "Fetch video bundle success",
            "content": {
                "application/json": {
                    "example": {
                        "audio": "https://aws.presigned.url/...",
                        "subtitle": [
                            {
                                "time": 1.432,
                                "text": "Hello eveyone.",
                                "end": 6.098
                            },
                            {
                                "time": 6.698,
                                "text": "This is my first lectures.",
                                "end": 12.025
                            },
                        ]
                    }
                }
            }
        },
        404: {
            "description": "Fetch video bundle fail",
            "content": {
                "application/json": {
                    "examples": {
                        "video_not_exist": {
                            "summary": "video not exist",
                            "value": {"detail": "video id: 1 not found or video have not converted to ko."}
                        },
                        "invalid_user": {
                            "summary": "Invalid user",
                            "value": {"detail": "Video 1 not found."}
                        },
                    }
                }
            }
        }
    }
)
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
                    detail=(f"video id: {video_id} not found or video have not converted to {lang_code}.")
                )

    except Exception as e:
        print(e)
