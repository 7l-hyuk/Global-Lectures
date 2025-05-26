from pathlib import Path
from src.utils.path import UserPath


def extract_audio(mp4_path: Path, wav_path: Path):
    return [
        'ffmpeg',
        '-i', mp4_path,
        '-vn',
        '-acodec', 'pcm_s16le',
        '-ar', '44100',
        '-ac', '2',
        wav_path
    ]


def make_dub(userpath: UserPath) -> list[str]:
    return [
        "ffmpeg",
        "-i", userpath.original_video,
        "-i", userpath.dub_audio,
        "-c:v", "copy",
        "-map", "0:v:0",
        "-map", "1:a:0",
        "-shortest",
        userpath.dub_video
    ]
