import time

from fastapi import APIRouter, UploadFile, Depends, File, Form

# from src.auth.authentication import authenticate, AuthenticatedPayload
from src.services.dubbing import get_setup_pipeline, get_dubbing_pipeline
from src.path_manager import get_user_path, UserFile, UserDir
from src.utils.pipelines.dubbing_stages import DubbingPipelineConfig
from src.utils.pipelines.pipeline import Pipeline

dubbing_router = APIRouter(prefix="/api/v1/dubbing", tags=["Dubbing Service"])


@dubbing_router.post("/")
def get_dubbing_video(
    video: UploadFile = File(...),
    source_lang: str = Form(...),
    target_lang: str = Form(...),
    stt_model: str = Form(...),
    translation_model: str = Form(...),
    tts_model: str = Form(...),
    dubbing_resource_pipeline: Pipeline = Depends(get_setup_pipeline),
    dubbing_pipeline: Pipeline = Depends(get_dubbing_pipeline),
    # user: AuthenticatedPayload = Depends(authenticate)
):
    start = time.time()
    with get_user_path() as user_path_ctx:
        dubbing_resource_pipeline.run(
            user_path_ctx,
            video
        )
        dubbing_pipeline.run(
            user_path_ctx.get_path(UserFile.AUDIO.VOCALS),
            DubbingPipelineConfig(
                source_lang=source_lang,
                target_lang=target_lang,
                stt_model=stt_model,
                translation_model=translation_model,
                tts_model=tts_model,
                stt_requset_timeout=600,
                translation_requset_timeout=600,
                tts_request_timeout=600,
                reference_speaker=user_path_ctx.get_path(UserFile.AUDIO.REFERENCE_SPEAKER),
                tts_output=user_path_ctx.get_path(UserDir.DUBBING),
                dubbing_audio_output=user_path_ctx.get_path(UserFile.AUDIO.DUBBING)
            )
        )
    print(f"Service Processed In: {time.time() - start} s")
