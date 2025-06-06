import os
import subprocess
from pathlib import Path

from src.utils.path import UserPath
import src.utils.audio.cmd.ffmpeg as ffmpeg
import src.utils.audio.cmd.sox as sox
import src.utils.audio.cmd.demucs as demucs
from src.utils.logger import logger


def seperate_vocal(userpath: UserPath):
    cmd = demucs.seperate_vocal(userpath)
    subprocess.run(cmd)


# TODO: 오디오와 비디오를 분리하는 로직 -> seperate_audio
def seperate_audio(userpath: UserPath, vocal_seperation: bool):

    original_video = userpath.original_video
    reference_speaker = userpath.reference_speaker

    if not os.path.exists(original_video):
        raise FileNotFoundError(f"File not found: {original_video}")

    extract_audio_command = ffmpeg.extract_audio(
        mp4_path=original_video,
        wav_path=reference_speaker
    )

    try:
        subprocess.run(
            extract_audio_command,
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        
        logger.info(f"Audio extracted successfully: {reference_speaker}")
        
        remove_audio_command = ffmpeg.remove_audio_from_video(original_video, userpath.video)
        subprocess.run(
            remove_audio_command,
            check=True,
        )
        logger.info(f"Audio removed successfully: {original_video}")

        if vocal_seperation:
            seperate_vocal(userpath)
            output_path = userpath.user / "video_with_bgm.mp4"
            merge_video_bgm_command = ffmpeg.merge_video_bgm(userpath, output_path=output_path)

            subprocess.run(merge_video_bgm_command)
            userpath.reference_speaker = userpath.vocal
            userpath.video = output_path
            
    except subprocess.CalledProcessError as e:
        logger.error("AUDIO processing FAILED!!!", e)


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


def length(mp4_path: Path) -> float:
    command = ffmpeg.extract_video_length(mp4_path)
    length = subprocess.run(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    return float(length.stdout.strip())
