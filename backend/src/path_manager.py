import os
import shutil
from enum import Enum
from pathlib import Path
from contextlib import contextmanager

import uuid


class UserFile:
    class VIDEO(Enum):
        BASE = "video.mp4"
        NO_SOUND = "no_sound.mp4"
        NO_VOCAL = "no_vocal.mp4"

    class AUDIO(Enum):
        BASE = "audio.wav"
        REFERENCE_SPEAKER = "reference_speaker.wav"
        DUBBING = "dubbing.wav"
        VOCALS = "htdemucs/audio/vocals.wav"
        BGM = "htdemucs/audio/no_vocals.wav"
    
    class SUBTITLE(Enum):
        SOURCE = "source_subtitle.json"
        TARGET = "target_subtitle.json"


class UserDir(Enum):
    DUBBING = "dubbing"
    SYNC_DUBBING = "sync"
    HTDEMUCS = "htdemucs/audio"


class UserPathContext:
    def __init__(self, user_id: uuid.UUID, base_dir: Path = Path("/tmp")):
        self.user_dir = base_dir / str(user_id)

        self._ensure_dirs([
            self.user_dir,
            self.user_dir / UserDir.DUBBING.value,
            self.user_dir / UserDir.SYNC_DUBBING.value,
            self.user_dir / UserDir.HTDEMUCS.value
        ])

    def _ensure_dirs(self, dirs):
        for d in dirs:
            os.makedirs(d, exist_ok=True)

    def get_path(self, src: UserFile | UserDir) -> Path:
        return self.user_dir / src.value

    def clear(self):
        shutil.rmtree(self.user_dir)


@contextmanager
def get_user_path():
    user_path_ctx = UserPathContext(user_id=uuid.uuid4())
    yield user_path_ctx
    # user_path_ctx.clear()
