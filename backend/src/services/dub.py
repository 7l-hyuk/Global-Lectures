from pathlib import Path
import json

import subprocess
from sqlalchemy.orm import Session

import src.utils.audio.cmd.ffmpeg as ffmpeg
from src.utils.logger import logger
from src.utils.path import UserPath
from src.utils.audio.audio import seperate_audio, merge_audio
from src.models.registry import create_service
from src.db.transactions import add_video_to_postgres


def make_subtitle_json(segments: dict, path: Path) -> None:
    subtitle = [
        {
            "time": segment["start"],
            "text": segment["text"]
        }
        for segment in segments
    ]
    
    with open(path, "w", encoding="utf-8") as f:
        json.dump(subtitle, f, ensure_ascii=False, indent=2)



def dub(
    userpath: UserPath,
    src_lang: str,
    tar_lang: str,
    user_id: int,
    video_title: Path,
    db: Session
) -> Path:
    user = userpath.user
    seperate_audio(userpath)

    logger.info(f"STT: {user}")
    stt = create_service(
        "stt",
        userpath=userpath,
        language=[src_lang],
    )
    segments = stt.run()
    make_subtitle_json(segments=segments, path=userpath.src_subtitle)

    translator = create_service(
        name="translator",
        userpath=None,
        language=[src_lang, tar_lang],
    )
    
    logger.info(f"TRANSLATION: {user}")
    translator.run(segments)
    make_subtitle_json(segments=segments, path=userpath.tar_subtitle)

    tts = create_service(
        name="tts",
        userpath=userpath,
        language=[tar_lang],
    )
    logger.info(f"TTS: {user}")
    tts.run(segments)

    merge_audio(segments, userpath.dub_audio)

    logger.info(f"MAKE DUB: {user}")

    add_video_to_postgres(
        db=db,
        user_id=user_id,
        userpath=userpath,
        title=video_title,
        src_lang=src_lang,
        tar_lang=tar_lang
    )

    # TODO: 합치는 과정 필요 없나?
    command = ffmpeg.make_dub(userpath)
    subprocess.run(command, check=True)
