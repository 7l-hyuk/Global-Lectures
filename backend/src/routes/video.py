from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.responses import FileResponse, JSONResponse
from sqlalchemy.orm import Session

from src.db.aws_handler import s3
from src.db.postgres import get_db
from src.db.user import User
from src.db.video import Video
from src.auth.authenticate import authenticate

video_router = APIRouter(prefix="/api/videos", tags=["Videos"])
videos = [
    {
        "id": 1,
        "title": "But what is a neural network_ _ Deep learning chapter 1_Full-HD_1",
        "length": "00:00:43",
        "url": "data/But what is a neural network_ _ Deep learning chapter 1_Full-HD_1.mp4"
    },
    {
        "id": 2,
        "title": "Python 제어문 1 오리엔테이션_Full-HD_2",
        "length": "00:02:31",
        "url": "data/ssss.mp4"
    }
]


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


@video_router.get("/")
async def get_videos(user: dict = Depends(authenticate), db: Session = Depends(get_db)):
    print(user["user"], user["id"])
    return videos


@video_router.get("/{id}")
async def get_video(id: int, user: dict = Depends(authenticate)):
    print(user["user"], user["id"])
    for video in videos:
        if video["id"] == id:
            return FileResponse(
                path=video["url"],
                media_type="video/mp4",
                status_code=status.HTTP_200_OK,
                filename=video["title"]
            )
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Video {id} not found."
    )


@video_router.get("/subtitle/{id}")
async def get_subtitle(id: int, user: dict = Depends(authenticate)):
    print(user["user"], user["id"])
    for subtitle in subtitles:
        if subtitle["video_id"] == id:
            return JSONResponse(content=subtitle["subtitle"])
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"subtitle {id} not found."
    )


@video_router.get("/test/test")
async def test():
    # s3.upload_file("data/But what is a neural network_ _ Deep learning chapter 1_Full-HD_1.mp4", "test.mp4")
    res = s3.create_presigned_url("test.mp4")
    return res
