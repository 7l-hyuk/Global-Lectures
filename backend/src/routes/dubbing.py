import time
from pathlib import Path

from fastapi import APIRouter, UploadFile, Depends, File, Form,  status

from src.auth.authentication import authenticate, AuthenticatedPayload
from src.path_manager import get_user_path, UserFile
from src.utils.audio import AudioSegment
from src.utils.pipelines.dubbing_stages import (
    DubbingPipelineConfig,
    STT,
    TranslateSubtitle,
    TTS,
    RenderingVideo
)
from src.utils.pipelines.setup_stages import (
    DownloadVideo,
    ExtractAudio,
    SeperateBGMFromAudio,
    RemoveVocalsFromVideo,
    ExtractReferenceSpeaker
)
from src.models.unit_of_work import UnitOfWork, get_uow
from src.models.tables import Video, VideoLanguage
from src.models.s3_handler import s3, S3UploadFileConfig
from src.utils.pipelines.pipeline import Pipeline

dubbing_router = APIRouter(prefix="/api/v1/dubbing", tags=["Dubbing Service"])


@dubbing_router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {
            "description": "Video processing success.",
            "content": {
                "application/json": {
                    "example": {"msg": "Video processing success."}
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
    uow: UnitOfWork = Depends(get_uow)
):
    start = time.time()
    dubbing_resource_pipeline = Pipeline(
        [
            DownloadVideo(),
            ExtractAudio(),
            SeperateBGMFromAudio(),
            RemoveVocalsFromVideo(),
            ExtractReferenceSpeaker()
        ]
    )
    dubbing_pipeline = Pipeline(
        [
            STT(),
            TranslateSubtitle(),
            TTS(),
            RenderingVideo()
        ]
    )
    with get_user_path() as user_path_ctx:
        dubbing_resource_pipeline.run(
            user_path_ctx,
            video
        )
        voice_id = dubbing_pipeline.run(
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
                user_path_ctx=user_path_ctx
            )
        )
        audio_time = round(
            AudioSegment(str(user_path_ctx.get_path(UserFile.AUDIO.DUBBING)))
            .time
        )
        video = Video(
            title=Path(video.filename).stem,
            length=f"{audio_time // 3600:02}:{(audio_time % 3600) // 60:02}:{audio_time % 60:02}",
            key=None,
            creator_id=user.id,
            voice_id=voice_id
        )
        try:
            with uow as u:
                u.video.add(video)

                try:
                    upload_config = S3UploadFileConfig(
                        video_id=video.id,
                        target_lang=target_lang,
                        source_lang=source_lang
                    )
                    s3.upload_files(
                        user_path_ctx=user_path_ctx,
                        upload_config=upload_config
                    )
                # TODO: Processing s3-upload-fail
                except Exception as e:
                    print(e)

                video.key = upload_config.video_key
                languages = [
                    VideoLanguage(
                        lang_code=source_lang,
                        audio_key=upload_config.source_audio_key,
                        subtitle_key=upload_config.source_subtitle_key
                    ),
                    VideoLanguage(
                        lang_code=target_lang,
                        audio_key=upload_config.target_audio_key,
                        subtitle_key=upload_config.target_subtitle_key
                    )
                ]
                video.languages = languages
        # TODO: Processing db-transaction-fail
        except Exception as e:
            print(e)
    print(f"Service Processed In: {time.time() - start} s")
    return {"msg": "Video processing success"}
