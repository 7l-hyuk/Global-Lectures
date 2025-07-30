from pathlib import Path
import shutil
import uuid

from fastapi import APIRouter, UploadFile, Depends, File, Form,  status
from celery.result import AsyncResult

from src.auth.authentication import authenticate, AuthenticatedPayload
from src.worker.dubbing import (
    dubbing_worker,
    make_dubbing_video,
    DubbingWorkerConfig
)

dubbing_router = APIRouter(prefix="/api/v1/dubbing", tags=["Dubbing Service"])


@dubbing_router.post(
    "/",
    status_code=status.HTTP_200_OK,
    responses={
        200: {
            "description": "Return uuid task id",
            "content": {
                "application/json": {
                    "example": {"taskId": "123e4567-e89b-12d3-a456-426614174000"}
                }
            }
        },
    }
)
def get_dubbing_video(
    video: UploadFile = File(...),
    source_lang: str = Form(...),
    target_lang: str = Form(...),
    stt_model: str = Form(...),
    translation_model: str = Form(...),
    tts_model: str = Form(...),
    user: AuthenticatedPayload = Depends(authenticate),
):
    tmp_id = str(uuid.uuid4())
    with open(f"/tmp/{tmp_id}", "wb") as f:
        shutil.copyfileobj(video.file, f)

    task = make_dubbing_video.apply_async(
        kwargs=DubbingWorkerConfig(
            tmp_id=tmp_id,
            creator_id=user.id,
            title=Path(video.filename).stem,
            source_lang=source_lang,
            target_lang=target_lang,
            stt_model=stt_model,
            translation_model=translation_model,
            tts_model=tts_model
        ).model_dump()
    )
    print(task.id)
    return {"taskId": task.id}


@dubbing_router.get(
    "/progress/{task_id}",
    status_code=status.HTTP_200_OK,
    responses={
        200: {
            "description": "Celery worker progress.",
            "content": {
                "application/json": {
                    "example": {
                        "task": "STT",
                        "percent": 33,
                    }
                }
            }
        },
    }
)
def get_task_progress(task_id: str):
    result = AsyncResult(task_id, app=dubbing_worker)
    if result.state == "PROGRESS":
        return {
            "task": result.info.get("task", "waiting"),
            "percent": result.info.get("percent", 0),
        }
    if result.successful():
        return {
            "task": "Success",
            "percent": 100
        }
    return {
        "task": "Fail",
        "percent": 0
    }
