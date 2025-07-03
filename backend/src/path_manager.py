import os
import shutil
from pathlib import Path
from contextlib import contextmanager

from fastapi import UploadFile
import uuid


class UserPath:
    def __init__(self, user_id: uuid.UUID):
        self.user_dir = Path("/tmp") / str(user_id)

        self.initial_video = self.user_dir / "video.mp4"
        self.initial_audio = self.user_dir / "audio.wav"
    
        self.dubbing_video = self.user_dir / "dubbing.mp4"
        self.dubbing_audio = self.user_dir / "dubbing.wav"

        self.tts_audio_dir = self.user_dir / "dubbing"
        self.tts_audio_sync_dir = self.user_dir / "sync"

        self.source_subtitle = self.user_dir / "source_subtitle.json"
        self.target_subtitle = self.user_dir / "target_subtitle.json"

        bgm_seperation_dir = self.user_dir / "htdemucs" / "audio"
        self.vocals = bgm_seperation_dir / "vocals.wav"
        self.reference_speaker = self.user_dir / "reference_speaker.wav"
        self.background = bgm_seperation_dir / "no_vocals.wav"

        for dir in [self.user_dir, self.tts_audio_dir, self.tts_audio_sync_dir, bgm_seperation_dir]:
            os.makedirs(dir, exist_ok=True)

    def clear(self):
        shutil.rmtree(self.user_dir)


@contextmanager
def get_user_path():
    user_path = UserPath(user_id=uuid.uuid4())
    yield user_path
    # user_path.clear()
