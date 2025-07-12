import os
import subprocess

from src.path_manager import UserPathContext, UserFile
import src.utils.cmd.ffmpeg as ffmpeg


def seperate_audio(user_path_ctx: UserPathContext):

    base_video = user_path_ctx.get_path(UserFile.VIDEO.BASE)
    base_audio = user_path_ctx.get_path(UserFile.AUDIO.BASE)

    if not os.path.exists(base_video):
        raise FileNotFoundError(f"File not found: {base_video}")

    extract_audio_command = ffmpeg.extract_audio(
        mp4_path=str(base_video),
        wav_path=str(base_audio)
    )

    subprocess.run(
        extract_audio_command,
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )


