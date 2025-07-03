from fastapi import APIRouter, UploadFile, Depends, File, Form
import shutil

from src.auth.authentication import authenticate, AuthenticatedPayload
from src.path_manager import get_user_path
from src.services.stt import SttClient
from src.services.translator import TranslatorClient
from src.utils.video_processor import seperate_audio

dubbing_router = APIRouter(prefix="/api/v1/dubbing", tags=["Dubbing Service"])
stt_client = SttClient(API_URL="http://localhost:8001/api/v1/stt")
translator_client = TranslatorClient(API_URL="http://localhost:8002/api/v1/translation")


@dubbing_router.post("/")
async def get_dubbing_video(
    video: UploadFile = File(...),
    source_lang: str = Form(...),
    target_lang: str = Form(...),
    stt_model: str = Form(...),
    translation_model: str = Form(...),
    tts_model: str = Form(...),
    # user: AuthenticatedPayload = Depends(authenticate)
):
    with get_user_path() as user_path:
        with open(user_path.initial_video, "wb") as f:
            shutil.copyfileobj(video.file, f)
        seperate_audio(user_path=user_path)
        subtitles = stt_client.run(
            audio_path=user_path.vocals,
            language=source_lang,
            model=stt_model
        )
        translated_subtitles = translator_client.run(
            subtitles=subtitles,
            source_lang=source_lang,
            target_lang=target_lang,
            model=translation_model,
            timeout=600
        )
        return translated_subtitles

