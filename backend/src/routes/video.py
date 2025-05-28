from fastapi import APIRouter, HTTPException, status
from fastapi.responses import FileResponse
from src.db.aws_handler import s3

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
            [0, "Thdhiwquhdqwdddddddddddddddddddddddddddddddddddddddddddddddddddd"],
            [15, "Tdhqwiuddddddddddddddddddddddddddddddddddddddddddddddhwq"]
        ]
    },
    {
        "video_id": 2,
        "subtitle": [
            [0, "Thdhiwquhdqwd"],
            [15, "Tdhqwiudhwq"]
        ]
    },
]


@video_router.get("/")
async def get_videos():
    return videos


@video_router.get("/{id}")
async def get_video(id: int):
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
async def get_subtitle(id: int):
    for subtitle in subtitles:
        if subtitle["video_id"] == id:
            return subtitle["subtitle"]
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"subtitle {id} not found."
    )


@video_router.get("/test/test")
async def test():
    s3.upload_file("data/But what is a neural network_ _ Deep learning chapter 1_Full-HD_1.mp4", "test.mp4")
    return {"msg", "ddddddd"}