from pathlib import Path

import uuid
import shutil
from fastapi import APIRouter, UploadFile, Form, Depends
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from src.utils.path import UserPath
import src.services.dub as service
from src.models.language import SupportedLanguages
from src.auth.authenticate import authenticate
from src.db.postgres import get_db

dub_router = APIRouter(prefix="/v1/dub", tags=["dub service"])


@dub_router.post("/")
async def get_dub_video(
    video: UploadFile,
    source_lang: str = Form(..., alias="sourceLang"),
    target_lang: str = Form(..., alias="targetLang"),
    db: Session = Depends(get_db),
    user: dict = Depends(authenticate)
):
    source_lang = SupportedLanguages.CODE[source_lang]
    target_lang = SupportedLanguages.CODE[target_lang]
    userpath = UserPath(uuid.uuid4())

    with open(userpath.original_video, "wb") as f:
        shutil.copyfileobj(video.file, f)

    service.dub( 
        userpath=userpath,
        src_lang=source_lang,
        tar_lang=target_lang,
        user_id=user["id"],
        video_title=Path(video.filename).stem,
        db=db
    )

    output = userpath.dub_video
    return FileResponse(
        output,
        media_type="video/mp4",
        filename=output.name
    )


@dub_router.post("/audio")
async def get_dub_video(
    presigned_url: str,
    source_lang: str = Form(..., alias="sourceLang"),
    target_lang: str = Form(..., alias="targetLang"),
    db: Session = Depends(get_db),
    user: dict = Depends(authenticate)
):
    # presigned_url로 audio 리소스 접근
    # target_lang에 해당하는 언어로 더빙
    return 