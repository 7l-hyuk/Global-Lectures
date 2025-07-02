import os
import subprocess

from src.path_manager import UserPath
import src.utils.cmd.ffmpeg as ffmpeg


def seperate_audio(user_path: UserPath):

    initial_video = user_path.initial_video
    initial_audio = user_path.vocals

    if not os.path.exists(initial_video):
        raise FileNotFoundError(f"File not found: {initial_video}")

    extract_audio_command = ffmpeg.extract_audio(
        mp4_path=str(initial_video),
        wav_path=str(initial_audio)
    )

    subprocess.run(
        extract_audio_command,
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
                