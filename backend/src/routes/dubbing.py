import time
from pathlib import Path

from fastapi import APIRouter, UploadFile, Depends, File, Form

from src.auth.authentication import authenticate, AuthenticatedPayload
from src.services.dubbing import get_setup_pipeline, get_dubbing_pipeline
from src.path_manager import get_user_path, UserFile, UserDir
from src.utils.pipelines.dubbing_stages import DubbingPipelineConfig
from src.utils.pipelines.pipeline import Pipeline
from src.utils.audio import AudioSegment
from src.database.unit_of_work import UnitOfWork, get_uow
from src.database.tables import Video, VideoLanguage
from src.database.s3_handler import s3, S3UploadFileConfig

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
    user: AuthenticatedPayload = Depends(authenticate),
    uow: UnitOfWork = Depends(get_uow)
):
    start = time.time()
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
                reference_speaker=user_path_ctx.get_path(UserFile.AUDIO.REFERENCE_SPEAKER),
                tts_output=user_path_ctx.get_path(UserDir.DUBBING),
                dubbing_audio_output=user_path_ctx.get_path(UserFile.AUDIO.DUBBING),
                source_subtitle_path=user_path_ctx.get_path(UserFile.SUBTITLE.SOURCE),
                target_subtitle_path=user_path_ctx.get_path(UserFile.SUBTITLE.TARGET)
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


