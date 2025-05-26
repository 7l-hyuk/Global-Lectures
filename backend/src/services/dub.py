from pathlib import Path
import subprocess

import src.utils.audio.cmd.ffmpeg as ffmpeg
from src.utils.logger import logger
from src.utils.path import UserPath
from src.utils.audio.audio import extract_audio, merge_audio
from src.models.language import SupportedLanguages
from src.models.registry import create_service


def dub(
    userpath: UserPath,
    src_lang: str,
    tar_lang: str
) -> Path:
    user = userpath.user
    extract_audio(userpath)

    logger.info(f"STT: {user}")
    stt = create_service(
        "stt",
        userpath=userpath,
        language=[src_lang],
    )
    segments = stt.run()

    translator = create_service(
        name="translator",
        userpath=None,
        language=[src_lang, tar_lang],
    )
    
    logger.info(f"TRANSLATION: {user}")
    translator.run(segments)

    tts = create_service(
        name="tts",
        userpath=userpath,
        language=[tar_lang],
    )
    logger.info(f"TTS: {user}")
    tts.run(segments)

    merge_audio(segments, userpath.dub_audio)

    logger.info(f"MAKE DUB: {user}")
    command = ffmpeg.make_dub(userpath)
    subprocess.run(command, check=True)
