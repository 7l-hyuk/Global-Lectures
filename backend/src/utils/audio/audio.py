import os
import subprocess
from pathlib import Path

from src.utils.path import UserPath
import src.utils.audio.cmd.ffmpeg as ffmpeg
import src.utils.audio.cmd.sox as sox
from src.utils.logger import logger


def extract_audio(userpath: UserPath):
    original_video = userpath.original_video
    reference_speaker = userpath.reference_speaker

    if not os.path.exists(original_video):
        raise FileNotFoundError(f"File not found: {original_video}")

    command = ffmpeg.extract_audio(
        mp4_path=original_video,
        wav_path=reference_speaker
    )

    try:
        subprocess.run(
            command,
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        logger.info(f"Audio extracted successfully: {reference_speaker}")
    except subprocess.CalledProcessError as e:
        logger.error("AUDIO EXTRACTED FAILED!!!", e)


def audio_sync(
    input_file_path: Path,
    output_file_path: Path,
    speed: float
):
    try:
        command = sox.sync(input_file_path, output_file_path, speed)
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        logger.error(f"Sox Error!!!: {e}")


def merge_audio(segments: list[dict], output_path: Path):
    command = sox.merge_audio(segments, output_path)
    subprocess.run(command, shell=True)
    logger.info("Merge audio")
