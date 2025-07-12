from pathlib import Path
from src.path_manager import UserPathContext

FFPROBE, FFMPEG = "ffprobe", "ffmpeg"


def extract_video_length(mp4_path: Path):
    return [
        FFPROBE, "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        str(mp4_path)
    ]


def extract_audio(mp4_path: Path, wav_path: Path):
    return [
        FFMPEG,
        '-i', str(mp4_path),
        '-vn',
        '-acodec', 'pcm_s16le',
        '-ar', '44100',
        '-ac', '2',
        str(wav_path)
    ]


def remove_audio_from_video(mp4_path: Path, output: Path):
    return [
        FFMPEG,
        "-i", str(mp4_path),
        "-c:v", "copy",
        "-an",
        "-y",
        str(output)
    ]


def merge_video_bgm(mp4_path: Path, bgm_path: Path, output: Path):
    return [
        "ffmpeg",
        "-i", str(mp4_path),
        "-i", str(bgm_path),
        "-map", "0:v",
        "-map", "1:a",
        "-c:v", "copy",
        "-shortest",
        str(output)
    ]


def extract_reference_speaker(wav_path: Path, output: Path):
    return [
        "ffmpeg",
        "-y", 
        "-i", str(wav_path),
        "-af", "silenceremove=stop_periods=-1:stop_threshold=-30dB:detection=peak",
        "-ss", "0",
        "-t", "10",
        str(output)
    ]
