from fastapi import APIRouter, HTTPException, status

video_router = APIRouter(prefix="/api/videos", tags=["Videos"])
videos = [
    {
        "id": 1,
        "title": "But what is a neural network_ _ Deep learning chapter 1_Full-HD_1",
        "length": "00:00:43",
        "path": "data/But what is a neural network_ _ Deep learning chapter 1_Full-HD_1.mp4"
    },
    {
        "id": 2,
        "title": "Python - 제어문 - 1. 오리엔테이션_Full-HD_2",
        "length": "00:02:31",
        "path": "backend/data/Python - 제어문 - 1. 오리엔테이션_Full-HD_2.mp4"
    }
]


@video_router.get("/")
async def get_videos():
    return videos


@video_router.get("/{id}")
async def get_video(id: int):
    for video in videos:
        if video["id"] == id:
            return video
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Video {id} not found."
    )
