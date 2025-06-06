from openai import OpenAI
from pathlib import Path
import json

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
from src.schema.video import DubAudioRequest
from src.config import service_settings

dub_router = APIRouter(prefix="/v1/dub", tags=["dub service"])
BASIC_MODEL = "basic model"

@dub_router.post("/")
async def get_dub_video(
    video: UploadFile,
    source_lang: str = Form(..., alias="sourceLang"),
    target_lang: str = Form(..., alias="targetLang"),
    stt_model: str = Form(..., alias="sttModel"),
    translation_model: str = Form(..., alias="translationModel"),
    tts_model: str = Form(..., alias="ttsModel"),
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
        stt_model="stt" if stt_model == BASIC_MODEL else "stt-elevenlabs",
        translation_model="translator" if translation_model == BASIC_MODEL else "translator-gpt",
        tts_model="tts" if tts_model == BASIC_MODEL else "tts-elevenlabs",
        db=db
    )


# TODO: 기 등록된 영상에 더빙을 하는 라우터
@dub_router.post("/audio")
async def get_dub_audio(
    payload: DubAudioRequest,
    db: Session = Depends(get_db),
    user: dict = Depends(authenticate)
):
    source_lang = SupportedLanguages.CODE[payload.source_lang]
    target_lang = SupportedLanguages.CODE[payload.target_lang]
    userpath = UserPath(uuid.uuid4())

    service.dub_by_audio( 
        audio_presigned_url=payload.audio_presigned_url,
        userpath=userpath,
        subtitle=payload.subtitle,
        video_id=payload.video_id,
        src_lang=source_lang,
        tar_lang=target_lang,
        translation_model="translator" if payload.translation_model == BASIC_MODEL else "translator-gpt",
        tts_model="tts" if payload.tts_model == BASIC_MODEL else "tts-elevenlabs",
        db=db
    )
    