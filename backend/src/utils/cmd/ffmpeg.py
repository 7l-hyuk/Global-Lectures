from pathlib import Path
from src.path_manager import UserPath

FFPROBE, FFMPEG = "ffprobe", "ffmpeg"


def extract_video_length(mp4_path: Path):
    return [
        FFPROBE, "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        mp4_path
    ]


def extract_audio(mp4_path: Path, wav_path: Path):
    return [
        FFMPEG,
        '-i', mp4_path,
        '-vn',
        '-acodec', 'pcm_s16le',
        '-ar', '44100',
        '-ac', '2',
        wav_path
    ]


def remove_audio_from_video(mp4_path: Path, output: Path):
    return [
        FFMPEG,
        "-i", mp4_path,
        "-c:v", "copy",
        "-an",
        "-y",
        output
    ]


def merge_video_bgm(userpath: UserPath, output_path: Path):
    return [
        "ffmpeg",
        "-i", userpath.initilal_video,
        "-i", userpath.background,
        "-map", "0:v",
        "-map", "1:a",
        "-c:v", "copy",
        "-shortest",
        output_path
    ]