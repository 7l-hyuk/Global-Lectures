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


client = OpenAI(
    api_key=service_settings.GPT_API_KEY
)

def correct_and_translate(sentences: list[str], source_lang, target_lang) -> list[str]:
    combined_text = '\n'.join(f"- {sentence}" for sentence in sentences)
    
    prompt = (
        f"You are a professional translator. Consider the overall context of the following sentences, "
        f"silently correct any awkward or unnatural expressions based on that context, "
        f"then translate the corrected sentences directly from {source_lang} to {target_lang}. "
        f"Respond only with the final translated sentences as a list, preserving the original order, and no additional explanation:\n\n"
        f"{combined_text}\n\nTranslations:"
    )
    response = client.chat.completions.create(
        model='gpt-3.5-turbo',
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )
    
    translations = response.choices[0].message.content.strip().split('\n')
    translations = [line.lstrip('- ').strip() for line in translations if line.startswith('-')]
    
    return translations


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
        db=db
    )
    