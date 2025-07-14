import os
import subprocess
import shutil

from fastapi import UploadFile

from src.path_manager import UserPathContext, UserFile
from src.utils.pipelines.base_stage import PipelineStage
import src.utils.cmd.ffmpeg as ffmpeg
import src.utils.cmd.demucs as demucs 


class DownloadVideo(PipelineStage):
    def process(
            self,
            user_path_ctx: UserPathContext,
            video: UploadFile
    ) -> UserPathContext:
        with open(user_path_ctx.get_path(UserFile.VIDEO.BASE), "wb") as f:
            shutil.copyfileobj(video.file, f)
        return user_path_ctx,


class ExtractAudio(PipelineStage):
    def process(self, user_path_ctx: UserPathContext) -> UserPathContext:
        base_video = user_path_ctx.get_path(UserFile.VIDEO.BASE)
        base_audio = user_path_ctx.get_path(UserFile.AUDIO.BASE)

        if not os.path.exists(base_video):
            raise FileNotFoundError(f"File not found: {base_video}")

        cmd = ffmpeg.extract_audio(
            mp4_path=str(base_video),
            wav_path=str(base_audio)
        )

        subprocess.run(
            cmd,
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        return user_path_ctx,


class SeperateBGMFromAudio(PipelineStage):
    def process(self, user_path_ctx: UserPathContext) -> UserPathContext:
        cmd = demucs.seperate_bgm(
            output=user_path_ctx.user_dir,
            wav_path=user_path_ctx.get_path(UserFile.AUDIO.BASE)
        )
        subprocess.run(cmd)
        return user_path_ctx,


class RemoveVocalsFromVideo(PipelineStage):
    def process(self, user_path_ctx: UserPathContext) -> UserPathContext:
        remove_audio_command = ffmpeg.remove_audio_from_video(
            mp4_path=user_path_ctx.get_path(UserFile.VIDEO.BASE),
            output=user_path_ctx.get_path(UserFile.VIDEO.NO_SOUND)
        )
        merge_video_bgm_command = ffmpeg.merge_video_bgm(
            mp4_path=user_path_ctx.get_path(UserFile.VIDEO.NO_SOUND),
            bgm_path=user_path_ctx.get_path(UserFile.AUDIO.BGM),
            output=user_path_ctx.get_path(UserFile.VIDEO.NO_VOCAL)
        )
        subprocess.run(
            remove_audio_command,
            check=True,
        )
        subprocess.run(merge_video_bgm_command)
        return user_path_ctx,


class ExtractReferenceSpeaker(PipelineStage):
    def process(self, user_path_ctx: UserPathContext) -> UserPathContext:
        cmd = ffmpeg.extract_reference_speaker(
            wav_path=user_path_ctx.get_path(UserFile.AUDIO.VOCALS),
            output=user_path_ctx.get_path(UserFile.AUDIO.REFERENCE_SPEAKER)
        )
        subprocess.run(cmd, check=True)
        return user_path_ctx,
