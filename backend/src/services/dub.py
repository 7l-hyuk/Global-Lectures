import requests
from pathlib import Path
import json

from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from src.utils.logger import logger
from src.utils.path import UserPath
from src.utils.audio.audio import seperate_audio, merge_audio
from src.models.registry import create_service
from src.db.transactions import add_video_to_postgres, add_audio_to_postgres
from src.db.aws_handler import s3
from src.schema.video import SubtitleEntry
from src.db.video import Video


# TODO: subtitle이 end 데이터도 포함해야 함
def make_subtitle_json(segments: dict, path: Path) -> None:
    subtitle = [
        {
            "time": segment["start"],
            "text": segment["text"],
            "end": segment["end"]
        }
        for segment in segments
    ]
    
    with open(path, "w", encoding="utf-8") as f:
        json.dump(subtitle, f, ensure_ascii=False, indent=2)



# TODO: 오디오를 분리하는 로직과 더빙하는 로직을 분리
def dub(
    userpath: UserPath,
    src_lang: str,
    tar_lang: str,
    user_id: int,
    video_title: Path,
    db: Session,
    stt_model: str = "stt-elevenlabs",  
    translation_model: str = "translator-gpt",
    tts_model: str = "tts-elevenlabs"  
) -> Path:
    seperate_audio(userpath)

    stt = create_service(
        stt_model,
        userpath=userpath,
        language=[src_lang],
    )
    segments = stt.run()
    make_subtitle_json(segments=segments, path=userpath.src_subtitle)

    translator = create_service(
        name=translation_model,
        userpath=None,
        language=[src_lang, tar_lang],
    )
    
    translator.run(segments)
    make_subtitle_json(segments=segments, path=userpath.tar_subtitle)

    tts = create_service(
        name=tts_model,
        userpath=userpath,
        language=[tar_lang],
    )
    voice_id = tts.run(segments)

    merge_audio(segments, userpath.dub_audio)
    add_video_to_postgres(
        db=db,
        user_id=user_id,
        userpath=userpath,
        title=video_title,
        src_lang=src_lang,
        tar_lang=tar_lang,
        voice_id=voice_id
    )


def dub_by_audio(
    audio_presigned_url: str,
    subtitle: list[SubtitleEntry],
    userpath: UserPath,
    video_id: int,
    src_lang: str,
    tar_lang: str,
    db: Session,
    translation_model: str = "translator-gpt",
    tts_model: str = "tts-elevenlabs"
):
    res = requests.get(audio_presigned_url, stream=True)
    if res.status_code == 200:
        with open(userpath.reference_speaker, "wb") as f:
            for chunk in res.iter_content(chunk_size=65536):
                f.write(chunk)
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="s3 object not found"
        )
    
    segments = [{"start": sub.time, "text": sub.text, "end": sub.end} for sub in subtitle]
    
    translator = create_service(
        name=translation_model,
        userpath=None,
        language=[src_lang, tar_lang],
    )
    
    translator.run(segments)
    make_subtitle_json(segments=segments, path=userpath.tar_subtitle)

    video = db.query(Video).filter(Video.id == video_id).first()

    tts = create_service(
        name=tts_model,
        userpath=userpath,
        language=[tar_lang],
    )
    voice_id = tts.run(segments, voice_id=video.voice_id)

    merge_audio(segments, userpath.dub_audio)
    add_audio_to_postgres(
        db=db,
        video_id=video_id,
        userpath=userpath,
        tar_lang=tar_lang,
        voice_id=voice_id
    )