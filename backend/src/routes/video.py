from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.responses import FileResponse, JSONResponse
from sqlalchemy.orm import Session

from src.db.aws_handler import s3
from src.db.postgres import get_db
from src.db.user import User
from src.db.video import Video
from src.auth.authenticate import authenticate
from src.schema.video import VideoResponse
from src.utils.logger import logger

video_router = APIRouter(prefix="/api/videos", tags=["Videos"])
subtitles = [
    {
        "video_id": 1,
        "subtitle": [
            {
                "time": 0, 
                "text": "Thdhiwquhdqwdddddddddddddddddddddddddddddddddddddddddddddddddddd"
            },
            {
                "time": 7, 
                "text": "Thdhiwquhdqwdddddddddddddddddddddddddddddddddddddddddddddddddddd"
            },
            {
                "time": 15, 
                "text": "Thdhiwquhdqwdddddddddddddddddddddddddddddddddddddddddddddddddddd"
            },
            {
                "time": 30, 
                "text": "Thdhiwquhdqwdddddddddddddddddddddddddddddddddddddddddddddddddddd"
            },
            {
                "time": 33, 
                "text": "Thdhiwquhdqwdddddddddddddddddddddddddddddddddddddddddddddddddddd"
            }
        ]
    },
    {
        "video_id": 2,
        "subtitle": [
            {
                "time": 0, 
                "text": "Thdhiwquhdqwdddddddddddddddddddddddddddddddddddddddddddddddddddd"
            },
            {
                "time": 7, 
                "text": "Thdhiwquhdqwdddddddddddddddddddddddddddddddddddddddddddddddddddd"
            },
            {
                "time": 15, 
                "text": "Thdhiwquhdqwdddddddddddddddddddddddddddddddddddddddddddddddddddd"
            },
            {
                "time": 30, 
                "text": "Thdhiwquhdqwdddddddddddddddddddddddddddddddddddddddddddddddddddd"
            },
            {
                "time": 33, 
                "text": "Thdhiwquhdqwdddddddddddddddddddddddddddddddddddddddddddddddddddd"
            }
        ]
    },
]


@video_router.get("/", response_model=list[VideoResponse])
async def get_videos(
    user: dict = Depends(authenticate),
    db: Session = Depends(get_db)
):
    current_user = db.query(User).filter(User.id == user["id"]).first()
    return current_user.videos


# TODO: s3 presigned_url
@video_router.get("/{id}")
async def get_video(id: int, user: dict = Depends(authenticate), db: Session = Depends(get_db)) -> str:
    try:
        video = db.query(Video).filter(Video.id == id).first()
        presigned_url = s3.create_presigned_url(video.key)
        return presigned_url
    except Exception as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Video {id} not found."
        )


@video_router.get("/subtitle/{id}/{lang_code}")
async def get_subtitle(id: int, user: dict = Depends(authenticate)):
    print(user["user"], user["id"])
    for subtitle in subtitles:
        if subtitle["video_id"] == id:
            return JSONResponse(content=subtitle["subtitle"])
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"subtitle {id} not found."
    )
