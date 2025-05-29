from pathlib import Path

import subprocess
from sqlalchemy.orm import Session

import src.utils.audio.cmd.ffmpeg as ffmpeg
from src.utils.logger import logger
from src.utils.path import UserPath
from src.utils.audio.audio import seperate_audio, merge_audio
from src.models.language import SupportedLanguages
from src.models.registry import create_service


def dub(
    userpath: UserPath,
    src_lang: str,
    tar_lang: str,
    db: Session
) -> Path:
    user = userpath.user
    seperate_audio(userpath)
    # TODO: 추출된 원본 audio, video -> s3


    logger.info(f"STT: {user}")
    stt = create_service(
        "stt",
        userpath=userpath,
        language=[src_lang],
    )
    segments = stt.run()

    # TODO: 원본 언어 대본 -> csv -> s3 upload (make_csv)

    translator = create_service(
        name="translator",
        userpath=None,
        language=[src_lang, tar_lang],
    )
    
    logger.info(f"TRANSLATION: {user}")
    translator.run(segments)

    # TODO: 번역 대본 -> csv -> s3 upload (make_csv)

    tts = create_service(
        name="tts",
        userpath=userpath,
        language=[tar_lang],
    )
    logger.info(f"TTS: {user}")
    tts.run(segments)

    merge_audio(segments, userpath.dub_audio)

    # TODO: 번역된 audio -> s3 upload

    logger.info(f"MAKE DUB: {user}")

    # TODO: 합치는 과정 필요 없음.
    command = ffmpeg.make_dub(userpath)
    subprocess.run(command, check=True)
