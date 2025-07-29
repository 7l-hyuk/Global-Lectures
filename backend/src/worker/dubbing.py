import os
import time
import shutil

from celery import Celery, Task
from pydantic import BaseModel

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
    ExtractAudio,
    SeperateBGMFromAudio,
    RemoveVocalsFromVideo,
    ExtractReferenceSpeaker
)
from src.models.unit_of_work import UnitOfWork
from src.models.postgres import SessionLocal
from src.models.tables import Video, VideoLanguage
from src.models.s3_handler import s3, S3UploadFileConfig
from src.config import api_settings
from src.utils.pipelines.pipeline import Pipeline

import logging

logger = logging.getLogger(__name__)


dubbing_worker = Celery(
    "dubbing_worker",
    broker=api_settings.REDIS_DSN,
    backend=api_settings.REDIS_DSN
)

dubbing_worker.conf.task_track_started = True
dubbing_worker.conf.result_expires = 3600


class DubbingWorkerConfig(BaseModel):
    tmp_id: str
    creator_id: int
    title: str
    source_lang: str
    target_lang: str
    stt_model: str
    translation_model: str
    tts_model: str


@dubbing_worker.task(bind=True)
def make_dubbing_video(
    self: Task,
    tmp_id: str,
    creator_id: int,
    title: str,
    source_lang: str,
    target_lang: str,
    stt_model: str,
    translation_model: str,
    tts_model: str
):
    def update_state(task_name, total, current):
        self.update_state(
            state="PROGRESS",
            meta={
                "task": task_name,
                "percent": round((current / total) * 100)
            }
        )
    start = time.time()

    total_step = 3
    current_step = 0

    dubbing_resource_pipeline_stages = [
        ExtractAudio(),
        SeperateBGMFromAudio(),
        RemoveVocalsFromVideo(),
        ExtractReferenceSpeaker()
    ]
    dubbing_pipeline_stages = [
        STT(),
        TranslateSubtitle(),
        TTS(),
        RenderingVideo()
    ]

    dubbing_resource_pipeline = Pipeline(
        dubbing_resource_pipeline_stages
    )
    dubbing_pipeline = Pipeline(
        dubbing_pipeline_stages
    )

    with get_user_path() as user_path_ctx:
        video_src = f"/tmp/{tmp_id}"
        shutil.copy(
            video_src,
            user_path_ctx.get_path(UserFile.VIDEO.BASE)
        )
        os.remove(video_src)

        current_step += 1
        dubbing_resource_pipeline.run(
            user_path_ctx,
            total_step,
            current_step,
            len(dubbing_resource_pipeline_stages),
            update_state
        )

        current_step += 1
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
            ),
            total_step,
            current_step,
            len(dubbing_pipeline_stages),
            update_state
        )
        audio_time = round(
            AudioSegment(str(user_path_ctx.get_path(UserFile.AUDIO.DUBBING)))
            .time
        )
        video = Video(
            title=title,
            length=f"{audio_time // 3600:02}:{(audio_time % 3600) // 60:02}:{audio_time % 60:02}",
            key=None,
            creator_id=creator_id,
            voice_id=voice_id
        )
        try:
            uow = UnitOfWork(SessionLocal)
            with uow as u:
                current_step += 1
                update_state(
                    "Upload video",
                    total_step,
                    current_step
                )
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
                    logger.info(e)

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
            logger.info(e)
    logger.info(f"Service Processed In: {time.time() - start} s")
